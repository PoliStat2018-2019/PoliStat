
# Django
from django.shortcuts import render, redirect, get_object_or_404

# Models
from figures import models

# Create your views here.
def index(request):
    context = {
        'navbar': 'index',
    }

    return render(request, 'figures/index.html', context=context)

def about(request):
    context = {
        'navbar': 'about',
    }

    return render(request, 'figures/about.html', context=context)

def statemap(request):
    context = {
        'navbar': 'states',
        "states_list": models.State.manager.all()
    }

    return render(request, 'figures/statemap.html', context=context)

def state(request, state):
    state = get_object_or_404(models.State, name=state)
    districts = state.district_set.all()

    context = {
        'navbar': 'states',
        'state': state,
        'district_list': districts
    }

    return render(request, 'figures/state.html', context=context)

def district(request, name):
    pass