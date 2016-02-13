from django.db import models
import datetime

# Create your models here.
class NewsItem(models.Model):
    created_time = models.TimeField(default=datetime.date.today)
    title = models.TextField(default="Default Title")
    text = models.TextField(default='"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."')
    image = models.ImageField(blank=True,null=True)
    currently_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_image(self):
        if self.image != None:
            return self.image.url
        else:
            return '#'
