def get_text(elements):
    return list(map(lambda x: x.text, elements))

def parse_table_by_headers(heading, rows):
    headers = get_text(heading.find_all("th"))
    data_values = get_text(rows.find_all("td"))

    return dict(zip(headers, data_values))
