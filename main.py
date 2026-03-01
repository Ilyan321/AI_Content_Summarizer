import streamlit as st
import requests
from bs4 import BeautifulSoup

def fetch_Article(url):
    try:
        header={"User-Agent":"Ilyan khan"}
        response=requests.get(url,headers=header)

        if response.status_code==404:
            print("404 error. Article does not exists.")
            return 
        
        response.raise_for_status()    # to check error

        soup=BeautifulSoup(response.text,"html.parser")
        paragraphs=soup.find_all('p')
        content=" ".join([p.get_text() for p in paragraphs])

        if not content.strip():
            print("Pages loaded but no paragraphs found")
            return
        
        return content,"Success"

    except Exception as e:
        print("Extracting Error")
            