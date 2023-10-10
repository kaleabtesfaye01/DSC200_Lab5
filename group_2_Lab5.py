import slate3k as sl
import re
import csv


def get_categories(row):
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


def row_cleanup1(file):
    lines = file[0].split('\n\n')
    row = []
    for line in lines:
        char_replace = [" ", "\n"]
        for char in char_replace:
            line = line.replace(char, "")
        row.append(line)
    return row[593:614]


def get_countries_and_values(rows):
    countries = []
    values = []
    for row in rows:
        for row_idx in range(0, len(row), 15):
            countries.append(row[row_idx])
            values.append(row[row_idx + 1:row_idx + 15])
    return [countries, values]


def row_cleanup2(file):
    rows = []
    for page in file:
        lines = page.split('\n\n')
        row = []
        for line in lines:
            char_replace = [" ", "\n"]
            for char in char_replace:
                line = line.replace(char, "")
            if 'TABLE9CHILDPROTECTION' in line or 'SUMMARYINDICATORS' in line:
                break
            row.append(line)
        if row[6] == '9':
            row.pop(6)
        rows.append(row[6:])
    return rows


def write_csv(countries, values, categories):
    header = ['CountryName', 'CategoryName', 'CategoryTotal']
    with open('group_2_Lab5.csv', 'w') as csv_ptr:
        csv_writer = csv.writer(csv_ptr)
        csv_writer.writerow(header)
        for country_idx in range(len(countries)):
            for category_idx in range(len(categories)):
                total = values[country_idx][category_idx]
                if total == chr(8211) or total == '0':
                    continue
                total = re.findall(r'\d+', total)[0]
                csv_writer.writerow([
                    countries[country_idx],
                    categories[category_idx],
                    total
                ])


def main():
    with open('./data/Table9.pdf', 'rb') as pdfFile:
        reader = sl.PDF(pdfFile)
        countries, values = get_countries_and_values(row_cleanup2(reader))
        categories = get_categories(row_cleanup1(reader))
        write_csv(countries, values, categories)


main()
