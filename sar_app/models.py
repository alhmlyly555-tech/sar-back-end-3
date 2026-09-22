from django.db import models

class SARAnalysisResult(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    wkt_geometry = models.TextField()
    status = models.CharField(max_length=50, default='PENDING')
    result_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Task {self.task_id} - {self.status}"