import cv2 as cv
import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from store.models import Customer

from genderModel.main import *



def profile_create(sender, instance, created, **kwargs):
    if created:

        user = instance
        customer = Customer.objects.create(
            user=user,
            name=user.username,
            email=user.email,
        )

def profile_update(sender, instance, created, **kwargs):

    customer = instance
    user = customer.user
    user.username = customer.name
    user.email = customer.email
    user.save()

    print(customer.profile_image)
    print(settings.MEDIA_ROOT + str(customer.profile_image))
    path = os.path.join(settings.MEDIA_ROOT, str(customer.profile_image))
    img = cv.imread(path)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    haar_cascade = cv.CascadeClassifier('haar_face.xml')

    face_rect = haar_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors=2)
    print(face_rect)
    # for (x,y,w,h) in face_rect:
    if len(face_rect) > 0:
        (x, y, w, h) = face_rect[0]
            # img = cv.rectangle(img, (x,y), (x+w, y + h), (0, 255, 0), thickness=2)

    face_img = img[y:y+h, x:x+w]

    proper_image = cv.resize(face_img, (200, 200))
    img = cv.rectangle(img, (x,y), (x+w, y + h), (0, 255, 0), thickness=2)
    cv.imwrite(os.path.join(settings.MEDIA_ROOT, 'tmp.png'), proper_image)
    cv.imshow('cos', proper_image)
    cv.waitKey()

    # IMGPATH = path
    IMGPATH = os.path.join(settings.MEDIA_ROOT, 'tmp.png')
    MODELPATH = os.path.join(settings.BASE_DIR, 'genderModel', 'model.pth')
    model_.load_state_dict(torch.load(MODELPATH, map_location=DEVICE))
    model_.to(DEVICE)
    testimg = load_image(IMGPATH)
    output = predict_gender(model_, testimg)
    print(output)


post_save.connect(profile_create, sender=get_user_model())
post_save.connect(profile_update, sender=Customer)