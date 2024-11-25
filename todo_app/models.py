from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Не выполнено'),
        ('completed', 'Выполнено'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    deadline = models.DateTimeField(null=True, blank=True)
    overdue_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.title
