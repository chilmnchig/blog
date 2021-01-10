from django.template.response import TemplateResponse

from random import randint, choice
import csv


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
    with open('randomapp/weapon_names.csv') as f:
        weapon_list = list(csv.reader(f))
    if request.GET.get('display'):
        result = choice(weapon_list)[0]
    else:
        result = ""
    return TemplateResponse(request, 'random/weapon.html', {'result': result})


# %% テスト
if __name__ == '__main__':
    with open('randomapp/weapon_names.csv') as f:
        weapon_list = list(csv.reader(f))
    result = choice(weapon_list)[0]
    print(result)
