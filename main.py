# Put- depreciation by 5, 10, 20, 30, 40 in percentage
# Call- appreciation by 5, 10, 20, 30, 40 in percentage
# Strike price from user
# Spot price from user
# Calculate Expected gains
# Ask price to vary between call and put on the basis of appreciation and depreciation
# App_Expected_gains = (1.05(spot_price) - strike_price)/call ask_price
# Dep_Expected_gains = (strike_price - 0.95(spot_price)/put ask_price
# Calculate no of frequency
# diff_months = (Expiry_date - current_date) in months
# no_of_frequency = Expected_gains * diff_months
# Sorting on the basis of no of frequency
# Show columns for no_of_frequency, Expected_gains, diff_months
# Sorting on the basis of Expiry dates


import csv
import json
from datetime import datetime
from parameters import SPOT_PRICE, STRIKE_PRICE, FILE_FULL_PATH, LIST_OF_PERCENTAGE
from utils import diff_month, covert_json_to_csv, replace_with_null, appr_expected_gains, depre_expected_gains


def main():
    try:
        current_date = datetime.today()
        csvfile = open(FILE_FULL_PATH, 'r')

        fieldnames = ("ID", "COI", "CCHNGINOI", "CVOLUME", "CIV", "CLTP", "CCHNG", "CBIDQTY", "CBIDPRICE",
                      "Call Ask Price", "CASKQTY", "Expiry Date", "BIDQTY", "BIDPRICE", "Put Ask Price", "ASKQTY",
                      "CHNG", "LTP", "IV", "VOLUME", "CHNGINOI", "OI", "extras")
        reader = csv.DictReader(csvfile, fieldnames)

        arrdata = []

        for row in reader:
            arrdata.append(row)

        # Removing headers from the csv file
        arrdata = arrdata[2:]

        # Data conversion
        for row in arrdata:

            # Remove unwanted data
            row.pop("ID")
            row.pop("COI")
            row.pop("CCHNGINOI")
            row.pop("CVOLUME")
            row.pop("CIV")
            row.pop("CLTP")
            row.pop("CCHNG")
            row.pop("CBIDQTY")
            row.pop("CBIDPRICE")
            row.pop("CASKQTY")
            row.pop("BIDQTY")
            row.pop("BIDPRICE")
            row.pop("ASKQTY")
            row.pop("CHNG")
            row.pop("LTP")
            row.pop("IV")
            row.pop("VOLUME")
            row.pop("CHNGINOI")
            row.pop("OI")
            row.pop("extras")

            # Replace - with null values
            row = replace_with_null(row)

            # Adding the rows for spot price and strike price
            row['spot price'] = SPOT_PRICE
            row['strike price'] = STRIKE_PRICE

            # Changing date string to date object
            expiry_date = ""
            if row['Expiry Date']:
                expiry_date = datetime.strptime(row['Expiry Date'], '%d-%b-%Y')
                row['Expiry Date'] = expiry_date

            # Calculate Diff months
            diff_months = ""
            if expiry_date:
                diff_months = diff_month(expiry_date, current_date)
                row['Difference months'] = diff_months
            else:
                row['Difference months'] = ""

            # Data conversion from string to float
            if row['Call Ask Price']:
                row['Call Ask Price'] = float(row['Call Ask Price'].replace(',', ''))
            if row['Put Ask Price']:
                row['Put Ask Price'] = float(row['Put Ask Price'].replace(',', ''))

            # Depreciation and appreciation % data
            for percent in LIST_OF_PERCENTAGE:

                # Call Appreciation data
                appr_expected_gain = appr_expected_gains(row['Call Ask Price'], percent)
                row[str(percent) + '% Appreciation Expected Gain'] = appr_expected_gain

                # calculate No of frequency
                if appr_expected_gain and diff_months:
                    no_of_frequency = round(appr_expected_gain * diff_months, 4)
                    row[str(percent) + '% Appreciation No of Frequency'] = no_of_frequency
                else:
                    row[str(percent) + '% Appreciation No of Frequency'] = ""

                # Put Depreciation data
                dep_expected_gain = depre_expected_gains(row['Put Ask Price'], percent)
                row[str(percent) + '% Depreciation Expected Gain'] = dep_expected_gain

                # calculate No of frequency
                if dep_expected_gain and diff_months:
                    no_of_frequency = round(dep_expected_gain * diff_months, 4)
                    row[str(percent) + '% Depreciation No of Frequency'] = no_of_frequency
                else:
                    row[str(percent) + '% Depreciation No of Frequency'] = ""

            for row_key, row_value in row.items():
                if not row_value:
                    row[row_key] = '-'

        arrdata = sorted(arrdata, key=lambda i: i['Expiry Date'])

        # Converting date object to string
        for row in arrdata:
            now = row['Expiry Date']
            row['Expiry Date'] = now.strftime("%d/%m/%Y")

        out = json.dumps(arrdata)
        jsonfile = open('file.json', 'w')
        jsonfile.write(out)

        # Conversion from JSON to CSV
        status = covert_json_to_csv(arrdata)
        print({"status": True})

    except Exception as error:
        print({"status": False, "error": error})


main()
