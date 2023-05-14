from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Tag(models.Model):
    label = models.CharField(max_length=255)
    
    def __str__(self):
        return self.label
    
class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    # the following field is a generic foreign key, which means it can reference any model.
    # the content_type field is a ForeignKey to the ContentType model, 
    # which is a system model that stores information about all of the models in your Django project.
    # the object_id field is an IntegerField that stores the primary key of the related object.
    # the content_object field is a GenericForeignKey, which is a field that 
    # can point to any object, based on the content_type and object_id fields.
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    # the following line is a GenericForeignKey, which is a field that can point
    # to any object, based on the content_type and object_id fields.
    content_object = GenericForeignKey()
