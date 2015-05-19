# from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
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

    def create(self, request):
        """
        Create a new transaction record (record will be verified before saving to db)
        ---
        serializer : credit.serializers.TransactionSerializer
        """
        serializedTransaction = TransactionSerializer(data=request.data)
        if serializedTransaction.is_valid():
            package = get_object_or_404(Package,id=request.data['package'])
            serializedTransaction.save(member=request.user, amount=package.price, transaction_id='123')
            return Response(serializedTransaction.data, status=status.HTTP_201_CREATED)
        return Response({'errors':serializedTransaction.errors}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
