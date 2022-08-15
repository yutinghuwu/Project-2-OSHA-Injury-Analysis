# Project-OSHA-Injury-Analysis
![cover](cover.JPG)

## 1. Project Objective
Within this project we will analyze data of work-related injuries and illnesses from different employers in United States.

The objective is to explore the officially reported data from OSHA to have insights that can serve to spread awareness and contribute to improve workplace health & safety, and eventually save people lives.

Companies may also take these insights into consideration to:

✓ see relative level of injuries and illnesses among different industries

✓ understand why employees are suffering from injuries (which sometimes cause fatalities)

✓ determine problem areas and progress in preventing work-related injuries and illnesses


## 2. Data source
Data is extracted from OSHA (Occupational Safety and Health Administration), which is the federal agency of the United States, part of the United States Department of Labor, that regulates workplace safety and health:

https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data

## 3. Incident Rate
As per US Bureau of Labor Statistics, an incidence rate of injuries and illnesses is computed from the following formula:

𝑇𝐶𝑅 = (𝑁𝑢𝑚𝑏𝑒𝑟 𝑜𝑓 𝑖𝑛𝑗𝑢𝑟𝑖𝑒𝑠 𝑎𝑛𝑑 𝑖𝑙𝑙𝑛𝑒𝑠𝑠 𝑥 200,000)/𝐸𝑚𝑝𝑙𝑜𝑦𝑒𝑒 ℎ𝑜𝑢𝑟𝑠 𝑤𝑜𝑟𝑘𝑒𝑑

𝐷𝐴𝑅𝑇 = (Number of injuries and illnesses with days away from work, job transfer, or restriction 𝑥 200,000)/𝐸𝑚𝑝𝑙𝑜𝑦𝑒𝑒 ℎ𝑜𝑢𝑟𝑠 𝑤𝑜𝑟𝑘𝑒𝑑


Notes:

‐ The 200,000 hours in the formula represents the equivalent of 100 employees working 40 hours per week, 50 weeks
per year, and provides the standard base for the incidence rates).

‐ Hours worked should not include any nonwork time, even though paid, such as vacation, sick leave, holidays, etc.


## 4. Raw Data Exploration


## 5. Data Processing
In any data science project, data wrangling is a very important step, since it removes the risk by ensuring data is
in a reliable state before it is analyzed and leveraged, making it to be a critical part of the analytical process. 

Thus, despite dataset quality is good, it is highly advised to process and format the data.
✓ Clean the data: by keeping only the columns that are meaningful for the analysis; and use statistics to detect and remove outliers with reference to its interquartile range.
✓ Format the data, such as data conversion, remove negative numeric values, filling empty values, removing special characters, standardize company name, etc.

## 6. Exploratory Data Analysis
After processing the raw data, we will use the clean dataset output to perform EDA (Exploratory Data Analysis), to plot
our variables in order to extract meaningful insights and conclusions about our data, by means of visual explorations.
EDA is based on graphical and descriptive techniques whose objective is to:

✓ gain intuition about the data

✓ detect outliers

✓ extract important variables

✓ discover underlying structures in the data

✓ It also allows organizing the data, detecting failures and evaluating the existence of missing data


## 7. Technology Stack
❖ Python (Jupyter)

❖ Web Scrapping / Requests / BeautifulSoup

❖ Numpy, Pandas, Pickle

❖ Data wrangling. Main functions:

    ▪ import_data(), combine_csv()
    
    ▪ df_clean_format(** kwargs parameters)
    
❖ EDA and descriptive statistics techniques

❖ Matplotlib, Seaborn

❖ PowerBi

❖ …

## 8. Processed Data Results


## 9. Conclusions

1. 2020 has the highest number of recorded injury/illness and TCR.
2. TCR is very similar for all recorded years.
3. USPS is the company that registered highest number of total injuries, followed by Walmart.
4. 92.2% of the companies are SME (Small Medium Enterprises) with 20-249 employees.
5. 53.5% of injuries/illnesses occur only in the states of California and Texas.
6. There is correlation between injury cases and hours worked, dafw cases (days away from work) and djtr cases (job transfers or restrictions).

… but the most important one:

**Data Cleaning and Data Pre-processing part is essential.**

Figh with your data, will make it to confess their secrets.

Correct insights can only be extracted if you have good data.
