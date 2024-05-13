import random

import cv2
from django.contrib import messages
from django.shortcuts import redirect, render

from facemorphattacks.FaceMorph import facemorph
from facemorphattacks.FaceMatch import compare_images

from .models import *


# Create your views here.
def user_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        picture = request.FILES['picture']
        password = request.POST.get('password')
        UserModel.objects.create(name=name,email=email,mobile=mobile,city=city,picture=picture,password=password)
        messages.success(request, 'User Registration Successful')
        return redirect('user_login')
    return render(request, 'user/user-register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            obj = UserModel.objects.get(email=email,password=password)
            request.session['user_id']= obj.id
            messages.success(request, 'Login Successful')
            return redirect('user_dashboard')
        except:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('user_login')
        
    return render(request, 'user/user-login.html')

def user_logout(request):
    messages.success(request, 'Log out Successful')
    return redirect('index')

def dashboard(request):
    return render(request, 'user/user-dashboard.html')

def user_morph(request):
    user_id = request.session['user_id']
    user = UserModel.objects.get(pk=user_id)
    if request.method == 'POST':
        img1 = request.FILES['image1']
        img2 = request.FILES['image2']
        img3 = request.FILES['image2']
        obj = MorphedImages.objects.create(image1=img1,image2=img2,image3=img3,user=user)
        morphedimg = facemorph(obj.image1,obj.image2,obj.image3)
        randnumber = random.randint(0,9999)
        obj.morphedimage = f'morphed/image{randnumber}.png'
        cv2.imwrite(f'media/morphed/image{randnumber}.png',morphedimg)
        obj.save()
        # Merging the third image with the morphed imaged using image1 and image2
        # second_morph = facemorph(obj.image3,obj.morphedimage)
        # randnumber = random.randint(0,9999)
        # obj.morphedimage = f'morphed/image{randnumber}.png'
        # cv2.imwrite(f'media/morphed/image{randnumber}.png',second_morph)
        # obj.save()
        messages.success(request, 'Image_Morphed Successfully')
        return redirect('user_morph_result',id=obj.id)

    return render(request, 'user/user-morph.html')

def user_morph_result(request,id):
    data = MorphedImages.objects.get(pk=id)
    return render(request, 'user/user-morph-result.html',{'data':data})


def user_my_profile(request):
    user_id = request.session['user_id']
    user = UserModel.objects.get(pk=user_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        user.name = name
        user.mobile=mobile
        user.password=password
        try:
            user.picture = request.FILES['picture']
        except:
            pass
        user.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect('user_my_profile')
    context = {}
    context['user']=user
    return render(request, 'user/user-my-profile.html',context)

def user_apply(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        surname = request.POST.get('surname')
        dob = request.POST.get('dob')
        picture = request.FILES['picture']
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('martial')
        citizenship_by = request.POST.get('citizenship')
        education = request.POST.get('education')
        ApplicationModel.objects.create(fullname=fullname,surname=surname,dob=dob,picture=picture,email=email,mobile=mobile,
                                        gender=gender,marital_status=marital_status,citizenship_by=citizenship_by,education=education) 
        messages.success(request, 'Applied Successfully')
        return redirect('user_apply')
    return render(request, 'user/user-apply.html')

def user_analysis(request):
    # user_image = 'media/morphed/image5743.png'
    # original_image = 'media/original/1_14.jpg'
    # result = compare_images(user_image,original_image)
    # print(result)
    if request.method == 'POST':
        picture = request.FILES['picture']
        print(picture)
        obj = ImageAnalysisModel.objects.create(upload_image=picture)
        user_image = 'media/'+str(obj.upload_image)
        images = MorphedImages.objects.all()
        for i in images:
            original_image = 'media/'+str(i.morphedimage)
            print(original_image)
            result = compare_images(user_image,'media/'+str(i.morphedimage))
            print(result,type(result))
            if result >=0.9:
                messages.info(request, 'This is a Morphed Image')
                return redirect('user_analysis')
        
        messages.info(request, 'This is a clean Image')    
        return redirect('user_analysis')

        
        
    return render(request, 'user/user-analysis.html')


