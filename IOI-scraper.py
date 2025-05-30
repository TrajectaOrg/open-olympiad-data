import requests
from bs4 import BeautifulSoup
import pandas as pd

# List of country codes
country_codes = [
    "ALB", "DZA", "ARG", "ARM", "AUS", "AUT", "AZE", "BGD", "BLR", "BEL", "BOL", "BIH", "BRA", "BGR", "CAN", "CHL", 
    "CHN", "COL", "HRV", "CUB", "CYP", "CZE", "CSK", "DNK", "DOM", "ECU", "EGY", "SLV", "EST", "FIN", "FRA", "GAB", 
    "GEO", "DDR", "DEU", "GHA", "GRC", "HND", "HKG", "HUN", "ISL", "IND", "IDN", "IRN", "IRL", "ISR", "ITA", "JPN", 
    "JOR", "KAZ", "KEN", "KWT", "KGZ", "LVA", "LBY", "LTU", "LUX", "MAC", "MDG", "MYS", "MLT", "MUS", "MEX", "MDA", 
    "MNG", "MNE", "MAR", "MOZ", "NLD", "NZL", "NGA", "MKD", "NOR", "PAK", "PSE", "PER", "PHL", "POL", "PRT", "KOR", 
    "ROU", "RUS", "RWA", "SAU", "SRB", "SCG", "SGP", "SVK", "SVN", "ZAF", "SUN", "ESP", "LKA", "SWE", "CHE", "SYR", 
    "TWN", "TJK", "THA", "TTO", "TUN", "TUR", "TKM", "UKR", "ARE", "GBR", "USA", "UZB", "VEN", "VNM", "YUG", "ZWE"
]

# Extract table headers
headers = [
    "Year", "Contestant", "Country", 'Task1', 'Task2', 'Task3', 'Task4', 'Task5', 'Task6', 'Task7', 'Task8', 
    "Score Abs.", "Score Rel.", 
    "Rank Abs.", "Rank Rel.", 
    "Award"
]

for country_code in country_codes:
    # URL of the page to scrape
    url = f"https://stats.ioinformatics.org/results/{country_code}"

    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing the results
    table = soup.find('table')

    # Extract table rows
    rows = []
    current_year = None
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all('td')
        
        # Filter out cells with class "taskscore"
        filtered_cells = [cell for cell in cells if "taskscore" not in cell.get('class', [])]
        
        row_data = [cell.text.strip() for cell in filtered_cells]
        
        # Ensure row_data is not empty before accessing its elements
        if row_data and row_data[0].isdigit():
            current_year = row_data[0]
        elif row_data:
            # If the year is missing, use the last known year
            row_data.insert(0, current_year)
        
        # Adjust row length to match headers
        if len(row_data) < len(headers):
            row_data.extend([''] * (len(headers) - len(row_data)))  # Fill missing values with empty strings
        elif len(row_data) > len(headers):
            row_data = row_data[:len(headers)]  # Trim excess values
        rows.append(row_data)

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(rows, columns=headers)

    # Save the DataFrame to a CSV file
    df.to_csv(f'IOI/individual_results_{country_code}.csv', index=False)
