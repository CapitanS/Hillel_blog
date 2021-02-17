from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from posts.views import RegisterFormView, UpdateProfile
import os


urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('posts.urls')),
    path('', RedirectView.as_view(url='posts/', permanent=True)),

    # Add Django site authentication urls (for login, logout, password management)
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', RegisterFormView.as_view(), name='register'),
    path('accounts/update_profile/', UpdateProfile.as_view(), name='update_profile'),
]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
