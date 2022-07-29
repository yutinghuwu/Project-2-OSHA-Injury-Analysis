# Functions for "U.S. Workplace Injury Analysis" project

# General libraries
import pandas as pd
import numpy as np
import requests
from glob import glob

# Webscrapping
from bs4 import BeautifulSoup
import zipfile
import wget


def import_data():
    """
    This function will download all files from URL and save them in data folder and 
    unzip files in same folder
    """
    
    """
    downloading data
    """
    url = "https://www.osha.gov/Establishment-Specific-Injury-and-Illness-Data"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    links = []

    for link in soup.select('a[href*=".zip"]'):
        links.append(link["href"])

    zip_links = [f"https://www.osha.gov/{l}" for l in links]

    for f in zip_links:
        wget.download(f, "data/")
        
    """
    unzip files downloaded in *zip format to extract *csv
    """
    zipfiles = glob("data/*.zip")
    for zf in zipfiles:
        with zipfile.ZipFile(zf,"r") as zip_ref:
            zip_ref.extractall("data/")            

            
            
def combine_csv():
    """
    read all CSVs and combine all files merging in a single dataframe and keeping record of source
    filename in column named 'source'
    """
    csv_files = glob("data/*.csv")
    dfs = []
    for c in csv_files:
        print(c)
        try:
            df = pd.read_csv(c, low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(c, encoding="cp1252", low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(c, encoding="utf8", low_memory=False)
        df["source"] = c
        dfs.append(df)
    dfs = pd.concat(dfs).reset_index(drop=True)
    return dfs



def import_naics():
    """
    import files "NAICS Index File" from U.S. Census Bureau, convert to pandas df, 
    concatenate df on a common renamed column and drop duplicates to keep unique values
    """     
    url='https://www.census.gov/naics/'
    
    naics_2007 = pd.read_excel(url+'2007NAICS/2007_NAICS_Index_File.xls')
    naics_2012 = pd.read_excel(url+'2012NAICS/2012_NAICS_Index_File.xls')
    naics_2017 = pd.read_excel(url+'2017NAICS/2017_NAICS_Index_File.xlsx')
    naics_2022 = pd.read_excel(url+'2022NAICS/2022_NAICS_Index_File.xlsx')
    
    naics_df_list = [naics_2007, naics_2012, naics_2017, naics_2022]
    
    for df in naics_df_list:
        df.rename(columns = {df.columns[0]:'naics_code', df.columns[1]:'naics_industry_description',}, inplace = True)
    
    naics_df = pd.concat(naics_df_list, axis=0, join="outer", ignore_index=True)
    
    naics_df.drop_duplicates(subset=['naics_code'], inplace=True)
    return naics_df



def df_clean_format(df, columns_drop, outlier_column_list, float_columns, injury_number, size_column, year_column, company_column, establishment_column, industry_raw, industry_clean):
    """
    Drop columns listed in columns_list from dataframe
    """
    for col in columns_drop:
        df.drop(columns=col, axis=1, inplace=True)    
        
    """
    Drop outlier values for each df column with reference to interquartile range IQR
    """
    for outlier_column in outlier_column_list:
        IQR = df[outlier_column].quantile(q=0.75)-df[outlier_column].quantile(q=0.25)
        column_OL1 = df[outlier_column].quantile(q=0.25) - 1.5*IQR
        column_OL2 = df[outlier_column].quantile(q=0.75) + 1.5*IQR

        df2 = df.drop(df[
                (df[outlier_column] < column_OL1) | 
                (df[outlier_column] > column_OL2)
            ].index, inplace=True)    

    """
    Removing negative numeric values and setting to zero
    """
    df._get_numeric_data()[df._get_numeric_data() < 0] = 0

    """
    convert data type from listed columnd from float to integer
    """
    for i in float_columns:
        df[i] = df[i].map(int)
        
    """
    formatting no_injuries_illnesses to categorical meaning
    1 if the establishment had injuries or illnesses
    2 if the establishment did not have injuries or illnesses
    """    
    df.rename(columns={injury_number:'injury_illness'}, inplace=True)
    df['injury_illness'].replace(1.0, 'yes', inplace=True)
    df['injury_illness'].replace(2.0, 'no', inplace=True)      

    """
    formatting size to its categorical meaning
    1 if the establishment has < 20 employees
    2 if the establishment has 20-249 employees
    3 if the establishment has 250+ employees
    """         
    df[size_column].replace(1.0, '1-20', inplace=True)
    df[size_column].replace(2.0, '20-249', inplace=True)     
    df[size_column].replace(3.0, '250+', inplace=True)      
    
    """
    convert data type from a given column to datetime and keep only year
    """    
    df[year_column] = (pd.to_datetime(df[year_column], format="%Y")).dt.year

    """
    Filling company_name empty values (space, nan) with establishment_name
    """     
    df[company_column].replace(' ', np.nan, inplace=True)
    df[company_column].fillna(df[establishment_column], inplace=True)

    """
    Filling naics_industry_description empty values (space, nan) with
    industry_description and dropping this column afterwards
    """
    df[industry_clean].fillna(df[industry_raw], inplace=True)
    df.drop(columns=industry_raw, axis=1, inplace=True)

    """
    Revoving all special characters in company name
    """
    df[company_column] = df[company_column].str.replace(".", "", regex=True)
    df[company_column] = df[company_column].str.replace(",", "", regex=True)
    df[company_column] = df[company_column].str.replace("'", "", regex=True)
    df[company_column] = df[company_column].str.replace("&", "", regex=True)
    df[company_column] = df[company_column].str.replace("/", "", regex=True)
    df[company_column] = df[company_column].str.replace("+", "", regex=True)
    df[company_column] = df[company_column].str.replace("!", "", regex=True)
    df[company_column] = df[company_column].str.replace("`", "", regex=True)
    df[company_column] = df[company_column].str.replace("-", " ", regex=True)     
    
    """
    Format company name to standardized name
    """
    df[company_column] = df[company_column].str.title()
    df[company_column] = df[company_column].str.replace("Inc", "", regex=True)
    df[company_column] = df[company_column].str.replace("Llc", "", regex=True)
    df[company_column] = df[company_column].str.replace("Corp", "", regex=True)
    df[company_column] = df[company_column].str.replace("Ltd", "", regex=True)
    df[company_column] = df[company_column].str.replace("Lp", "", regex=True)
    df[company_column] = df[company_column].str.replace(" +", " ", regex=True)
    df[company_column] = df[company_column].str.strip()
    df[company_column].replace("Bed Bath And Beyond", "Bed Bath Beyond", inplace=True)
    df[company_column].replace("Lowes Home Improvement", "Lowes", inplace=True)
    df[company_column].replace("Us Postal Service", "Usps", inplace=True)
    df[company_column].replace("Wal Mart Stores East", "Walmart", inplace=True)
    df[company_column].replace("Wal Mart Stores", "Walmart", inplace=True)
    df[company_column] = df[company_column].apply(lambda x: "Fedex" if "Fedex" in x else x)
    df[company_column] = df[company_column].apply(lambda x: "Aldi" if "Aldi" in x else x)
    df[company_column] = df[company_column].apply(lambda x: "Lidl" if "Lidl" in x else x)
    df[company_column] = df[company_column].apply(lambda x: "Amazon" if "Amazon" in x else x)
    
def drop_outlier_rate(df, TCR_column):
    max_TCR = df.total_injuries.max()*200000 / df.total_hours_worked.max()    

    df2 = df.drop(df[
        (df[TCR_column] > max_TCR)
    ].index, inplace=True) 