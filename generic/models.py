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
        
    def __unicode__(self):
        return str(self.title)

    title       = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')


class OtherCategory(Category):
    def __unicode__(self):
        return str(self.title)
    owner       = models.OneToOneField('member.Member', related_name='other_category_owner')


class Announcement(GenericModel):
    title       = models.CharField(max_length=254)
    description = models.TextField(blank=True, default='')





