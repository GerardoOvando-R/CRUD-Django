from django.shortcuts import render, redirect
from .models import Profile , Bitacora
from .forms import ProfileForm
from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def tables(request):
    bitacora_list = Bitacora.objects.all()
    profile_list = Profile.objects.all()

    search_query = request.GET.get('filter', '')
    if search_query: 
        profile_list = profile_list.filter(
            Q(name__icontains = search_query) |
            Q(email__icontains = search_query) 
        )
    
    paginator = Paginator(profile_list, 5)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)

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
    profile = Profile.objects.last() #camibar form por Profile traera todos los registros que tenemos

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)# agregar request.FILES
        if form.is_valid():
            new_profile = form.save(commit=False)
            print(request.POST, request.FILES)
            new_profile.save() #Guardar base de datos

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


def signin(request):
    return render(request, 'sign-in.html')

def signup(request):
    return render(request, 'sign-up.html')

