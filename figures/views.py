from django.shortcuts import render, get_object_or_404, render
from .models import *
# Create your views here.
def index(request):
    context = {

    }

    return render(request, 'figures/index.html', context=context)

def about(request):
    context = {

    }

    return render(request, 'figures/about.html', context=context)

def state(request, state):

    context = {
        "state": get_object_or_404(State, abbr=state)

    }
    return render(request, 'figures/state.html', context)

def district(request, state, district):

    state_obj = get_object_or_404(State, abbr=state)
    context = {
        "district": District.objects.filter(state=state_obj, no=district)
    }
    return render(request, 'figures/state.html', context)
