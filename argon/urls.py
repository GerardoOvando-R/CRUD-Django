from django.contrib import admin
from django.urls import path
from apps.dashboard import views

from django.conf import settings  
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard,name='dashboard'),
    path('bitacora/', views.bitacora,name='bitacora'),
    path('profile/', views.profile,name='profile'),
    path('edit_profile/<int:profile_id>', views.edit_profile, name='edit_profile'),
    path('delete_profile/<int:profile_id>' , views.delete_profile, name='delete_profile'),
    path('export/', views.report, name='report-general'),
    

    path('signin/', views.signin,name='signin'),
    path('signup/', views.signup,name='signup'),
    path('close/', views.close,name='close'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
