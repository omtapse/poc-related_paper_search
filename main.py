import requests
import pdfplumber
from croma import ChromaClient

backendUrl = "http://localhost:3001/blogms/api/v1"
paperId = "arx/arx/2402.19473"
embeddingURl = "http://localhost:8000/embed"

def get_paper_data(id:str):
    url = backendUrl + "/research-paper/" + id
    response = requests.get(url)
    return response.json()

def get_all_related_papers(id:str):
    url = backendUrl + "/research-paper/" + id + "/related-papers"
    response = requests.get(url)
    return response.json()

def break_text_into_chunks(text):
    words = text.split()
    chunk_size = 200
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

def get_pdf_text(url):
    # Download the PDF file from the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Open the PDF file from the response content
        with open('temp_pdf.pdf', 'wb') as f:
            f.write(response.content)
        
        # Read the PDF file and extract text
        pdf_text = ''
        with pdfplumber.open('temp_pdf.pdf') as pdf:
            for page in pdf.pages:
                pdf_text += page.extract_text()
        
        # Remove temporary PDF file
        import os
        os.remove('temp_pdf.pdf')

        return pdf_text
    else:
        print("Failed to download PDF:", response.status_code)
        return None

def getEmbedding(text):
    url = "http://localhost:8000/embed"
    embeddings = requests.post(url, json={"text": text})
    embedding = embeddings.json()
    return embedding["embedding"]

def get_paper_references(paperId):
    limit = 100
    offset = 0
    # references = []
    # while True:
    url = backendUrl + '/research-paper/related/'+ paperId + '?offset=0&type=references&limit=5'
    response = requests.get(url)
    json = response.json()
    return json

    


def process_pdf_by_URL(url,paperData,lv=1):
    if(url is None):
        return
    pdfText = get_pdf_text(url)
    chunks = break_text_into_chunks(pdfText)

    text=[]
    metadata=[] 
    ids=[]
    for index, chunk in enumerate(chunks):
        meta = {
                "paperId": paperData["externalId"],
                "url":paperData["urlPdf"],
                "title": paperData["title"],
        }
        text.append(chunk)
        metadata.append(meta)
        ids.append(f"{paperData['externalId']} {index + 1}")

    c = ChromaClient()
    collection = c.get_collection("test")

    c.add_data_to_collection("test", ids, text, metadata)
    print("Added data to collection",lv, paperData["externalId"])
    return ids


def main():
    # paperData = get_paper_data(paperId)
    # process_pdf_by_URL(paperData["urlPdf"],paperData)
    # references = get_paper_references(paperId)
    # print(len(references))
    # for reference in references:
    #     if reference.keys().__contains__("urlPdf"):
    #         process_pdf_by_URL(reference["urlPdf"],reference,2)

    c = ChromaClient()
    query ="What is LESS"
    results = c.get_data(query,"test")
    print(results)
main()


