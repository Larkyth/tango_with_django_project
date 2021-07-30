from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponse

from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request,'rango/index.html',context=context_dict)


def about(request):
    context_about = {'boldmessage': 'This tutorial has been put together by Vic'}
    return render(request, 'rango/about.html', context=context_about)


def show_category(request, category_name_slug):

    context_ctdict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)

        context_ctdict['pages'] = pages
        context_ctdict['category'] = category       
    except Category.DoesNotExist:
        context_ctdict['category'] = None
        context_ctdict['pages'] = None

    return render(request, 'rango/category.html', context=context_ctdict)


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('{/rango/}')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':category_name_slug}))

        else:
            print(form.errors)

    context_adpdict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_adpdict)