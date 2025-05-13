"""
URL configuration for secureweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.urls import path
# from crypto import views
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('text/', views.encrypt_text_view, name='encrypt_text'),
#     path('image/', views.encrypt_image, name='encrypt_image'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.urls import path
from crypto import views

urlpatterns = [
    path('', views.home, name='home'),
    path('algo/des/', views.des_combined_view, name='des_combined'),
    path('algo/rsa/', views.rsa_combined_view, name='rsa_combined'),
    path('algo/text/', views.text_cipher_combined_view, name='text_combined'),
]