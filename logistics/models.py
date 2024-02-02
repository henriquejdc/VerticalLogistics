# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Project imports
from shared.models import BaseModelDate


class UserVL(BaseModelDate):

    user_id = models.BigIntegerField(
        primary_key=True
    )

    name = models.CharField(
        max_length=300,
        verbose_name=_("Name")
    )

    def __str__(self):
        return f"user_id: {self.user_id} - name: {self.name}"

    class Meta:
        ordering = ("user_id",)
        verbose_name = "Logistics User"
        verbose_name_plural = "Logistics Users"


class Order(BaseModelDate):

    order_id = models.BigIntegerField(
        primary_key=True
    )

    date = models.DateField()

    user = models.ForeignKey(
        UserVL,
        on_delete=models.PROTECT
    )

    product = models.ManyToManyField(
        "Product"
    )

    def __str__(self):
        return f"order_id: {self.order_id} - date: {self.date} - user: {self.user}"

    class Meta:
        ordering = ("order_id",)


class Product(BaseModelDate):

    product_id = models.BigIntegerField()

    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"product_id: {self.product_id} - value: {self.value}"


    class Meta:
        ordering = ("product_id",)
