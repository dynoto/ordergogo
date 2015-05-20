# from django.shortcuts import render
import paypalrestsdk
from ordergogo.settings import PAYPAL_MODE, PAYPAL_CLIENT_ID, PAYPAL_SECRET
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from credit.models import Package, Transaction
from credit.serializers import PackageSerializer, TransactionSerializer, TransactionReadSerializer
from django.shortcuts import get_object_or_404

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    # NO ACTIONS OVERRIDDEN BEACUSE USER CAN ONLY READ THE PACKAGES
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class TransactionViewSet(viewsets.ViewSet):
    # SHOW ONLY USER TRANSACTIONS

    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def list(self, request):
        """
        List all transaction details by this user
        ---
        serializer : credit.serializers.TransactionReadSerializer
        """
        queryset = Transaction.objects.filter(member=request.user)
        serializer = TransactionReadSerializer(queryset, exclude=['member'] , many=True)
        return Response(serializer.data)

    def retrieve(self, request, transaction_id):
        """
        See details for this particular transaction id
        ---
        serializer : credit.serializers.TransactionReadSerializer
        """
        queryset = get_object_or_404(Transaction, id=transaction_id, member=request.user)
        serializer = TransactionReadSerializer(queryset, exclude=['member'])
        return Response(serializer.data)

    @list_route(methods=['post'])
    def create_paypal(self, request):
        """
        Create a new transaction record (record will be verified before saving to db)
        ---
        serializer : credit.serializers.TransactionSerializer
        """
        serializedTransaction = TransactionSerializer(data=request.data)
        if serializedTransaction.is_valid():
            package = get_object_or_404(Package,id=request.data['package'])

            # CHECK PAYPAL TRANSACTION WHETHER ITS VALID OR NOT
            # EXAMPLE : PAY-0XR76137BE293122CKVOLLWI
            paypalrestsdk.configure({'mode':PAYPAL_MODE, 'client_id':PAYPAL_CLIENT_ID, 'client_secret':PAYPAL_SECRET})
            try:
                pp = paypalrestsdk.Payment.find(request.data['transaction_id'])
            except:
                return Response({'errors':'No such paypal transaction id'}, status=status.HTTP_400_BAD_REQUEST)

            if pp['state'] != 'approved':
                return Response({'errors':'Payment is not approved, please check'}, status=status.HTTP_400_BAD_REQUEST)

            serializedTransaction.save(member=request.user, amount=package.price, is_paypal=True)
            return Response(serializedTransaction.data, status=status.HTTP_201_CREATED)
        return Response({'errors':serializedTransaction.errors}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
