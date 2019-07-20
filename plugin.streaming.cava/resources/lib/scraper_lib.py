from bs4 import BeautifulSoup
import requests

class Element:
    def __init__(self, block, el_tag, el_id=None, el_class=None,
        el_property=None, get_text=False, recursive=True):

        self.block = block
        self.el_tag = el_tag
        self.el_id = el_id
        self.el_class = el_class
        self.el_property = el_property
        self.get_text = get_text
        self.recursive = recursive
    
    def get_element(self):
        el_attrs = {}
        if self.el_class is not None:
            el_attrs['class'] = self.el_class
        if self.el_id is not None:
            el_attrs['id'] = self.el_id

        res = self.block.find(self.el_tag, attrs=el_attrs,
                    recursive=self.recursive)

        if self.el_property is not None:
            res = res.get(self.el_property)
        if self.get_text:
            res = res.text

        return res




class Container:
    def __init__(self, block, tag, first=False, container_class=None,
        container_id=None, recursive=True, text=False):
        
        self.block = block
        self.tag = tag
        self.first = first
        self.container_class = container_class
        self.container_id = container_id
        self.recursive = recursive
        self.text = text

    def get_container(self):
        cont_attrs = {}
        if self.container_class is not None:
            cont_attrs['class'] = self.container_class
        if self.container_id is not None:
            cont_attrs['id'] = self.container_id

        if self.first:
            wrappers = self.block.find(self.tag, attrs=cont_attrs, recursive=self.recursive, text=self.text)
        else:
            wrappers = self.block.find_all(self.tag, attrs=cont_attrs, recursive=self.recursive, text=self.text)
        return wrappers




def get_page_soup(url):
    results_page = requests.get(url)
    results = results_page.text
    soup = BeautifulSoup(results, 'html.parser')
    return soup

def get_soup(page):
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def get_text(block):
    return block.text

def get_previous_sibling(block, tag=None):
    if tag is not None:
        return block.find(tag).previous_sibling
    else:
        return block.previous_sibling

def get_next_sibling(block, tag=None):
    if tag is not None:
        return block.find(tag).next_sibling
    else:
        return block.next_sibling

def get_tag(block, tag_name):
    return getattr(block,tag_name)

def get_hrefs(block, filters=None):
    href_list = []
    for a in block.find_all('a', href=True, recursive=True):
        if filters is None or any(f in a.get('href') for f in filters):
            href_list.append(a.get('href').strip())
    return href_list




if __name__ == "__main__":
    pass
