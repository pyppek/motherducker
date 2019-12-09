from django.db import models
from viewflow.models import Process

# hello world demo
class HelloWorldProcess(Process):
    text = models.CharField(max_length=150)
    approved = models.BooleanField(default=False)
