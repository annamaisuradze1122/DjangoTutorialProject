from django.urls import path
from . import views


urlpatterns = [ 
    path('',views.profiles,name='profiles' ),
    path('user-profile/<str:pk>',views.user_profile ,name='user-profile'),
    path('login/',views.user_login,name='login' ),
    path('logout/',views.user_logout,name='logout' ),
    path('register/',views.user_register,name='register' ),
    path('account/',views.get_user_account,name='account' ),
    path('edit_account/',views.edit_user_account,name='edit_account' ),

]