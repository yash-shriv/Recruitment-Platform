from django.db import models

# Create your models here.
class JobAdvert(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.CharField(max_length=255)
    job_type = models.CharField(max_length=50)
    experience = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
