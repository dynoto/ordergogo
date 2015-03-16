from django.db import models

# Create your models here.

class Photo(models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return str(self.id)

    caption     = models.CharField(max_length=254, default='')
    img_url     = models.URLField()
    img_thumb   = models.URLField(null=True)

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)