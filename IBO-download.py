import requests

# List of URLs to download
urls = [
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2024%20results.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2023.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2022.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO%202021%20-%20IBO%20Challenge%20II%20-%20results.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO%202020%20-%20IBO%20Challenge%20-%20Results.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2019-IBO-Ranking_web.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2018-IBO-Ranking_web.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2017Full.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2016.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2015-official-ranking.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2014_FINAL_scores.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2013_final_ranking.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2012_Detailed_Results.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2011_Ranking_total_final.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2010_Final_Results.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2009.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2008.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2007.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2006.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2005.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2004.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2003.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2002.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2001.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2000.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1999.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1998.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1997.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1996.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1995.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1994.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1993.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1992.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1991.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1990.pdf"
]

# Dictionary to map URLs to file names
url_to_filename = {
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2024%20results.pdf": "2024.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2023.pdf": "2023.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2022.pdf": "2022.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO%202021%20-%20IBO%20Challenge%20II%20-%20results.pdf": "2021.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO%202020%20-%20IBO%20Challenge%20-%20Results.pdf": "2020.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2019-IBO-Ranking_web.pdf": "2019.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2018-IBO-Ranking_web.pdf": "2018.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2017Full.pdf": "2017.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2016.pdf": "2016.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2015-official-ranking.pdf": "2015.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2014_FINAL_scores.pdf": "2014.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2013_final_ranking.pdf": "2013.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2012_Detailed_Results.pdf": "2012.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2011_Ranking_total_final.pdf": "2011.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2010_Final_Results.pdf": "2010.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2009.pdf": "2009.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2008.pdf": "2008.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2007.pdf": "2007.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2006.pdf": "2006.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2005.pdf": "2005.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2004.pdf": "2004.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2003.pdf": "2003.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2002.pdf": "2002.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2001.pdf": "2001.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO2000.pdf": "2000.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1999.pdf": "1999.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1998.pdf": "1998.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1997.pdf": "1997.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1996.pdf": "1996.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1995.pdf": "1995.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1994.pdf": "1994.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1993.pdf": "1993.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1992.pdf": "1992.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1991.pdf": "1991.pdf",
    "https://www.ibo-info.org/files/downloads/results-reports/results/IBO1990.pdf": "1990.pdf"
}

# Function to download a file from a URL
def download_file(url):
    local_filename = 'IBO/' + url_to_filename[url]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Downloaded: {local_filename}")

# Download each file
for url in urls:
    download_file(url)
