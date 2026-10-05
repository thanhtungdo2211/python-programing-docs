"""SRP: separate validation, model inference, and audit persistence.

Each component changes for a different reason: request policy, model runtime,
or storage schema. A small service coordinates them without owning their jobs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class CoupledInferenceService:
    """Anti-pattern: policy, prediction logic, and storage share one component."""

    def __init__(self) -> None:
        self.rows: list[dict[str, str]] = []

    def predict(self, request_id: str, text: str) -> str:
        if not text.strip() or len(text) > 1000:
            raise ValueError("invalid input")
        label = "positive" if "great" in text.casefold() else "neutral"
        self.rows.append({"request_id": request_id, "text": text, "label": label})
        return label


@dataclass(frozen=True, slots=True)
class PredictionRequest:
    request_id: str
    text: str


@dataclass(frozen=True, slots=True)
class Prediction:
    request_id: str
    label: str
    model_revision: str


@dataclass(frozen=True, slots=True)
class RequestValidator:
    max_characters: int = 1000

    def __post_init__(self) -> None:
        if self.max_characters < 1:
            raise ValueError("max_characters must be positive")

    def validate(self, request: PredictionRequest) -> None:
        if not request.request_id.strip() or not request.text.strip():
            raise ValueError("request ID and text must not be empty")
        if len(request.text) > self.max_characters:
            raise ValueError("input exceeds the character limit")


class Predictor(Protocol):
    def predict(self, request: PredictionRequest) -> Prediction: ...


class AuditSink(Protocol):
    def record(self, prediction: Prediction) -> None: ...


class KeywordPredictor:
    """Offline stand-in for an adapter around an actual model runtime."""

    def predict(self, request: PredictionRequest) -> Prediction:
        label = "positive" if "great" in request.text.casefold() else "neutral"
        return Prediction(request.request_id, label, "keyword-v1")


@dataclass
class InMemoryAuditSink:
    records: list[Prediction] = field(default_factory=list)

    def record(self, prediction: Prediction) -> None:
        # Retain prediction metadata, not the potentially sensitive prompt.
        self.records.append(prediction)


class InferenceService:
    def __init__(
        self, validator: RequestValidator, predictor: Predictor, audit: AuditSink
    ) -> None:
        self._validator = validator
        self._predictor = predictor
        self._audit = audit

    def predict(self, request: PredictionRequest) -> Prediction:
        self._validator.validate(request)
        prediction = self._predictor.predict(request)
        # This example requires audit success before returning a prediction.
        # For durable asynchronous audit, use an outbox with an explicit contract.
        self._audit.record(prediction)
        return prediction


def main() -> None:
    audit = InMemoryAuditSink()
    service = InferenceService(RequestValidator(), KeywordPredictor(), audit)
    print(service.predict(PredictionRequest("req-1", "A great product")))
    print(f"Audited predictions: {len(audit.records)}")


if __name__ == "__main__":
    main()
