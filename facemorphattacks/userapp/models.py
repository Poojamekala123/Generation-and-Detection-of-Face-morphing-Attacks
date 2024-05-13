from django.db import models

# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=12)
    city = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='images/')
    password = models.CharField(max_length=100)

    class Meta:
        db_table = 'user_details'


class MorphedImages(models.Model):
    image1 = models.ImageField(upload_to='original/')
    image2 = models.ImageField(upload_to='original/')
    image3 = models.ImageField(upload_to='original/',null=True)
    morphedimage = models.ImageField(upload_to='morphed/',null=True)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name='user_morphed_images')
    data = models.DateField(auto_now=True)

    class Meta:
        db_table = 'morphed_images'
   

class ImageAnalysisModel(models.Model):
    upload_image = models.ImageField(upload_to='uploads/')

    class Meta:
        db_table = 'image_analysis'


class ApplicationModel(models.Model):
    fullname = models.CharField(max_length=100)
    surname = models.CharField(max_length=50)
    dob = models.DateField()
    picture = models.ImageField(upload_to='uploads/')
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    gender = models.CharField(max_length=15)
    marital_status = models.CharField(max_length=15)
    citizenship_by = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    status = models.CharField(max_length=50,default='Pending')

    class Meta:
        db_table = 'application_details'
