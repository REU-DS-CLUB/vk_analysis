# -*- coding: utf-8 -*-
"""vk_analysis

### Libraries
"""

# pip install vk_api

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import vk_api
import datetime
import time

"""### VK API
"""

vk = vk_api.VkApi(token=token)
vk._auth_token()

"""### Functions
"""


def get_token():
    
        """Returns a link where by clicking on it a user can get his/her token. """
        
    link_token = 'https://oauth.vk.com/authorize?client_id=5440699&display=page&redirect_uri=vk.com/callback&response_type=token&v=5.80&scope=offline'
    return 'Use this link to get your token. It will be after "access_token=" and before "&expires_in=86400":', str(
        link_token)


def parse_data_from_table(file_name, sheet_number=None, column=None) -> list:
    
        """Returns the list of abbreviations for partners to create a utm tag 
       
    Parameters
    ----------
    file_name : str
     a string with a name of a file where a table with information about partners and their abbreviations for utm tags is stored 
     
    sheet_number : int
     integer that represents the sheet of the table where all the info is stored 
     
    column : int 
     integer that represents the column of the table where all the info is stored 
    
     
    """
 
    
    if sheet_number is None or column is None:
        raise ValueError("Column or Sheet number where abbreviations are stored should be included in the input")
    if ".xlsx" not in file_name:
        file_name += ".xlsx"
    data = pd.read_excel(file_name, sheet_name=sheet_number)
    data = [x for x in data[data.columns[column]]]

    return data


def create_unique_link(abbreviations: list, add_link: str) -> list:
    
            """Returns the list of unqiue links for partners 
            
    Parameters
    ----------
    abbreviations : list
     a list where abbreviations are stored 
     
    add_link : str
     link that will be delivered to partners (for an event/website and etc)
     
    """
    
    if abbreviations is str:
        raise ValueError("abbreviation should be put into a list")

    temp_list = []
    # фильтрация абревиатур
    for abb in abbreviations:
        if str(abb) == 'nan' or str(abb) == '':
            temp_list.append('')
        else:
            temp_list.append(add_link + '?utm_source=' + abb)
    return temp_list


def create_short_links(links: list, private=0) -> list:
    
                """Returns the list of short links that can be sent to partners and further will be used to gather stats 
            
    Parameters
    ----------
    links : list
     a list of unqiue links that should be generated via the function: create_short_links
     
    private : 0 / 1 
     private = 0 by default - the stats is public, everyone with knowing a link can analyse it | private = 1 if it is for private use only
     
     """


    if links is not None:
        short_links = []
        for i in range(len(links)):
            time.sleep(0.5)
            l = links[i]

            if l is not None and l != "" and l != " ":
                short_links.append(vk.method("utils.getShortLink", {'url': l, 'private': private})['short_url'])

            short_links.append('')
    else:
        raise ValueError("Column where abbreviations are stored should be included in the input")
        return None

    return short_links


def view_stats(link, interval='day', intervals_count=90, extended=0):
        
                """Returns the list of lists with views per chosen unit in parameter interval in format: 
                   if interval='days' : ['dd.mm.yyyy', VIEWS] 
    
    Parameters
    ----------
    link : str
     a string with a shorthened link (generated with func: create_short_links) for a partner that a user wants to gather stats about  
     
    interval : str
     Unit of time for a stats computation. Possible values:
     - hour 
     - day 
     - week 
     - month
     - forever — since the day a link has been created

    intervals_count : int
     Number of periods for stats reviewing in chosen units (from a parameter: interval)
     intervals_count cannot be set as 0
     Ex. if interval = 'day' and intervals_count = 5 : func will return the stats for 5 days 
    
    extended : 0 / 1
     extended = 1 if sex, age, country, city of viewers are needed
     
     """
    
  
    
    key = link[14:]
    dict_stats = vk.method("utils.getLinkStats", {'key': key, 'interval': interval, 'extended': extended,
                                                  'intervals_count': intervals_count})['stats']
    stat = []
    for list in dict_stats:
        t_arr = [datetime.datetime.utcfromtimestamp(list['timestamp']).strftime('%d.%m.%Y'), list['views']]
        stat.append(t_arr)
    stat.reverse()
    return stat


def visualize_stats(link, x_name='', y_name='Views', title_name=""):
    
                    """Returns the line chart with the dynamic of views for a partner 
            
    Parameters
    ----------
    link : str
     a shorthened link (generated with func: create_short_links) for a partner that a user wants to gather stats about  
     
    x_name : 
     a preferrable title for x axis
     
    y_name : 
     a preferrable title for y axis
    
    
    title_name : str
     a preferrable title for a partner
     
     """
    
    # visualization of stats
    key = link[14:]
    
    if title_name == "":
        title_name = key

    dataFrame = view_stats(key, intervals_count=10)

    df = pd.DataFrame(dataFrame, columns=[x_name, title_name])

    graph = df.plot(x_name, title_name)

    graph.set_title(title_name)
    plt.xticks(rotation=45)
    graph.set_ylabel('Views')
    graph.grid()
    plt.show()

