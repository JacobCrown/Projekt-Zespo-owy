import cv2 as cv
import os

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from store.models import Customer

from genderModel.main import *
from ageModel.main import *



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

    if customer.profile_image != 'profiles/user-default.png':
        # print('changed image')
        # print(customer.profile_image)
        # print(settings.MEDIA_ROOT + str(customer.profile_image))
        path = os.path.join(settings.MEDIA_ROOT, str(customer.profile_image))
        img = cv.imread(path)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        haar_cascade = cv.CascadeClassifier('haar_face.xml')

        face_rect = haar_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors=2)
        # print('face_rect: ', face_rect)
        # for (x,y,w,h) in face_rect:
        if len(face_rect) > 0:
            (x, y, w, h) = face_rect[0]
                # img = cv.rectangle(img, (x,y), (x+w, y + h), (0, 255, 0), thickness=2)

            face_img = img[y:y+h, x:x+w]

            proper_image = cv.resize(face_img, (200, 200))
            img = cv.rectangle(img, (x,y), (x+w, y + h), (0, 255, 0), thickness=2)
            cv.imwrite(os.path.join(settings.MEDIA_ROOT, f'{str(customer.name)}_tmp.png'), proper_image)
            cv.imshow('cos', proper_image)
            cv.waitKey()

            # IMGPATH = path
            # gender estimation
            IMGPATH = os.path.join(settings.MEDIA_ROOT, f'{str(customer.name)}_tmp.png')
            MODELPATH = os.path.join(settings.BASE_DIR, 'genderModel', 'model.pth')
            model_.load_state_dict(torch.load(MODELPATH, map_location=DEVICE))
            model_.to(DEVICE)
            testimg = load_image(IMGPATH)
            output = predict_gender(model_, testimg)
            customer.predicted_gender = True
            customer.gender = output
            print('gender: ', output)

            # age category estimation
            IMGPATH_AGE = os.path.join(settings.MEDIA_ROOT, f'{str(customer.name)}_tmp.png')
            MODELPATH_AGE = os.path.join(settings.BASE_DIR, 'ageModel', 'model_age.pth')
            model_age_.load_state_dict(torch.load(MODELPATH_AGE, map_location=DEVICE_AGE))
            model_age_.to(DEVICE_AGE)
            testimg = load_image(IMGPATH_AGE)
            output = predict_gender(model_, testimg)
            customer.predicted_age = True
            customer.age = output
            customer._meta.auto_created = True
            customer.save()
            customer._meta.auto_created = False
            print('age', output)
        else:
            print('Face not detected')


post_save.connect(profile_create, sender=get_user_model())
post_save.connect(profile_update, sender=Customer)
