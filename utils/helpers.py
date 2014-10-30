__author__ = 'yawen'

def to_human_readable(size):
    size = int(size)
    if size < 1024:
        return ('%d' % size) + ' Bytes'
    size /= 1024.0
    if size < 1024:
        return ('%.2f' % size) + ' KB'
    size /= 1024.0
    if size < 1024:
        return ('%.2f' % size) + ' MB'
    size /= 1024.0
    return ('%.2f' % size) + ' GB'


def gen_pagination_list(page_count, current_page):
    pages = []
    if page_count > 10:
        if current_page < 7:
            pages = [i + 1 for i in range(7)]
            pages += ['..', page_count - 1, page_count]
        elif current_page > page_count - 7:
            pages = [1, 2, '..']
            pages += [page_count - 6 + i for i in range(7)]
        else:
            pages += [1, 2, 3, '..']
            pages += [current_page - 1, current_page, current_page + 1, '..']
            pages += [page_count - 1, page_count]
    else:
        pages = [i + 1 for i in range(page_count)]
    return pages