def containsKey(dict: dict, key: str) -> bool:
    return key in dict.keys()


def retrieve_data_and_sheet_name(kwargs: dict):
    data = None
    sheetname = 'unspecified'

    if containsKey(kwargs, 'data'):
        data = kwargs['data']
        if containsKey(kwargs, 'sheet') and kwargs['sheet'].strip() != '':
            sheetname = kwargs['sheet']

    return data, sheetname


def get_headers_and_content(data):
    headers = []
    content = []
    for key in data.keys():
        headers.append(key)
        content.append(data[key])
    return headers, content
