from django.contrib import admin
from django.urls import path
from apps.dashboard import views

from django.conf import settings  
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard,name='dashboard'),
    path('tables/', views.tables,name='tables'),
    path('profile/', views.profile,name='profile'),
    path('signin/', views.signin,name='signin'),
    path('signup/', views.signup,name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
