# V 1.0 CGT_Calculator
# Written by Sam H
# USE AT OWN RISK
# ----------------------------------------------------------------------------------------------------------------------
# This program is designed to import a .csv file of asset transactions. Once imported it will calculate and return the
# applicable CGT tax. The program will also write to a file showing a summary of all the CGT transactions for a
# specific financial year.
#
# Version 1 - Australian Shares
# The first version only supports Australian shares. The CSV must be structured with 4 columns in this order:
# 1.TICKER -- ASX ticker name
# 2.QUANTITY -- number of shares purchased/sold
# 3.TOTAL (PAID)/RECEIVED -- total $AUD (paid)/received. note, if PAID, the number recorded should be negative
# 4.DATE -- date of purchase or sale
#
# Additionally, the CSV file must be sorted by date.
#
# Version 2 - International Shares - COMING SOON
# Version 3 - Cryptocurrency  - COMING SOON


import csv
from dateutil import parser


# class to store values of a share bundle
class Bundle:
    def __init__(self, ticker, quantity, price, date):
        self.ticker = ticker
        self.quantity = float(quantity)
        self.price = float(price)
        self.unit_price = float(price) / float(quantity)
        self.date = parser.parse(date)

    def __str__(self):
        return f"{self.ticker} {self.quantity} {self.unit_price} {self.date}"


def main():
    print("Welcome to CGT Calculator. \n\nPlease select from the following by typing it out: \nShares or Crypto\n")
    mode = input()
    print(mode)
    print("Please paste the file-path of the .csv file holding the transaction history:\n")
    filepath = input()
    try:
        csv_file = open(filepath, 'r')
        calculator(mode, csv_file)
    except Exception as e:
        print(e)
    finally:
        csv_file.close()


# function to call the different calculators depending on user requirements
def calculator(mode, csv_file):
    trade_data = csv.reader(csv_file)
    if mode.lower() == "shares":
        csv_to_share_bundles(trade_data)
    elif mode.lower() == "crypto":
        print("Not implemented yet")


# function is given CSV data and puts it into classes
# when a sale is found in the CSV a separate function is called to update the internal data
# function will output:
# 1. a summary of all the sales and resulting net gain
# 2. the remaining purchases for input next FY if needed.
def csv_to_share_bundles(trade_data):
    # go past headers
    next(trade_data)
    shares_dict = {}
    f = open("summary.txt", "w+")
    f2 = open("next_fy_data.csv", "w+")
    CGT_amount = 0
    for row in trade_data:
        # go past blanks (if any)
        if row[0] == '':
            continue
        if row[0] in shares_dict:
            # check if it is a sale - only need to check in this if statement because a stock needs to have been
            # purchased to be able to be sold - therefore there must be another entry in the dictionary
            if float(row[2]) > 0:
                net_sale = calculate_share_cgt(shares_dict[row[0]], row)
                f.write("The sale on {date} of {quantity} shares of {ticker} for {price} ".format(date=row[3],
                                                                                                  quantity=row[1],
                                                                                                  ticker=row[0],
                                                                                                  price=row[2]))
                f.write(" resulted in the net gain/(loss) of: ")
                f.write(str(round(net_sale, 2)))
                f.write("\n")
                CGT_amount += net_sale
            else:
                shares_dict[row[0]].append(Bundle(row[0], row[1], row[2], row[3]))
        else:
            shares_dict[row[0]] = [Bundle(row[0], row[1], row[2], row[3])]
    f.write("Resulting in a net gain or (loss) of: ")
    f.write(str(round(CGT_amount, 2)))
    # write the remaining purchases to a CSV file for use in future FYs
    f2.write("TICKER,QUANTITY,TOTAL (PAID)/RECEIVED,DATE\n")
    for share in shares_dict:
        for i in range(0, len(shares_dict[share])):
            f2.write("{ticker}, {quantity}, {price}, {date}\n".format(ticker=shares_dict[share][i].ticker,
                                                                      quantity=shares_dict[share][i].quantity,
                                                                      price=shares_dict[share][i].unit_price *
                                                                            shares_dict[share][i].quantity,
                                                                      date=shares_dict[share][i].date))
    f.close()
    f2.close()
    return shares_dict


# it is always guaranteed that the earliest sale for a specific stock will be at the start of the array
# assuming that the CSV is sorted by date
# because you have to have the stock to be able to sell it - not including shorting but that isn't taxed under CGT
# function processes a sale using FIFO and returns the updated dictionary along with the taxable gain/loss
# function that is given a sale and an array of the corresponding purchases of a particular asset
# it then returns the net gain.
def calculate_share_cgt(share_transactions, sale):
    sale_quantity = float(sale[1])
    sale_proceeds = float(sale[2])
    cgt_date = parser.parse(sale[3])
    i = 0
    # Total amount recorded under CGT - for this particular sale --- Sum of all net sales
    net_gain = 0
    # Amount recorded under CGT for each particular parcel (each purchase)
    net_parcel_sale = 0
    while sale_quantity != 0:
        if sale_quantity < share_transactions[i].quantity:
            share_transactions[i].quantity -= sale_quantity
            net_parcel_sale = (sale_quantity * share_transactions[i].unit_price) + sale_proceeds
            # need to apply CGT discount if a gain and purchased > 12 months ago
            if net_parcel_sale > 0 and (cgt_date - share_transactions[i].date).days > 365:
                net_gain += 0.5 * net_parcel_sale
            else:
                net_gain += net_parcel_sale
            sale_quantity = 0
        else:
            net_parcel_sale = (share_transactions[i].quantity * share_transactions[i].unit_price) + \
                              (share_transactions[i].quantity * sale_proceeds / sale_quantity)
            # need to apply CGT discount if a gain and purchased > 12 months ago
            if net_parcel_sale > 0 and (cgt_date - share_transactions[i].date).days > 365:
                net_gain += 0.5 * net_parcel_sale
            else:
                net_gain += net_parcel_sale
            sale_quantity -= share_transactions[i].quantity
            share_transactions.pop(i)
    return net_gain


main()
# Below for testing
# calculator("Shares", "/Users/samholder/PycharmProjects/CGT_Calculator/Aus_Shares.csv")


