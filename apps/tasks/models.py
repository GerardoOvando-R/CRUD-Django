from django.db import models
from apps.dashboard.views import Profile

class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField(max_length=50)
    descripcion = models.TextField(max_length=100)
    estatus = models.BooleanField(default=False)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id', default=False)
    class Meta:
        db_table='tasks'
