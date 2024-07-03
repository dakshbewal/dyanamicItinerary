from django.contrib import admin
from django.urls import path, include
from itineraries.views import itinerary_list
from itineraries import views

urlpatterns = [
    path("", itinerary_list, name="itinerary_list"),
    path("create-itinerary", views.create_itinerary, name= "create-itinerary" ),
    path("delete/<int:id>", views.delete_itinerary, name= "delete_itinerary" ),
    path("update/<int:id>", views.update_itinerary, name="update_itinerary"),
    path('create/details/<int:itinerary_id>/', views.create_itinerary_details, name='create_itinerary_details'),  # Create itinerary details
    path('itineraries/<int:itinerary_id>/', views.itinerary_with_details, name='itinerary_with_details'),
    path('update_itinerary_detail/<int:itinerary_id>/', views.update_itinerary_detail, name="update_itinerary_detail"),
    path('edit_itinerary_detail/<int:detail_id>/', views.edit_itinerary_detail, name="edit_itinerary_detail"),
    path('delete_itinerary_detail/<int:detail_id>/', views.delete_itinerary_detail, name="delete_itinerary_detail"),
    path('api/create/', views.api_create, name= "api_create"),
    path('api/get/', views.get_detail, name= "all_detail"),
    path('api/edit/', views.api_edit_itineraryDetails, name= "api_edit"),
    path('search', views.search_itineraries, name= "search_itineraries"),
    path('create_or_edit_itinerary/<int:itinerary_id>', views.create_or_edit_itinerary, name= "create_or_edit_itinerary"),
    
]
    