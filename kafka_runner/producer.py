from django.conf import settings
from confluent_kafka import Producer

def kafka_produce(topic: str, message:str) -> None:
    producer = Producer({'bootstrap.servers': settings.KAFKA.get("KAFKA_BROKER")})
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()
    print("Producing Done ....")

