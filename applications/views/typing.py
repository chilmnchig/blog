from django.template.response import TemplateResponse

import csv
from random import sample
import re
import json


def index(request):
    with open('./applications/views/characters/edited_words.csv') as f:
        rows = list(csv.reader(f))
    selected_rows = sample(rows, 15)
    proverbs = []
    for proverb in selected_rows:
        string = ''.join(proverb)
        lis = re.split('（|）', string)
        proverbs.append(lis)
    proverbs = dict(enumerate(proverbs, 1))

    context = {'proverbs': json.dumps(proverbs)}
    return TemplateResponse(request, "typing/index.html", context)
