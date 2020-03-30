from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    
    # path('category/<slug:category_slug>/', views.category_view, name='category_detail'),
    path('comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
    path('category/<slug:category_slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('tag/<slug:tag_slug>/', views.TagsCategoryDetailView.as_view(), name='tag'),
    path('<slug:category_slug>/<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
    
    # path('category-by-created/<slug:category_slug>/', views.category_view_by_created, name='category_detail_by_created'),
    path('scrape/', views.scrape, name='scrape'),
]