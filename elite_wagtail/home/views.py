
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ArticlePage, UserFeedBack
from .utils import verify_parameters_exist
from django.utils.translation import ugettext as _


@api_view(['GET', 'PUT'])
def liked(request, pk, *args, **kwargs):
    article = get_object_or_404(ArticlePage, pk=pk)

    if request.method == 'PUT':
        article.liked_count += 1
        article.save()

    return Response({
        'liked_count': article.liked_count
    })


@api_view(['POST'])
def UserFeedback(request, *args, **kwargs):
    
    if request.method == 'POST': 
        image_url = request.POST.get('image_url', '')
        nick_name = request.POST.get('username', '')
        content = request.POST.get('content', '')
        contact = request.POST.get('contact', '')

        if len(content) > 100:
            return Response({
                'success': False,
                'code': 400,
                'msg': _("输入数字超过100个字")
            })

        parameters_dict = {
            'image_url': image_url,
            'nick_name': nick_name,
            'content': content,
            'contact': contact
        }
       
        result = verify_parameters_exist(parameters_dict)
        if result is not None:
            return Response(result)
        
        try:
            userfeedback = UserFeedBack(
                image_url=image_url,
                nick_name=nick_name,
                content=content,
                contact=contact
            ) 
            userfeedback.save()
        except Exception as e:
            return Response({
                'success': False,
                'code': 400,
                'msg': _("提交反馈失败")
            })   

    return Response({
        'success': True,
        'code': 200,
        'msg': _("反馈成功")
    })

