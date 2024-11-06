import threading
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class EvaluationsConfig(AppConfig):
    name = 'evaluations'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        eval_thread = threading.Thread(target=self.start_evaluation_consumer)
        eval_thread.daemon = True
        eval_thread.start()
        logger.info("Evaluation Consumer Started")

    def start_evaluation_consumer(self):
        from .consumers.evaluation import evaluation_consumer
        try:
            evaluation_consumer()
        except Exception as e:
            logger.error(f"Error starting evaluation consumer: {e}", exc_info=True)
