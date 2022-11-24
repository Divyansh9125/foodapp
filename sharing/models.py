from django.db import models


class User(models.Model):
    work_email = models.EmailField(primary_key=True)
    fname = models.CharField(max_length=250, null=False)
    lname = models.CharField(max_length=250)
    contact = models.BigIntegerField(null=False, unique=True)

    def __str__(self) -> str:
        return self.work_email

class Giver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portion = models.BooleanField(null=False)
    date = models.DateField(auto_now=True)
    order_id = models.CharField(max_length=10)
    veg = models.BooleanField(null=False)
    piece = models.BooleanField(null=False)

    def __str__(self) -> str:
        return self.user.fname