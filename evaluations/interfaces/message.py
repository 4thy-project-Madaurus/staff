from typing import TypedDict
import json
class EvaluationConsumer(TypedDict):
    userId: str
    evaluationPoint: int
    date: str  # Format YYYY-MM-DD

def parse_message(message: str) -> EvaluationConsumer:
    data = json.loads(message)
    return EvaluationConsumer(
        userId=data['userId'],
        evaluationPoint=data['evaluationPoint'],
        date=data['date']
    )