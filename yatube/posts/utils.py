from django.conf import settings
from django.core.paginator import Paginator


def get_page_context_with_paginator(request, post_list):
    paginator = Paginator(post_list, settings.LIM_POSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
