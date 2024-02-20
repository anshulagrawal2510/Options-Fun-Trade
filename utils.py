import pandas as pd
from parameters import SPOT_PRICE, STRIKE_PRICE


def diff_month(d1, d2):
    return round(((d1.year - d2.year)*365 + (d1.month - d2.month)*30 + (d1.day - d2.day))/30, 4)


def covert_json_to_csv(json_data):
    try:
        df = pd.DataFrame(json_data)
        df.to_csv("../output.csv")
        return True
    except Exception as error:
        print(error)
        return False


def replace_with_null(row):
    try:
        for row_key, row_value in row.items():
            if row_value == '-':
                row[row_key] = ""
        return row
    except Exception as error:
        print(error)
        return False


def appr_expected_gains(ask_price, percent):
    try:
        expected_gains = ''
        if ask_price:
            expected_gains = round((((1 + percent/100) * SPOT_PRICE) - STRIKE_PRICE)/ask_price, 4)
        return expected_gains
    except Exception as error:
        print(error)
        return ''


def depre_expected_gains(ask_price, percent):
    try:
        expected_gains = ''
        if ask_price:
            expected_gains = round((STRIKE_PRICE - ((1 - percent/100) * SPOT_PRICE))/ask_price, 4)
        return expected_gains
    except Exception as error:
        print(error)
        return ''
