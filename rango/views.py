from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    categories = Category.objects.order_by('-likes')[:5];
    pages = Page.objects.order_by('-views')[:5]
    context = {}
    context['categories'] =  categories
    context['pages'] = pages
    return render(request, 'rango/index.html', context);

def about(request):
    context = {'boldmessage' : ' I am in about page bold font', 
               'message' : 'About page'}
    return render(request, 'rango/about.html', context)

def category_view(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass
    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:   
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return category_view(request, category_name_slug)
        else:
            print(form.errors)
    else:
         form = PageForm()
    context_dict = { 'form': form, 'category' : category,
        'category_name_slug': category_name_slug}
    return render(request, 'rango/add_page.html', context_dict)
