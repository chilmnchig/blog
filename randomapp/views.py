from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect

from random import randint


def perform(request):
    if request.GET.get("display"):
        try:
            min = int(request.GET.get("min"))
            max = int(request.GET.get("max"))
            result = randint(min, max)
            error = False
        except:
            result = "正しく整数を入力してください"
            error = True
    else:
        result = "-"
        error = False
        min = 1
        max = 10
    return TemplateResponse(request, 'random/index.html',{'result': result, 'error': error, 'min': min, 'max': max})
