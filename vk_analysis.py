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

# token = 'f7ebf5112379b724e1d11b0a8ab124b74f0d3b5d72af68a9efd90db22e46f69473be213ba81bd8af92d02'

# link = 'https://docs.google.com/forms/d/e/1FAIpQLSfKtUbT3qzkRLLYP0tOfvlRHqiUH3as0Mi3mV06Yi8poCcw1Q/viewform'

vk = vk_api.VkApi(token=token)
vk._auth_token()

"""### Functions
"""


def get_token():
    link_token = 'https://oauth.vk.com/authorize?client_id=5440699&display=page&redirect_uri=vk.com/callback&response_type=token&v=5.80&scope=offline'
    return 'Use this link to get your token. It will be after "access_token=" and before "&expires_in=86400":', str(
        link_token)


def parse_data_from_table(file_name, sheet_number=None, column=None) -> list:
    
    if sheet_number is None or column is None:
        raise ValueError("Column or Sheet number where abbreviations are stored should be included in the input")
    if ".xlsx" not in file_name:
        file_name += ".xlsx"
    data = pd.read_excel(file_name, sheet_name=sheet_number)
    data = [x for x in data[data.columns[column]]]

    return data


def create_unique_link(abbreviations: list, add_link: str) -> list:
    
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
    
    # links should be generated via the function: create_short_links
    # private=1 if it is for private use only

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
    
    # extended=1 if sex, age, country, city of viewers are needed
    # intervals_count cannot be set as 0
    
    key = link[14:]
    dict_stats = vk.method("utils.getLinkStats", {'key': key, 'interval': interval, 'extended': extended,
                                                  'intervals_count': intervals_count})['stats']
    stat = []
    for list in dict_stats:
        t_arr = [datetime.datetime.utcfromtimestamp(list['timestamp']).strftime('%d.%m.%Y'), list['views']]
        stat.append(t_arr)
    stat.reverse()
    return stat


def visualize_stats(key, x_name='', y_name='Views', title_name=""):
    
    # visualization of stats
    
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

