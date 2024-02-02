# Django Imports
from datetime import datetime

from django.core.files.uploadedfile import InMemoryUploadedFile

from logistics.models import UserVL, Order, Product


def create_datadb(file: InMemoryUploadedFile) -> None:
    """
    Create objects db
    """
    for line in file:
        line_decoded = line.decode().strip()
        user, _ = UserVL.objects.get_or_create(
            user_id=int(line_decoded[0:10]),
            name=line_decoded[10:55].strip(),
        )

        product = Product.objects.create(
            product_id=int(line_decoded[65:75]),
            value=float(line_decoded[75:87]),
        )

        order, _ = Order.objects.get_or_create(
            user=user,
            order_id=int(line_decoded[55:65]),
            date=datetime.strptime(line_decoded[87:95], '%Y%m%d').date(),
        )

        order.product.add(product)
        order.save()
