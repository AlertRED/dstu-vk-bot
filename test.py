def foo(faculties):
    row_len = 0
    result = 0
    count_items_in_row = 0
    count_rows = 0
    limit_row_len = 30
    limit_items_in_row = 4
    limit_rows = 9
    for faculty in faculties:
        row_len += len(faculty)
        print(faculty, end=', ')
        count_items_in_row += 1
        result += 1
        if not ((count_items_in_row == 0) or (
                row_len + len(faculty) < limit_row_len and count_items_in_row < limit_items_in_row)):
            print('(%s, %s)' % (count_items_in_row, row_len))
            count_items_in_row = 0
            row_len = 0
            count_rows += 1
            if count_rows == limit_rows:
                break
    else:
        print('(%s, %s)' % (count_items_in_row, row_len))

    return result


print(
    foo(['1234567', '123', '12345', '123456789', '12345678', '123456789', '123456789', '12345678', '12345', '123456789',
         '12345678', '123456789', '12345678', '12345', '123456789']))
