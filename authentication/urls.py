from authentication import views
from django.urls import path

urlpatterns = [
    path('user/login/',views.LoginView.as_view(),name='user-login'),
    path('user/logout/',views.LogoutView.as_view(),name='user-logout'),
]
