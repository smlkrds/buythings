from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('details/<int:pk>/', views.details, name='details'),
	path('search/', views.search, name='search'),
	path('categories/', views.categories, name='categories'),
	path('categories/<int:pk>/', views.product_list, name='product_list'),
	path('logout/', views.logout_view, name='logout'),
	path('sell_stuff/', views.add_product, name='sell_stuff'),
	path('my_stuff/', views.my_stuff, name='my_stuff'),
	path('remove_my_stuff/<int:pk>/', views.remove_my_stuff, name='remove_my_stuff'),
]
