# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import generic.utils as GenericUtils
from django.http import Http404
from generic.models import Category
from generic.serializers import CategorySerializer

# Create your views here.

class GenericList(APIView):
    Model = None
    ModelSerializer = None
    swagger = {
        'message':'',
        'request_serializer':'',
        'response_serializer':''
    }

    def get_objects(self, request):
        return self.Model.objects.all()

    def get(self, request, format=None):
        objects = self.get_objects(request)
        objects, count = GenericUtils.paginator(objects, request.QUERY_PARAMS.get('page'))
        serializedObjects = self.ModelSerializer(objects, many=True)
        return Response({self.Model._meta.verbose_name_plural.title():serializedObjects.data, 'count':count})

class GenericListOwner(GenericList):
    def get_objects(self, request):
        return self.Model.objects.filter(owner=request.user)

class GenericDetails(APIView):
    Model = None
    ModelSerializer = None

    def get_object(self, user, model_id):
        try:
            return self.Model.objects.get(owner=user, id=model_id)
        except:
            raise Http404

    def get(self, request, model_id, format=None):
        modelObject = self.get_object(request.user, model_id)
        serializedModelInstance = self.ModelSerializer(modelObject)
        return Response({self.Model._meta.verbose_name_plural.title():serializedModelInstance.data})


    def delete(self, request, model_id, format=None):
        modelObject = self.get_object(request.user, model_id)
        try:
            modelObject.delete()
            return Response({'message':'%s deleted successfully' % (self.Model.__name__)})
        except:
            return Response({'error':'%s cannot be deleted because it is still associated with other objects' %(self.Model.__name__)}, status=status.HTTP_400_BAD_REQUEST)



class CategoryList(GenericList):
    Model = Category
    ModelSerializer = CategorySerializer
    
    def get(self, request, format=None):
        """
        This API is to list out all categories that is available for choosing by vendor or customer
        ---
        serializer: generic.serializers.CategorySerializer
        """
        return super(CategoryList, self).get(request)