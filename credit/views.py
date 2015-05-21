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
        return Response({'transaction':serializer.data})

    def retrieve(self, request, transaction_id):
        """
        See details for this particular transaction id
        ---
        serializer : credit.serializers.TransactionReadSerializer
        """
        queryset = get_object_or_404(Transaction, id=transaction_id, member=request.user)
        serializer = TransactionReadSerializer(queryset, exclude=['member'])
        return Response({'transaction':serializer.data})

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
                return Response({'error':{'transaction_id':['We cannot find your paypal transaction, please verify that the transaction_id is correct']}}, status=status.HTTP_400_BAD_REQUEST)

            # IF NOT APPROVED THROW USER ERROR
            if pp['state'] != 'approved':
                return Response({'error':{'transaction_id':['Payment is not approved, please check your transaction_id and try again']}}, status=status.HTTP_400_BAD_REQUEST)

            # IF THE VALUE OF THE TRANSACTION DOES NOT MATCH PACKAGE, THROW USER ERROR
            elif pp['transactions'][0]['amount']['total'] != str(package.price):
                return Response({'error':{'transaction_id':['Payment total for this transaction does not match the package price']}}, status=status.HTTP_400_BAD_REQUEST)


            # ADD CREDITS TO THE USER
            request.user.credit += package.credit
            request.user.save()

            # SAVE TRANSACTION AND RETURN DATA
            serializedTransaction.save(member=request.user, amount=package.price, is_paypal=True)
            return Response({'transaction':serializedTransaction.data}, status=status.HTTP_201_CREATED)
        return Response({'error':serializedTransaction.errors}, status=status.HTTP_403_BAD_REQUEST)


# Create your views here.
