from django.shortcuts import render, redirect
from .models import Profile , Bitacora
from .forms import ProfileForm

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def tables(request):
    return render(request, 'tables.html')

def profile(request):
    profile = Profile.objects.first() #camibar form por Profile traera todos los registros que tenemos

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)# agregar request.FILES
        if form.is_valid():
            new_profile = form.save(commit=False)
            print(request.POST, request.FILES)
            new_profile.save() #Guardar base de datos

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

