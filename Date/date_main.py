# SPOT_PRICE from the params.py
# Strike price form the sheet
# no of frequency = expected gains * diff months
# Expiry date from the params.py
# Problem statement

import csv
import json
from datetime import datetime
from date_parameters import SPOT_PRICE, FILE_FULL_PATH, EXPIRY_DATE
from utils.utils import diff_month, covert_json_to_csv, replace_with_null, expected_gains_no_of_frequency


def main():
    try:
        current_date = datetime.today()
        csvfile = open(FILE_FULL_PATH, 'r')

        fieldnames = ("ID", "COI", "CCHNGINOI", "CVOLUME", "CIV", "CLTP", "CCHNG", "CBIDQTY", "CBIDPRICE",
                      "Call Ask Price", "CASKQTY", "strike price", "BIDQTY", "BIDPRICE", "Put Ask Price", "ASKQTY",
                      "CHNG", "LTP", "IV", "VOLUME", "CHNGINOI", "OI", "extras")
        reader = csv.DictReader(csvfile, fieldnames)

        unwanted_columns = ["ID", "COI", "CCHNGINOI", "CVOLUME", "CIV", "CLTP", "CCHNG", "CBIDQTY", "CBIDPRICE",
                            "CASKQTY", "BIDQTY", "BIDPRICE", "ASKQTY", "CHNG", "LTP", "IV", "VOLUME", "CHNGINOI",
                            "OI", "extras"]

        arrdata = []

        for row in reader:
            arrdata.append(row)

        # Removing headers from the csv file
        arrdata = arrdata[2:]

        arr_data_len = len(arrdata)

        # Data conversion
        for index, row in enumerate(arrdata):

            # Remove unwanted data
            for key in unwanted_columns:
                row.pop(key)

            # Replace - with null values
            row = replace_with_null(row)

            # Adding the rows for spot price and strike price
            row['spot price'] = SPOT_PRICE
            row['Expiry Date'] = EXPIRY_DATE

            # Changing date string to date object
            expiry_date = ""
            if row['Expiry Date']:
                expiry_date = datetime.strptime(row['Expiry Date'], '%d-%b-%Y')
                row['Expiry Date'] = expiry_date

            # Calculate Diff months
            row['Difference months'] = ''
            diff_months = ''
            if expiry_date:
                diff_months = diff_month(expiry_date, current_date)
                row['Difference months'] = diff_months

            # Data conversion from string to float
            if row['Call Ask Price']:
                row['Call Ask Price'] = float(row['Call Ask Price'].replace(',', ''))
            if row['Put Ask Price']:
                row['Put Ask Price'] = float(row['Put Ask Price'].replace(',', ''))

            # Depreciation and appreciation % data
            return_data = expected_gains_no_of_frequency(row)
            if return_data['success']:
                row = return_data['row']
            else:
                raise Exception

            for row_key, row_value in row.items():
                if not row_value:
                    row[row_key] = '-'

            if arr_data_len - 1 == index:
                arrdata = sorted(arrdata, key=lambda i: i['Expiry Date'])
                for exp_row in arrdata:
                    if exp_row['Expiry Date']:
                        now = exp_row['Expiry Date']
                        exp_row['Expiry Date'] = now.strftime("%d/%m/%Y")

        out = json.dumps(arrdata)
        jsonfile = open('../../output.json', 'w')
        jsonfile.write(out)

        # Conversion from JSON to CSV
        status = covert_json_to_csv(arrdata)
        print({"success": status})

    except Exception as error:
        print({"success": False, "error": error})


main()
