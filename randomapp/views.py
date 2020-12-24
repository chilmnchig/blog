from django.template.response import TemplateResponse

from random import randint, choice

from randomapp.weapon_names import weapon_names


def perform(request):
    if request.GET.get("display"):
        try:
            min = int(request.GET.get("min"))
            max = int(request.GET.get("max"))
            result = randint(min, max)
            error = False
        except ValueError:
            result = "正しく整数を入力してください"
            error = True
    else:
        result = "-"
        error = False
        min = 1
        max = 10
    context = {'result': result, 'error': error, 'min': min, 'max': max}
    return TemplateResponse(request, 'random/index.html', context)


def weapon(request):
    weapon_list = weapon_names.split("\n")
    if request.GET.get('display'):
        result = choice(weapon_list)
    else:
        result = ""
    return TemplateResponse(request, 'random/weapon.html', {'result': result})
