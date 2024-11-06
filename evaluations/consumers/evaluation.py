import datetime
import logging
from typing import Any

from django.conf import settings
from kafka_runner.consumer import get_kafka_consumer, kafka_consume
logger = logging.getLogger(__name__)
# Constants
EVALUATION_CONSUMER_GROUP = "EVALUATION_CONSUMER"
EVALUATION_TOPIC = settings.KAFKA.get("EVALUATION_TOPIC")


def message_handler(topic: str, message: str) -> None:
    from ..interfaces.message import parse_message
    logger.info(f"Received message from topic {topic}: {message}")
    try:
        data = parse_message(message)
        save_student_score(data)
        upsert_contribution(data)
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)

def save_student_score(data: dict[str, Any]) -> None:
    from ..models import StudentScore
    StudentScore.objects.create(
        student_id=data['userId'],
        score=data['evaluationPoint'],
        created_at=data['date']
    )


def upsert_contribution(data: dict[str, Any]) -> None:
    from ..models import Contribution
    date = data['date']
    try:
        date_time = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        logger.error(f"Error parsing date '{date}': {e}")
        return

    try:
        contribution = Contribution.objects.get(
            student_id=data['userId'],
            created_at=date_time
        )
        contribution.commits += 1
        contribution.save()
    except Contribution.DoesNotExist:
        Contribution.objects.create(
            student_id=data['userId'],
            created_at=date_time,
            commits=1
        )
    except Exception as e:
        logger.error(f"Error upserting contribution: {e}", exc_info=True)


def evaluation_consumer() -> None:
    consumer = get_kafka_consumer(EVALUATION_CONSUMER_GROUP)
    kafka_consume(consumer, [EVALUATION_TOPIC], message_handler)
