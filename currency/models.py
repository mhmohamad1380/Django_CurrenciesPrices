from django.db import models


class Currencies(models.Model):
    title = models.CharField(max_length=120, null=True, blank=False)
    price = models.FloatField(null=True, blank=False)
    percentage = models.CharField(null=True, blank=False,max_length=10)

    def __str__(self):
        return self.title
