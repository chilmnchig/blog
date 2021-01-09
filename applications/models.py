from django.db import models


class MontyHole(models.Model):
    change = models.BooleanField(default=False)
    judge = models.BooleanField(default=False)

    class Meta:
        db_table = "MontyHole"
        verbose_name = verbose_name_plural = "モンティ・ホール"

    @classmethod
    def show_percentage(cls):
        total_changed = cls.objects.filter(change=True).count()
        total_not_changed = cls.objects.filter(change=False).count()
        total_changed_true = cls.objects.filter(
            change=True, judge=True).count()
        total_not_changed_true = cls.objects.filter(
            change=False, judge=True).count()
        if total_changed == 0:
            total_changed = 1
        if total_not_changed == 0:
            total_not_changed = 1
        percentage_changed = total_changed_true * 100 / total_changed
        percentage_not_changed = (
            total_not_changed_true * 100 / total_not_changed)
        percentage_changed = round(percentage_changed, 2)
        percentage_not_changed = round(percentage_not_changed, 2)
        return percentage_changed, percentage_not_changed
