"""
Payment related views are here
"""
import datetime
import json

import jwt
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import get_authorization_header

from eon_payment.settings import APP_CONSTANTS, DECODE_KEY
from payment.models import Payment
from payment.serializers import PaymentSerializer
from utils.common import api_error_response, api_success_response

CONSTANTS = APP_CONSTANTS['transaction']['values']


class EventPaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        """
        Event payment method added here
        """
        data = json.loads(request.body)
        card_number = data.get('card_number', None)
        expiry_month = data.get('expiry_month', None)
        expiry_year = data.get('expiry_year', None)
        amount = data.get('amount', None)
        discount_amount = data.get('discount_amount', None)
        total_amount = data.get('total_amount', )
        no_of_tickets = data.get('no_of_tickets', None)
        now = datetime.datetime.now()
        year = now.year
        month = now.month

        token = get_authorization_header(request).split()[1]
        payload = jwt.decode(token, DECODE_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        if not discount_amount:
            discount_amount = 0
        if not total_amount:
            if amount < 0:
                total_amount = amount*(-1) - discount_amount
                amount = amount*-1
            else:
                total_amount = amount - discount_amount

        check = False
        if no_of_tickets < 0:
            check = True
            status = 3
        else:
            if not amount or not card_number or not expiry_year or not expiry_month:
                return api_error_response(message="Request Parameters are invalid")
            status = 0
            if isinstance(card_number, int) and len(str(card_number)) == 16 and (
                    expiry_year > year or (expiry_year == year and expiry_month > month)):
                check = True
        if check:
            data = dict(amount=amount, discount_amount=discount_amount, total_amount=total_amount,
                        status=status, user_id=user_id)
            serializer = PaymentSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return api_success_response(data=data, message="Payment SuccessFul")

        return api_error_response(message="Payment Failed")

    def list(self, request, *args, **kwargs):
        """
            List the payment entry
        """
        data = json.loads(request.body)
        list_of_payment_ids = data.get("list_of_payment_ids")

        token = get_authorization_header(request).split()[1]

        payload = jwt.decode(token, DECODE_KEY, verify=False, algorithms=['HS256'])
        user_id = payload['user_id']

        user_instance = self.queryset.filter(user_id=user_id)
        if not user_instance:
            return api_error_response(message="No entry for this user", status=400)
        payment_details = user_instance.filter(id__in=list_of_payment_ids)

        serializer = PaymentSerializer(payment_details, many=True)
        return api_success_response(data=serializer.data, message="Payment details")

