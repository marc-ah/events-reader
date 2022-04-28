import os
from datetime import datetime
import requests
import logging
import sys
import re

import html2text
h2t = html2text.HTML2Text()
h2t.ignore_links = True
h2t.ignore_images = True
h2t.RE_MD_CHARS_MATCHER = True

def scrape_url(url):

    #Loggin
   
    logging.basicConfig(filename='scrape.log',
                    filemode='a',
                    format='%(asctime)s;%(levelname)s;%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

    #request website
    try:
        response = requests.get(url, allow_redirects=True)
        content = response.content
        text = response.text
        status = response.status_code
    
        if status != 200:
            logging.warning(f" Request to {url} FAILED. Status: {status}")
        else:
            logging.info(f" Request to {url} successful. Status: {status}")
            
        return response.content
          
    except:
        logging.error(f" An Error occured while requesting {url}")
        logging.error(f" Unexpected error:", sys.exc_info()[0])
        


def clean_html_description(d):
    d = re.sub("\[(.|\n)*?\]", '', d)
    d = h2t.handle(d)
    d = d.replace('\n\n\n','\n')
    d = d.replace('\n','<br>')
    d = d.replace('###','')
    d = d.replace('##','')
    d = d.strip('<br>')
    d = d.strip(' ')
    d = d.strip('#')
    return d



if __name__ == "__main__":
    logging.warning(" scrape_website: You can run this module only within another script")
