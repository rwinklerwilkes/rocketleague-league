from django.db import models
import datetime

# Create your models here.
class NewsItem(models.Model):
    created_time = models.TimeField(default=datetime.date.today)
    text = models.TextField()
    currently_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.text
