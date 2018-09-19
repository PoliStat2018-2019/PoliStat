from django.shortcuts import render

# Create your views here.
def index(request):
    context = {

    }

    return render(request, 'figures/index.html', context=context)

def about(request):
    context = {

    }

    return render(request, 'figures/about.html', context=context)