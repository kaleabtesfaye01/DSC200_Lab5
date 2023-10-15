"""
Name: Kaleab Alemu and Manogya Aryal
DSC 200
Lab 5: PDF Data Extraction

This program reads data from "Table.pdf" which contains data collected from countries regarding child abuse in those
respective countries and creates a CSV file containing the country name, category of child abuse and category total.

Due Date: Oct 14, 2023
"""

# We import the slate3k module to read the PDF file and the csv module to write the output to a csv file.
import slate3k as sl
import re  # We import the re module to use regular expressions.
import csv  # We import the csv module to write the output to a csv file.


# This function "get_categories" returns a list of categories of child abuse
def get_categories():
    return [
        'Childlabour(%)+2005–2012*_total',
        'Childlabour(%)+2005–2012*_male',
        'Childlabour(%)+2005–2012*_female',
        'Childmarriage(%)2005–2012*_marriedby15',
        'Childmarriage(%)2005–2012*_marriedby18',
        'Birthregistration(%)+2005–2012*_total',
        'Femalegenitalmutilation/cutting(%)+2002–2012*_prevalence_womena',
        'Femalegenitalmutilation/cutting(%)+2002–2012*_prevalence_girlsb',
        'Femalegenitalmutilation/cutting(%)+2002–2012*_attitudes_supportforthepracticec',
        'Justificationofwifebeating(%)2005–2012*_male',
        'Justificationofwifebeating(%)2005–2012*_female',
        'Violentdiscipline(%)+2005–2012*_total',
        'Violentdiscipline(%)+2005–2012*_male',
        'Violentdiscipline(%)+2005–2012*_female'
    ]


# This function "get_countries_and_values" takes in a list of rows as a parameter and returns a list of countries and a
# list of values
def get_countries_and_values(rows):
    countries = []  # initialize our countries list to an empty list
    values = []  # initialize our values list to an empty list
    for row in rows:  # iterate through the rows
        for row_idx in range(0, len(row), 15):  # iterate through the columns
            countries.append(row[row_idx])  # add the country name to our countries list
            values.append(row[row_idx + 1:row_idx + 15])  # add the values to our values list
    return [countries, values]  # return the list of countries and the list of values


# This function "row_cleanup" takes in a file as a parameter and returns a list of rows. This function cleans up the
# rows by removing unnecessary characters and removing the rows that contain the strings 'TABLE9CHILDPROTECTION' and
# 'SUMMARYINDICATORS'
def row_cleanup(file):
    rows = []  # initialize our rows list to an empty list
    for page in file:  # iterate through the pages
        lines = page.split('\n\n')  # split the page into lines
        row = []  # initialize our row list to an empty list
        for line in lines:  # iterate through the lines
            char_replace = [" ", "\n"]  # initialize our char_replace list to a list of characters to replace
            for char in char_replace:  # iterate through the characters to replace
                line = line.replace(char, "")  # replace the character with an empty string

            # if the line contains the below strings, we break out of the loop
            if 'TABLE9CHILDPROTECTION' in line or 'SUMMARYINDICATORS' in line:
                break
            row.append(line)  # add the line to our row list

        if row[6] == '9':  # if the row contains the number 9, we remove the number 9 from the row
            row.pop(6)
        rows.append(row[6:])  # add the row to our rows list
    return rows


# This function "write_csv" takes in a list of countries, a list of values and a list of categories as parameters and
# writes the output to a csv file
def write_csv(countries, values, categories):
    header = ['CountryName', 'CategoryName', 'CategoryTotal']  # initialize our header list to a list of headings
    with open('group_2_Lab5.csv', 'w') as csv_ptr:  # open the csv file
        csv_writer = csv.writer(csv_ptr)  # create a csv writer object
        csv_writer.writerow(header)  # write the header into the csv file
        for country_idx in range(len(countries)):  # iterate through the countries
            for category_idx in range(len(categories)):  # iterate through the categories
                total = values[country_idx][category_idx]  # get the total for the category
                # if the total is an en dash or 0, we continue to the next iteration
                if total == chr(8211) or total == '0':
                    continue
                total = re.findall(r'\d+', total)[0]  # extract the number from the total

                # write the country name, category name and category total into the csv file
                csv_writer.writerow([
                    countries[country_idx],
                    categories[category_idx],
                    total
                ])


def main():
    # open the pdf file
    with open('./data/Table9.pdf', 'rb') as pdfFile:
        reader = sl.PDF(pdfFile)  # create a PDF reader object
        countries, values = get_countries_and_values(row_cleanup(reader))  # get the countries and values
        categories = get_categories()  # get the categories
        write_csv(countries, values, categories)  # write the output to a csv file


main()
