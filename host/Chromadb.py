from llm import llm_davinci
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
import os
import uuid
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.document_loaders import UnstructuredPowerPointLoader
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings

"""
### delete the db
!zip -r db.zip ./db  #store in the zip file, can be extract later
# To cleanup, you can delete the collection
vectordb.delete_collection()
vectordb.persist()

# delete the directory
!rm -rf db/

### reload the db
!unzip db.zip
persist_directory = 'db'
embedding = instructor_embeddings

vectordb2 = Chroma(persist_directory=persist_directory, 
                  embedding_function=embedding,
                   )

retriever = vectordb2.as_retriever(search_kwargs={"k": 2})
"""


"""
DB class

1) can be initialized with a persist_directory
2) should allow people to upload the file to the db
    i)the user maybe upload differebt types of file, like pdf, docx, pptx, csv, txt
    ii) use different loader for different file type
    iii) use different splitter for different file type (if necessary)
    iv) embedding the file with the embedding key, function?
    v) store the embedding in the db, at the same time store the id of the file
3) should allow people to delete the file from the db
    i) delete the file from the db by the id or the name of the file
4) should allow people to review differents file from the db
    i) review the file by the id and the name of the file by a list
5) should allow people to search the file from the db
    i) use the retriever in langchain to search through the whole db, different files by a prompt
"""


class DB:
    def __init__(self, persist_directory):
        # Create persist directory
        self.persist_directory = persist_directory
        os.makedirs(self.persist_directory, exist_ok=True)

        self.embedding = HuggingFaceInstructEmbeddings(
            model_name="hkunlp/instructor-xl", model_kwargs={"device": "cuda"})
        self.db = Chroma(persist_directory=self.persist_directory,
                         embedding_function=self.embedding)

        # Create QA chain
        self.llm = llm_davinci  # should be change here later
        self.retriever = self.db.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm, chain_type="stuff", retriever=self.retriever, return_source_documents=True)
        self.doc_id_map = {}

    def upload(self, file_path):
        file_type = file_path.split('.')[-1]
        if file_type == "txt":
            loader = TextLoader(file_path)
        elif file_type == "pdf":
            loader = PyPDFLoader(file_path)
        elif file_type == "docx":
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_type == "csv":
            loader = CSVLoader(file_path)
        elif file_type == "pptx":
            loader = UnstructuredPowerPointLoader(file_path)
        elif file_path == 'xlsx':
            loader = UnstructuredExcelLoader(file_path)
        else:
            return "File type not supported"
        # may be more here later
        parent_id = str(uuid.uuid4())
        # child_ids = []

        for doc in loader.load():
            child_ids = self.db.add_documents([doc])
            doc.metadata["id"] = child_ids

            self.doc_id_map[parent_id] = {
                "ids": child_ids,
                "filename": os.path.basename(file_path)
            }
        return {"message": "File uploaded successfully"}

    def delete(self, id):
        if id in self.doc_id_map:
            info = self.doc_id_map[id]
            child_ids = info["ids"]
        else:
            child_ids = [id]

        del self.doc_id_map[id]
        self.db.delete(child_ids)

    def search(self, query):
        result = self.qa_chain(query)
        response = "Answer: " + result["result"] + "\nSources:"
        # for source in result["source_documents"]:
        #     response += "\n"+source.metadata["source"]
        response += "\n"+str(result["source_documents"][0].metadata["source"])
        return response

    def list_documents(self):
        out = ""
        for parent_id, info in self.doc_id_map.items():
            out += f"File name: {info['filename']}, id: {parent_id}\n"
        return out
