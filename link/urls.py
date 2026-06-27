from link import views
from django.urls import path

urlpatterns= [
    path('list/',views.LinkListView.as_view(),name='link-list'),
    path('create/',views.LinkCreateView.as_view(),name='link-add'),
    path('update/<int:pk>/',views.LinkUpdateView.as_view(),name='link-update'),
    path('delete/<int:pk>/',views.LinkDeleteView.as_view(),name='link-delete'),
]
