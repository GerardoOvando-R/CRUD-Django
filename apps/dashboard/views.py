from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile , Bitacora
from .forms import ProfileForm
from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator

from openpyxl import Workbook
from django.http import HttpResponse
from django.utils import timezone

# Create your views here.

def signin(request):
    return render(request, 'sign-in.html')

def signup(request):
    return render(request, 'sign-up.html')


def dashboard(request):
    return render(request, 'dashboard.html')

def tables(request):
    bitacora_list = Bitacora.objects.all()
    profile_list = Profile.objects.all()

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
        'search_query2' : search_query2
    }

    return render(request, 'tables.html' ,context)

def profile(request):
    profile = Profile.objects.last() 

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            print(request.POST, request.FILES)
            new_profile.save() 

            messages.success(request, f'Se guardó el perfil {new_profile.name}')

            #Bitacora
            Bitacora.objects.create(
                movimiento=f"se creo el perfil: {new_profile.name} con phone {new_profile.phone}"
            )
        return redirect(to='profile')
    else:
        print('No está mostrando los datos')
        form = ProfileForm()

    context = {
        'profile': profile,
        'form': form
    } 
    return render(request, 'profile.html', context)

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
    profile.delete()

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