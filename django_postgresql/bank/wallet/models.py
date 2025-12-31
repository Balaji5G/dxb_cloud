from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    txn_type = models.CharField(
        max_length=10,
        choices=(('credit', 'Credit'), ('debit', 'Debit'))
    )
    metadata = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
