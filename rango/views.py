from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, \
     LoginForm, \
     PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    categories = Category.objects.order_by('-likes')[:5];
    pages = Page.objects.order_by('-views')[:5]
    context = {}
    context['categories'] =  categories
    context['pages'] = pages
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).seconds > 10:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context['visits'] = visits
    response = render(request, 'rango/index.html', context)
    return response

def about(request):
    context = {'boldmessage' : ' I am in about page bold font', 
               'message' : 'About page'}
    visits = request.session.get('visits')
    if not visits:
        visits = 1
    context['visits'] = visits;
    return render(request, 'rango/about.html', context)

def category_view(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()
        print ("Querying the search engine")
        context_dict['result_list'] = "Search results Dummy"
        context_dict['query'] = query

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass
    if not context_dict['query']:
        context_dict['query'] = category.name
    return render(request, 'rango/category.html', context_dict)

@login_required
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

@login_required
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

def register_view(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'registered' : registered}
    return render(request, 'rango/registration.html', context_dict)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your rango account is disabled")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
         return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you are logged in you can see this page")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/rango/')

def password_change_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        if password != c_password:
            print(" Password didn't match ")
            return render(request, 'rango/passwordchange.html', {})
        if request.user.is_authenticated():
            request.user.set_password(password)
            request.user.save()
            return index(request)
        else:
            return HttpResponseRedirect('/rango/login/')
    else:
        password_form = PasswordChangeForm()
    return render(request, 'rango/passwordchange.html', {})
        
def track_url(request, page_id):
    if request.method == 'GET': 
        page = Page.objects.get(id=page_id)
        if page:
            page.views += 1
            page.save()
            return HttpResponseRedirect(page.url)
    return HttpResponse("Page id doesn't exist")
