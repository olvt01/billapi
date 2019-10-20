from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Bill

from bill.serializers import BillSerializer


BILLS_URL = reverse('bill:bill-list')
SUBSCRIBE_URL = reverse('bill:subscribe-list')


class PublicBillsApiTests(TestCase):
    """Test the publicly available bills API"""

    def setUp(self):
        self.client = APIClient()
        call_command('loaddata', 'dump_bill_for_test.json')

    def test_retrieve_bills(self):
        """Test retrieving bills"""
        res = self.client.get(BILLS_URL)

        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_login_required_for_subscribed_list(self):
        """Test that login required for retrieving subscribed lists"""
        res = self.client.get(SUBSCRIBE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBillsApiTests(TestCase):
    """Test the authorized user bills API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'password'
        )
        self.client.force_authenticate(self.user)
        call_command('loaddata', 'dump_bill_for_test.json')

    def test_retrieve_bills(self):
        """Test retrieving bills"""
        res = self.client.get(BILLS_URL)

        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
