from django.urls import path
from . import views as userViews

urlpatterns = [
    path('dashboard',userViews.dashboard,name='user_dashboard'),
    path('morph',userViews.user_morph,name='user_morph'),
    path('morph-result/<int:id>',userViews.user_morph_result,name='user_morph_result'),
    path('analysis',userViews.user_analysis,name='user_analysis'),
    path('apply',userViews.user_apply,name='user_apply'),
    path('login',userViews.user_login,name='user_login'),
    path('logout',userViews.user_logout,name='user_logout'),
    path('register',userViews.user_register,name='user_register'),
    path('profile',userViews.user_my_profile,name='user_my_profile'),
]