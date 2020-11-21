from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

import random


class MontyHole(models.Model):
    change = models.BooleanField(default=False)
    judge = models.BooleanField(default=False)

    class Meta:
        db_table = "MontyHole"
        verbose_name = verbose_name_plural = "モンティ・ホール"
