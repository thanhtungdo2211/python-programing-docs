# Advanced Python for AI services

These examples cover Python techniques used around model serving, training hooks,
and document indexing: bounded work, deadlines, cancellation, typed callbacks,
process isolation, and resource ownership. They require **Python 3.11 or newer**
and use only the standard library. All comments, docstrings, and demo output are
in English.

The providers and models are deliberately small offline adapters. They demonstrate
control flow and failure handling, rather than model quality or complete serving
infrastructure. Replace them with actual SDK adapters and verify their contracts
before using these patterns in a deployed application.

## Examples and learning order

| File | AI scenario | Technique to study |
| --- | --- | --- |
| [callback-function.py](callback-function.py) | Training metrics and early stopping | Callable protocols, immutable events, state per run, explicit observer failure policy |
| [io-cpu_bound.py](io-cpu_bound.py) | Download documents and compute features | Measure with `perf_counter`; compare serial, thread, and process execution |
| [parallelism.py](parallelism.py) | Preprocess a document source | Spawn workers, serializable inputs, bounded pending futures, completion order, propagated failures |
| [concurrency.py](concurrency.py) | Call an inference provider for a small batch | `TaskGroup`, semaphore, attempt timeout, overall deadline, capped exponential backoff with full jitter |
| [streaming_pipeline.py](streaming_pipeline.py) | Embed documents and upsert vectors | Async source, fixed workers, bounded queue, backpressure, stable IDs for replay |
| [resource_lifecycle.py](resource_lifecycle.py) | Start serving resources and trace requests | `ExitStack`, partial startup cleanup, `ContextVar` tokens, nested request scopes |
| [singleton_design.py](singleton_design.py) | Share loaded models within one application | Explicit registry injection, revision and device keys, lock, capacity, shutdown |

The existing filenames remain available. `singleton_design.py` now explains why an
application-owned registry is often easier to configure and test than a hidden
global singleton. Each worker process owns its own registry and model memory.

## Run the examples

Run from the repository root; no API keys, network access, or model downloads are
required:

```bash
python3 advanced-python/callback-function.py
python3 advanced-python/io-cpu_bound.py
python3 advanced-python/parallelism.py
python3 advanced-python/concurrency.py
python3 advanced-python/streaming_pipeline.py
python3 advanced-python/resource_lifecycle.py
python3 advanced-python/singleton_design.py
```

Keep the `if __name__ == "__main__"` guard when adapting process examples. Run
them as scripts rather than pasting worker definitions into an interactive shell;
process workers need an importable main module and serializable callables and
data. See the [ProcessPoolExecutor documentation](https://docs.python.org/3.12/library/concurrent.futures.html#processpoolexecutor).

## Execution choices

| Workload | Starting point | Constraint |
| --- | --- | --- |
| Async provider or database client | Async tasks | Bound active calls and use a request deadline |
| Blocking network or storage SDK | Small thread pool or `asyncio.to_thread` | Configure timeouts in the SDK; cancelling an await does not stop an already running thread |
| Substantial pure Python CPU preprocessing | Process pool | Account for startup, serialization, and memory per worker |
| GPU inference or native tensor operations | Model runtime and its batching scheduler | Profile the actual runtime before adding Python workers |

This table is implementation guidance, not a speed guarantee. Under conventional
CPython with the GIL, threads typically suit blocking I/O; pure Python CPU work
does not gain multicore execution just by adding threads. Native extensions may
release the GIL, so profile your tokenizer and numerical runtime separately. See
the [threading documentation](https://docs.python.org/3.12/library/threading.html)
and [asyncio thread integration](https://docs.python.org/3.12/library/asyncio-task.html#asyncio.to_thread).

The CPU demo uses very small documents. Process execution may take longer than
serial execution; its purpose is to demonstrate scheduling and verify equivalent
outputs, not to establish a benchmark.

## Failure and ownership contracts

`infer_batch` preserves input order. It retries only classified transient errors
and attempt timeouts. A terminal error cancels sibling tasks and surfaces through
an `ExceptionGroup`; expiration of the overall deadline raises `TimeoutError`.
Backoff releases the semaphore slot. A semaphore bounds active calls, but the
function still allocates one task per input, so use it for small batches. These
semantics follow [TaskGroup and timeout behavior](https://docs.python.org/3.12/library/asyncio-task.html).

`index_documents` bounds queued documents and worker tasks. Its producer pauses
when the queue fills, as defined by [asyncio.Queue](https://docs.python.org/3.12/library/asyncio-queue.html).
The item deadline covers embedding and upsert; the caller must also set a job
deadline to cover a stalled source. One failure cancels the pipeline. Previously
completed writes remain committed: stable document IDs and an idempotent sink
support replay, but do not create a transaction or exactly-once processing.
The demo sink retains vectors in memory; a real sink persists them externally.
Queue capacity bounds item count, so enforce document byte limits separately.

`preprocess` yields completion order. Carry document IDs if downstream consumers
need to restore order. Closing the iterator cancels pending work where possible;
already running jobs can still finish during pool shutdown. A pool is not a
mechanism for forcibly interrupting arbitrary CPU jobs.

`ModelRegistry` owns loaded models until application shutdown. Drain requests
before closing it; the registry lock guards loading, not concurrent prediction.
Capacity exhaustion is explicit rather than silently evicting a model that a
request might still be using. Cleanup attempts every model and aggregates errors.

## Adapting to an AI deployment

Use the examples as component boundaries. An actual provider adapter needs
transport timeouts, connection lifecycle management, and error classification.
Check whether an operation is safe to retry: remote work can continue after a
client timeout, and retries can duplicate billing or side effects. Concurrency
limits do not enforce requests-per-minute or token quotas; add provider-aware
rate limiting and honor retry hints at the adapter boundary.

Record latency, queue depth, retry count, and model revision through telemetry
adapters. Keep prompt retention an explicit decision. For ingestion, define
durable progress checkpoints and failed-document handling; for serving, decide
between failing a whole batch and returning individual errors. The examples
choose failure of the whole batch to keep their contract clear.

Continue with [SOLID for AI applications](../design-principle/solid/README.md) to
organize these components behind application interfaces.

## Verification

```bash
python3 -m unittest discover -s advanced-python/tests -v
ruff check advanced-python
ruff format --check advanced-python
```

The tests exercise retry counts, input order, concurrency bounds, cancellation,
backpressure, replay, process worker failures, concurrent model loading, and
cleanup after partial startup. Ruff is optional development tooling; running the
examples and tests requires no third-party dependencies.
