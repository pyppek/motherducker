from django.db import models
from connections.models import Connection


class Payload(models.Model):
    payload_name = models.CharField(null=True, max_length=120)
    payload_description = models.CharField(null=True, max_length=400)
    payload = models.TextField('default', null=True)

    def __str__(self):
        return self.payload_name


class Log(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    payload = models.ForeignKey(Payload, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class TerminalHistory(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    command = models.TextField()
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)

    def __str__(self):
        return self.command