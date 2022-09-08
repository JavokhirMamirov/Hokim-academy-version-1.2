from django.core.paginator import Paginator


def pagination_json(page, query, serializer, number_of_object):
    if page is None:
        page = 1
    p = Paginator(query, number_of_object)
    pg = p.page(page)
    ser = serializer(pg.object_list, many=True)

    if pg.has_next():
        next_page = pg.next_page_number()
    else:
        next_page = None

    if pg.has_previous():
        pervios_page = pg.previous_page_number()
    else:
        pervios_page = None

    pagination = {
        "next_page": next_page,
        "current_page": page,
        "pervios_page": pervios_page,
        "pages_count": p.num_pages,
        "number_of_object": number_of_object,
        "items_count": query.count()
    }
    dt = {
        "pagination": pagination,
        "result": ser.data
    }

    return dt
