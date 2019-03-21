from django.db import models
import json
import cv2
from django.core.files import File
import random, string
from mie_monitor_web.settings import host

# Create your models here.


class Image(models.Model):
    id = models.AutoField(primary_key=True)

    img = models.ImageField(upload_to="img")
    rect_body_img = models.ImageField(upload_to="img")
    face_detect_result = models.TextField()
    body_detect_result = models.TextField()

    def rect_body(self):
        bodies = eval(str(self.body_detect_result))
        img = cv2.imread(self.img.path)
        for body in bodies:
            left = int(body["humanbody_rectangle"]["left"])
            top = int(body["humanbody_rectangle"]["top"])
            width = int(body["humanbody_rectangle"]["width"])
            height = int(body["humanbody_rectangle"]["height"])
            cv2.rectangle(img, (left, top), (left + width, top + height), (0, 255, 0), 4)
        cv2.imwrite('temp.jpg', img)
        self.rect_body_img = File(open('temp.jpg', 'rb'))
        self.save()

    def get_face_set(self):
        faces_set = []
        faces = eval(str(self.face_detect_result))
        img = cv2.imread(self.img.path)
        for face in faces:
            tmp_img = img.copy()
            left = int(face["face_rectangle"]["left"])
            top = int(face["face_rectangle"]["top"])
            width = int(face["face_rectangle"]["width"])
            height = int(face["face_rectangle"]["height"])
            tmp_img = tmp_img[top: top + height, left: left + width]
            tmp_path = 'media/img_crop/{0}.jpg'.format(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15)))
            cv2.imwrite(tmp_path, tmp_img)
            face['face_img_url'] = host + '/' + tmp_path
            faces_set.append(face)

        return faces_set
