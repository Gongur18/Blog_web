from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from webApp import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'books', views.BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('webApp.urls')),
]
