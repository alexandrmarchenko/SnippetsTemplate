from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm, UserRegistrationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def my_snippets(request):
    context = {'pagename': 'Мои сниппеты'}
    snippets = Snippet.objects.filter(user=request.user)
    context["snippets"] = snippets
    return render(request, 'pages/view_snippets.html', context)


@login_required
def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }
        return render(request, 'pages/add_snippet.html', context)
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect('snippets-list')
        return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets, 'count': Snippet.objects.filter().count()}
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, id):
    try:
        snippet = Snippet.objects.get(id=id)
        context = {'pagename': 'Просмотр сниппета', 'snippet': snippet, 'type': 'view'}
        return render(request, 'pages/snippet-detail.html', context)
    except ObjectDoesNotExist:
        raise Http404


def snippet_delete(request, id):
    snippet = Snippet.objects.get(id=id)
    snippet.delete()
    # Перенаправление на туже страницу, с которой пришел запрос
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def snippet_edit(request, sid):
    try:
        snippet = Snippet.objects.get(id=sid)
    except ObjectDoesNotExist:
        raise Http404
    if request.method == "GET":
        context = {
            'pagename': 'Редактирование сниппета',
            'snippet': snippet,
            'type': 'edit'
        }
        return render(request, 'pages/snippet-detail.html', context)
    if request.method == "POST":
        form_data = request.POST
        snippet.name = form_data["name"]
        snippet.code = form_data["code"]
        snippet.creation_date = form_data["creation_date"]
        snippet.public = form_data.get("public", False)
        snippet.save()
        return redirect('snippets-list')


def create_user(request):
    context = {'pagename': 'Регистрация пользователя'}
    if request.method == "GET":
        form = UserRegistrationForm()
        context["form"] = form
        return render(request, 'pages/registration.html', context)
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        context['form'] = form
        return render(request, 'pages/registration.html', context)


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': 'PythonBin',
                'errors': ["wrong username or password"]
            }
            return render(request, 'pages/index.html', context)
    return redirect('home')


def logout(request):
    auth.logout(request)
    return redirect('home')
