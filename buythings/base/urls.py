from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('details/<int:pk>/', views.details, name='details'),
	path('categories/', views.categories, name='categories'),
	path('categories/<int:pk>/', views.product_list, name='product_list'),
]
