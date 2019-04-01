
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ArticlePage


@api_view(['GET', 'PUT'])
def liked(request, pk, *args, **kwargs):
    article = get_object_or_404(ArticlePage, pk=pk)

    if request.method == 'PUT':
        article.liked_count += 1
        article.save()

    return Response({
        'liked_count': article.liked_count
    })
