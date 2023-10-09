from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect

from core.decorators import increase_views
from core.filters import NewsFilter
from core.forms import LoginForm
from core.models import News, Category, Comment


def main(request):
    search = request.GET.get('search', None)
    if search:
        news = News.objects.filter(name__icontains=search, is_published=True).order_by('-id')
    else:
        news = News.objects.filter(is_published=True).order_by('-id')
    tag = request.GET.get('tag', None)
    if tag:
        news = news.filter(tags__id=tag).order_by('-id')

    filter_set = NewsFilter(request.GET, queryset=news)

    offset = request.GET.get('offset', 1)
    limit = request.GET.get('limit', 3)

    paginator = Paginator(filter_set.qs, limit)
    news = paginator.get_page(offset)

    return render(request, 'index.html', {'news_list': news, 'filter': filter_set})


@increase_views
def detail_news(request, id):
    news = get_object_or_404(News, id=id, is_published=True)
    comments = Comment.objects.filter(news=news)
    return render(request, 'detail_news.html', {'news': news, 'comments': comments})


def about(request):
    return render(request, 'about.html')


def news_by_category(request, id):
    category = get_object_or_404(Category, id=id)
    news = News.objects.filter(category=category).order_by('-id')
    return render(request, 'index.html', {'news_list': news})


def create_comment_ajax(request):
    news_id = int(request.POST.get('news'))
    name = request.POST.get('name')
    text = request.POST.get('text')
    news = get_object_or_404(News, id=news_id)

    new_comment = Comment.objects.create(
        news=news,
        name=name,
        text=text,
    )
    return JsonResponse({
        'id': new_comment.id,
        'news': new_comment.news.id,
        'name': new_comment.name,
        'text': new_comment.text,
        'date': new_comment.date.strftime('%d %B %Y')
    })


def login_profile(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if request.session.get('next_link', None) is None:
        request.session.modified = True
        request.session['next_link'] = request.GET.get('next') or '/'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next_link = request.session['next_link']
                return redirect(next_link)
            return render(request, 'auth/login.html', {
                'message': 'The user is not found or invalid password', 'form': form})
    return render(request, 'auth/login.html', {'form': form})


def logout_profile(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('/')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'auth/profile.html')
    return redirect('/')


def change_profile(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            userChecking = User.objects.filter(username=username)

            if userChecking.exists() and request.user.username != username:
                return render(request, 'auth/change_profile.html', {
                    'message': f'User with this username {username} is already exists'})

            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()
            return redirect('/profile/')

        return render(request, 'auth/change_profile.html')
    return redirect('/')


def change_password(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            user = request.user

            if not user.check_password(password):
                return render(request, 'auth/change_password.html', {'message': 'Please enter valid password'})
            if new_password != confirm_password:
                return render(request, 'auth/change_password.html', {'message': 'The passwords don\'t match'})
            if len(new_password) < 8:
                return render(request, 'auth/change_password.html', {
                    'message': 'You password must contain more than 8 charchers'})

            user.set_password(new_password)
            user.save()
            login(request, user)
            return redirect('/profile/')

        return render(request, 'auth/change_password.html')
    return redirect('/')


# Create your views here.
def login_ajax(request):
    if request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'isAuthenticated': True}, status=200)
            return JsonResponse({'isAuthenticated': False, 'message': 'The user is not found or invalid password', },
                                status=400)
    return HttpResponseNotAllowed


def logout_ajax(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({'isLogout': True}, status=200)