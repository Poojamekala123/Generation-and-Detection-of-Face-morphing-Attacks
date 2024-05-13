from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from userapp.models import *
from facemorphattacks.FaceMatch import compare_images

# Create your views here.
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin':
            messages.success(request, 'Login Successful')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('admin_login')
    return render(request, 'main/admin-login.html')

def admin_logout(request):
    messages.success(request, 'Successfully Logged Out')
    return redirect('index')

def admin_dashboard(request):
    users = UserModel.objects.all().count()
    pending = ApplicationModel.objects.filter(status = 'Pending').count()
    verified = ApplicationModel.objects.filter(status = 'Verified').count()
    invalid = ApplicationModel.objects.filter(status = 'Invalid').count()
    context = {
        'users':users,
        'pending':pending,
        'verified':verified,
        'invalid':invalid
    }
    # context['users'] = users
    # context['pending'] = pending
    # context['verified'] = verified
    # context['invalid'] = invalid
    return render(request, 'admin/admin-dashboard.html',context)

def admin_view_users(request):
    users = UserModel.objects.all()    
    return render(request, 'admin/admin-view-users.html',{
        'users':users
    })


def admin_detect_morph(request):
    applications = ApplicationModel.objects.filter(status = 'Pending').order_by('-id')
    return render(request, 'admin/admin-detect-morph.html', {
        'applications':applications
    })

def admin_pending_applications(request):
    applications = ApplicationModel.objects.filter(status = 'Pending').order_by('-id')
    return render(request, 'admin/admin-pending-applications.html',{
        'applications':applications
    })

def admin_verified_applications(request):
    applications = ApplicationModel.objects.filter(status = 'Verified').order_by('-id')

    return render(request, 'admin/admin-verified-applications.html',{
        'applications':applications
    })

def admin_invalid_applications(request):
    applications = ApplicationModel.objects.filter(status = 'Invalid').order_by('-id')

    return render(request, 'admin/admin-invalid-applications.html',{
        'applications':applications
    })

def admin_analysis(request):
    pending = ApplicationModel.objects.filter(status = 'Pending').count()
    verified = ApplicationModel.objects.filter(status = 'Verified').count()
    invalid = ApplicationModel.objects.filter(status = 'Invalid').count()

    return render(request, 'admin/admin-analysis.html',{
        'pending':pending,
        'verified':verified,
        'invalid':invalid
    })

def admin_verify_application(request,id):
    app = ApplicationModel.objects.get(pk=id)
    user_image = 'media/'+str(app.picture)
    images = MorphedImages.objects.all()
    for i in images:
        original_image = 'media/'+str(i.morphedimage)
        print(original_image)
        result = compare_images(user_image,'media/'+str(i.morphedimage))
        print(result,type(result))
        if result >=0.9:
            app.status = 'Invalid'
            app.save()
            messages.info(request, 'This Application Contains a Morphed Image')
            return redirect('admin_invalid_applications')
    app.status = 'Verified'
    app.save()
    messages.success(request, 'This Application Has a Clean Image')

    return redirect('admin_verified_applications')