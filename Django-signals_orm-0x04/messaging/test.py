from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='sender', password='123')
        self.receiver = User.objects.create_user(username='receiver', password='123')

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )
        notifications = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().message, message)
