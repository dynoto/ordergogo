# from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import generic.utils as GenericUtils
from django.http import Http404

# Create your views here.
def get_object(self, user, item_id):
        try:
            return Item.objects.get(owner=user, id=item_id)
        except:
            raise Http404

class GenericList(APIView):
    Model = None
    ModelSerializer = None

    def get(self, request, format=None):
        objects = self.Model.objects.filter(owner=request.user)
        objects, count = GenericUtils.paginator(objects, request.QUERY_PARAMS.get('page'))
        serializedObjects = self.ModelSerializer(objects, many=True)
        return Response({self.Model._meta.verbose_name_plural.title():serializedObjects.data, 'count':count})


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
        return Response(serializedModelInstance.data)


    def delete(self, request, model_id, format=None):
        modelObject = self.get_object(request.user, model_id)
        try:
            modelObject.delete()
            return Response({'message':'%s deleted successfully' % (self.Model.__name__)})
        except:
            return Response({'error':'%s cannot be deleted because it is still associated with other objects' %(self.Model.__name__)}, status=status.HTTP_400_BAD_REQUEST)

