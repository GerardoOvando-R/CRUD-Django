from django.shortcuts import render
from .models import Tasks

def tasks(request):
    task = Tasks.objects.all()
    
    print(request.GET)
    if request.GET:
        task = Tasks.objects.filter(nombre=request.GET)
    else:
        print('no se encontraron datos')
    context = {
        'tasks' : task
    }
    
    return render(request, 'tasks.html', context)
# Create your views here.
