# from django.shortcuts import render
from rest_framework import viewsets
from credit.models import Credit, Package, Transaction
from credit.serializers import PackageSerializer

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

# class CreditViewSet(viewsets.ModelViewSet):
#     queryset = Credit.objects.all()


# Create your views here.
