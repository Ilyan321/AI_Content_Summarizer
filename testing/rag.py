from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv,find_dotenv


def fetch_Article(url):
    header={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response=requests.get(url, headers=header)
    soup=BeautifulSoup(response.text,"html.parser")
    paragraphs=soup.find_all("p")
    content=" ".join([p.get_text() for p in paragraphs])
    return content

def chunks(text,chunk_size=1000,overlap=100):
    print("Splitting text into chunks...")
    chunks=[]
    start=0
    while start<len(text):
        end=start+chunk_size
        chunk=text[start:end]
        chunks.append(chunk)
        start+=chunk_size-overlap
    print("Total chunks created: ",len(chunks))
    return chunks


def create_embeddings(my_chunks,api_key):
    print("Sending ",len(my_chunks),"chunks to AI for embedding...")
    API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
    api_key=os.getenv("Hugging_Face_API")
    headers={"Authorization":"Bearer "+str(api_key)}
    response=requests.post(API_URL,headers=headers,json={"inputs":my_chunks})

    if response.status_code==200:
        embedding=response.json()
        print("Successfully received embeddings for ",len(embedding),"chunks.")
        return embedding
    else:
        print("Error in embedding request: ",response.status_code, response.text)
        print(response.text)
        return []
    

if __name__=="__main__":
    load_dotenv(find_dotenv())

    url="https://en.wikipedia.org/wiki/Artificial_intelligence"
    text=fetch_Article(url)
    my_chunks=chunks(text)
    # print("1st chunk:",my_chunks[1])
    # print("2nd chunk:",my_chunks[2])
    # print("3rd chunk:",my_chunks[3])
    api_key=os.getenv("Hugging_Face_API")

    my_embeddings=create_embeddings(my_chunks,api_key)

    # To verify that it worked
    if len(my_embeddings)>0:
        print("\n-----Embedding Results-----")
        print("we recieved ",len(my_embeddings),"embeddings for ",len(my_chunks),"chunks.")
        print(my_embeddings[0][:5])
