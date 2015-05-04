from rest_framework import serializers
from generic.models import Category

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        exclude = kwargs.pop('exclude', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if exclude:
            # Drop any fields that are not specified in the `fields` argument.
            exclusion = set(exclude)
            # existing = set(self.fields.keys())
            for field_name in exclusion:
                self.fields.pop(field_name)

class CategorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title','description')