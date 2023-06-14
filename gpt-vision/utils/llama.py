import os
import pathlib
from llama_index import download_loader, GPTSimpleVectorIndex
# from pdf-loader.base import PDFReader

def query_docx(query , file):
    DocxReader = download_loader("DocxReader")
    loader = DocxReader()
    documents = loader.load_data(file=file)
    index = GPTSimpleVectorIndex.from_documents(documents=documents)
    print("response")
    response= index.query(query)
    print(response.response)
    return response.response


def query_pdf(query , file):
    PDFReader = download_loader("PDFReader")
    docx_data = pathlib.Path('temp.pdf') .write_bytes(file.getbuffer() .tobytes())
    loader = PDFReader()
    documents = loader.load_data(file=pathlib.Path('./temp.pdf'))
    index = GPTSimpleVectorIndex.from_documents(documents=documents)
    print("response")
    response= index.query(query)
    print(response.response)
    return response.response