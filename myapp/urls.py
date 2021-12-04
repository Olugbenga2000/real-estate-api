from .views import RegisterAPI,LoginView,LogoutView,PropertyView
from django.urls import path,include
from rest_framework.authtoken import views as Token_views

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/property/', PropertyView.as_view({'get': 'list',
                                                'post': 'create'}), name='property'),
    path('api/property/<int:pk>', PropertyView.as_view({'get': 'retrieve',
                                                'put': 'update',
                                                'patch' : 'partial_update',
                                                'delete' : 'destroy'}), name='single'),
    
]