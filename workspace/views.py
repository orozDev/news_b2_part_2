from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from core.models import News, Category, Tag, Comment
from workspace.forms import NewsForm


def workspace(request):
    if request.user.is_authenticated:
        news = News.objects.filter(author=request.user).order_by('-id')
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 6)
        paginator = Paginator(news, limit)
        news = paginator.get_page(offset)
        return render(request, 'workspace/index.html', {'news_list': news})
    return redirect('/')


def list_of_categories(request):
    if request.user.is_authenticated:
        categories = Category.objects.all().order_by('-id')
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 2)
        paginator = Paginator(categories, limit)
        categories = paginator.get_page(offset)
        return render(request, 'workspace/categories.html', {'categories': categories})
    return redirect('/')


def detail_news(request, id):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=id, author=request.user)
        comments = Comment.objects.filter(news=news)
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 2)
        paginator = Paginator(comments, limit)
        comments = paginator.get_page(offset)
        return render(request, 'workspace/detail_news.html', {'news': news, 'comments': comments})
    return redirect('/')


def create_category(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/create_category.html', {'message': 'Name is required'})
            category = Category.objects.create(name=name)
            return redirect('/workspace/categories/')

        return render(request, 'workspace/create_category.html')
    return redirect('/')


def update_category(request, id):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, id=id)
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/update_category.html', {
                    'message': 'Name is required',
                    'category': category,
                })

            category.name = name
            category.save()
            return redirect('/workspace/categories/')

        return render(request, 'workspace/update_category.html', {'category': category})
    return redirect('/')


def delete_category(request, id):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, id=id)
        category.delete()
        return redirect('/workspace/categories/')
    return redirect('/')


def create_news(request):
    if request.user.is_authenticated:
        form = NewsForm()
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES)
            if form.is_valid():
                news = form.save(commit=False)
                news.author = request.user
                news.save()
                return redirect('/workspace/')
        return render(request, 'workspace/create_news.html', {'form': form})
    return redirect('/')


def update_news(request, id):
    news = get_object_or_404(News, id=id)
    form = NewsForm(instance=news)
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = NewsForm(request.POST, request.FILES, instance=news)
            if form.is_valid():
                form.save()
                return redirect(f'/workspace/news/{id}/')
        return render(request, 'workspace/update_news.html', {
            'form': form,
            'news': news,
        })

    return redirect('/')


def list_of_tags(request):
    if request.user.is_authenticated:
        tags = Tag.objects.all().order_by('-id')
        offset = request.GET.get('offset', 1)
        limit = request.GET.get('limit', 20)
        paginator = Paginator(tags, limit)
        tags = paginator.get_page(offset)
        return render(request, 'workspace/tags.html', {'tags': tags})
    return redirect('/')


def create_tag(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/create_tag.html', {'message': 'Name is required'})
            tag = Tag.objects.create(name=name)
            return redirect('/workspace/tags/')

        return render(request, 'workspace/create_tag.html')
    return redirect('/')


def update_tag(request, id):
    if request.user.is_authenticated:
        tag = get_object_or_404(Tag, id=id)
        if request.method == 'POST':
            name = request.POST.get('name', None)
            if name is None or name == '':
                return render(request, 'workspace/update_tag.html', {
                    'message': 'Name is required',
                    'tag': tag,
                })

            tag.name = name
            tag.save()
            return redirect('/workspace/tags/')

        return render(request, 'workspace/update_tag.html', {'tag': tag})
    return redirect('/')


def delete_tag(request, id):
    if request.user.is_authenticated:
        tag = get_object_or_404(Tag, id=id)
        tag.delete()
        return redirect('/workspace/tags/')
    return redirect('/')


def delete_news(request, id):
    if request.user.is_authenticated:
        news = get_object_or_404(News, id=id)
        news.delete()
        return redirect('/workspace/')
    return redirect('/')


def delete_comment(request, id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        return JsonResponse({'isDeleted': True})
    return HttpResponseForbidden()
