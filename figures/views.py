
# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json

# Models
from figures import models

# Create your views here.
def index(request):

    national = models.NationalPrediction.manager.all().order_by('-date')[0]
    data = {}
    for district in models.District.manager.all():
        data[district.id] = district.prediction_set.last().dem_win_percent
    context = {
        'navbar': 'index',
        'national': national,
        'cartogram_data': json.dumps(data),
    }

    return render(request, 'figures/index.html', context=context)

def about(request):
    context = {
        'navbar': 'about',
    }

    return render(request, 'figures/about.html', context=context)

def blog_list(request,
              template='figures/blog_list.html',
              page_template='figures/includes/blog_summary.html'):
    blog_list = models.BlogPost.manager.all()

    context = {
        'navbar': 'blog',
        'blog_list': blog_list,
        'page_template': page_template
    }

    if request.is_ajax():
        template = page_template

    return render(request, template, context=context)

def blog(request, pk, slug=None):
    blog = get_object_or_404(models.BlogPost, pk=pk)

    context = {
        'blog': blog
    }

    return render(request, 'figures/blog.html', context=context)

def statemap(request):
    context = {
        'navbar': 'states',
        "states_list": models.State.manager.all()
    }

    return render(request, 'figures/statemap.html', context=context)

def cartogram(request):
    data = {}
    for district in models.District.manager.all():
        data[district.id] = district.prediction_set.last().dem_win_percent

    context = {
        'navbar': 'cartogram',
        'cartogram_data': json.dumps(data)
    }

    return render(request, 'figures/cartogram.html', context=context)

def state(request, state):
    state = get_object_or_404(models.State, name=state)
    districts = state.district_set.all()

    context = {
        'navbar': 'states',
        'state': state,
        'district_list': districts,
    }

    return render(request, 'figures/state.html', context=context)

def district(request, state, districtno):
    district = get_object_or_404(models.District, state=state, no=districtno)
    district_profile = get_object_or_404(models.DistrictProfile, district=district)
    latest_prediction = district.prediction_set.last()

    context = {
        'navbar': 'states',
        'state': state,
        'district': district,
        'district_profile': district_profile,
        'latest_prediction': latest_prediction
    }

    return render(request, 'figures/district.html', context=context)

def districtbyid(request, id):
    return redirect(get_object_or_404(models.District, id=id))
