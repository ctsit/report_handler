# Utility functions


# Checks if a dictionary contains the key, returns a boolean
def containsKey(dict: dict, key: str) -> bool:
    return key in dict.keys()


# Gets the sheetname and data from the dictionary
def retrieve_data_and_sheet_name(kwargs: dict):
    data = None
    sheetname = 'unspecified'

    if containsKey(kwargs, 'data'):
        data = kwargs['data']
        if containsKey(kwargs, 'sheet') and kwargs['sheet'].strip() != '':
            sheetname = kwargs['sheet']

    return data, sheetname


# Separates the headers(columns) and the data(rows) for the sheet
def get_headers_and_content(data):
    headers = []
    content = []
    for key in data.keys():
        headers.append(key)
        content.append(str(data[key]))

    return headers, content
