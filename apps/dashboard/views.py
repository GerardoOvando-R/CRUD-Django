from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile , Bitacora, User
from .forms import ProfileForm, EditForm
from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator

from openpyxl import Workbook
from django.http import HttpResponse
from django.utils import timezone

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


def signin(request):
    if request.method == 'GET':
        return render(request, 'sign-in.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            Bitacora.objects.create(
                    user = None,
                    movimiento=f"Intento de inicio de sesión fallido para el usuario: {username}"
                )
            return render(request, 'sign-in.html', {
                'error_match' : 'Usuario o contraseña son incorrectas'
            })
        else:
            Bitacora.objects.create(
                    user = user,
                    movimiento=f"Inicio de sesión exitoso para el usuario: {username}"
                )
            login(request,user)
            return redirect('profile')
#Cerrar sesión
def close(request):
    if request.user.is_authenticated:
        username = request.user.username

    Bitacora.objects.create(
        user= request.user,
        movimiento= f'Cierra sesión: {username}'
    )

    logout(request)
    return redirect('signin')

#Resitrar usuarios
def signup(request):
    if request.method == 'GET':
        return render(request, 'sign-up.html')
    else: 
        print(request.POST)
        #Comparación de contraseñas
        if request.POST['password1'] == request.POST['password2']:
            #Generar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1']
                )
                user.save() #Guardar objesto en db
                login(request, user) #Guardar sesión
                
                Bitacora.objects.create(
                    user = user,
                    movimiento=f"Registro exitoso para el usario: {user.username}"
                )

                return redirect('profile')
            except:
                Bitacora.objects.create(
                    user = None,
                    movimiento=f"Intento fallido para el usuario: {request.POST['username']}, Usuario ya existente"
                )
                return render(request, 'sign-up.html', {
                    'error_exists' : 'Usuario ya existe'
                })
        else:
            Bitacora.objects.create(
                    user = None,
                    movimiento=f"Intento de registro fallido: {request.POST['username']}, Las contraseñas no coinciden"
                )
        return render(request, 'sign-up.html', {
                    'error_match' : 'Las contraseñas no coinciden'
                })

def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def bitacora(request):
    #profile_list = Profile.objects.filter(estatus1=True, username= 'Gera').order_by('name')
    profile_list = Profile.objects.all().order_by('estatus1')
    #filter(estatus1=True).order_by('name')
    bitacora_list = Bitacora.objects.all().order_by('-fecha')

    #Buscador perfiles
    search_query = request.GET.get('filter', '')
    if search_query: 
        profile_list = profile_list.filter(
            Q(name__icontains = search_query) |
            Q(email__icontains = search_query) 
        )
    
    #Paginador
    paginator = Paginator(profile_list, 5)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)

    #-----------------------------------------

    search_query2 = request.GET.get('filter2', '')
    if search_query2: 
        bitacora_list = bitacora_list.filter(
            Q(movimiento__icontains = search_query2) |
            Q(fecha__icontains = search_query2) 
        )
    
    paginator2 = Paginator(bitacora_list, 5)
    page_number2 = request.GET.get('page')
    bitacoras = paginator2.get_page(page_number2)

    context={
        'bitacoras': bitacoras,
        'profiles' : profiles,
        'search_query' : search_query,
        'search_query2' : search_query2,
    }

    return render(request, 'bitacora.html' ,context)

@login_required
def profile(request):
    profile = Profile.objects.filter(user=request.user).first() 
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            if profile is None:
                new_profile = form.save(commit=False)
                new_profile.user=request.user
                print(request.POST, request.FILES)
                new_profile.save() 

                messages.success(request, f'Se guardó el perfil {new_profile.name}')

                #Bitacora
                Bitacora.objects.create(
                    movimiento=f"se creo el perfil: {new_profile.name} con phone {new_profile.phone}"
                )
            else:
                messages.error(request, 'Ya tienes un perfil creado')
            return redirect(to='profile')
    else:
        print('No está mostrando los datos')
        form = ProfileForm()

    context = {
        'profile': profile,
        'form': form
    } 
    return render(request, 'profile.html', context)

def edit(request):
    profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'edit.html', {
        'profile':profile,
        })

def save(request, id_user):#-> Obtenemos el id por parámetro
    profile = get_object_or_404(Profile, pk=id_user)# Si existe el id nos crea el objeto profile
    
    if request.method == 'POST':# Validando si se manda la información del formulario para actualizar
        form = EditForm(request.POST, instance=profile)#Guardando los datos que se pasan por el formulario en el form "EditForm"
        comp = Profile.objects.filter(username=request.POST['username']).first()
        
        
        if form.is_valid() and comp is None:
            update_profile = form.save(commit=False)
            update_profile.save()
            messages.success(request, f'Se actualizó el perfil de manera correcta')
            return redirect('profile')
        else:
            print('entro en el elif')
            messages.error(request, f'El usuario {comp.username} ya existe, por favor elije otro.')
            print("no se guardaron los datos desde la validación")
            return redirect('edit')
        
    else:
        print("erro en el primer if")
    return redirect('profile')
    
def cancel(request):
    return redirect('profile')

def edit_profile(request, profile_id):
    #Buscar objeto profile
    profile = get_object_or_404(Profile, pk=profile_id)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            update_profile = form.save(commit=False)
            print(request.POST)
            update_profile.save()

            #Bitacora
            Bitacora.objects.create(
                movimiento=f"se actualizó el perfil: {update_profile.name} con phone {update_profile.phone}"
            )

            return redirect('tables')
        
        else:
            print("No se ha actualizado los datos en la base de datos")
    else:
        print("Error")

        context = {
            'profile': profile,
        }

        return render(request, 'edit-profile.html', context)

def delete_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    profile.estatus1 = False
    profile.save()
    #profile.delete()

    #Bitacora
    Bitacora.objects.create(
                movimiento=f"se dió de baja el perfil: {profile.name} con phone {profile.phone}"
            )
    return redirect( 'tables')
    
def report(request):
    profiles = Profile.objects.all().order_by('name') 

    #Filtrar por algún campo
    #profiles = Profile.objects.filter(phone='12345').order_by('name')
    time = timezone.now().date()

    #Libro de Trabajo
    wb = Workbook()
    ws = wb.active

    #Agregar encabezados al archivo excel
    ws.append(['Username', 'Nombre', 'Telefono', 'Correo'])

    #Agregar contenido
    for profile in profiles:
        ws.append([profile.username, profile.name, profile.phone, profile.email] )

    #Respuesta HTTP
    response= HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachement; filename=profiles-{time}.xlsx'

    wb.save(response)
    return response