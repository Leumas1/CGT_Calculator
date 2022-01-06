# CGT_Calculator - Version 1.0
USE AT OWN RISK

This program is designed to import a .csv file of asset transactions. Once imported it will calculate and return the applicable CGT tax. 
The first version of the program only supports Australian shares.

## Inputs:
1. A CSV file containing share transactions<br />
  The CSV must be structured with 4 columns in this order:<br />
    a.TICKER -- ASX ticker name<br />
    b.QUANTITY -- number of shares purchased/sold<br />
    c.TOTAL (PAID)/RECEIVED -- total $AUD (paid)/received. note, if PAID (purchase), the number recorded should be negative<br />
    d.DATE -- date of purchase or sale -- The CSV should be sorted based off of this column (easily done in excel)<br />

## Outputs:
1. summary.txt<br />
  a. Will show what the net gain/(loss) is for each sale.<br />
  b. As well as the total CGT assessable amount or loss to be carried forward.<br />
2. next_fy_data.csv<br />
  a. will translate the outstanding shares into a .csv file identical in format to the input .csv, that can be used for next years calculation.<br />
  
  
