from django.urls import path
from . import views as adminViews

urlpatterns = [ 
            path('login',adminViews.admin_login,name='admin_login'),
            path('logout',adminViews.admin_logout,name='admin_logout'),
            path('dashboard',adminViews.admin_dashboard, name='admin_dashboard'),
            path('view-users',adminViews.admin_view_users,name='admin_view_users'),
            path('detect-morph-attack',adminViews.admin_detect_morph, name='admin_detect_morph'),
            path('pending-applications',adminViews.admin_pending_applications,name='admin_pending_applications'),
            path('verified-applications',adminViews.admin_verified_applications,name='admin_verified_applications'),
            path('admin-invalid-applications',adminViews.admin_invalid_applications,name='admin_invalid_applications'),
            path('analysis',adminViews.admin_analysis,name='admin_analysis'),
            path('verify-application/<int:id>',adminViews.admin_verify_application,name='admin_verify_application'),
]