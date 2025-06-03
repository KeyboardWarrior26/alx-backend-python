from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatAppTests(TestCase):
    def setUp(self):
        # Create users with username, email, and password as required by your model
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass1234'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass1234'
        )

        # You can create additional setup here, like conversations or messages

    def test_access_permission(self):
        # your test logic here
        pass

    def test_create_conversation(self):
        # your test logic here
        pass

    def test_create_message_in_conversation(self):
        # your test logic here
        pass

    def test_list_conversations(self):
        # your test logic here
        pass

    def test_message_permission(self):
        # your test logic here
        pass

