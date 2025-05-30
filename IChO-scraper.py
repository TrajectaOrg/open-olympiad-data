import requests
from bs4 import BeautifulSoup
import csv

# List of countries and their corresponding URL-encoded names
countries = [
    "Afghanistan", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bangladesh", "Belarus", "Belgium", "Brazil", "Bulgaria", "Canada",
    "China%2C%20People%27s%20Republic%20of", "Chinese%20Taipei", "Commonwealth%20of%20Independent%20States",
    "Costa%20Rica", "Croatia", "Cuba", "Cyprus", "Czech%20Republic", "Czechoslovakia",
    "Denmark", "Ecuador", "Egypt", "El%20Salvador", "Estonia", "Finland",
    "France", "Georgia", "German%20Democratic%20Republic", "Germany", "Germany%2C%20Federal%20Republic%20of",
    "Greece", "Hungary", "Iceland", "India", "Individual%201", "Individual%202",
    "Indonesia", "Iran%2C%20Islamic%20Republic%20of", "Ireland", "Israel", "Italy", "Japan",
    "Kazakhstan", "Korea%2C%20Republic%20of", "Kuwait", "Kyrgyzstan", "Latvia", "Liechtenstein",
    "Lithuania", "Luxembourg", "Macedonia%2C%20North", "Malaysia", "Mexico", "Moldova",
    "Mongolia", "Montenegro", "Nepal", "Netherlands", "New%20Zealand", "Nigeria",
    "Norway", "Oman", "Pakistan", "Paraguay", "Peru", "Philippines",
    "Poland", "Portugal", "Qatar", "Romania", "Russian%20Federation", "Saudi%20Arabia",
    "Serbia", "Singapore", "Slovakia", "Slovenia", "South%20Africa", "Soviet%20Union",
    "Spain", "Sri%20Lanka", "Sweden", "Switzerland", "Syria", "Tajikistan",
    "Thailand", "Trinidad%20and%20Tobago", "T%C3%BCrkiye", "Turkmenistan", "Ukraine", "United%20Arab%20Emirates",
    "United%20Kingdom", "Uruguay", "USA", "Uzbekistan", "Venezuela", "Vietnam", "Yugoslavia"
]

# Base URL of the IChO results page
base_url = "http://www.icho-official.org/results/country_info.php?country="

# Dictionary mapping country names to their codes
country_name_to_code = {
    "Afghanistan": "AFG", "Argentina": "ARG", "Armenia": "ARM", "Australia": "AUS", "Austria": "AUT", "Azerbaijan": "AZE",
    "Bangladesh": "BGD", "Belarus": "BLR", "Belgium": "BEL", "Brazil": "BRA", "Bulgaria": "BGR", "Canada": "CAN",
    "China%2C%20People%27s%20Republic%20of": "CHN", "Chinese%20Taipei": "TWN", "Commonwealth%20of%20Independent%20States": "CIS",
    "Costa%20Rica": "CRI", "Croatia": "HRV", "Cuba": "CUB", "Cyprus": "CYP", "Czech%20Republic": "CZE", "Czechoslovakia": "CZS",
    "Denmark": "DEN", "Ecuador": "ECU", "Egypt": "EGY", "El%20Salvador": "SLV", "Estonia": "EST", "Finland": "FIN",
    "France": "FRA", "Georgia": "GEO", "German%20Democratic%20Republic": "GDR", "Germany": "GER", "Germany%2C%20Federal%20Republic%20of": "GFR",
    "Greece": "GRE", "Hungary": "HUN", "Iceland": "ISL", "India": "IND", "Individual%201": "Individual%201", "Individual%202": "Individual%202",
    "Indonesia": "IDN", "Iran%2C%20Islamic%20Republic%20of": "IRN", "Ireland": "IRL", "Israel": "ISR", "Italy": "ITA", "Japan": "JPN",
    "Kazakhstan": "KAZ", "Korea%2C%20Republic%20of": "KOR", "Kuwait": "KWT", "Kyrgyzstan": "KGZ", "Latvia": "LVA", "Liechtenstein": "LIE",
    "Lithuania": "LTU", "Luxembourg": "LUX", "Macedonia%2C%20North": "MKD", "Malaysia": "MAS", "Mexico": "MEX", "Moldova": "MDA",
    "Mongolia": "MNG", "Montenegro": "MNE", "Nepal": "NPL", "Netherlands": "NLD", "New%20Zealand": "NZL", "Nigeria": "NGA",
    "Norway": "NOR", "Oman": "OMN", "Pakistan": "PAK", "Paraguay": "PAR", "Peru": "PER", "Philippines": "PHI",
    "Poland": "POL", "Portugal": "POR", "Qatar": "QAT", "Romania": "ROU", "Russian%20Federation": "RUS", "Saudi%20Arabia": "SAU",
    "Serbia": "SRB", "Singapore": "SGP", "Slovakia": "SVK", "Slovenia": "SVN", "South%20Africa": "SAF", "Soviet%20Union": "USS",
    "Spain": "ESP", "Sri%20Lanka": "LKA", "Sweden": "SWE", "Switzerland": "SUI", "Syria": "SYR", "Tajikistan": "TJK",
    "Thailand": "THA", "Trinidad%20and%20Tobago": "TTO", "T%C3%BCrkiye": "TUR", "Turkmenistan": "TKM", "Ukraine": "UKR", "United%20Arab%20Emirates": "UAE",
    "United%20Kingdom": "UNK", "Uruguay": "URY", "USA": "USA", "Uzbekistan": "UZB", "Venezuela": "VEN", "Vietnam": "VNM", "Yugoslavia": "YUG"
}

for country in countries:
    # Construct the full URL for each country
    url = base_url + country

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the individual results
    table = soup.find('table', {'class': 'table table-sm table-hover table-responsive caption-top w-auto mx-auto'})

    # Check if the table was found
    if table is None:
        print(f"Error: Could not find the table for {country}.")
        continue

    # Extract the table headers
    headers = [header.text.strip() for header in table.find('thead').find_all('th')]

    # Extract the table rows
    rows = table.find('tbody').find_all('tr')
    
    # Prepare data for CSV
    data = []
    for row in rows:
        columns = row.find_all('td')
        data.append([column.text.strip() for column in columns])

    # Use the country code for the CSV filename
    country_code = country_name_to_code.get(country, "UNK")
    csv_filename = f'IChO/individual_results_{country_code}.csv'

    # Write data to a CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)  # Write headers
        csvwriter.writerows(data)    # Write data rows

    print(f"Data for {country} has been written to {csv_filename}")
