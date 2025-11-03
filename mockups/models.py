from django.db import models

# Create your models here.
# mockups/models.py
from django.db import models
class Mockup(models.Model):
    text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='mockups/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text