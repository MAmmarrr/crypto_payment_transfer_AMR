from django.db import models

# Create your models here.
class Invoice(models.Model):
    STATUS_CHOICES = ((-1,"Not Started"),(0,"Unconfirmed"),(1,"Partially Confirmed"),(2,"Confirmed"))
    amount = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES,default=1)
    order_id = models.CharField(max_length=255)
    address = models.CharField(max_length=250, blank=True,null=True)
    btcvalue = models.IntegerField(blank=True,null=True)
    recieved = models.IntegerField(blank=True,null=True)
    txid = models.CharField(max_length=250,blank=True,null=True)
    rbf = models.IntegerField(blank=True,null=True)
    created_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.address