import unittest
from unittest.mock import patch, MagicMock
from .consumers.evaluation import message_handler
from .models import StudentScore, Contribution
import datetime

class TestMessageHandler(unittest.TestCase):
    @patch('evaluations.consumers.evaluation.parse_message')
    @patch('evaluations.models.StudentScore.objects.create')
    @patch('evaluations.models.Contribution.objects.get_or_create')
    @patch('evaluations.consumers.evaluation.logger')
    def test_message_handler_success(self, mock_logger, mock_get_or_create, mock_student_score_create,
                                     mock_parse_message):
        # Arrange
        mock_parse_message.return_value = {
            'userId': '12345',
            'evaluationPoint': 85,
            'date': '2023-06-01'
        }
        contribution_instance = MagicMock()
        mock_get_or_create.return_value = (contribution_instance, False)

        topic = 'test_topic'
        message = '{"userId": "12345", "evaluationPoint": 85, "date": "2023-06-01"}'

        message_handler(topic, message)

        # Assert
        mock_parse_message.assert_called_once_with(message)
        mock_student_score_create.assert_called_once_with(
            student_id='12345',
            score=85,
            created_at='2023-06-01'
        )
        mock_get_or_create.assert_called_once_with(
            student_id='12345',
            created_at=datetime.datetime(2023, 6, 1),
            defaults={'commits': 1}
        )
        contribution_instance.save.assert_called_once()
        self.assertEqual(contribution_instance.commits, 2)
        mock_logger.error.assert_not_called()

    @patch('evaluations.consumers.evaluation.parse_message')
    @patch('evaluations.models.StudentScore.objects.create')
    @patch('evaluations.models.Contribution.objects.get_or_create')
    @patch('evaluations.consumers.evaluation.logger')
    def test_message_handler_parse_error(self, mock_logger, mock_get_or_create, mock_student_score_create,
                                         mock_parse_message):
        # Arrange
        mock_parse_message.side_effect = ValueError("Invalid JSON")

        topic = 'test_topic'
        message = '{"invalid_json"}'

        # Act
        message_handler(topic, message)

        # Assert
        mock_parse_message.assert_called_once_with(message)
        mock_student_score_create.assert_not_called()
        mock_get_or_create.assert_not_called()
        mock_logger.error.assert_called_once_with(
            'Error processing message: Invalid JSON', exc_info=True
        )

    @patch('evaluations.consumers.evaluation.parse_message')
    @patch('evaluations.models.StudentScore.objects.create')
    @patch('evaluations.models.Contribution.objects.get_or_create')
    @patch('evaluations.consumers.evaluation.logger')
    def test_message_handler_date_parse_error(self, mock_logger, mock_get_or_create, mock_student_score_create,
                                              mock_parse_message):
        mock_parse_message.return_value = {
            'userId': '12345',
            'evaluationPoint': 85,
            'date': 'invalid-date'
        }

        topic = 'test_topic'
        message = '{"userId": "12345", "evaluationPoint": 85, "date": "invalid-date"}'
        message_handler(topic, message)
        mock_parse_message.assert_called_once_with(message)
        mock_student_score_create.assert_called_once_with(
            student_id='12345',
            score=85,
            created_at='invalid-date'
        )
        mock_get_or_create.assert_not_called()
        mock_logger.error.assert_called_once_with(
            "Error parsing date 'invalid-date': time data 'invalid-date' does not match format '%Y-%m-%d'"
        )


if __name__ == '__main__':
    unittest.main()
