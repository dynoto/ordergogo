from django.db import models
from random import randrange

def generate_photo_name(self, filename):
        url = "media/item/%s/%s%s" % (self.item.id, randrange(100000,999999), filename)
        return url

# Create your models here.
class GenericModel(models.Model):
    class Meta:
        abstract = True

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)


class Photo(GenericModel):
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    caption     = models.CharField(max_length=254, default='')
    img_url     = models.URLField()
    img_thumb   = models.URLField(null=True)
