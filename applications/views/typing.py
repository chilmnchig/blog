from django.template.response import TemplateResponse

import csv
from random import sample
import re


def index(request):
    with open('./applications/views/characters/edited_words.csv') as f:
        rows = list(csv.reader(f))
    selected_rows = sample(rows, 15)
    proverbs = []
    i = 1
    for proverb in selected_rows:
        string = ''.join(proverb)
        lis = re.split('（|）', string)
        lis.insert(0, i)
        proverbs.append(lis)
        i += 1

    context = {'proverbs': proverbs}
    return TemplateResponse(request, "typing/index.html", context)
