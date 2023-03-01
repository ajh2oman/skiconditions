#!/usr/bin/env python
# coding: utf-8

# In[68]:


import requests
import urllib.request
import re
import sys
import pandas as pd
import numpy as np
import json
from bs4 import BeautifulSoup as bs
import cloudscraper
import datetime
import schedule
import time
import datetime
import os
import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options

# In[3]:

t1 = time.time() 
for trial_scraper in range(10):
    try:
        scraper = cloudscraper.create_scraper(allow_brotli=False , browser = "firefox" )
        break
        
    except:
        None

# In[4]:

options = Options()
options.add_argument('--headless')

print("the driver is on set")
for trial_driver in range(10):
    try:
        driver = webdriver.Chrome(options=options)
        break
    except:
        None
# ft





 
# def get_1_website():
#     """MOHAWK MOUNTAIN:  https://www.mohawkmtn.com/snow-report/"""
    
    
#     url = "https://www.mohawkmtn.com/snow-report/"
#     r = requests.get(url)
#     soup = bs(r.text , "lxml")
    
#     trails = soup.select("div.cell.open-night-skiing-trails")[0].text
#     lifts = soup.select("div.cell.open-night-skiing-lifts")[0].text
    
#     if trails == "":
#         trails = "0"
        
#     if lifts == "":
#         lifts = "0"
        
#     data_dict = {"MOHAWK MOUNTAIN": {"trails" : trails ,
#                 "lifts" : lifts}}
    
#     return data_dict

# newer version
# ft
def get_1_website():
    """MOHAWK MOUNTAIN:  https://www.mohawkmtn.com/snow-report/"""
    
    global driver
    
    url = "https://www.mohawkmtn.com/snow-report/"
    driver.get(url )
    time.sleep(5)
    r = driver.page_source
    soup = bs(r , "lxml")
    
    trails = soup.select("div.cell.open-night-skiing-trails")[0].text
    lifts = soup.select("div.cell.open-night-skiing-lifts")[0].text
    
    if trails == "":
        trails = 0
        
    if lifts == "":
        lifts = 0
        
    data_dict = {"MOHAWK MOUNTAIN": {"trails" : int(trails) ,
                "lifts" : int(lifts)}}
    
    return data_dict

# In[5]:


# ft
def get_2_website():
    """MOUNT SOUTHINGTON:  https://mountsouthington.com/trails-and-conditions/"""
    
    
    url = "https://mountsouthington.com/trails-and-conditions/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    table = soup.select("div.overall-conditions")[0]
    all_data = [t.text for t in table.select("tr")]
    
    trails = int([d for d in all_data if "Trails Open:" in d][0].split("Trails Open:\n")[1].split("\n")[0].split("/")[0])
    lifts = int([d for d in all_data if "Lifts Open:" in d][0].split("Lifts Open:\n")[1].split("\n")[0].split("/")[0])
    try:
        depth = re.findall( "\d+" , [d for d in all_data if "Depth:" in d][0].split("Depth:\n")[1].split("\n")[0])[0]
    except:
        depth = 0
    
    data_dict = {"MOUNT SOUTHINGTON" : {"trails" : trails,
                "lifts" : lifts,
                "depth" : int(depth)}}
    
    return data_dict
# In[6]:


# ft
def get_3_website():
    """POWDER RIDGE:  https://powderridgepark.com/about-us/trail-report/"""
    
    

    url = "https://powderridgepark.com/about-us/trail-report/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    
    all_trails = [t.text for t in soup.select("td.column-4 > font")]
    trails_num = 0
    
    for trail in all_trails:
        if trail == "OPEN":
            trails_num +=  1
            
            
            
    lifts_table = soup.select("div.avia_textblock")[-1]
    all_lifts = [t.text for t in lifts_table.select("td.column-2 > font")]
    
    lifts_num = 0
    
    for lift in all_lifts:
        if lift == "OPEN":
            lifts_num += 1

    try:    
        depth = re.findall("\d+" , soup.select("div.avia_textblock")[2].select("td.column-2")[1].text)[0]
    except:
        depth = 0
            
    data_dict = {"POWDER RIDGE" : {"trails" : trails_num,
                                  "lifts" : lifts_num,
                                  "depth" : int(depth)}}
    return data_dict
# In[7]:


# ft
def get_4_website():
    
    """SKI SUNDOWN:  https://skisundown.com/the-mountain/mountain-information/conditions-report/"""
    
    url = "https://skisundown.com/the-mountain/mountain-information/conditions-report/"
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',}
    
    r = requests.get(url , headers = headers)
    soup = bs(r.text , "lxml")
    
    data_table = soup.select("div.row.conditions")[0]
    data_rows = [ d for p in data_table for d in p.text.split("\n") if d.strip() != ""]
    lifts = [l for l in data_rows if "Num. of Lifts Open:" in l][0].split("Num. of Lifts Open:")[1]
    trails = [t for t in data_rows if "Num. of Trails Open:" in t][0].split("Num. of Trails Open:")[1]
    try:
        depth = re.findall("\d+" , [t for t in data_rows if "Base Snow:" in t][0].split("Base Snow:")[1])[0]
    except:
        depth = 0

    try:
        new_snow = re.findall("\d+" , [t for t in data_rows if "New Snow 24hrs:" in t][0].split("New Snow 24hrs:")[1])[0]
    except:
        new_snow = 0
    
    data_dict = {"SKI SUNDOWN" : {"trails" : int(trails) ,
                 "lifts" : int(lifts) ,
                 "depth" : int(depth),
                 "new snow" : new_snow}}
    
    return data_dict 




# In[ ]:





# In[8]:


# ft
def get_5_website():
    
    """BIGROCK:  https://www.bigrockmaine.com/trails/"""
    
    url = "https://www.bigrockmaine.com/trails/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    tables = pd.read_html(r.text) 
    
    try:
        depth = int(re.findall( "\d+" , tables[0].set_index(0).loc["Base Depth:" , 1])[0])
    except:
        depth = 0

    
    try:
        new_snow = float(re.findall("\d+" , tables[0].set_index(0).loc["Snowfall (24hr):" , 1])[0])
    except:
        new_snow = 0
        None
    
    trails_list = tables[1].loc[: , 3][1:].tolist()
    trails = np.sum([1 if t == "OPEN" else 0 for t in trails_list])
    
    
    lifts_list = tables[2].loc[: , 2][1:].tolist()
    lifts = np.sum([1 if t == "OPEN" else 0 for t in lifts_list])
    
    data_dict = {"BIGROCK" : {"trails" : trails,
                 "lifts" : lifts ,
                 "depth" : depth ,
                 "new snow" : new_snow} }
    
    return data_dict

# In[9]:


# ft
def flatten_lists(list_of_lists):
    final_list = []
    for sub_list in list_of_lists:
        final_list.extend(sub_list)
        
    return final_list


# In[10]:


# ft
def get_6_website():
    """BLACK MOUNTAIN MAINE:  https://www.blackmt.com/conditions"""
    
    url = "https://www.blackmt.com/conditions"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    all_divs = soup.select("div[data-testid='richTextElement']")
    main_titles = [(index , div ) for index , div in zip( range(len(all_divs)) , all_divs )  if len(div.select("h4.font_4")) > 0]
    
    lifts_div_index = [ d[0] for d in main_titles  if "Lifts" in d[1].text][0]
    trails_div_index = [ d[0] for d in main_titles  if "Beginner" in d[1].text][0]
    
    all_lifts_section = all_divs[lifts_div_index : trails_div_index]
    all_trails_section = all_divs[ trails_div_index : ]
    
    all_lifts = [l.text for l in flatten_lists([l.select("h2.font_2 > span") for l in all_lifts_section])  if l.text.strip(" \u200b\n\t") != ""]
    all_trails = [l.text for l in flatten_lists([l.select("h2.font_2 > span > span > span") for l in all_trails_section]) if l.text.strip(" \u200b\n\t") != ""]
    
    lifts_num = len(all_lifts) - len([t for t in all_lifts if t.lower() == "closed"]) 
    trails_num =  (len(all_trails)) - len([t for t in all_trails if t.lower() == "closed"]) 
    
    data_dict = {"BLACK MOUNTAIN MAINE" : {"trails" : int(trails_num),
                     "lifts" : int(lifts_num) } }
    return data_dict







# In[11]:


# ft
# def get_7_website():
#     """CAMDEN SNOW BOWL:  https://camdensnowbowl.com/current-conditions/"""
    
#     global scraper
    
#     r = scraper.get("https://camdensnowbowl.com/current-conditions/")
#     soup = bs(r.text , "lxml")
#     tables = pd.read_html(r.text)
#     info = tables[-1]
#     info.columns = info.iloc[0 , :]
#     info = info.iloc[1: , :]
#     info_dict = info.to_dict(orient = "records")[0]
#     data_dict = {"CAMDEN SNOW BOWL" : {"lifts" : int(info_dict["LIFTS"])  , 
#                                       "trails" : int(info_dict["TRAILS"]) , 
#                                       "new snow" : int(info_dict["NEW SNOW"].strip('"'))}}
    
#     return data_dict

# the newer version
# ft
def get_7_website():
    """CAMDEN SNOW BOWL:  https://camdensnowbowl.com/current-conditions/"""
    
    global scraper
    
    headers = {
        'authority': 'camdensnowbowl.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'dnt': '1',
#         'if-modified-since': 'Tue, 24 Jan 2023 16:37:12 GMT',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    
    r = requests.get('https://camdensnowbowl.com/current-conditions/', headers=headers)
    soup = bs(r.text , "lxml")
    tables = pd.read_html(r.text)

    info = tables[1]
    
    info.columns = info.iloc[0 , :]
    info = info.iloc[1: , :]
    info = info.replace("-" , "0")
    info_dict = info.to_dict(orient = "records")[0]
    data_dict = {"CAMDEN SNOW BOWL" : {"lifts" : int(info_dict["LIFTS"].split("/")[0])  , 
                                      "trails" : int(info_dict["TRAILS"].split("/")[0]) , 
                                      "new snow" : int(info_dict["NEW SNOW"].strip('"'))}}
    
    return data_dict


# In[12]:


# ft
# def get_8_website():
#     """LOST VALLEY:  https://www.lostvalleyski.com/conditions/"""
    
#     url = "https://www.lostvalleyski.com/conditions/"
#     r = scraper.get(url)
#     soup = bs(r.text , "lxml")
#     trails_section = soup.select("body > div.wrap > div > main > section.snocountry.flex-section.relative.pb-0 > div > div > div > div:nth-child(2) > div > div:nth-child(3)")[0]
#     num_trails = len([ t for t in trails_section.text.split("\n") if (t.strip() != "") and (t != 'OPEN TRAILS')])
    
#     data_dict = {"LOST VALLEY" : {"trails" : num_trails}}
#     return data_dict

# the newer version
# ft
def get_8_website():
    """LOST VALLEY:  https://www.lostvalleyski.com/conditions/"""
    
    url = "https://www.lostvalleyski.com/conditions/"
    r = scraper.get(url)
    soup = bs(r.text , "lxml")
    trails_section = soup.select("body > div.wrap > div > main > section.snocountry.flex-section.relative.pb-0 > div > div > div > div:nth-child(2) > div > div:nth-child(3) > p.w-full.text-left.snocountry-data.leading-snug.text-dusk-blue")[0]
#     num_trails = len([ t for t in trails_section.text.split("\n") if (t.strip() != "") and (t != 'OPEN TRAILS')])
    num_trails = int(trails_section.text)
    
    data_dict = {"LOST VALLEY" : {"trails" : num_trails}}
    return data_dict
# In[13]:


# ft
# def get_9_website():
    
#     """MOUNT ABRAM:  https://mtabram.com/?page_id=1419"""
    
    
#     url = "https://mtabram.com/?page_id=1419"
#     r = requests.get(url)
#     soup = bs(r.text , "lxml")
    
#     table = pd.read_html(r.text)[0]
#     table.columns = ["titles" , "kind" , "status" , "snow_status"]
    
#     lifts_index = table.index[table["kind"] == "LIFTS"].tolist()[0]
#     trails_index = table.index[table["kind"] == "TRAILS"].tolist()[0]
    
#     lifts_section = table.iloc[lifts_index + 1 : trails_index , :]["status"].tolist()
#     num_lifts = np.sum([1 if s == "OPEN" else 0 for s in lifts_section])
    
#     trails_section = table.iloc[trails_index + 1 : , :]["status"].tolist()
#     num_trails = np.sum([1 if s == "OPEN" else 0 for s in trails_section])
    
#     data_dict = {"MOUNT ABRAM" : {"trails" : num_trails,
#                                  "lifts" : num_lifts}}
#     return data_dict


# the newer version
# ft
def get_9_website():
    
    """MOUNT ABRAM:  https://mtabram.com/?page_id=1419"""
    
    
    url = "https://mtabram.com/?page_id=1419"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    
    i_frame = soup.select("#main-content > div:nth-child(3) > div.wpb_row.row > div > div > div.wpb_text_column.wpb_content_element > div > div > iframe")[0].get("src")
    r2 = requests.get(i_frame)
    
    table_trails = pd.read_html(r2.text)[1].iloc[1: -2 , :2].dropna()
    table_trails["kind"] = "TRAILS"
    
    table_lifts = pd.read_html(r2.text)[0].iloc[1: , :2].dropna()
    table_lifts["kind"] = "LIFTS"
    
    table = pd.concat([table_trails , table_trails]).dropna().drop_duplicates().fillna("Closed")
    
    table.columns = ["titles"  , "status" , "kind"]
    
    lifts_section = table[table["kind"] == "LIFTS"]["status"].values.tolist()
    trails_section = table[table["kind"] == "TRAILS"]["status"].values.tolist()
    
    
    num_lifts = np.sum([1 if s != "Closed" else 0 for s in lifts_section])
    
    num_trails = np.sum([1 if s != "Closed" else 0 for s in trails_section])-3
    
    data_dict = {"MOUNT ABRAM" : {"trails" : num_trails,
                                 "lifts" : num_lifts}}
    return data_dict

# In[14]:


# ft
def get_10_website():
    """SADDLEBACK:  https://www.saddlebackmaine.com/the-mountain/snow--weather/"""
    
    url = "https://www.saddlebackmaine.com/the-mountain/snow--weather/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    lifts = [ d for d in soup.select("div.count-box") if "Lifts Open" in d.text][0].text
    num_lifts = int(lifts.replace("Lifts Open" , "").strip("\n").split("/")[0])
    
    trails = [ d for d in soup.select("div.count-box") if "Trails Open" in d.text][0].text
    num_trails = int(trails.replace("Trails Open" , "").strip("\n").split("/")[0])
    
    temp = [ d for d in soup.select("div.temp") if "24 HR SNOW" in d.text][0].text
    num_temp = int(temp.replace("24 HR SNOW" , "").strip('"\n').split("/")[0])
    
    min_depth = [ d for d in soup.select("div.count-box") if "Base Depth Min" in d.text][0].text
    num_min_depth = int(min_depth.replace("Base Depth Min" , "").strip('"\n').split("/")[0])
    
    
    max_depth = [ d for d in soup.select("div.count-box") if "Base Depth Max" in d.text][0].text
    num_max_depth = int(max_depth.replace("Base Depth Max" , "").strip('"\n').split("/")[0])
    
    data_dict = {"SADDLEBACK" : {"lifts" : num_lifts,
                                "trails" : num_trails,
                                "new snow" : num_temp,
                                "depth" : num_min_depth}}
    return data_dict


# In[15]:


# ft
def get_11_website():
    
    """PLEASANT MOUNTAIN:  https://www.pleasantmountain.com/mountain-report"""
    
    url = "https://www.pleasantmountain.com/mountain-report"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [d.text.replace("\n" , " ").replace(" " , "") + " " for d in soup.select("ul.vList.vList_1")]
    num_trails = int([t for t in all_lists if "TrailsOpen " in t][0].replace("TrailsOpen " , ""))
    num_lifts = int([t for t in all_lists if "LiftsOpen " in t][0].replace("LiftsOpen " , ""))
    new_snow = int([t for t in all_lists if "NewSnow " in t][0].replace("NewSnow " , "").replace('"' , ""))
    
    
    data_dict = {"PLEASANT MOUNTAIN" : {"trails" : num_trails,
                                       "lifts" : num_lifts,
                                       "new snow" : new_snow}}
    return data_dict


# In[16]:


# ft
def get_12_website():
    
    """SUGARLOAF:  https://www.sugarloaf.com/mountain-report"""
    
    url = "https://www.sugarloaf.com/mountain-report"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [d.text.replace("\n" , " ").replace(" " , "") + " " for d in soup.select("ul.vList.vList_1")]
    
    num_trails = int([t for t in all_lists if "TrailsOpen " in t][0].replace("TrailsOpen " , ""))
    
    new_snow = int([t for t in all_lists if '"InchesLast24Hours ' in t][0].replace( '"InchesLast24Hours ' , ""))
    
    lifts_list = soup.select("#conditions_lifts_dee2e4a816064ad8b3df04324de73500 > div > div > div.box.mix-box_bordered > div > div")
    all_images = [l.select("img")[0].get("src") for l in lifts_list]
    all_lifts_from_images = [s.split("/")[-1] for s in all_images]
    lifts_status = [1 if "open" in l else 0 for l in all_lifts_from_images]
    num_lifts = np.sum(lifts_status)
    
    data_dict = {"SUGARLOAF" : {"trails" : num_trails , 
                               "lifts" : num_lifts , 
                               "new snow": new_snow}}
    
    return  data_dict
        


# In[17]:


# ft
def get_13_website():
    
    """SUNDAY RIVER:  https://www.sundayriver.com/mountain-report"""
    
    url = "https://www.sundayriver.com/mountain-report"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [d.text.replace("\n" , " ").replace(" " , "") + " " for d in soup.select("ul.vList.vList_1")]
    num_trails = int([t for t in all_lists if "TrailsOpen " in t][0].replace("TrailsOpen " , ""))
    num_lifts = int([t for t in all_lists if "LiftsOpen " in t][0].replace("LiftsOpen " , ""))
    new_snow = int([t for t in all_lists if "NewSnow " in t][0].replace("NewSnow " , "").replace('"' , ""))
        
    data_dict = {"SUNDAY RIVER" : {"trails" : num_trails,
                                  "lifts" : num_lifts , 
                                  "new snow" : new_snow}} 
    return data_dict


# In[18]:


# ft
def get_14_website():
    
    """BERKSHIRE EAST:  https://berkshireeast.com/plan/cams-conditions"""
    
    url = "https://berkshireeast.com/plan/cams-conditions"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [d.text.replace("\n" , " ").replace(" " , "") for d in soup.select("div.clearfix.text-formatted.field.field--name-field-copy-first-column.rte.field__item > div")]
    
    num_trails = int([l for l in all_lists if "TrailsOpen" in l][0].replace("TrailsOpen" , "").split("/")[0])
    num_lifts = int([l for l in all_lists if "LiftsOpen" in l][0].replace("LiftsOpen" , "").split("/")[0])
    new_snow = int([l for l in all_lists if "NewSnowLast24hours" in l][0].replace("NewSnowLast24hours" , "").replace('"' , ""))
    depth = int([l for l in all_lists if "MinimumBaseDepth" in l][0].replace("MinimumBaseDepth" , "").replace('"' , ""))
    
    data_dict = {"BERKSHIRE EAST" : {"trails" : num_trails,
                                    "lifts" : num_lifts , 
                                    "depth" : depth,
                                    "new snow" : new_snow}}
    return data_dict
    
    


# In[19]:


# ft
def get_15_website():
    
    """BOUSQUET:  https://bousquetmountain.com/lift-trail-status/"""
    
    url = "https://bousquetmountain.com/lift-trail-status/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lifts = [l.text.strip() for l in soup.select("section[data-id='396d401']")[0].select("div[class*='elementor-tablet-align-right elementor-mobile-align-right elementor-align-right elementor-icon-list--layout-traditional elementor-list-item-link-full_width elementor-widget elementor-widget-icon-list']")]
    all_trails = [l.text.strip() for l in soup.select("#content > div > div.elementor.elementor-10566 > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-745600d.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > div > div")[0].select("div[class*='elementor-tablet-align-right elementor-mobile-align-right elementor-align-right elementor-icon-list--layout-traditional elementor-list-item-link-full_width elementor-widget elementor-widget-icon-list']")]
    num_lifts = np.sum([1 if l == "OPEN" else 0 for l in all_lifts])
    num_trails = np.sum([1 if l == "OPEN" else 0 for l in all_trails])
    
    data_dict = {"BOUSQUET" : {"trails" : num_trails , 
                              "lifts" : num_lifts}}
    return data_dict
    





# In[20]:


# ft
def get_16_website():
    
    """CATAMOUNT:  https://catamountski.com/winter/mountain-conditions"""
    
    url = "https://catamountski.com/winter/mountain-conditions"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    all_lists = [d.text.replace(" " , "").replace("\n" , '') for d  in soup.select("ul.uk-list.uk-list-striped > li")]

    num_lifts = int([l for l in all_lists if "LiftsOpen:" in l][0].replace("LiftsOpen:" , "").split("/")[0])
    
    try:
        new_snow = float([l for l in all_lists if "NewSnowLast24hours:" in l][0].strip('"').replace("NewSnowLast24hours:" , ""))
    except:
        new_snow = 0
    
    depth = float([l for l in all_lists if "MinimumBaseDepth:" in l][0].strip('"').replace("MinimumBaseDepth:" , ""))
    
    num_trails = int([l for l in all_lists if "TrailsOpen:" in l][0].replace("TrailsOpen:" , "").split("/")[0])
    
    data_dict = {"CATAMOUNT" : {"trails" : num_trails,
                               "lifts" : num_lifts,
                               "depth" : depth , 
                               "new snow" : new_snow}}
    return data_dict


# In[21]:


# ft
def get_17_website():
    
    """JIMINY PEAK:  https://www.jiminypeak.com/The-Mountain/Mountain-Information/Snow-Report"""
    
    headers = {
        'authority': 'api.jiminypeak.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'dnt': '1',
        'origin': 'https://www.jiminypeak.com',
        'referer': 'https://www.jiminypeak.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            }
    
    response = requests.get('https://api.jiminypeak.com/api/SnowReport', headers=headers)
    
    j = json.loads(response.text)
    num_lifts = np.sum([l['Status']["OpenDay"]  for l in j["Lifts"]])
    num_trails = np.sum([l['Status']["OpenDay"]  for l in j["Trails"]])
    depth = j["Report"]["DepthMin"]
    new_snow = j["Report"]["NewSnow"]
    
    data_dict = {"JIMINY PEAK" : {"trails" : num_trails , 
                                 "lifts" : num_lifts,
                                 "depth" : depth,
                                 "new snow" : new_snow}}
    
    return data_dict


# In[22]:


# ft
def get_18_website():
    
    """NASHOBA VALLEY:  https://skinashoba.com/snow_report/"""
    
    url = "https://skinashoba.com/snow_report/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    tables = pd.read_html(r.text)
    
    trails_table = tables[2]
    trails_table.columns = trails_table.iloc[0 , :]
    trails_table = trails_table.iloc[1: , :]
    num_trails = np.sum([ 1 if "OPEN" in t else 0 for t in trails_table.Status.tolist()])
    
    lifts_table = tables[3]
    lifts_table.columns = lifts_table.iloc[0 , :]
    lifts_table = lifts_table.iloc[1 : , :]
    num_lifts = np.sum([ 1 if "OPEN" in t else 0 for t in lifts_table.dropna().Status.tolist()])
    
    orig_table = tables[0].set_index(0).T
    
    depth = int(orig_table["Base Depth"].tolist()[0].split("-")[0].strip('″"'))
    new_snow = int(orig_table["Recent Snowfall (24 hours)"].tolist()[0].strip('″"'))
    
    data_dict = {"NASHOBA VALLEY" : {"trails" : num_trails , 
                                    "lifts" : num_lifts,
                                    "depth" : depth,
                                    "new snow" : new_snow}}
    return data_dict


# In[23]:

#ft
def get_19_website():
    
    """BRADFORD:  https://skibradford.com/category/current-conditions/ (TRAILS ONLY)"""
    

    
    headers = {
        'authority': 'skibradford.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        # 'cookie': '_gcl_au=1.1.184952803.1674689409; _fbp=fb.1.1674689409082.2070154183; _ga=GA1.2.1227694022.1674689409; _gid=GA1.2.824277775.1674689409',
        'dnt': '1',
        'referer': 'https://skibradford.com/category/current-conditions/',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    
    r = requests.get('https://skibradford.com/trail-map/', headers=headers)
    soup = bs(r.text , "lxml")
    all_ps = [p.text for p in soup.select("p") if "Open Trails" in p.text][0]
    
    try:
        num_trails = re.findall("\d+" , all_ps)[0]
        
    except:
        num_trails = 0
        
        
    data_dict = {"BRADFORD" : {"trails" : num_trails}}
    
    return data_dict


   

# In[24]:


# ft
def get_20_website():
    
    """BUTTERNUT:  https://skibutternut.com/the-mountain/trails-conditions/condition-report"""
    
    url = "https://skibutternut.com/the-mountain/trails-conditions/condition-report"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists_labels = [d.text.replace("\n" , "") for d in soup.select("div.report-breakdown > div[class*='col'] > div.row > div.label")]
    all_lists_values = [d.text.replace("\n" , "") for d in soup.select("div.report-breakdown > div[class*='col'] > div.row > div.value")]
    values_dict = {key : val for key , val in zip(all_lists_labels , all_lists_values)}
    
    base_data = [d.strip() for d in soup.select("div.mountain-printout-info")[0].text.split("        ") if d.strip() != ""]
    
    depth = int([b for b in base_data if "Base Depth:" in b][0].split(":")[-1].split("-")[0])
    new_snow = int(re.findall("\d+" , [b for b in base_data if "Natural Snow (last 24 hrs):" in b][0].split(":")[-1])[0])
    
    num_trails = int(values_dict[[k for k in values_dict.keys() if "trails" in k.lower()][0]])

    num_lifts = int(values_dict[[k for k in values_dict.keys() if "lifts" in k.lower()][0]])

    data_dict = {"BUTTERNUT" : {"trails" : num_trails , 
                               "lifts" : num_lifts,
                               "depth" : depth,
                               "new snow" : new_snow}}
    return data_dict


# In[25]:


# ft
def get_21_website():
    
    """SKI WARD:  https://www.skiward.com/mountain-info/snow-report/"""
    
    url = "https://www.skiward.com/mountain-info/snow-report/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    table = pd.read_html(r.text)[0].iloc[1: , 0:2].set_index(0).T
    
    depth = int(re.findall( "\d+" , table["Average Base Depth:"].tolist()[0])[0])
    
    num_trails = int(re.findall( "\d+" , table["Open Terrain:"].tolist()[0])[0])
    num_lifts = int(re.findall( "\d+" , table["Lifts Open"].tolist()[0])[0])
    
    data_dict = {"SKI WARD" : {"trails" : num_trails,
                              "lifts" : num_lifts , 
                              "depth" : depth}}
    
    return data_dict


# In[26]:


# ft
def get_22_website():
    
    """WACHUSETT:  https://www.wachusett.com/The-Mountain/Your-Visit/Snow-Report.aspx"""
    
    headers = {
        'authority': 'wp-api.wachusett.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'dnt': '1',
        'origin': 'https://www.wachusett.com',
        'referer': 'https://www.wachusett.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    
    response = requests.get('https://wp-api.wachusett.com/api/SnowReport/Status', headers=headers)
    j = json.loads(response.text)
    num_lifts = np.sum([l['Status']["Open"]  for l in j["Lifts"]])
    num_trails = np.sum([l['Status']["Open"]  for l in j["Trails"]])
    depth = j["Report"]["DepthMin"]
    new_snow = j["Report"]["NewSnow"]
    
    data_dict = {"WACHUSETT" : { "trails" : num_trails , 
                               "lifts" : num_lifts,
                               "depth" : depth,
                               "new snow" : new_snow}}
    return data_dict


# In[27]:


# ft
def get_23_website():
    
    """ATTITASH:  https://www.attitash.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"""
    
    url = "https://www.attitash.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
        
    num_lifts = int(soup.select("div[data-terrain-status-id='lifts']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    num_trails = int(soup.select("div[data-terrain-status-id='runs']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    
        
    url2 = 'https://www.attitash.com/api/PageApi/GetWeatherDataForHeader'
    r2 = requests.get(url2)
    soup2 = bs(r2.text , "lxml")
    
    j = json.loads(r2.text)
    new_snow = int(j["SnowReportSections"][0]['Depth']['Centimeters'])
    depth = int(j["SnowReportSections"][-1]['Depth']['Centimeters'])

    data_dict = {"ATTITASH" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth" : depth,
                              "new snow" : new_snow}}
    return data_dict


# In[28]:


# ft
def get_24_website():
    
    """BRETTON WOODS:  https://www.brettonwoods.com/alpine_conditions/snow_conditions"""
    
    url = "https://www.brettonwoods.com/alpine_conditions/snow_conditions"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists_main = [d.text.replace("\n" , "").strip() for d in soup.select("div#report-top > div")]
    num_trails = int([d for d in all_lists_main if "Trail Count" in d][0].replace("Trail Count"  , "").split("/")[0])
    
    num_lifts = int([d for d in all_lists_main if "Lifts Open" in d][0].replace("Lifts Open"  , "").split("/")[0])
    
    all_lists_sec = [d.text.replace("\n" , "").strip() for d in soup.select("div#report-second")][0]
    
    snow_fall = int(re.findall( 'Snowfall - recent: (.*?)"Snowfall' , all_lists_sec)[0])
    depth = int(re.findall( 'Base Depth: (.*?)"Snowmaking:' , all_lists_sec)[0].split("-")[0])
    
    data_dict = {"BRETTON WOODS" : {"trails" : num_trails , 
                                   "lifts" : num_lifts,
                                   "depth" : depth,
                                   "new snow" : snow_fall}}
    
    return  data_dict


# In[29]:


# ft
def get_25_website():
    
    """CANNON MOUNTAIN:  https://www.cannonmt.com/mountain-report"""
    
    url = "https://www.cannonmt.com/mountain-report"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    new_snow = int(soup.select("div#data-new-snowfall > div.datum.long")[0].text.split("-")[0])
    num_lifts = int(soup.select("div#data-lifts > div.datum")[0].text)
    num_trails = int(soup.select("div#data-trails > div.datum")[0].text)
    depth = int(soup.select("div#data-base-depth > div.datum")[0].text.split("-")[0])
    
    data_dict = {"CANNON MOUNTAIN" : {"trails" : num_trails , 
                                     "lifts" : num_lifts,
                                     "depth" : depth,
                                     "new snow" : new_snow}}
    
    return data_dict


# In[30]:


# ft
def get_26_website():
    
    """CRANMORE:  https://www.cranmore.com/Snow-Report"""
    
    
    response = requests.get('https://digital.cranmore.com/_module/snow_report/feed.json')
    
    j = json.loads(response.text)
    
    num_trails = np.sum([ 0 if "Closed" in tt else 1 for tt in  [ t[ 'statuses']  for t in j["report"]["facilities"]['trails'] if t['excluded'] == False ]])
    num_lifts = np.sum([ 0 if "Closed" in tt else 1 for tt in  [ t[ 'statuses']  for t in j["report"]["facilities"]['lifts']]])
    
    
    depth = int(j["report"]["currentConditions"]["resortLocations"]["location"]["baseRange"].split("-")[0])
    
    try:
        new_snow = int(j["report"]["currentConditions"]["resortLocations"]["location"]["snow24Hours"].split("-")[0])
    except:
        new_snow = 0
        
    data_dict = {"CRANMORE" : {"trails" : num_trails ,
                              "lifts" : num_lifts,
                              "depth" : depth,
                              "new snow" : new_snow}}
    return data_dict 


# In[31]:


# ft
def get_27_website():
    
    """CROTCHED:  https://www.crotchedmtn.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx"""
    
    r = requests.get("https://www.crotchedmtn.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx")
    soup = bs(r.text , "lxml")
    
    num_lifts = int(soup.select("div[data-terrain-status-id='lifts']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    num_trails = int(soup.select("div[data-terrain-status-id='runs']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
        
    params = {
        '_': '1671547080977',
    }
    
    response = requests.get(
        'https://www.crotchedmtn.com/api/PageApi/GetWeatherDataForHeader',
        params=params
    )  
    
    j = json.loads(response.text)
    new_snow = int(j["SnowReportSections"][0]['Depth']['Centimeters'])
    depth = int(j["SnowReportSections"][-1]['Depth']['Centimeters'])
    
    data_dict = {"CROTCHED" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth": depth,
                              "new snow" : new_snow}}
    return data_dict


# In[32]:


# ft
def get_28_website():
    
    """DARTMOUTH SKIWAY:  https://sites.dartmouth.edu/skiway/mountain/ (LIFTS ONLY)"""
    
    headers = {
        'authority': 'www.snocountry.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
        'dnt': '1',
        'referer': 'https://sites.dartmouth.edu/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'object',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    
    params = {
        'code': 'vr-603008',
        'state': 'nh',
        'type': 'NA_Alpine',
        'region': 'us',
        'pettabs': '3',
        'size': 'xsmall',
        'color': 'white',
        'noads': 'no',
    }
    
    response = requests.get('https://www.snocountry.com/widget/widget_resort.php', params=params , headers = headers)
    tables = pd.read_html(response.text)
    
    df = tables[0]
    df.columns = df.iloc[1 , :]
    df = df.iloc[2:  ,:]
    
    num_lifts = int(df["Lifts Open"].tolist()[0].split("of")[0].strip())
    
    data_dict = {"DARTMOUTH SKIWAY" : {"lifts" : num_lifts}}
    return data_dict
        


# In[33]:


# ft
def get_29_website():
    
    """KING PINE:  https://www.kingpine.com/snow-report-conditions"""

    headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=2jduhq6nr0lvpts9m1c0u51vq1; _gcl_au=1.1.2069138583.1671548344; _ga=GA1.2.599575828.1671548345; _gid=GA1.2.443481992.1671548345; ipAddress=157.97.121.196; ll_visitorObject_ec4a5532-40c4-430f-8d97-24d16fe127a4={"timeRemove":"24","trackingLevel":"identifyStrong","ruleSelected":{"id":"39005344-2e9b-4d75-b750-67f09a6d3c89","key":"defaultOpen","name":"Open Consent - Worldwide","consentMethod":"openConsent","dataStorageRetention":{"timeRemove":"24","region":"northAmerica"},"geographicRegions":[{"regionType":"worldWide","continent":"","country":"","stateProvinces":""}],"visitorIdentification":{"notAllow":"","allow":"identifyVisitors","level":"identifyStrong"}},"consentListener":{"consentTool":"","listenerForGPC":true,"gpc":{"ad_storage":false,"analytics_storage":true,"functionality_storage":true,"personalization_storage":true,"security_storage":true}},"consentType":{"ad_storage":true,"analytics_storage":true,"functionality_storage":true,"personalization_storage":true,"security_storage":true},"tracking":{"trackingLevel":"identify","identifyStrength":"strong"},"ip":"157.97.121.196","visitorId":"5c2e6750c60d3fd171fcad789f57d6d9","consentSet":false}; ll_initSessionec4a5532-40c4-430f-8d97-24d16fe127a4={"visitorType":"5c2e6750c60d3fd171fcad789f57d6d9","visitorId":"5c2e6750c60d3fd171fcad789f57d6d9","id":"04f7d2cf-39d6-40dc-be77-49aa010c509c","number":1,"endTime":"2022-12-20T15:29:13Z","trackingLevel":"identifyStrong"}; ll_sid_5c2e6750c60d3fd171fcad789f57d6d9=04f7d2cf-39d6-40dc-be77-49aa010c509c; ll_vid=5c2e6750c60d3fd171fcad789f57d6d9; ll_udec4a5532-40c4-430f-8d97-24d16fe127a4=04f7d2cf-39d6-40dc-be77-49aa010c509c; ll_userSourceec4a5532-40c4-430f-8d97-24d16fe127a4=04f7d2cf-39d6-40dc-be77-49aa010c509c; ll_lastReferrerec4a5532-40c4-430f-8d97-24d16fe127a4=; ll_lastUserSourceec4a5532-40c4-430f-8d97-24d16fe127a4=Direct; ll_geolocationec4a5532-40c4-430f-8d97-24d16fe127a4={"latitude":"40.7126","longitude":"-74.0066"}; _dc_gtm_UA-2661962-1=1',
        'DNT': '1',
        'Referer': 'https://www.kingpine.com/',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    response = requests.get('https://conditions.kingpine.com/conditions/snow-report/', headers=headers)
    soup = bs(response.text , "lxml")
    
    all_lists = [d.text.replace("\n" , "") for d in soup.select("dl.SnowReport-measure")]
    num_lifts = int([l for l in all_lists if "Lifts Open" in l][0].split("of")[0].replace("Lifts Open" , ""))
    num_trails = int([l for l in all_lists if "Trails Open" in l][0].split("of")[0].replace("Trails Open" , ""))
    depth = int([l for l in all_lists if "Base Depth" in l][0].split("-")[0].replace("Base Depth" , ""))
    new_snow = int(re.findall( "\d+", [l for l in all_lists if "Past 24 Hours" in l][0].replace("Past 24 Hours" , "") )[0])
    
    data_dict = {"KING PINE" : {"trails" : num_trails,
                               "lifts" : num_lifts,
                               "depth" : depth,
                               "new snow" : new_snow}}
    
    return data_dict


# In[34]:


# ft
def get_30_website():
    
    """MOUNT SUNAPEE:  https://www.mountsunapee.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"""
    
    r = requests.get("https://www.mountsunapee.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx")
    soup = bs(r.text , "lxml")
    
        
    num_lifts = int(soup.select("div[data-terrain-status-id='lifts']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    num_trails = int(soup.select("div[data-terrain-status-id='runs']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    
    r = requests.get("https://www.mountsunapee.com/the-mountain/mountain-conditions/snow-and-weather-report.aspx")
    soup = bs(r.text , "lxml")
    script = str(soup.select("#body-content > div > div:nth-child(2) > div.weather_detail.container-fluid > div:nth-child(1) > div > script:nth-child(3)")[0])
    
    try:
        new_snow = int(re.findall('"TwentyFourHourSnowfall":{"Inches":"(.*?)","Centimeters":"(.*?)"},' , script)[0][1])
    except:
        new_snow = 0
        
    depth = int(re.findall('"BaseDepth":{"Inches":"(.*?)","Centimeters":"(.*?)"},' , script)[0][1])
    
    data_dict = {"MOUNT SUNAPEE" : {"trails" : num_trails , 
                                   "lifts" : num_lifts,
                                   "depth" : depth,
                                   "new snow" : new_snow}}
    
    return data_dict


# In[35]:


# ft
def get_31_website():
    
    """PATS PEAK:  https://www.patspeak.com/Plan-Your-Visit/Snow-Report.aspx"""
    
    response = requests.get('https://services.patspeak.com/api/SnowReport/Status')
    
    j = json.loads(response.text)
    
    num_lifts = np.sum([ l["Status"]["Open"] for l in j["Lifts"]])
    num_trails = np.sum([ l["Status"]["Open"] for l in j["Trails"] ])
    depth = j["Report"]["DepthMin"]
    new_snow = j["Report"]["NewSnowPast24HoursMax"]
    
    data_dict = {"PATS PEAK" : {"trails" :num_trails,
                               "lifts" : num_lifts,
                               "depth" : depth,
                               "new snow" : new_snow}}
    
    return data_dict


# In[36]:


# ft
def get_32_website():
    
    """RAGGED MOUNTAIN: https://raggedmountainresort.com/Slopes/"""
    
    url = "https://raggedmountainresort.com/Slopes/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_data = soup.select("table:nth-child(1)")[0].text.replace("\n" , "").replace("\xa0" , "")
    
    num_trails = int(re.findall("Slopes Open:(.*?)Lifts" , all_data)[0])
    num_lifts = int(re.findall("Lifts Open:(.*?)Average" , all_data)[0])
    depth = int(re.findall('Average Base:(.*?)"' , all_data)[0])
    new_snow = int(re.findall('24h Snow:(.*?)"' , all_data)[0])
    
    data_dict = {"RAGGED MOUNTAIN" : {"trails" : num_trails , 
                                     "lifts" : num_lifts,
                                     "depth" : depth , 
                                     "new snow" : new_snow}}
    return data_dict
    


# In[37]:


# ft
def get_33_website():
    
    
    """WATERVILLE VALLEY:  https://www.waterville.com/snow-report-maps"""
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9,ar;q=0.8',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=elrbprugavf6p2mr9078pm31m7',
        'DNT': '1',
        'Referer': 'https://www.waterville.com/',
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-site',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    response = requests.get('https://features.waterville.com/propmaps/map/map/',  headers=headers)
    soup = bs(response.text , "lxml")
    
    all_lists = [d.text for d in soup.select("dl.SnowReport-measure")]
    
    num_lifts = int(re.findall("\d+" , [l for l in all_lists if "Open Lifts" in l][0])[0])
    num_trails = int(re.findall("\d+" , [l for l in all_lists if "Open Trails" in l][0])[0])
    depth = int(re.findall("\d+" , [l for l in all_lists if "Base Depth" in l][0])[0])
    try:
        new_snow = int(re.findall("\d+" , [l for l in all_lists if "Past 24 Hours in." in l][0].replace("Past 24 Hours in." , ""))[0])
    except:
        new_snow = 0
        
    data_dict = {"WATERVILLE VALLEY" : {"trails" : num_trails,
                                       "lifts" : num_lifts,
                                       "depth" : depth,
                                       "new snow" :new_snow}}
    
    return data_dict


# In[38]:


# ft
def get_34_website():
    
    
    """WHALEBACK:  https://www.whaleback.com/conditions-trail-report"""
    
    r = requests.get("https://www.whaleback.com/conditions-trail-report")
    soup = bs(r.text , "lxml")
    iframe= soup.select("#block-yui_3_17_2_1_1608985974347_16168 > div > iframe")[0].get("src").split("&")[0]
    tables = pd.read_html(requests.get(iframe).text)
    
    
    df = tables[1].dropna()
    df.columns = ["un" , "label" , "value"]
    
    num_lifts = int(df[ df["label"].str.contains("Lifts Open:")]["value"].tolist()[0].split("/")[0])
    num_trails = int(df[ df["label"].str.contains("Trails Open:")]["value"].tolist()[0].split("/")[0])
    depth = int(df[ df["label"].str.contains("Base:")]["value"].tolist()[0])
    new_snow = int(df[ df["label"].str.contains("New Snow In The Last 24 Hours:")]["value"].tolist()[0].replace("Inches" , ""))
    
    data_dict = {"WHALEBACK" : {"trails" : num_trails , 
                               "lifts" : num_lifts,
                               "depth" : depth,
                               "new snow" : new_snow}}
    
    return data_dict


# In[39]:


# ft
def get_35_website():
    
    """WILDCAT:  https://www.skiwildcat.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"""
    
    url = "https://www.skiwildcat.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
        
    num_lifts = int(soup.select("div[data-terrain-status-id='lifts']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    num_trails = int(soup.select("div[data-terrain-status-id='runs']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    
        
    url2 = 'https://www.skiwildcat.com/api/PageApi/GetWeatherDataForHeader'
    r2 = requests.get(url2)
    soup2 = bs(r2.text , "lxml")
    
    j = json.loads(r2.text)
    new_snow = int(j["SnowReportSections"][0]['Depth']['Centimeters'])
    depth = int(j["SnowReportSections"][-1]['Depth']['Centimeters'])
    
    data_dict = {"WILDCAT" : {"trails" : num_trails , 
                             "lifts" : num_lifts,
                             "depth" : depth,
                             "new snow" : new_snow}}
    
    return data_dict


# In[40]:


# ft
def get_36_website():
    
    """YAWGOO VALLEY:  https://yawgoo.com/winter/report/"""
    
    url = "https://yawgoo.com/winter/report/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [l.text.strip() for l in soup.select("ul.uabb-info-list-wrapper.uabb-info-list-left > li")]
    
    lifts_list = [ 0 if "closed" in t.lower() else 1 for t in [l for l in all_lists if "lift" in l.lower()]]
    num_lifts = np.sum(lifts_list)
    
    trails_list = [ 0 if "closed" in t.lower() else 1 for t in [l for l in all_lists if "lift" not in l.lower()]]
    num_trails = np.sum(trails_list)
    
    data_dict = {"YAWGOO VALLEY" : {"trails" : num_trails , 
                                   "lifts" : num_lifts}}
    return data_dict


# In[41]:


# ft
def get_37_website():
    
    """BOLTON VALLEY:  https://www.boltonvalley.com/winter/trail-maps-snow-reports/snow-reports/"""
    url = "https://www.boltonvalley.com/wp-admin/admin-ajax.php"

    params = {
        'action': 'get_prop_conditions',
    }
    r = scraper.get(url , params = params)
    soup = bs(r.text , "lxml")
    
    j = json.loads(r.text)
    
    num_lifts = int(j['report']['facilities']['openDownHillLifts'])
    num_trails = int(j['report']['facilities']['openDownHillTrails'])
    depth = int(j['report']['currentConditions']['resortLocations']['location']['baseRange'].split("-")[0])
    new_snow = int(j['report']['currentConditions']['resortLocations']['location']['snow24Hours'].split("-")[0])
    
    data_dict = {"BOLTON VALLEY" : {"trails" : num_trails , 
                                  "lifts" : num_lifts , 
                                  "depth" : depth,
                                  "new snow" : new_snow} }
    
    return data_dict


# In[42]:


#ft
# def get_38_website():
    
#     """BROMLEY:  https://www.bromley.com/the-mountain/snow-report/"""
#     """ the correct url : https://www.bromley.com/snow-report/"""
    
#     url = "https://www.bromley.com/snow-report/"
#     r = requests.get(url)
#     soup = bs(r.text , "lxml")
    
#     all_lists = [d.text.replace("\n" , "") for d in soup.select("div[class*='col-12 col-md-6 col-lg-3']")]
    
#     num_lifts = int([l for l in all_lists if "Lifts Open" in l][0].replace("Lifts Open" , "").split("/")[0])
#     num_trails = int([l for l in all_lists if "Trails Open" in l][0].replace("Trails Open" , "").split("/")[0])
#     depth = int([l for l in all_lists if "Base Depth" in l][0].replace("Base Depth" , "").split("-")[0].strip('" '))
#     new_snow = int([l for l in all_lists if "New Snow" in l][0].replace("New Snow" , "").split("-")[0])
    
#     data_dict = {"BROMLEY" : {"trails" : num_trails , 
#                              "lifts" : num_lifts,
#                              "depth" : depth,
#                              "new snow" : new_snow}}
#     return data_dict

# the newer version 
# ft
def get_38_website():
    
    """BROMLEY:  https://www.bromley.com/the-mountain/snow-report/"""
    """ the correct url : https://www.bromley.com/snow-report/"""
    
    url = "https://www.bromley.com/snow-report/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [d.text.replace("\n" , "") for d in soup.select("div[class='row justify-content-center'] > div")]
    
    num_lifts = int([l for l in all_lists if "Lifts Open" in l][0].replace("Lifts Open" , "").split("/")[0])
    
    num_trails = int([l for l in all_lists if "Trails Open" in l][0].replace("Trails Open" , "").split("/")[0])
    
    depth = int([l for l in all_lists if "Base Depth" in l][0].replace("Base Depth" , "").split("-")[0].strip('" '))

    new_snow = int(re.findall( "\d+" , [l for l in all_lists if "New Snow" in l][0])[0])
    
    data_dict = {"BROMLEY" : {"trails" : num_trails , 
                             "lifts" : num_lifts,
                             "depth" : depth,
                             "new snow" : new_snow}}
    return data_dict






# In[43]:


# ft
def get_39_website():
    
    """BURKE:  https://www.skiburke.com/skiing-and-riding/the-mountain/trails-lifts-and-grooming/"""
    
    url = "https://www.skiburke.com/skiing-and-riding/the-mountain/trails-lifts-and-grooming/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    num_lifts = np.sum([0 if "closed" in t.lower() else 1 for t in [l.get("class")[0] for l in soup.select("table")[0].select("td.value:nth-child(2) > span")]])
    
    trails_list = [l.get("class")[0] for l in soup.select("table")[1].select("td.value:nth-child(2) > span")]
    num_trails = np.sum([0 if "closed" in t.lower() else 1 for t in trails_list])
    
    data_dict = {"BURKE" : {"trails" : num_trails , 
                           "lifts" : num_lifts}}
    
    return data_dict


# In[44]:


# ft
def get_40_website():
    
    """JAY PEAK:  https://jaypeakresort.com/todayatjay"""
    
    """the correct url : https://jaypeakresort.com/skiing-riding/snow-report-maps/snow-report"""
    
    url = "https://jaypeakresort.com/skiing-riding/snow-report-maps/snow-report"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    iframe = soup.select("iframe.trailmap")[0].get("src")
    r2 = requests.get(iframe)
    soup2 = bs(r2.text , "lxml")
    
    all_lists = [d.text for d in soup2.select("dl.SnowReport-measure")]
    num_lifts = int([l for l in all_lists  if "Open Lifts" in l][0].replace("Open Lifts" , "").split("/")[0])
    num_trails = int([l for l in all_lists  if "Open Trails" in l][0].replace("Open Trails" , "").split("/")[0])
    depth =  int([l for l in all_lists  if "Base Depth" in l][0].replace("Base Depth" , "").split("-")[0])
    new_snow = int([l for l in all_lists  if "Last 24 Hours" in l][0].replace("Last 24 Hours" , "").split("-")[0].strip('" '))
    
    data_dict = {"JAY PEAK" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth" : depth,
                              "new snow" : new_snow}}
    
    return data_dict


# In[45]:


# ft
def get_41_website():
    
    """KILLINGTON:  https://www.killington.com/the-mountain/conditions-weather/lifts-trails-report"""
    
    
    url = "https://api.killington.com/api/v1/dor/conditions"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    j = json.loads(r.text)
    
    num_lifts = j['liftReport']["open"]
    num_trails = j['trailReport']["open"]
    depth = [i["amount"] for i in j["snowReport"][0]["items"] if i["duration"] == 'base-depth'][0]
    new_snow = [i["amount"] for i in j["snowReport"][0]["items"] if i["duration"] == '24 Hours'][0]
    
    data_dict = {"KILLINGTON" : {"trails" : num_trails , 
                                "lifts" : num_lifts,
                                "depth" : depth,
                                "new snow" : new_snow}}
    return  data_dict


# In[46]:


# ft
def get_42_website():
    
    """MAD RIVER GLEN:  https://www.madriverglen.com/conditions/"""
    
    url = "https://www.madriverglen.com/conditions/"
    r = scraper.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [d.text.strip() for d in soup.select("div.condition_pagetop_middle.fix > div.condition_middle_item.fix")]
    num_lifts = int([l for l in all_lists if "LIFTS" in l][0].replace("LIFTS" , ""))
    num_trails = int([l for l in all_lists if "TRAILS" in l][0].replace("TRAILS" , ""))
    new_snow = int([l for l in all_lists if "NEW SNOW" in l][0].replace("NEW SNOW" , "").split("-")[0])
    
    data_dict = {"MAD RIVER GLEN" : {"trails" : num_trails , 
                                    "lifts" : num_lifts , 
                                    "new snow" : new_snow}}
    
    return data_dict


# In[47]:


# ft
def get_43_website():
    
    """MAGIC MOUNTAIN:  https://magicmtn.com/snow-report/"""
    
    url = "https://magicmtn.com/snow-report/"
    r = scraper.get(url)
    soup = bs(r.text , "lxml")
    
    tables= pd.read_html(r.text,  displayed_only=False)
    lift_table = tables[0]
    trails_table = pd.concat(tables[1:])
    
    num_lifts = np.sum([ t for t in lift_table["OPEN"].dropna().tolist() if ("yes" in t.lower()) or ("open" in t.lower())])
    num_trails = np.sum([ t for t in trails_table["OPEN"].dropna().tolist() if ("yes" in t.lower()) or ("open" in t.lower())])
    new_snow = int([ t for t in [d.get("data-number-value") for d in soup.select("div") if "24 HRS" in d.text ] if t != None][0])
    
    data_dict = {"MAGIC MOUNTAIN"  : {"trails" : num_trails , 
                                     "lifts" : num_lifts,
                                     "new snow" : new_snow}}
    return data_dict


# In[48]:


# # ft
# def get_44_website():
    
#     """MIDDLEBURY SNOW BOWL:  https://www.middleburysnowbowl.com/conditions/"""
    
#     url = "https://www.middleburysnowbowl.com/conditions/"
#     r = requests.get(url)
#     soup = bs(r.text , "lxml")
    
#     iframe = soup.select("#post-668 > div > div > p:nth-child(5) > iframe")[0].get("src")
    
#     r2 = requests.get(iframe)
#     soup2 = bs(r2.text , "lxml")
    
#     all_lists = [t.text for t in soup2.select("tr")]
    
#     num_lifts = int(re.findall("\d+" , [l for l in all_lists if "Lifts open:" in l][0].split("Lifts open:")[1])[0])
#     num_trails = int(re.findall("\d+" , [l for l in all_lists if "Trails open:" in l][0].split("Trails open:")[1])[0])
#     depth = int(re.findall("\d+" , [l for l in all_lists if "Base:" in l][0].split("Base:")[1])[0])
#     new_snow = int(re.findall("\d+" , [l for l in all_lists if "New Snow:" in l][0].split("New Snow:")[1])[0])
    
#     data_dict = {"MIDDLEBURY SNOW BOWL" : {"trails" : num_trails ,
#                                           "lifts" : num_lifts,
#                                           "depth" : depth,
#                                           "new snow" : new_snow}}
#     return data_dict

# newer version
# ft
def get_44_website():
    
    """MIDDLEBURY SNOW BOWL:  https://www.middleburysnowbowl.com/conditions/"""
    
    url = "https://www.middleburysnowbowl.com/conditions/"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
    
    iframe = soup.select("#post-668 > div > div > p:nth-child(5) > iframe")[0].get("src")
    
    r2 = requests.get(iframe)
    soup2 = bs(r2.text , "lxml")
    
    all_lists = [t.text for t in soup2.select("tr")]
    
    num_lifts = int(re.findall("\d+" , [l for l in all_lists if "Lifts open:" in l][0].split("Lifts open:")[1])[0])
    num_trails = int(re.findall("\d+" , [l for l in all_lists if "Trails open:" in l][0].split("Trails open:")[1])[0])
    depth = int(re.findall("\d+" , [l for l in all_lists if "Base:" in l][0].split("Base:")[1])[0])
    
    try:
        new_snow = int(re.findall("\d+" , [l for l in all_lists if "New Snow:" in l][0].split("New Snow:")[1])[0])
    except:
        new_snow = 0
    
    data_dict = {"MIDDLEBURY SNOW BOWL" : {"trails" : num_trails ,
                                          "lifts" : num_lifts,
                                          "depth" : depth,
                                            "new snow" : new_snow}}
    
    return data_dict




# ft
def get_45_website():
    
    """MOUNT SNOW:  https://www.mountsnow.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"""
    
    url = "https://www.mountsnow.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
        
    num_lifts = int(soup.select("div[data-terrain-status-id='lifts']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    num_trails = int(soup.select("div[data-terrain-status-id='runs']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    
    url2 = "https://www.mountsnow.com/api/PageApi/GetWeatherDataForHeader"
    r2 = requests.get(url2)
    soup2 = bs(r2.text , "lxml")
    
    j = json.loads(r2.text)
    new_snow = int(j["SnowReportSections"][0]['Depth']['Centimeters'])
    depth = int(j["SnowReportSections"][-1]['Depth']['Centimeters'])
    
    data_dict = {"MOUNT SNOW" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth" : depth,
                              "new snow" : new_snow}}
    return data_dict


# In[50]:


# ft
def get_46_website():
    
    """OKEMO:  https://www.okemo.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"""
    
    url = "https://www.okemo.com/the-mountain/mountain-conditions/lift-and-terrain-status.aspx"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
        
    num_lifts = int(soup.select("div[data-terrain-status-id='lifts']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    num_trails = int(soup.select("div[data-terrain-status-id='runs']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    
    url2 = "https://www.okemo.com/api/PageApi/GetWeatherDataForHeader"
    r2 = requests.get(url2)
    soup2 = bs(r2.text , "lxml")
    
    j = json.loads(r2.text)
    try:
        new_snow = int(j["SnowReportSections"][0]['Depth']['Centimeters'])
    except:
        new_snow = 0
        
    try:
        depth = int(j["SnowReportSections"][-1]['Depth']['Centimeters'])
    except:
        depth = 0
    data_dict = {"OKEMO" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth" : depth,
                              "new snow" : new_snow}}
    
    return data_dict


# In[51]:


# ft
# def get_48_website():
    
#     """SMUGGLERS NOTCH:  https://www.smuggs.com/pages/winter/snowReport/"""
#     url = "https://www.smuggs.com/pages/winter/snowReport/"
#     r = scraper.get(url)
#     soup = bs(r.text , "lxml")
    
#     all_lists = [d.text for d in soup.select("div#trail-summary > p")] + [d.text for d in soup.select("div#base-summary > p")]
#     num_lifts = int(re.findall("\d+" , [l for l in all_lists if "Lifts" in l][0])[0])
#     num_trails = int(re.findall("\d+" , [l for l in all_lists if "Trails Open" in l][0])[0])
#     new_snow = int(re.findall("\d+" , [l for l in all_lists if "New Snow" in l][0])[0])
    
#     data_dict = {"SMUGGLERS NOTCH" : {"trails" : num_trails ,
#                                      "lifts" : num_lifts,
#                                      "new snow" : new_snow}}
    
#     return data_dict


# the newer version
# ft
def get_48_website():
    
    """SMUGGLERS NOTCH:  https://www.smuggs.com/pages/winter/snowReport/"""
    url = "https://www.smuggs.com/pages/winter/snowReport/"
    r = scraper.get(url)
    soup = bs(r.text , "lxml")
    
    all_lists = [d.text for d in soup.select("div#trail-summary > p")] + [d.text for d in soup.select("div#base-summary > p")]
    num_lifts = int(re.findall("\d+" , [l for l in all_lists if "Lifts" in l][0])[0])
    num_trails = int(re.findall("\d+" , [l for l in all_lists if "Trails Open" in l][0])[0])
    
    try:
        new_snow = int(re.findall("\d+" , [l for l in all_lists if "New Snow" in l][0])[0])
    except:
        new_snow = 0
    
    data_dict = {"SMUGGLERS NOTCH" : {"trails" : num_trails ,
                                     "lifts" : num_lifts,
                                     "new snow" : new_snow}}
    
    return data_dict


# ft
def get_49_website():
    
    """STOWE:  https://www.stowe.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx"""
    
    
    url = "https://www.stowe.com/the-mountain/mountain-conditions/terrain-and-lift-status.aspx"
    r = requests.get(url)
    soup = bs(r.text , "lxml")
        
    num_lifts = int(soup.select("div[data-terrain-status-id='lifts']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    num_trails = int(soup.select("div[data-terrain-status-id='runs']")[0].select("div.terrain_summary__circle")[0].get("data-open"))
    
        
    url2 = 'https://www.stowe.com/api/PageApi/GetWeatherDataForHeader'
    r2 = requests.get(url2)
    soup2 = bs(r2.text , "lxml")
    
    j = json.loads(r2.text)
    new_snow = int(j["SnowReportSections"][0]['Depth']['Centimeters'])
    depth = int(j["SnowReportSections"][-1]['Depth']['Centimeters'])
    
    data_dict = {"STOWE" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth" : depth,
                              "new snow" : new_snow}}
    return data_dict
    
    


# In[53]:


# ft
def get_50_website():
    
    """STRATTON:  https://www.stratton.com/the-mountain/mountain-report"""
    params = {
        'format': 'json',
        'resortId': '1',
    }
    
    response = requests.get('https://www.mtnpowder.com/feed', params=params)
    soup = bs(response.text , "lxml")
    
    j = json.loads(response.text)
    
    num_lifts = j['SnowReport']['TotalOpenLifts']
    num_trails = j['SnowReport']['TotalOpenTrails']
    depth = float(j['SnowReport']["BaseArea"]['BaseCm'])
    
    data_dict = {"STRATTON" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth" : depth}}
    
    return data_dict


# In[54]:


# ft
def get_51_website():
    
    """SUGARBUSH:  https://www.sugarbush.com/mountain/conditions"""
    
    
    url = 'https://www.mtnpowder.com/feed?format=json&resortId=70'
    r = requests.get(url)
    j = json.loads(r.text)
        
    num_lifts = j['SnowReport']['TotalOpenLifts']
    num_trails = j['SnowReport']['TotalOpenTrails']
    new_snow = float(j['SnowReport']["BaseArea"]['Last24HoursIn'])
    depth = float(j['SnowReport']["BaseArea"]['BaseCm'])
    
    data_dict = {"SUGARBUSH" : {"trails" : num_trails,
                              "lifts" : num_lifts,
                              "depth" : depth,
                              "new snow" : new_snow}}
    return data_dict


# In[ ]:





# In[55]:


def get_final_json_data():
    """this function combines all the extracted data from all 50 websites into one json file with the name of data_today_date.json"""
    final_json = []
    
    # data = get_1_website()
    # final_json.append(data)
    # print('1 website is done scraping' )
    # #############################################
    # data = get_2_website()
    # final_json.append(data)
    # print('2 website is done scraping' )
    # #############################################
    # data = get_3_website()
    # final_json.append(data)
    # print('3 website is done scraping' )
    # #############################################
    # data = get_4_website()
    # final_json.append(data)
    # print('4 website is done scraping' )
    # #############################################
    # data = get_5_website()
    # final_json.append(data)
    # print('5 website is done scraping' )
    # #############################################
    # data = get_6_website()
    # final_json.append(data)
    # print('6 website is done scraping' )
    # #############################################
    # data = get_7_website()
    # final_json.append(data)
    # print('7 website is done scraping' )
    # #############################################
    # data = get_8_website()
    # final_json.append(data)
    # print('8 website is done scraping' )
    # #############################################
    # data = get_9_website()
    # final_json.append(data)
    # print('9 website is done scraping' )
    # #############################################
    # data = get_10_website()
    # final_json.append(data)
    # print('10 website is done scraping' )
    # #############################################
    # data = get_11_website()
    # final_json.append(data)
    # print('11 website is done scraping' )
    # #############################################
    # data = get_12_website()
    # final_json.append(data)
    # print('12 website is done scraping' )
    # #############################################
    # data = get_13_website()
    # final_json.append(data)
    # print('13 website is done scraping' )
    # #############################################
    # data = get_14_website()
    # final_json.append(data)
    # print('14 website is done scraping' )
    # #############################################
    # data = get_15_website()
    # final_json.append(data)
    # print('15 website is done scraping' )
    # #############################################
    # data = get_16_website()
    # final_json.append(data)
    # print('16 website is done scraping' )
    # #############################################
    # data = get_17_website()
    # final_json.append(data)
    # print('17 website is done scraping' )
    # #############################################
    # data = get_18_website()
    # final_json.append(data)
    # print('18 website is done scraping' )
    # #############################################
    # data = get_19_website()
    # final_json.append(data)
    # print('19 website is done scraping' )
    # #############################################
    # data = get_20_website()
    # final_json.append(data)
    # print('20 website is done scraping' )
    # #############################################
    # data = get_21_website()
    # final_json.append(data)
    # print('21 website is done scraping' )
    # #############################################
    # data = get_22_website()
    # final_json.append(data)
    # print('22 website is done scraping' )
    # #############################################
    # data = get_23_website()
    # final_json.append(data)
    # print('23 website is done scraping' )
    # #############################################
    # data = get_24_website()
    # final_json.append(data)
    # print('24 website is done scraping' )
    # #############################################
    # data = get_25_website()
    # final_json.append(data)
    # print('25 website is done scraping' )
    # #############################################
    # data = get_26_website()
    # final_json.append(data)
    # print('26 website is done scraping' )
    # #############################################
    # data = get_27_website()
    # final_json.append(data)
    # print('27 website is done scraping' )
    # #############################################
    # data = get_28_website()
    # final_json.append(data)
    # print('28 website is done scraping' )
    # #############################################
    # data = get_29_website()
    # final_json.append(data)
    # print('29 website is done scraping' )
    # #############################################
    # data = get_30_website()
    # final_json.append(data)
    # print('30 website is done scraping' )
    # #############################################
    # data = get_31_website()
    # final_json.append(data)
    # print('31 website is done scraping' )
    # #############################################
    # data = get_32_website()
    # final_json.append(data)
    # print('32 website is done scraping' )
    # #############################################
    # data = get_33_website()
    # final_json.append(data)
    # print('33 website is done scraping' )
    # #############################################
    # data = get_34_website()
    # final_json.append(data)
    # print('34 website is done scraping' )
    # #############################################
    # data = get_35_website()
    # final_json.append(data)
    # print('35 website is done scraping' )
    # #############################################
    # data = get_36_website()
    # final_json.append(data)
    # print('36 website is done scraping' )
    # #############################################
    # data = get_37_website()
    # final_json.append(data)
    # print('37 website is done scraping' )
    # #############################################
    # data = get_38_website()
    # final_json.append(data)
    # print('38 website is done scraping' )
    # #############################################
    # data = get_39_website()
    # final_json.append(data)
    # print('39 website is done scraping' )
    # #############################################
    # data = get_40_website()
    # final_json.append(data)
    # print('40 website is done scraping' )
    # #############################################
    # data = get_41_website()
    # final_json.append(data)
    # print('41 website is done scraping' )
    # #############################################
    # data = get_42_website()
    # final_json.append(data)
    # print('42 website is done scraping' )
    # #############################################
    # data = get_43_website()
    # final_json.append(data)
    # print('43 website is done scraping' )
    # #############################################
    # data = get_44_website()
    # final_json.append(data)
    # print('44 website is done scraping' )
    # #############################################
    # data = get_45_website()
    # final_json.append(data)
    # print('45 website is done scraping' )
    # #############################################
    # data = get_46_website()
    # final_json.append(data)
    # print('46 website is done scraping' )
    # #############################################
    # #     data = get_47_website()
    # #     final_json.append(data)
    # #     print('47 website is done scraping' )
    # #############################################
    # data = get_48_website()
    # final_json.append(data)
    # print('48 website is done scraping' )
    # #############################################
    # data = get_49_website()
    # final_json.append(data)
    # print('49 website is done scraping' )
    # #############################################
    # data = get_50_website()
    # final_json.append(data)
    # print('50 website is done scraping' )
    # #############################################
    # data = get_51_website()
    # final_json.append(data)
    # print('51 website is done scraping' )



    try:
        data = get_1_website()
        final_json.append(data)
        print('1 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_2_website()
        final_json.append(data)
        print('2 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_3_website()
        final_json.append(data)
        print('3 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_4_website()
        final_json.append(data)
        print('4 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_5_website()
        final_json.append(data)
        print('5 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_6_website()
        final_json.append(data)
        print('6 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_7_website()
        final_json.append(data)
        print('7 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_8_website()
        final_json.append(data)
        print('8 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_9_website()
        final_json.append(data)
        print('9 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_10_website()
        final_json.append(data)
        print('10 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_11_website()
        final_json.append(data)
        print('11 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_12_website()
        final_json.append(data)
        print('12 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_13_website()
        final_json.append(data)
        print('13 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_14_website()
        final_json.append(data)
        print('14 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_15_website()
        final_json.append(data)
        print('15 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_16_website()
        final_json.append(data)
        print('16 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_17_website()
        final_json.append(data)
        print('17 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_18_website()
        final_json.append(data)
        print('18 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_19_website()
        final_json.append(data)
        print('19 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_20_website()
        final_json.append(data)
        print('20 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_21_website()
        final_json.append(data)
        print('21 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_22_website()
        final_json.append(data)
        print('22 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_23_website()
        final_json.append(data)
        print('23 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_24_website()
        final_json.append(data)
        print('24 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_25_website()
        final_json.append(data)
        print('25 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_26_website()
        final_json.append(data)
        print('26 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_27_website()
        final_json.append(data)
        print('27 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_28_website()
        final_json.append(data)
        print('28 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_29_website()
        final_json.append(data)
        print('29 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_30_website()
        final_json.append(data)
        print('30 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_31_website()
        final_json.append(data)
        print('31 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_32_website()
        final_json.append(data)
        print('32 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_33_website()
        final_json.append(data)
        print('33 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_34_website()
        final_json.append(data)
        print('34 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_35_website()
        final_json.append(data)
        print('35 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_36_website()
        final_json.append(data)
        print('36 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_37_website()
        final_json.append(data)
        print('37 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_38_website()
        final_json.append(data)
        print('38 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_39_website()
        final_json.append(data)
        print('39 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_40_website()
        final_json.append(data)
        print('40 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_41_website()
        final_json.append(data)
        print('41 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_42_website()
        final_json.append(data)
        print('42 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_43_website()
        final_json.append(data)
        print('43 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_44_website()
        final_json.append(data)
        print('44 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_45_website()
        final_json.append(data)
        print('45 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_46_website()
        final_json.append(data)
        print('46 website is done scraping' )
    except:
        None
    #############################################
    # try:
    #     data = get_47_website()
    #     final_json.append(data)
    #     print('47 website is done scraping' )
    # except:
    #     None
    #############################################
    try:
        data = get_48_website()
        final_json.append(data)
        print('48 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_49_website()
        final_json.append(data)
        print('49 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_50_website()
        final_json.append(data)
        print('50 website is done scraping' )
    except:
        None
    #############################################
    try:
        data = get_51_website()
        final_json.append(data)
        print('51 website is done scraping' )
    except:
        None
    ############################################
    
    return final_json
    


# In[66]:


import numpy
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        if isinstance(obj, numpy.floating):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
 


# In[67]:

print("we are here ")

def write_final_json_file():
    """this function scrape all the data from all sources and write them into a json file"""
    print("getting the data from all the sources")
    global t1
    

    json_data = get_final_json_data()
    
    # today = datetime.datetime.now().strftime("%Y_%m_%d")
    # today_hourly = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
    
    try:
        os.remove(f"data.json")
        
    except:
        None
        
    with open(f"data.json" , "w") as file:
        file.write(json.dumps(json_data , cls=NpEncoder))
        
    print(f"your data is stored in data.json ")
    print("the scraping for today is finished")
    t2 = time.time()

    print(f"the overall time for scraping is {(t2 - t1)/60} minutes only")
    print(f" 51 websites are scraped into .json file with name of data.json")
#     return json_data


# In[ ]:

# write_final_json_file()
# scheduling the code to run every day at 6 am

schedule.every().day.at("06:00").do(write_final_json_file)
#schedule.every().day.at("12:00").do(write_final_json_file)
# schedule.every(1).hour.do(write_final_json_file)

while True:
    
    schedule.run_pending()
    # time.sleep(1)
    


# In[697]:


# pip install schedule


# In[ ]:




