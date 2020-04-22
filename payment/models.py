"""
Payment related model created here
"""
import uuid
from django.conf import settings
from django.db import models

# Create your models here.

PAYMENT_CONSTANTS = settings.APP_CONSTANTS["transaction"]
PAYMENT_STATUS = PAYMENT_CONSTANTS['status']


class ModelBase(models.Model):
    """
    Abstract Model Base
    """
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name="Date Range Filter")

    class Meta:
        """
        To override the database table name, use the db_table parameter in class Meta.
        """
        abstract = True


class Payment(ModelBase):
    """
    Payment model created here
    """
    amount = models.PositiveIntegerField()
    discount_amount = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    ref_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.PositiveSmallIntegerField(choices=PAYMENT_CONSTANTS["status"], default=0)
    user_id = models.IntegerField()

    def __str__(self):
        amount = "{}".format(self.total_amount)
        if self.status == 0:
            status = " (CREDIT)"
        else:
            status = " (REFUND)"
        return amount + status
