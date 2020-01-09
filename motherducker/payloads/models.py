from django.db import models
from connections.models import Connection


class Payload(models.Model):
    payload_name = models.CharField(null=True, max_length=120)
    payload_description = models.CharField(null=True, max_length=400)
    payload = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.payload_name


class TerminalLog(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    current_directory = models.TextField(blank=True, null=True)


class ScriptLog(models.Model):
    payload = models.ForeignKey(Payload, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)