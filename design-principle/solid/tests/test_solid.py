"""Verify application contracts independently of infrastructure selection."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import dip
import isp
import lsp
import ocp
import srp


class SingleResponsibilityTests(unittest.TestCase):
    def test_validation_prevents_model_and_audit_side_effects(self) -> None:
        class Predictor:
            calls = 0

            def predict(self, request):
                self.calls += 1
                return srp.Prediction(request.request_id, "label", "v1")

        predictor = Predictor()
        audit = srp.InMemoryAuditSink()
        service = srp.InferenceService(srp.RequestValidator(), predictor, audit)
        with self.assertRaises(ValueError):
            service.predict(srp.PredictionRequest("req-1", " "))
        self.assertEqual(predictor.calls, 0)
        self.assertEqual(audit.records, [])

    def test_audit_contains_prediction_metadata_without_prompt(self) -> None:
        audit = srp.InMemoryAuditSink()
        service = srp.InferenceService(
            srp.RequestValidator(), srp.KeywordPredictor(), audit
        )
        result = service.predict(srp.PredictionRequest("req-1", "great private input"))
        self.assertEqual(result.label, "positive")
        self.assertEqual(audit.records, [result])
        self.assertFalse(hasattr(result, "text"))

    def test_required_audit_failure_is_visible(self) -> None:
        class FailedAudit:
            def record(self, prediction) -> None:
                raise OSError("audit offline")

        service = srp.InferenceService(
            srp.RequestValidator(), srp.KeywordPredictor(), FailedAudit()
        )
        with self.assertRaises(OSError):
            service.predict(srp.PredictionRequest("req-1", "text"))


class OpenClosedTests(unittest.TestCase):
    def test_new_strategy_works_without_pipeline_changes(self) -> None:
        class QualityOnly:
            def score(self, candidate) -> float:
                return candidate.quality

        candidates = [ocp.Candidate("a", 0.9, 0.1), ocp.Candidate("b", 0.1, 0.9)]
        selected = ocp.RetrievalPipeline(QualityOnly()).select(candidates, top_k=1)
        self.assertEqual(selected[0].document_id, "b")

    def test_ties_are_independent_of_source_order(self) -> None:
        pipeline = ocp.RetrievalPipeline(ocp.SimilarityRanking())
        candidates = [ocp.Candidate("b", 0.5, 0.5), ocp.Candidate("a", 0.5, 0.5)]
        self.assertEqual(pipeline.select(candidates), pipeline.select(candidates[::-1]))
        self.assertEqual(pipeline.select(candidates)[0].document_id, "a")

    def test_invalid_extension_output_is_rejected(self) -> None:
        class InvalidRanking:
            def score(self, candidate) -> float:
                return float("nan")

        with self.assertRaises(ValueError):
            ocp.RetrievalPipeline(InvalidRanking()).select([ocp.Candidate("a", 1, 1)])


class SubstitutionTests(unittest.TestCase):
    def test_adapters_share_cardinality_order_and_dimension_contract(self) -> None:
        texts = ["first", "second has several words", "third", "last input"]
        baseline = lsp.LocalEmbedder().embed(texts)
        for model in (lsp.LocalEmbedder(), lsp.BatchedEmbedder(lsp.LocalEmbedder())):
            with self.subTest(adapter=type(model).__name__):
                self.assertEqual(lsp.checked_embed(model, texts), baseline)
                self.assertEqual(lsp.checked_embed(model, []), [])
                with self.assertRaises(ValueError):
                    lsp.checked_embed(model, ["valid", " "])

    def test_broken_adapter_strengthens_precondition(self) -> None:
        text = ["a valid long document"]
        self.assertEqual(len(lsp.checked_embed(lsp.LocalEmbedder(), text)), 1)
        with self.assertRaises(ValueError):
            lsp.checked_embed(lsp.BrokenShortTextEmbedder(), text)

    def test_invalid_shape_and_non_finite_vectors_are_rejected(self) -> None:
        class BrokenOutput:
            dimensions = 2

            def __init__(self, vectors) -> None:
                self.vectors = vectors

            def embed(self, texts):
                return self.vectors

        for vectors in ([], [(1.0,)], [(float("nan"), 1.0)]):
            with self.subTest(vectors=vectors), self.assertRaises(ValueError):
                lsp.checked_embed(BrokenOutput(vectors), ["text"])


class InterfaceSegregationTests(unittest.TestCase):
    def test_indexer_only_needs_embed(self) -> None:
        class EmbeddingOnly:
            def embed(self, text):
                return (42.0,)

        self.assertEqual(isp.SemanticIndexer(EmbeddingOnly()).index("text"), (42.0,))

    def test_streaming_only_adapter_is_consumed_lazily(self) -> None:
        consumed: list[str] = []

        class StreamOnly:
            def stream(self, prompt):
                for chunk in ("first", "second"):
                    consumed.append(chunk)
                    yield chunk

        chunks = isp.render_stream(StreamOnly(), "question")
        self.assertEqual(consumed, [])
        self.assertEqual(next(chunks), "first")
        self.assertEqual(consumed, ["first"])
        chunks.close()


class DependencyInversionTests(unittest.TestCase):
    def test_injected_adapters_receive_query_limit_and_context(self) -> None:
        document = dip.Document("source", "supporting text")
        searches = []
        generations = []

        class Retriever:
            def search(self, query, *, limit):
                searches.append((query, limit))
                return [document]

        class Generator:
            def generate(self, question, context):
                generations.append((question, tuple(context)))
                return "answer"

        service = dip.RAGService(Retriever(), Generator(), top_k=3)
        self.assertEqual(service.answer("query"), dip.Answer("answer", ("source",)))
        self.assertEqual(searches, [("query", 3)])
        self.assertEqual(generations, [("query", (document,))])

    def test_no_context_does_not_call_generator(self) -> None:
        class Generator:
            def generate(self, question, context):
                raise AssertionError("must not generate without context")

        service = dip.RAGService(dip.InMemoryRetriever([]), Generator())
        self.assertEqual(service.answer("query").source_ids, ())
        with self.assertRaises(ValueError):
            service.answer(" ")


if __name__ == "__main__":
    unittest.main()
