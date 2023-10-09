from django.shortcuts import get_object_or_404

from core.models import News


def increase_views(func):

    def inner(request, id, *args, **kwargs):
        news = get_object_or_404(News, id=id)
        if request.user.is_authenticated and news.author.id == request.user.id:
            return func(request, id, *args, **kwargs)
        news.views += 1
        news.save()
        return func(request, id, *args, **kwargs)

    return inner