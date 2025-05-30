import requests
import xml.etree.ElementTree as ET
import pandas as pd

def fetch_imo_results(url):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses

    # Parse the XML content
    root = ET.fromstring(response.content)

    # Extract the data
    data = []
    for contestant in root.findall('contestant'):
        year = contestant.find('year').text
        name = contestant.find('name').text
        surname = contestant.find('surname').text
        problems = [contestant.find(f'problem{i}').text for i in range(1, 7)]
        total = contestant.find('total').text
        rank = contestant.find('rank').text
        award = contestant.find('award').text

        data.append([year, name, surname] + problems + [total, rank, award])

    # Define the headers
    headers = ['Year', 'Name', 'Surname', 'Problem1', 'Problem2', 'Problem3', 'Problem4', 'Problem5', 'Problem6', 'Total', 'Rank', 'Award']

    # Create a DataFrame for better data handling
    df = pd.DataFrame(data, columns=headers)

    return df

# List of country codes
country_codes = [
    "AFG", "ALB", "ALG", "AGO", "ARG", "ARM", "AUS", "AUT", "AZE", "BAH", "BGD", "BLR", "BEL", "BEN", "BTN", "BOL", 
    "BIH", "BWA", "BRA", "BRU", "BGR", "BFA", "KHM", "CMR", "CAN", "CHI", "CHN", "COL", "CIS", "CRI", "HRV", "CUB", 
    "CYP", "CZE", "CZS", "DEN", "DOM", "ECU", "EGY", "EST", "FIN", "FRA", "GMB", "GEO", "GDR", "GER", "GHA", "HEL", 
    "GTM", "HND", "HKG", "HUN", "ISL", "IND", "IDN", "IRQ", "IRN", "IRL", "ISR", "ITA", "CIV", "JAM", "JPN", "KAZ", 
    "KEN", "PRK", "KOR", "KSV", "KWT", "KGZ", "LAO", "LVA", "LIE", "LTU", "LUX", "MAC", "MDG", "MAS", "MRT", "MEX", 
    "MDA", "MNG", "MNE", "MAR", "MOZ", "MMR", "NAM", "NPL", "NLD", "NZL", "NIC", "NGA", "MKD", "NOR", "OMN", "PAK", 
    "PSE", "PAN", "PAR", "PER", "PHI", "POL", "POR", "PRI", "ROU", "RUS", "RWA", "SLV", "SAU", "SEN", "SRB", "SCG", 
    "SGP", "SVK", "SVN", "SAF", "ESP", "LKA", "SWE", "SUI", "SYR", "TWN", "TJK", "TZA", "THA", "TTO", "TUN", "TUR", 
    "NCY", "TKM", "UGA", "UKR", "UAE", "UNK", "USA", "URY", "USS", "UZB", "VEN", "VNM", "YEM", "YUG", "ZWE"
]

# Fetch and save results for each country
for code in country_codes:
    url = f"https://www.imo-official.org/country_individual_r.aspx?code={code}&column=award&order=desc&download=XML"
    try:
        imo_results = fetch_imo_results(url)
        
        # Save the results to a CSV file
        imo_results.to_csv(f'IMO/individual_results_{code}.csv', index=False)
        print(f"Results for {code} saved to 'imo_results_{code}.csv'")
    except Exception as e:
        print(f"Failed to fetch results for {code}: {e}")
