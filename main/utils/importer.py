import pandas
import random
import string


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


def random_string(size=7, allowed=None, prefix=""):
    """
    A random string generator function.  This function allows the caller to generate a random string either using the
    default settings, or some specific values.

    :param size: The length of the random string that should be generated.  The default for this is 7 characters long.
    :type size: int

    :param allowed: The alphabet of all possible values which should be used when generating the random string.  If no
    alphabet is supplied then a default of `string.ascii_letters` and 'string.digits` will be used.
    :type allowed: str or a non-empty sequence

    :return:
    """

    if allowed is None or not isinstance(allowed, str):
        allowed = string.ascii_letters + string.digits
    return prefix + "-" + "".join(random.choice(allowed) for x in range(size))
