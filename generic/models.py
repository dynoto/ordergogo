from django.db import models

# Create your models here.
class GenericModel(models.Model):
    class Meta:
        abstract = True

    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    deleted     = models.BooleanField(default=False)

class Category(GenericModel):
    def __str__(self):
        return "%s" %(self.title)
        
    title       = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')

class OtherCategory(Category):
    owner       = models.OneToOneField('member.Member', related_name='other_category_owner')