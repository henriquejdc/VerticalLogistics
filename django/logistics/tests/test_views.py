# Base imports
import json
import os
from typing import List

# Django imports
from django.urls import reverse

# Third party imports
from unittest.mock import patch
from rest_framework import status

# Project imports
from shared.tests import BaseAPITestCase


class OrderViewSetTestCase(BaseAPITestCase):
    """Test all scenarios for OrderViewSet."""

    tests_to_perform: List = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("order_by_user-list")
        self.response_all = {
            "count": 3,
            "next": None,
            "previous": None,
            "results": [
                {
                    "user_id": 49,
                    "name": "Ken Wintheiser",
                    "orders": [
                        {
                            "order_id": 523,
                            "date": "2021-09-03",
                            "total": "586.74",
                            "products": [
                                {
                                    "product_id": 3,
                                    "value": "586.74",
                                }
                            ]
                        }
                    ]
                },
                {
                    "user_id": 70,
                    "name": "Palmer Prosacco",
                    "orders": [
                        {
                            "order_id": 753,
                            "date": "2021-03-08",
                            "total": "1836.74",
                            "products": [
                                {
                                    "product_id": 3,
                                    "value": "1836.74",
                                }
                            ]
                        }
                    ]
                },
                {
                    "user_id": 75,
                    "name": "Bobbie Batz",
                    "orders": [
                        {
                            "order_id": 798,
                            "date": "2021-11-16",
                            "total": "1578.57",
                            "products": [
                                {
                                    "product_id": 2,
                                    "value": "1578.57",
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        self.response_retrieve = {
            'user_id': 49,
            'name': 'Ken Wintheiser',
            'orders': [
                {
                    'order_id': 523,
                    'date': '2021-09-03',
                    'total': '586.74',
                    'products': [{'product_id': 3, 'value': '586.74'}]
                }
            ]
        }

    def create_data(self):
        file_path = os.path.join(os.path.dirname(__file__), 'data.txt')
        response = self.client.post(
            self.url,
            {'file': open(file_path, 'rb')},
            format='multipart'
        )
        return response

    def test_create_ok(self):
        response = self.create_data()
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        content = json.loads(response.content)
        self.assertDictEqual(self.response_all, content)

    @patch('logistics.models.Order.objects.get_or_create')
    def test_create_error(self, order):
        response = self.create_data()

        order.side_effect = Exception('Error')

        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

    def test_create_validation_error(self):
        response = self.client.post(
            self.url,
            {'file': self.create_mock_image_file('test.jpg', 'JPEG', 'RGB')},
            format='multipart'
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        contents = json.loads(response.content)
        self.assertDictEqual({
            'status': 400,
            'error': 'ValidationError',
            'description': {'detail': {'file': ['Unsupported file extension.']}}
        }, contents)

    def test_list(self):
        # Create data
        self.create_data()

        # Get all data
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        content = json.loads(response.content)
        self.assertDictEqual(self.response_all, content)

        # Get page data
        response = self.client.get(f'{self.url}?page=1&page_size=1')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        content = json.loads(response.content)
        self.assertDictEqual({
            'count': 3,
            'next': 'http://testserver/v1/orders-by-user/?page=2&page_size=1',
            'previous': None,
            'results': [self.response_retrieve]
        }, content)

    @patch('logistics.models.UserVL.objects.filter')
    def test_list_error(self, order):
        # Create data
        self.create_data()

        order.side_effect = Exception('Error')

        # Get all data
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)

    def test_list_with_filters(self):
        # Create data
        self.create_data()

        # Get order_id filtered data
        response = self.client.get(f'{self.url}?order_id=523')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        content = json.loads(response.content)
        self.assertDictEqual({
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.response_retrieve
            ]
        }, content)

        # Get order_id filtered data
        response = self.client.get(f'{self.url}?date__gte=2021-09-01&date__lte=2021-09-30')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        content = json.loads(response.content)
        self.assertDictEqual({
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                self.response_retrieve
            ]
        }, content)

    def test_retrieve(self):
        # Create data
        self.create_data()

        # Get retrieve data
        response = self.client.get(f'{self.url}523/')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        content = json.loads(response.content)
        self.assertDictEqual(self.response_retrieve, content)

    def test_retrieve_not_found(self):
        # Get retrieve data
        response = self.client.get(f'{self.url}523/')
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    @patch('logistics.views.Response')
    def test_retrieve_error(self, response):
        # Create data
        self.create_data()

        response.side_effect = Exception('Error')

        # Get retrieve data
        response = self.client.get(f'{self.url}523/')
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code)
