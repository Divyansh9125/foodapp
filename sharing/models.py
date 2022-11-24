from django.db import models


class User(models.Model):
    work_email = models.EmailField(primary_key=True)
    fname = models.CharField(max_length=250, null=False)
    lname = models.CharField(max_length=250)
    contact = models.BigIntegerField(null=False, unique=True)

    def __str__(self) -> str:
        return str(self.work_email)

class Giver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portion = models.BooleanField(null=False)
    date = models.DateTimeField(auto_now=True, null=False)
    order_id = models.CharField(max_length=10)
    veg = models.BooleanField(null=False)
    piece = models.BooleanField(null=False)
    available = models.BooleanField(null=False, default=1)

    def __str__(self) -> str:
        return str(self.user.work_email)

class Taker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    req_portion = models.BooleanField(null=True)
    got_food = models.BooleanField(null=False)
    veg_preference = models.BooleanField(null=False, default=0)

    def __str__(self) -> str:
        return str(self.user.work_email)