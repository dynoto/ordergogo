from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

def paginator(objects, page=1):
    paginator = Paginator(objects,15)
    try:
      objects = paginator.page(page)
    except PageNotAnInteger:
      objects = paginator.page(1)
    except EmptyPage:
      objects = paginator.page(paginator.num_pages)
    return objects, paginator.count


def validate_email_format(email):
    pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return bool(re.match(pattern, email))
