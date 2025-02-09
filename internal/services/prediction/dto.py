from pydantic import BaseModel


class GetFireRiskPredictionOut(BaseModel):
    data: float