from django.shortcuts import render
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    return render(request,'rango/index.html',context=context_dict)


def about(request):
    context_about = {'boldmessage': 'This tutorial has been put together by Vic'}
    return render(request,'rango/about.html',context=context_about)


def show_category(request, category_name_slug):

    context_catdict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_catdict['pages'] = pages
        context_catdict['category'] = category
        
    except Category.DoesNotExist:
        context_catdict['category'] = None
        context_catdict['pages'] = None

    return render(request,'rango/category.html', context=context_catdict)