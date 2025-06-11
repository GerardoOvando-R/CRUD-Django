from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)    
    name = models.CharField(max_length=50)
    phone = models.IntegerField(max_length=50)
    email = models.EmailField(max_length=50)
    photo = models.ImageField(upload_to='photos')
    estatus1 = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user')
    def __str__(self):
        return f'{self.id}, {self.name}'
    
    class Meta:
        db_table='profile'

class Bitacora(models.Model):
    id = models.AutoField(primary_key=True)
    movimiento = models.CharField(max_length=150)
    fecha = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='id_user', default=0)
    class Meta:
        db_table='bitacora'
