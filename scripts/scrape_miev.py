#!python3
# coding: utf-8

from dotenv import load_dotenv
import os
import sys
from datetime import date as dt
from datetime import datetime
import pandas as pd
import requests
import json
import re
import ast
from sqlalchemy import create_engine

sys.path.append('./lib')
import scrape  

load_dotenv()

host = str(os.getenv("POSTGRES_HOST"))
port = str(os.getenv("POSTGRES_PORT"))
user = str(os.getenv("POSTGRES_USER"))
password = str(os.getenv("POSTGRES_PASS"))
db = str(os.getenv("POSTGRES_DB"))

postgres_connection_string = "postgresql://" + db + ":" + password + "@" + host + ":" + port + "/" + db

# PostgreSQL connection
engine = create_engine(postgres_connection_string, connect_args={'options': '-csearch_path={}'.format('stage')})

raw_data = scrape.scrape_url("https://www.miev.info/index.php/wp-json/tribe/events/v1/events")

#Load JSON and convert
json_data = json.loads(raw_data)


events = json_data["events"]


event_info = []
event_list = []

# Write to dataframefor event in events:
for event in events:
    event_id = event["id"]
    title = event["title"]
    category = "Feiern & Geselligkeit"
    description = scrape.clean_html_description(event["description"])
    event_date = event["start_date"][0:10]
    img_url = event['image']['url']
    event_url = event["url"]
    
    event_info = dict(
        event_id=event_id,
        title=title,
        description=description,
        event_date=event_date,
        category=category,
        organizer='Muskerinitiative e.V.',
        img_url=img_url,
        event_url=event_url,
    )
    
    event_list.append(event_info)
    
df = pd.DataFrame(event_list)
 
# Upload to PostgreSQL database
df.to_sql('events_miev', engine, if_exists='replace', index=False)

# Execute Merge Procedure
engine.execute('CALL merge_events_miev(); COMMIT;')