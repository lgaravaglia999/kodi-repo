from bs4 import BeautifulSoup
import re
import json
import requests

def return_first_regroup(pattern, text):
    try:
        m = re.search(pattern, text)
        return m.group(1)
    except:
        return 'n'

def get_stream_url(url):
    r = requests.get(url)
    if(r.status_code != 200):
        print("Error getting url")
        return

    if '<input type="hidden" name="op" value="' in r.text:
        op = return_first_regroup('<input type="hidden" name="op" value="(.*)">', r.text)
        usr_login = return_first_regroup('<input type="hidden" name="usr_login" value="(.*)">', r.text)
        id = return_first_regroup('<input type="hidden" name="id" value="(.*)">', r.text)
        fname = return_first_regroup('<input type="hidden" name="fname" value="(.*)">', r.text)
        referer = return_first_regroup('<input type="hidden" name="referer" value="(.*)">', r.text)
        hash = return_first_regroup('<input type="hidden" name="hash" value="(.*)">', r.text)
        
        site = return_first_regroup('<Form method="POST" action=\'(.*)\'>', r.text)
        
        r = requests.post(site, data = {
                'op': op, 
                'usr_login': usr_login,
                'id': id,
                'fname': fname,
                'referer': referer,
                'hash': hash
            }
        )

    stream_url = return_first_regroup('var linkfile ="(.*)";', r.text)
    result = requests.get(stream_url, allow_redirects=False, timeout=5, stream=True)
    source_url_mp4 = result.headers["Location"]
    return source_url_mp4