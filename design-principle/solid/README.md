# SOLID for AI applications

These examples apply SOLID to inference, embedding adapters, retrieval ranking,
streaming, and RAG composition. Each file includes a named anti-pattern and an
improved design, with English comments and docstrings, explicit contracts, type
hints, and an import-safe demo. Use **Python 3.11 or newer**; only the standard
library is required.

The goal is to identify which parts change independently and make them easy to
replace and test. The models and stores are offline stand-ins. The application
boundaries are useful for production code, but a deployed service still needs
actual SDK adapters, integration tests, resource management, and operational
policies.

## Principle and application mapping

| Principle | Example | AI application |
| --- | --- | --- |
| Single Responsibility | [srp.py](srp.py) | Separate request validation, prediction, and audit persistence; orchestrate them in one small service |
| Open Closed | [ocp.py](ocp.py) | Inject a ranking strategy so similarity, weighted quality, and future learned ranking can share selection logic |
| Liskov Substitution | [lsp.py](lsp.py) | Embedding adapters preserve accepted inputs, cardinality, vector dimension, finite values, and input order |
| Interface Segregation | [isp.py](isp.py) | Indexing depends on embeddings, answering on generation, and streaming on a lazy chunk interface |
| Dependency Inversion | [dip.py](dip.py) | RAG orchestration depends on retriever and generator ports; a composition root chooses infrastructure |

The original LSP file contained duplicated classes and an explanation that did
not match their `move()` behavior. Its replacement demonstrates a concrete
violation: an adapter rejects long texts accepted by the original contract. The
correct batch adapter handles its backend's batch limit internally while
preserving public behavior.

## Run the examples

From the repository root:

```bash
python3 design-principle/solid/srp.py
python3 design-principle/solid/ocp.py
python3 design-principle/solid/lsp.py
python3 design-principle/solid/isp.py
python3 design-principle/solid/dip.py
```

All demos run locally without credentials, external services, or model downloads.
Importing these modules does not start work or print demo output.

## Contracts that matter in AI code

In `srp.py`, validation precedes inference and audit. The limit is a character
limit, not a tokenizer-aware model context limit. Audit contains prediction
metadata rather than the original prompt. Audit failure fails the request in this
example; a durable asynchronous audit design would need its own persistence and
delivery contract.

In `ocp.py`, the pipeline orders scores and applies a document-ID tie-breaker.
Adding a strategy changes the composition code rather than the selection
algorithm. Weights assume comparable score scales. A production reranker may
need a batch-scoring interface to avoid one remote call per candidate; choose
that contract when the workload requires it.

In `lsp.py`, matching method signatures is insufficient. All adapters must accept
the promised inputs and preserve output meaning. Boundary validation catches
wrong shapes and non-finite values; contract tests check order and accepted
inputs. Equal vector dimensions do not imply equal embedding spaces. Pin the
model revision and index version when replacing an embedding provider.

In `isp.py`, a client can implement several narrow interfaces without every
consumer depending on all capabilities. An embedding-only client needs no dummy
generation method that raises `NotImplementedError`. The streaming example is a
lazy synchronous iterator; an async provider should have an async streaming
contract that supports cancellation and closure.

In `dip.py`, the application owns `Retriever` and `GroundedGenerator` contracts.
Constructor injection supplies implementations. The no-context path returns
without calling a generator. Returned source IDs identify supplied documents;
they do not prove that every generated claim is supported. Actual RAG adapters
need context budgeting, trust boundaries for retrieved text, and grounding
evaluation.

## Protocols and composition

The examples use `typing.Protocol` for structural interfaces: an adapter can
implement the required methods without inheriting an application base class.
Protocols support static checking; annotations do not automatically validate
behavior at runtime. See the [Python Protocol documentation](https://docs.python.org/3.12/library/typing.html#typing.Protocol).
Use an abstract base class when shared implementation or runtime construction
rules are useful. Neither abstraction replaces behavioral contract tests.

Keep concrete SDK creation in an application factory or composition root.
Services receive dependencies that are already configured. Avoid making an
interface for every class: add a boundary when behavior changes independently,
when an external system is involved, or when a consumer needs a smaller contract.
OCP protects a useful extension point; it does not prohibit changing an interface
when requirements change.

For serving lifecycle, deadlines, retry policy, process preprocessing, and bounded
ingestion, see [Advanced Python for AI services](../../advanced-python/README.md).

## Verification

```bash
python3 -m unittest discover -s design-principle/solid/tests -v
ruff check design-principle/solid
ruff format --check design-principle/solid
```

Tests verify rejection before side effects, audit failure, strategy extension,
deterministic ranking, embedding substitution, invalid provider output, narrow
client dependencies, lazy streaming, and RAG behavior with injected adapters.
They run with the standard library; Ruff is optional development tooling.
