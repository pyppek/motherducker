from django.db import models


class Connection(models.Model):
    uuid = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=128)
    ip = models.GenericIPAddressField()
    status = models.BooleanField(default=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)


class TempData(models.Model):
    input = models.TextField()
    connection_id = models.ForeignKey(Connection, on_delete=models.CASCADE)
