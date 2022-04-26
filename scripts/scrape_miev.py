#!python3
# coding: utf-8

import os
import sys
from datetime import date as dt
from datetime import datetime
import pandas as pd
import requests
import json
import re
import ast

sys.path.append('./lib')
import scrape  

# PostgreSQL connection
engine = create_engine('postgresql://cdn_events:###@cdn.bplaced.net:5432/cdn_events', connect_args={'options': '-csearch_path={}'.format('stage')})

# Current date for deltaload
startMonth = datetime.now().strftime('%Y%m%d')

# API-URL
raw_data = scrape.scrape_url("https://exchange.cmcitymedia.de/geislingenNeu/veranstaltungenData.php?mapHomepageId=4500&action=getAllData&startMonth=" + startMonth)

# Read JSONP and convert
raw_data = raw_data.decode('utf-8')
raw_data = re.match(".*?({.*}).*",raw_data,re.S).group(1)
raw_data = raw_data.replace('{sites:','{"sites":')

# Convert to Dictionary
dict_data = ast.literal_eval(raw_data)

events = dict_data["sites"]


picture_url_prefix = "https://publish.cmcitymedia.de/calendar/getPicture.php?id="

event_info = []
event_list = []

# Write to dataframe
for event in events:
    event_id = event["cal_id"]
    title = event["title"]
    category = event["category"]
    organizer = event["organizer"]
    description = scrape.clean_html_description(event["description"])
    event_date = event["dateFrom"]
    img_url = picture_url_prefix + event["picture"]
    event_url = "https://www.geislingen.de/index.php?id=93"
    
    event_info = dict(
        event_id=event_id,
        title=title,
        description=description,
        event_date=event_date,
        category=category,
        organizer=organizer,
        img_url=img_url,
        event_url=event_url,
    )
    
    event_list.append(event_info)
    
 df = pd.DataFrame(event_list)
 
 # Upload to PostgreSQL database
 df.to_sql('events_geislingen', engine, if_exists='replace', index=False)
 
 
 # Execute Merge Procedure
 engine.execute('CALL merge_events_geislingen(); COMMIT;')