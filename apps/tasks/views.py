from django.shortcuts import render
from .models import Tasks
from django.db.models import Q
from django.core.paginator import Paginator

def tasks(request):
    
    print(request.user)
    task = Tasks.objects.all().order_by('estatus')
    
    search_query = request.GET.get('filter', '')
    if search_query: 
        task = task.filter(
            Q(nombre__icontains = search_query)
        )
    
    paginator = Paginator(task,3)
    page_number = request.GET.get('page')
    task_paginator = paginator.get_page(page_number)

    context = {
        'tasks' : task,
        'tasks_paginator' : task_paginator
    }
    
    return render(request, 'tasks.html', context)
# Create your views here.
