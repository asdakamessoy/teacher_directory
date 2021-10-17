import pandas


def get_data_from_upload(file_path, file_type, header_mapping=None):
    """
    Extract Teacher's data from file

    :param file_path:
    :param file_type:
    :param header_mapping:
    :return: data_dict, headers and errors
    """
    errors = None
    data_dict = []
    headers = []
    try:
        raw_data = None
        if file_type == "csv":
            # csv should be utf-8
            raw_data = pandas.read_csv(file_path, encoding="utf-8")

        else:
            # get 1st excel sheet only
            raw_data = pandas.read_excel(file_path)
        # convert data frame to dictionary
        headers = raw_data.keys()
        for row_data in raw_data.values:
            entry = {}
            for header, val in zip(headers, row_data):
                if header and str(val):
                    if header_mapping:
                        header = header_mapping[header]
                    # replace nan string value
                    entry[header] = str(val).replace("nan", "")
            data_dict.append(entry)
    except UnicodeDecodeError as e:
        print(e)
        errors = "We experienced a decoding issue with this file. Please ensure documents are uploaded in utf-8 format."
    return data_dict, headers, errors
