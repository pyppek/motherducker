from django.db import models


# Create your models here.
class Payload(models.Model):
    payload_name = models.CharField(null=True, max_length=120)
    payload_description = models.CharField(null=True, max_length=400)
    payload = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.payload_name