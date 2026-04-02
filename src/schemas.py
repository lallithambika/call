from pydantic import BaseModel, Field
from typing import Literal


class CallAnalyticsRequest(BaseModel):
    language: Literal["Hindi", "Tamil", "Hinglish", "Tanglish"]
    audioFormat: Literal["mp3"]
    audioBase64: str = Field(min_length=32)


class SOPValidation(BaseModel):
    greeting: bool
    identification: bool
    problemStatement: bool
    solutionOffering: bool
    closing: bool
    complianceScore: float
    adherenceStatus: Literal["FOLLOWED", "NOT_FOLLOWED"]
    explanation: str


class AnalyticsExtraction(BaseModel):
    paymentPreference: Literal["EMI", "FULL_PAYMENT", "PARTIAL_PAYMENT", "DOWN_PAYMENT"]
    rejectionReason: Literal[
        "HIGH_INTEREST",
        "BUDGET_CONSTRAINTS",
        "ALREADY_PAID",
        "NOT_INTERESTED",
        "NONE",
    ]
    sentiment: Literal["Positive", "Neutral", "Negative"]


class CallAnalyticsResponse(BaseModel):
    status: Literal["success"]
    language: str
    transcript: str
    summary: str
    sop_validation: SOPValidation
    analytics: AnalyticsExtraction
    keywords: list[str]
