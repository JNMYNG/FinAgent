from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os


load_dotenv()


# 금융 문서 읽기
with open(
    "data/finance.txt",
    "r",
    encoding="utf-8"
) as f:
    text = f.read()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=30
)

documents = splitter.create_documents(
    [text]
)


# Embedding 모델
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


# Vector DB 생성
vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="finance"
)


# 검색 함수
def search_finance(query):

    results = vectorstore.similarity_search(
        query,
        k=1
    )

    return results[0].page_content


if __name__ == "__main__":

    result = search_finance(
        "적금이 뭐야?"
    )

    print(result)