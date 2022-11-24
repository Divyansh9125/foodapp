from django.db import models


class User(models.Model):
    work_email = models.EmailField(primary_key=True)
    fname = models.CharField(max_length=250, null=False)
    lname = models.CharField(max_length=250)
    contact = models.BigIntegerField(null=False, unique=True)

    def __str__(self) -> str:
        return self.work_email