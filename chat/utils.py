from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator


def get_paginator(qs, page_size, page, paginated_type, **kwargs):
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return paginated_type(
        page=page_obj.number,
        total_pages=p.num_pages,
        has_next=page_obj.has_next(),
        messages=page_obj.object_list,
        **kwargs
    )
