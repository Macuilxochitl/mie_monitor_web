from django.db import models


# Create your models here.


class Image(models.Model):
    id = models.AutoField(primary_key=True)

    img = models.ImageField(upload_to="img")
    face_detect_result = models.TextField()
    body_detect_result = models.TextField()
