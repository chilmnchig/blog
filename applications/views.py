from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.urls import reverse
from urllib.parse import urlencode

from applications.models import MontyHole

import random

nums = [1, 2, 3]


def monty_open(res, ans):
    nums = [1, 2, 3]
    if res == ans:
        nums.remove(res)
        result = random.choice(nums)
    else:
        nums.remove(res)
        nums.remove(ans)
        result = nums[0]
    return result


def show_percentage():
    objects = MontyHole.objects.all()
    total_changed = 0
    total_not_changed = 0
    total_changed_true = 0
    total_not_changed_true = 0
    for object in objects:
        if object.change:
            total_changed += 1
            if object.judge:
                total_changed_true += 1
        else:
            total_not_changed += 1
            if object.judge:
                total_not_changed_true += 1
    if total_changed == 0:
        total_changed = 1
    if total_not_changed == 0:
        total_not_changed = 1
    percentage_changed = total_changed_true * 100 / total_changed
    percentage_not_changed = total_not_changed_true * 100 / total_not_changed
    percentage_changed = round(percentage_changed, 2)
    percentage_not_changed = round(percentage_not_changed, 2)
    return percentage_changed, percentage_not_changed


def index(request):
    if request.method == "POST":
        if request.POST.get("select"):  # ドアを最初に動作を選んだとき
            res = request.POST.get("select")[0]
            res = int(res)
            ans = random.randint(1, 3)
            opened = monty_open(res, ans)
            open = ""
            change = ""
            judge = ""
        elif request.POST.get("open"):
            res = request.POST.get("res")
            ans = request.POST.get("ans")
            opened = request.POST.get("opened")
            open = request.POST.get("open")[0]
            res = int(res)
            ans = int(ans)
            opened = int(opened)
            open = int(open)
            change = False
            judge = False
            if res != open:
                change = True
            if open == ans:
                judge = True
            MontyHole.objects.create(change=change, judge=judge)
            context = {'res': res, 'ans': ans, 'opened': opened, 'open': open}
            base_url = reverse('result')
            query_string = urlencode(context)
            url = "{}?{}".format(base_url, query_string)
            return redirect(url)

    else:
        res = ""
        ans = ""
        opened = ""
        open = ""
        change = ""
        judge = ""

    restart = False
    p_changed, p_not_changed = show_percentage()
    context = {'nums': nums, 'res': res, 'ans': ans, 'opened': opened,
               'open': open, 'change': change, 'judge': judge,
               'restart': restart, 'p_changed': p_changed,
               'p_not_changed': p_not_changed}
    return TemplateResponse(request, "monty_hole/index.html", context)


def result(request):
    res = request.GET.get("res", "")
    ans = request.GET.get("ans", "")
    opened = request.GET.get("opened", "")
    open = request.GET.get("open", "")
    try:
        res = int(res)
        ans = int(ans)
        opened = int(opened)
        open = int(open)
        change = False
        judge = False
        if res != open:
            change = True
        if open == ans:
            judge = True
    except ValueError:
        change = ""
        judge = ""

    restart = True
    p_changed, p_not_changed = show_percentage()
    context = {'nums': nums, 'res': res, 'ans': ans, 'opened': opened,
               'open': open, 'change': change, 'judge': judge,
               'restart': restart, 'p_changed': p_changed,
               'p_not_changed': p_not_changed}
    if "" not in list(context.values()):
        return TemplateResponse(request, "monty_hole/index.html", context)
    else:
        return redirect('index')
