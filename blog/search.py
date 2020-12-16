from functools import reduce
from operator import and_
from django.db.models import Q

import re


def search_objects(objects, keyword):
    q_list = re.split(' |　', keyword)
    query = reduce(
                and_, [Q(title__icontains=q) | Q(content__icontains=q) for q in q_list]
            )
    objects = objects.filter(query)
    return objects
