from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=120)
    notes = models.TextField(blank=True, max_length=2000)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
