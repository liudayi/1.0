from navbar import views
from django.urls import path

urlpatterns=[
    path('list/',views.NavbarView.as_view(),name='navbar-list'),
    path('create/',views.NavCreateView.as_view(),name='navbar-add'),
    path('update/<int:pk>/',views.NavUpdateView.as_view(),name='navbar-update'),
    path('show/',views.NavbarView.as_view(),name='dashboard'),   
    path('delete/<int:pk>/',views.NavDeteleView.as_view(),name='navbar-delete'),
]