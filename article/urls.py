from django.urls import path
from .views import *

urlpatterns = [
    path('Backend_blog_list',BlogListView.as_view(),name='blog-list-backend'),
    path('blog_create',BlogCreateView.as_view(),name='blog-add'),
    path('<int:pk>/blog_update',BlogUpdateView.as_view(),name='blog-update'),
    path('<int:pk>/blog_delete',BlogDeleteView.as_view(),name='blog-delete'),
    
    path('article_detail/<int:pk>',ArticleDetailView.as_view(),name='blog-detail'),
    #path('article_list',ArticleListView.as_view(),name='blog-list'),

    path('category_create',CategoryCreateView.as_view(),name='category-add'),
    path('category_list',CategoryListView.as_view(),name='category-list'),
    path('<int:pk>/category_update',CategoryUpdateView.as_view(),name='category-update'),
    path('<int:pk>/category_delete',CategoryDeleteView.as_view(),name='category-delete'),
    path('<int:pk>/category_list',CategoryWeightView.as_view(),name='category-article-list'),
    #点击目录标签进入目录页面,会显示每个分类下的文章摘要
    
    path('purepage_create',PurepageCreateView.as_view(),name='pure-page-add'),
    path('<int:pk>/purepage_update',PurepageUpdateView.as_view(),name='pure-page-update'),
    path('<int:pk>/purepage_delete',PurepageDeleteView.as_view(),name='pure-page-delete'),
    path('purepage_list',PurepageListView.as_view(),name='pure-page-list'),

    path('blog_create_image_upload',ImageUpload.as_view(),name='image-upload'),
]
