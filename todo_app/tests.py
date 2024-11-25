from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Task
from unittest.mock import patch


class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            status='pending',
            deadline=timezone.now() + timezone.timedelta(hours=1),
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertEqual(self.task.status, 'pending')
        self.assertIsNotNone(self.task.deadline)


class TaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(title='Test Task', description='Test Description', status='pending')

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_create_view(self):
        with patch('todo_app.views.send_message_sync') as mock_send_message:
            response = self.client.post(
                reverse('task_create'),
                {'title': 'New Task', 'description': 'New Description', 'status': 'pending', 'deadline': ''},
            )
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Task.objects.filter(title='New Task').exists())
            mock_send_message.assert_called_once()

    def test_task_update_view(self):
        with patch('todo_app.views.send_message_sync') as mock_send_message:
            response = self.client.post(
                reverse('task_update', args=[self.task.id]),
                {'title': 'Updated Task', 'description': 'Updated Description', 'status': 'completed', 'deadline': ''},
            )
            self.assertEqual(response.status_code, 302)
            updated_task = Task.objects.get(id=self.task.id)
            self.assertEqual(updated_task.title, 'Updated Task')
            self.assertEqual(updated_task.status, 'completed')
            mock_send_message.assert_called_once()

    def test_task_delete_view(self):
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class TelegramNotificationTest(TestCase):
    @patch('todo_app.views.send_message_sync')
    def test_send_notification_on_task_creation(self, mock_send_message):
        self.client.post(
            reverse('task_create'),
            {
                'title': 'Notification Task',
                'description': 'Notification Description',
                'status': 'pending',
                'deadline': '',
            },
        )
        mock_send_message.assert_called_once_with('Новая задача добавлена: Notification Task')

    @patch('todo_app.views.send_message_sync')
    def test_send_notification_on_task_update(self, mock_send_message):
        task = Task.objects.create(title='Old Task', description='Old Description', status='pending')
        self.client.post(
            reverse('task_update', args=[task.id]),
            {'title': 'Old Task', 'description': 'Old Description', 'status': 'completed', 'deadline': ''},
        )
        mock_send_message.assert_called_once_with('Задача обновлена: Old Task - Выполнено')


class OverdueTaskTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title='Overdue Task',
            description='Overdue Description',
            status='pending',
            deadline=timezone.now() - timezone.timedelta(minutes=1),
            overdue_notified=False,
        )

    @patch('todo_app.management.commands.check_overdue_tasks.send_message_sync')
    def test_overdue_task_notification(self, mock_send_message):
        from django.core.management import call_command

        call_command('check_overdue_tasks')

        self.task.refresh_from_db()
        self.assertTrue(self.task.overdue_notified)
        mock_send_message.assert_called_once_with(
            f"Задача просрочена: {self.task.title}\nДедлайн был: {self.task.deadline.strftime('%Y-%m-%d %H:%M')}"
        )
