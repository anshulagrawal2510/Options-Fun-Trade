import pandas as pd


def diff_month(d1, d2):
    return round(((d1.year - d2.year)*365 + (d1.month - d2.month)*30 + (d1.day - d2.day))/30, 4)


def covert_json_to_csv(json_data, date):
    try:
        if date:
            out_file_name = "../date_output.csv"
        else:
            out_file_name = "../strike_output.csv"

        df = pd.DataFrame(json_data)
        df.to_csv(out_file_name)
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


def appr_expected_gains(ask_price, percent, strike_price, spot_price):
    try:
        expected_gains = ''
        if ask_price and strike_price and spot_price:
            expected_gains = round((((1 + percent/100) * spot_price) - strike_price)/ask_price, 4)
        return expected_gains
    except Exception as error:
        print(error)
        return ''


def depre_expected_gains(ask_price, percent, strike_price, spot_price):
    try:
        expected_gains = ''
        if ask_price and strike_price and spot_price:
            expected_gains = round((strike_price - ((1 - percent/100) * spot_price))/ask_price, 4)
        return expected_gains
    except Exception as error:
        print(error)
        return ''


def expected_gains_no_of_frequency(row, list_of_percentage):
    try:
        diff_months = row['Difference months']

        for percent in list_of_percentage:
            appre_expected_gain_column_name = str(percent) + ' Appreciation Expected Gain'
            appre_no_of_frequency_column_name = str(percent) + ' Appreciation No of frequency'
            depr_expected_gain_column_name = str(percent) + ' Depreciation Expected Gain'
            depr_no_of_frequency_column_name = str(percent) + ' Depreciation No of frequency'

            # Call Appreciation data
            appr_expected_gain = appr_expected_gains(row['Call Ask Price'], percent, row['strike price'], row['spot price'])
            row[appre_expected_gain_column_name] = appr_expected_gain

            # calculate No of frequency

            # Put Depreciation data
            dep_expected_gain = depre_expected_gains(row['Put Ask Price'], percent, row['strike price'], row['spot price'])
            row[depr_expected_gain_column_name] = dep_expected_gain

            # calculate No of frequency
            row[appre_no_of_frequency_column_name] = ""
            row[depr_no_of_frequency_column_name] = ""
            if diff_months:
                if appr_expected_gain:
                    no_of_frequency = round(appr_expected_gain * diff_months, 4)
                    row[appre_no_of_frequency_column_name] = no_of_frequency
                if dep_expected_gain:
                    no_of_frequency = round(dep_expected_gain * diff_months, 4)
                    row[depr_no_of_frequency_column_name] = no_of_frequency

        return {"success": True, "row": row}

    except Exception as error:
        return {"success": False, "error":  error}
