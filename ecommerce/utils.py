import os
from uuid import uuid4
from django.db import models

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # managed = True
        abstract = True


def path_and_rename(instance, filename):
    upload_to = "media_files"
    ext = filename.split(".")[-1]
    # get filename
    if instance.pk:
        filename = f"{instance.pk}.{ext}"
    else:
        # set filename as random string
        filename = f"{uuid4().hex}.{ext}"
    # return the whole path to the file
    return os.path.join(upload_to, filename)