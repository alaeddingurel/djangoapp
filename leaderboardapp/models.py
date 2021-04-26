from django.db import models
import uuid
import datetime
from django.utils import timezone
from django.db.models.fields import DateTimeField, FloatField

class User(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, unique=True)
    display_name = models.CharField(max_length=40)
    iso_code = models.TextField(max_length=40)
    points = models.IntegerField(default=0)
    rank = models.IntegerField(default=888888)


class Submission(models.Model):
    score_worth = FloatField()
    user_id = models.UUIDField(default=uuid.uuid4)
    timestamp = DateTimeField(auto_now_add=True)


# Create your models here.
