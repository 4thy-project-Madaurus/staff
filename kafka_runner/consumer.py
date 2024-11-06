from confluent_kafka import Consumer, KafkaError
from django.conf import settings
def get_kafka_consumer(consumer_group_id: str) -> Consumer:
    consumer = Consumer({
        'bootstrap.servers': settings.KAFKA.get("KAFKA_BROKER"),
        'group.id': consumer_group_id,
        'auto.offset.reset': 'earliest'
    })
    return consumer

def kafka_consume(consumer:Consumer, topic:list, on_message: callable):
    consumer.subscribe(topic)
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            on_message(msg.value().decode('utf-8'))
    finally:
        consumer.close()
