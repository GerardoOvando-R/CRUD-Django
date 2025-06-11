from django.contrib import admin
from django.urls import path
from apps.dashboard import views as dashboard_views
from apps.tasks import views as tasks_views 

from django.conf import settings  
from django.conf.urls.static import static





urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_views.dashboard,name='dashboard'),
    path('bitacora/', dashboard_views.bitacora,name='bitacora'),
    path('profile/', dashboard_views.profile,name='profile'),
    path('edit_profile/<int:profile_id>', dashboard_views.edit_profile, name='edit_profile'),
    path('delete_profile/<int:profile_id>' , dashboard_views.delete_profile, name='delete_profile'),
    path('export/', dashboard_views.report, name='report-general'),
    
    path('signin/', dashboard_views.signin,name='signin'),
    path('signup/', dashboard_views.signup,name='signup'),
    path('close/', dashboard_views.close,name='close'),
    #Editar perfil
    path('edit/', dashboard_views.edit,name='edit'),
    path('save/<int:id_user>', dashboard_views.save,name='save'),
    path('cancel/', dashboard_views.cancel,name='cancel'),

    #Tasks
    path('task/', tasks_views.tasks, name='tasks')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
