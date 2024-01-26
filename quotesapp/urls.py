from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_tag/', views.add_tag, name='add_tag'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('tag/<tag_name>/', views.tag_detail, name='tag_detail'),
    path('author/<int:pk>/', views.author_detail, name='author_detail'),
    path('delete/<int:pk>/', views.QuoteDelete.as_view(), name='quote_delete'),
    path('update/<int:pk>/', views.QuoteUpdate.as_view(), name='quote_update'),
]
