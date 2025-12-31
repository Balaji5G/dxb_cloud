from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db import transaction
from .models import Wallet, Transaction
from .serializer import *

# Create your views here.
class WalletView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        wallet = Wallet.objects.all()
        serializer = WalletSerializer(wallet, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        amount = request.data.get('amount', 0)
        txn_type = request.data.get('txn_type')

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=request.user)

            if txn_type == 'debit' and wallet.balance < amount:
                return Response({'error': 'Insufficient funds'}, status=400)

            wallet.balance += amount if txn_type == 'credit' else -amount
            wallet.save()

            Transaction.objects.create(
                wallet=wallet,
                amount=amount,
                txn_type=txn_type,
                metadata={'api': 'manual'},
            )
        return Response({'Message': f'Amount {amount} was {txn_type}ed successfully to {request.user}'})
