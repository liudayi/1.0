from django.urls import path
from mood import views
urlpatterns = [
    path('mood-list',views.MoodListView.as_view(),name='mood-list'),
    path('mood-add',views.MoodCreateView.as_view(),name='mood-add'),
    path('<int:pk>/mood-update',views.MoodUpdateView.as_view(),name='mood-update'),
    path('<int:pk>/mood-delete',views.MoodDeleteView.as_view(),name='mood-delete'),
    path('mood-time-line',views.MoodTimeLineView.as_view(),name='mood-time-line'),
]
