# Django Imports
from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from logistics.models import UserVL, Order, Product


class CreateDataDB:

    def __init__(self, file: InMemoryUploadedFile) -> None:
        self.file = file

    def execute_creation(self) -> None:
        """
        Create objects db
        """
        try:
            for line in self.file:
                line_decoded = line.decode().strip()
                self.create_objects_from_line(line_decoded)
        except Exception as exception:
            raise exception

    def create_objects_from_line(self, line_decoded: str) -> None:
        """
        Create user, product, and order objects from a decoded line
        """

        user_id = int(line_decoded[0:10])
        user_name = line_decoded[10:55].strip()
        product_id = int(line_decoded[65:75])
        product_value = float(line_decoded[75:87])
        order_id = int(line_decoded[55:65])
        order_date_str = line_decoded[87:95]

        user = self._get_or_create_user(user_id, user_name)
        product = self._create_product(product_id, product_value)
        order = self._get_or_create_order(user, order_id, order_date_str)

        order.products.add(product)
        order.save()

    @staticmethod
    def _get_or_create_user(user_id: int, user_name: str) -> UserVL:
        """
        Get or create a user object
        """
        user, _ = UserVL.objects.get_or_create(
            user_id=user_id,
            defaults={'name': user_name}
        )
        return user

    @staticmethod
    def _create_product(product_id: int, product_value: float) -> Product:
        """
        Create a product object
        """
        return Product.objects.create(
            product_id=product_id,
            value=product_value
        )

    @staticmethod
    def _get_or_create_order(user: UserVL, order_id: int, order_date_str: str) -> Order:
        """
        Get or create an order object
        """
        order_date = datetime.strptime(order_date_str, '%Y%m%d').date()
        order, _ = Order.objects.get_or_create(
            user=user,
            order_id=order_id,
            defaults={'date': order_date}
        )
        return order
