"""Behavioral tests for cancellation, bounded work, and resource ownership."""

from __future__ import annotations

import asyncio
import importlib
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
concurrency = importlib.import_module("concurrency")
callbacks = importlib.import_module("callback-function")
parallelism = importlib.import_module("parallelism")
registry_module = importlib.import_module("singleton_design")
streaming = importlib.import_module("streaming_pipeline")
lifecycle = importlib.import_module("resource_lifecycle")


class InferenceTests(unittest.IsolatedAsyncioTestCase):
    async def test_retry_and_input_order(self) -> None:
        provider = concurrency.FakeProvider()
        results = await concurrency.infer_batch(provider, ["retry me", "second"])
        self.assertEqual(results, ["prediction:RETRY ME", "prediction:SECOND"])
        self.assertEqual(provider.calls["retry me"], 2)
        self.assertEqual(provider.calls["second"], 1)

    async def test_active_calls_are_bounded(self) -> None:
        class Provider:
            active = 0
            peak = 0

            async def predict(self, text: str) -> str:
                self.active += 1
                self.peak = max(self.peak, self.active)
                try:
                    await asyncio.sleep(0)
                    return text
                finally:
                    self.active -= 1

        provider = Provider()
        inputs = [str(i) for i in range(20)]
        self.assertEqual(
            await concurrency.infer_batch(provider, inputs, concurrency=3), inputs
        )
        self.assertEqual(provider.peak, 3)
        self.assertEqual(provider.active, 0)

    async def test_permanent_error_cancels_siblings_without_retry(self) -> None:
        started = asyncio.Event()
        cancelled = asyncio.Event()
        calls: list[str] = []

        class Provider:
            async def predict(self, text: str) -> str:
                calls.append(text)
                if text == "fail":
                    await started.wait()
                    raise ValueError("invalid prompt")
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cancelled.set()
                return text

        with self.assertRaises(ExceptionGroup) as raised:
            await concurrency.infer_batch(Provider(), ["wait", "fail"])
        self.assertIsInstance(raised.exception.exceptions[0], ValueError)
        self.assertTrue(cancelled.is_set())
        self.assertEqual(calls.count("fail"), 1)

    async def test_attempt_timeout_exhausts_retries(self) -> None:
        class Provider:
            calls = 0

            async def predict(self, text: str) -> str:
                self.calls += 1
                await asyncio.Event().wait()
                return text

        provider = Provider()
        policy = concurrency.RetryPolicy(attempts=2, attempt_timeout=0.01, base_delay=0)
        with self.assertRaises(ExceptionGroup) as raised:
            await concurrency.infer_batch(provider, ["wait"], policy=policy)
        self.assertIsInstance(raised.exception.exceptions[0], TimeoutError)
        self.assertEqual(provider.calls, 2)

    async def test_batch_deadline_includes_queue_wait(self) -> None:
        class Provider:
            async def predict(self, text: str) -> str:
                await asyncio.Event().wait()
                return text

        with self.assertRaises(TimeoutError):
            await concurrency.infer_batch(
                Provider(), ["one", "two"], concurrency=1, batch_timeout=0.01
            )

    async def test_caller_cancellation_propagates(self) -> None:
        started = asyncio.Event()
        cleaned = asyncio.Event()

        class Provider:
            async def predict(self, text: str) -> str:
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()
                return text

        task = asyncio.create_task(concurrency.infer_batch(Provider(), ["wait"]))
        await asyncio.wait_for(started.wait(), timeout=1)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertTrue(cleaned.is_set())

    async def test_empty_batch_and_invalid_configuration(self) -> None:
        self.assertEqual(
            await concurrency.infer_batch(concurrency.FakeProvider(), []), []
        )
        with self.assertRaises(ValueError):
            await concurrency.infer_batch(concurrency.FakeProvider(), [], concurrency=0)
        with self.assertRaises(ValueError):
            concurrency.RetryPolicy(attempt_timeout=float("nan"))


class PipelineTests(unittest.IsolatedAsyncioTestCase):
    async def test_replay_upserts_by_stable_id(self) -> None:
        async def source():
            for index in range(8):
                yield streaming.Document(str(index), f"text {index}")

        sink = streaming.InMemorySink()
        for _ in range(2):
            count = await streaming.index_documents(
                source(), streaming.FakeEmbedder(), sink, queue_size=1
            )
            self.assertEqual(count, 8)
        self.assertEqual(len(sink.vectors), 8)
        self.assertEqual(sink.vectors["0"], (6.0, 2.0))

    async def test_source_read_ahead_is_bounded_and_cancellation_cleans_workers(
        self,
    ) -> None:
        emitted = 0
        active = 0
        started = asyncio.Event()

        async def source():
            nonlocal emitted
            for index in range(100):
                emitted += 1
                yield streaming.Document(str(index), "text")

        class BlockingEmbedder:
            async def embed(self, text: str) -> tuple[float, ...]:
                nonlocal active
                active += 1
                if active == 2:
                    started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    active -= 1
                return (1.0,)

        task = asyncio.create_task(
            streaming.index_documents(
                source(),
                BlockingEmbedder(),
                streaming.InMemorySink(),
                workers=2,
                queue_size=2,
            )
        )
        try:
            await asyncio.wait_for(started.wait(), timeout=1)
            await asyncio.sleep(0)
            # Queue + active consumers + the producer's blocked item.
            self.assertLessEqual(emitted, 5)
        finally:
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertEqual(active, 0)

    async def test_sink_failure_stops_pipeline(self) -> None:
        async def source():
            for index in range(100):
                yield streaming.Document(str(index), "text")

        class FailedSink:
            async def upsert(self, document_id, vector) -> None:
                raise OSError("vector store unavailable")

        with self.assertRaises(ExceptionGroup) as raised:
            await asyncio.wait_for(
                streaming.index_documents(
                    source(), streaming.FakeEmbedder(), FailedSink()
                ),
                timeout=1,
            )
        self.assertTrue(
            any(isinstance(e, OSError) for e in raised.exception.exceptions)
        )

    async def test_source_failure_does_not_wait_for_stop_markers(self) -> None:
        async def source():
            yield streaming.Document("one", "text")
            raise OSError("source failed")

        with self.assertRaises(ExceptionGroup):
            await asyncio.wait_for(
                streaming.index_documents(
                    source(), streaming.FakeEmbedder(), streaming.InMemorySink()
                ),
                timeout=1,
            )

    async def test_empty_source(self) -> None:
        async def source():
            if False:
                yield streaming.Document("unused", "unused")

        count = await streaming.index_documents(
            source(), streaming.FakeEmbedder(), streaming.InMemorySink()
        )
        self.assertEqual(count, 0)


class CallbackTests(unittest.TestCase):
    def test_all_observers_receive_the_stopping_epoch(self) -> None:
        recorder = callbacks.MetricsRecorder()
        stopping = callbacks.EarlyStopping(patience=2)
        count = callbacks.train([0.9, 0.6, 0.61, 0.62, 0.1], [stopping, recorder])
        self.assertEqual(count, 4)
        self.assertEqual([item.epoch for item in recorder.history], [1, 2, 3, 4])
        self.assertEqual(stopping.best_loss, 0.6)

    def test_improvement_resets_patience(self) -> None:
        stopping = callbacks.EarlyStopping(patience=2)
        self.assertEqual(callbacks.train([1, 1, 0.5, 0.6, 0.7], [stopping]), 5)

    def test_non_finite_loss_and_callback_failure_abort_training(self) -> None:
        with self.assertRaises(ValueError):
            callbacks.train([float("nan")], [])

        def failed_observer(metrics) -> bool:
            raise OSError("checkpoint failed")

        with self.assertRaises(OSError):
            callbacks.train([0.5], [failed_observer])


class RegistryTests(unittest.TestCase):
    def test_concurrent_get_loads_once(self) -> None:
        loads: list[object] = []

        def loader(key):
            loads.append(key)
            return registry_module.FakeModel(key)

        registry = registry_module.ModelRegistry(loader)
        key = registry_module.ModelKey("model", "v1")
        try:
            with ThreadPoolExecutor(max_workers=8) as pool:
                models = list(pool.map(registry.get, [key] * 32))
            self.assertEqual(len(loads), 1)
            self.assertTrue(all(model is models[0] for model in models))
        finally:
            registry.close()
        self.assertTrue(models[0].closed)

    def test_revision_keys_capacity_and_closed_state(self) -> None:
        registry = registry_module.ModelRegistry(registry_module.FakeModel, capacity=2)
        first = registry.get(registry_module.ModelKey("model", "v1"))
        second = registry.get(registry_module.ModelKey("model", "v2"))
        self.assertIsNot(first, second)
        with self.assertRaises(RuntimeError):
            registry.get(registry_module.ModelKey("model", "v3"))
        registry.close()
        registry.close()
        self.assertTrue(first.closed and second.closed)
        with self.assertRaises(RuntimeError):
            registry.get(first.key)

    def test_failed_load_is_not_cached(self) -> None:
        attempts = 0

        def loader(key):
            nonlocal attempts
            attempts += 1
            if attempts == 1:
                raise OSError("missing model")
            return registry_module.FakeModel(key)

        registry = registry_module.ModelRegistry(loader)
        key = registry_module.ModelKey("model", "v1")
        try:
            with self.assertRaises(OSError):
                registry.get(key)
            self.assertEqual(registry.get(key).key, key)
            self.assertEqual(attempts, 2)
        finally:
            registry.close()

    def test_cleanup_attempts_all_models_when_one_close_fails(self) -> None:
        closed: list[str] = []

        class Model:
            def __init__(self, key) -> None:
                self.key = key

            def close(self) -> None:
                closed.append(self.key.name)
                if self.key.name == "failed":
                    raise OSError("cleanup failed")

        registry = registry_module.ModelRegistry(Model)
        registry.get(registry_module.ModelKey("failed", "v1"))
        registry.get(registry_module.ModelKey("healthy", "v1"))
        with self.assertRaises(ExceptionGroup):
            registry.close()
        self.assertEqual(closed, ["failed", "healthy"])


class ResourceTests(unittest.TestCase):
    def test_nested_context_is_restored_after_exception(self) -> None:
        before = lifecycle.request_id.get()
        with lifecycle.request_scope("outer"):
            with self.assertRaises(ValueError):
                with lifecycle.request_scope("inner"):
                    self.assertEqual(lifecycle.request_id.get(), "inner")
                    raise ValueError("failed request")
            self.assertEqual(lifecycle.request_id.get(), "outer")
        self.assertEqual(lifecycle.request_id.get(), before)

    def test_partial_startup_closes_acquired_model(self) -> None:
        model = lifecycle.ServingResource("test model")
        with (
            patch.object(lifecycle, "load_model", return_value=model),
            patch.object(
                lifecycle, "connect_vector_store", side_effect=OSError("offline")
            ),
            redirect_stdout(StringIO()),
        ):
            with self.assertRaises(OSError):
                with lifecycle.serving_resources():
                    self.fail("startup should fail before entering the body")
        self.assertTrue(model.closed)


class ProcessTests(unittest.TestCase):
    def test_spawn_pool_matches_serial_results(self) -> None:
        documents = [(0, "AI retrieval"), (1, "Embedding vectors"), (2, "third")]
        expected = [parallelism.featurize(document) for document in documents]
        actual = list(parallelism.preprocess(documents, max_pending=2))
        self.assertEqual(sorted(actual, key=lambda item: item.document_id), expected)

    def test_worker_failure_propagates(self) -> None:
        with self.assertRaises(AttributeError):
            list(parallelism.preprocess([(0, None)], workers=1, max_pending=1))

    def test_lazy_source_submission_is_bounded(self) -> None:
        produced = 0

        def source():
            nonlocal produced
            for index in range(100):
                produced += 1
                yield index, "test"

        results = parallelism.preprocess(source(), workers=1, max_pending=2)
        try:
            next(results)
            self.assertEqual(produced, 2)
        finally:
            results.close()


if __name__ == "__main__":
    unittest.main()
