from django.core.management.base import BaseCommand
from django.utils import timezone
from todo_app.models import Task
from todo_app.utils import send_message_sync


class Command(BaseCommand):
    help = 'Проверяет просроченные задачи и отправляет уведомления'

    def handle(self, *args, **options):
        now = timezone.now()
        overdue_tasks = Task.objects.filter(
            status='pending', deadline__isnull=False, deadline__lt=now, overdue_notified=False
        )

        for task in overdue_tasks:
            message = (
                f"Задача просрочена: {task.title}\n"
                f"Дедлайн был: {task.deadline.strftime('%Y-%m-%d %H:%M')}"  # type: ignore
            )
            send_message_sync(message)
            task.overdue_notified = True
            task.save(update_fields=['overdue_notified'])

        self.stdout.write(self.style.SUCCESS(f"Проверено задач: {overdue_tasks.count()}"))
