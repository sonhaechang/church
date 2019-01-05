from django.db import models

# Create your models here.

class Schedule(models.Model):
    title = models.CharField(max_length=100, unique=True)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.title
