# Generic Real Estate Consulting Project

Group: Group 36

Author: Junqi Shan (1392759)

Goal: Our goal is to conduct a thorough study of rental prices in the VIC area, in order to provide developers or investors with well-informed recommendations for property development.

Assumption: We operate under the assumption that rent serves as a representative measure of a property’s value and reflects people's preferences.

Running the project: 

1. The script is located at ../data/scripts/scraping.py. You must run this script first to gather raw data for the project.

2. Ensure the scraping script is executed before running any notebooks to ensure data is available for further analysis.

3. The script will automatically save the scraped data into CSV files in the /data directory.
Scrapin

4. Once the data is scraped using ../data/scripts/scraping.py, all notebooks should run smoothly if executed in sequence. However, please pay attention to the following details to ensure proper data processing:

- School-related Preprocessing:
Before running the complete dataset notebook, make sure to first run the school-related preprocessing notebook. This is necessary to handle properties with multiple nearby schools, and to ensure that each property has a unique ID by consolidating the multiple school instances into a single record per property.

Datasets:

Internal VIC rental datasets is from Domain.au.

All external datasets is sourced from the Victoria (VIC) government, containing associated features such as education, transport, and life indexes for analysis.