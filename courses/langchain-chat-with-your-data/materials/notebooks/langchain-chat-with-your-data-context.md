# LangChain Chat with Your Data

---

## 01_document_loading/01_document_loading.ipynb

[markdown] cell 0

# Document Loading

[markdown] cell 1

## Note to students.
During periods of high load you may find the notebook unresponsive. It may appear to execute a cell, update the completion number in brackets [#] at the left of the cell but you may find the cell has not executed. This is particularly obvious on print statements when there is no output. If this happens, restart the kernel using the command under the Kernel tab.

[markdown] cell 2

## Retrieval augmented generation
 
In retrieval augmented generation (RAG), an LLM retrieves contextual documents from an external dataset as part of its execution. 

This is useful if we want to ask question about specific documents (e.g., our PDFs, a set of videos, etc). 

[markdown] cell 3

![overview.jpeg](attachment:overview.jpeg)

[code] cell 4

#! pip install langchain

[code] cell 5

import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

[markdown] cell 6

## PDFs

Let's load a PDF [transcript](https://see.stanford.edu/materials/aimlcs229/transcripts/MachineLearning-Lecture01.pdf) from Andrew Ng's famous CS229 course! These documents are the result of automated transcription so words and sentences are sometimes split unexpectedly.

[code] cell 7

# The course will show the pip installs you would need to install packages on your own machine.
# These packages are already installed on this platform and should not be run again.
#! pip install pypdf 

[code] cell 8

from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture01.pdf")
pages = loader.load()

[markdown] cell 9

Each page is a `Document`.

A `Document` contains text (`page_content`) and `metadata`.

[code] cell 10

len(pages)

[code] cell 11

page = pages[0]

[code] cell 12

print(page.page_content[0:500])

[code] cell 13

page.metadata

[markdown] cell 14

## YouTube

[code] cell 15

from langchain.document_loaders.generic import GenericLoader,  FileSystemBlobLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

[code] cell 16

# ! pip install yt_dlp
# ! pip install pydub

[markdown] cell 17

**Note**: This can take several minutes to complete. This has been modified relative to the lesson video to fetch the video file locally.

[code] cell 18

url="https://www.youtube.com/watch?v=jGwO_UgTS7I"
save_dir="docs/youtube/"
loader = GenericLoader(
    #YoutubeAudioLoader([url],save_dir),  # fetch from youtube
    FileSystemBlobLoader(save_dir, glob="*.m4a"),   #fetch locally
    OpenAIWhisperParser()
)
docs = loader.load()

[code] cell 19

docs[0].page_content[0:500]

[markdown] cell 20

## URLs

[code] cell 21

from langchain.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://github.com/basecamp/handbook/blob/master/titles-for-programmers.md")

[markdown] cell 22

> Note: the URL sent to the WebBaseLoader differs from the one shonw in the video because for 2024 it was updated.

[code] cell 23

docs = loader.load()

[code] cell 24

print(docs[0].page_content[:500])

[markdown] cell 25

## Notion

[markdown] cell 26

Follow steps [here](https://python.langchain.com/docs/modules/data_connection/document_loaders/integrations/notion) for an example Notion site such as [this one](https://yolospace.notion.site/Blendle-s-Employee-Handbook-e31bff7da17346ee99f531087d8b133f):

* Duplicate the page into your own Notion space and export as `Markdown / CSV`.
* Unzip it and save it as a folder that contains the markdown file for the Notion page.
 

[markdown] cell 27

![image.png](./img/image.png)

[code] cell 28

from langchain.document_loaders import NotionDirectoryLoader
loader = NotionDirectoryLoader("docs/Notion_DB")
docs = loader.load()

[code] cell 29

print(docs[0].page_content[0:200])

[code] cell 30

docs[0].metadata

[code] cell 31

(empty)

---

## 02_document_splitting/02_document_splitting.ipynb

[markdown] cell 0

# Document Splitting

[code] cell 1

import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

[code] cell 2

from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter

[code] cell 3

chunk_size =26
chunk_overlap = 4

[code] cell 4

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)
c_splitter = CharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

[markdown] cell 5

Why doesn't this split the string below?

[code] cell 6

text1 = 'abcdefghijklmnopqrstuvwxyz'

[code] cell 7

r_splitter.split_text(text1)

[code] cell 8

text2 = 'abcdefghijklmnopqrstuvwxyzabcdefg'

[code] cell 9

r_splitter.split_text(text2)

[markdown] cell 10

Ok, this splits the string but we have an overlap specified as 5, but it looks like 3? (try an even number)

[code] cell 11

text3 = "a b c d e f g h i j k l m n o p q r s t u v w x y z"

[code] cell 12

r_splitter.split_text(text3)

[code] cell 13

c_splitter.split_text(text3)

[code] cell 14

c_splitter = CharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separator = ' '
)
c_splitter.split_text(text3)

[markdown] cell 15

Try your own examples!

[markdown] cell 16

## Recursive splitting details

`RecursiveCharacterTextSplitter` is recommended for generic text. 

[code] cell 17

some_text = """When writing documents, writers will use document structure to group content. \
This can convey to the reader, which idea's are related. For example, closely related ideas \
are in sentances. Similar ideas are in paragraphs. Paragraphs form a document. \n\n  \
Paragraphs are often delimited with a carriage return or two carriage returns. \
Carriage returns are the "backslash n" you see embedded in this string. \
Sentences have a period at the end, but also, have a space.\
and words are separated by space."""

[code] cell 18

len(some_text)

[code] cell 19

c_splitter = CharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0,
    separator = ' '
)
r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=450,
    chunk_overlap=0, 
    separators=["\n\n", "\n", " ", ""]
)

[code] cell 20

c_splitter.split_text(some_text)

[code] cell 21

r_splitter.split_text(some_text)

[markdown] cell 22

Let's reduce the chunk size a bit and add a period to our separators:

[code] cell 23

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,
    separators=["\n\n", "\n", "\. ", " ", ""]
)
r_splitter.split_text(some_text)

[code] cell 24

r_splitter = RecursiveCharacterTextSplitter(
    chunk_size=150,
    chunk_overlap=0,
    separators=["\n\n", "\n", "(?<=\. )", " ", ""]
)
r_splitter.split_text(some_text)

[code] cell 25

from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture01.pdf")
pages = loader.load()

[code] cell 26

from langchain.text_splitter import CharacterTextSplitter
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=150,
    length_function=len
)

[code] cell 27

docs = text_splitter.split_documents(pages)

[code] cell 28

len(docs)

[code] cell 29

len(pages)

[code] cell 30

from langchain.document_loaders import NotionDirectoryLoader
loader = NotionDirectoryLoader("docs/Notion_DB")
notion_db = loader.load()

[code] cell 31

docs = text_splitter.split_documents(notion_db)

[code] cell 32

len(notion_db)

[code] cell 33

len(docs)

[markdown] cell 34

## Token splitting

We can also split on token count explicity, if we want.

This can be useful because LLMs often have context windows designated in tokens.

Tokens are often ~4 characters.

[code] cell 35

from langchain.text_splitter import TokenTextSplitter

[code] cell 36

text_splitter = TokenTextSplitter(chunk_size=1, chunk_overlap=0)

[code] cell 37

text1 = "foo bar bazzyfoo"

[code] cell 38

text_splitter.split_text(text1)

[code] cell 39

text_splitter = TokenTextSplitter(chunk_size=10, chunk_overlap=0)

[code] cell 40

docs = text_splitter.split_documents(pages)

[code] cell 41

docs[0]

[code] cell 42

pages[0].metadata

[markdown] cell 43

## Context aware splitting

Chunking aims to keep text with common context together.

A text splitting often uses sentences or other delimiters to keep related text together but many documents (such as Markdown) have structure (headers) that can be explicitly used in splitting.

We can use `MarkdownHeaderTextSplitter` to preserve header metadata in our chunks, as show below.

[code] cell 44

from langchain.document_loaders import NotionDirectoryLoader
from langchain.text_splitter import MarkdownHeaderTextSplitter

[code] cell 45

markdown_document = """# Title\n\n \
## Chapter 1\n\n \
Hi this is Jim\n\n Hi this is Joe\n\n \
### Section \n\n \
Hi this is Lance \n\n 
## Chapter 2\n\n \
Hi this is Molly"""

[code] cell 46

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

[code] cell 47

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)
md_header_splits = markdown_splitter.split_text(markdown_document)

[code] cell 48

md_header_splits[0]

[code] cell 49

md_header_splits[1]

[markdown] cell 50

Try on a real Markdown file, like a Notion database.

[code] cell 51

loader = NotionDirectoryLoader("docs/Notion_DB")
docs = loader.load()
txt = ' '.join([d.page_content for d in docs])

[code] cell 52

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on
)

[code] cell 53

md_header_splits = markdown_splitter.split_text(txt)

[code] cell 54

md_header_splits[0]

[code] cell 55

(empty)

---

## 03_vectorstores_and_embeddings/03_vectorstores_and_embeddings.ipynb

[markdown] cell 0

# Vectorstores and Embeddings

Recall the overall workflow for retrieval augmented generation (RAG):

[markdown] cell 1

![overview.jpeg](attachment:overview.jpeg)

[code] cell 2

import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

[markdown] cell 3

We just discussed `Document Loading` and `Splitting`.

[code] cell 4

from langchain.document_loaders import PyPDFLoader

# Load PDF
loaders = [
    # Duplicate documents on purpose - messy data
    PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture01.pdf"),
    PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture01.pdf"),
    PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture02.pdf"),
    PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture03.pdf")
]
docs = []
for loader in loaders:
    docs.extend(loader.load())

[code] cell 5

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)

[code] cell 6

splits = text_splitter.split_documents(docs)

[code] cell 7

len(splits)

[markdown] cell 8

## Embeddings

Let's take our splits and embed them.

[code] cell 9

from langchain.embeddings.openai import OpenAIEmbeddings
embedding = OpenAIEmbeddings()

[code] cell 10

sentence1 = "i like dogs"
sentence2 = "i like canines"
sentence3 = "the weather is ugly outside"

[code] cell 11

embedding1 = embedding.embed_query(sentence1)
embedding2 = embedding.embed_query(sentence2)
embedding3 = embedding.embed_query(sentence3)

[code] cell 12

import numpy as np

[code] cell 13

np.dot(embedding1, embedding2)

[code] cell 14

np.dot(embedding1, embedding3)

[code] cell 15

np.dot(embedding2, embedding3)

[markdown] cell 16

## Vectorstores

[code] cell 17

# ! pip install chromadb

[code] cell 18

from langchain.vectorstores import Chroma

[code] cell 19

persist_directory = 'docs/chroma/'

[code] cell 20

!rm -rf ./docs/chroma  # remove old database files if any

[code] cell 21

vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

[code] cell 22

print(vectordb._collection.count())

[markdown] cell 23

### Similarity Search

[code] cell 24

question = "is there an email i can ask for help"

[code] cell 25

docs = vectordb.similarity_search(question,k=3)

[code] cell 26

len(docs)

[code] cell 27

docs[0].page_content

[markdown] cell 28

Let's save this so we can use it later!

[code] cell 29

vectordb.persist()

[markdown] cell 30

## Failure modes

This seems great, and basic similarity search will get you 80% of the way there very easily. 

But there are some failure modes that can creep up. 

Here are some edge cases that can arise - we'll fix them in the next class.

[code] cell 31

question = "what did they say about matlab?"

[code] cell 32

docs = vectordb.similarity_search(question,k=5)

[markdown] cell 33

Notice that we're getting duplicate chunks (because of the duplicate `MachineLearning-Lecture01.pdf` in the index).

Semantic search fetches all similar documents, but does not enforce diversity.

`docs[0]` and `docs[1]` are indentical.

[code] cell 34

docs[0]

[code] cell 35

docs[1]

[markdown] cell 36

We can see a new failure mode.

The question below asks a question about the third lecture, but includes results from other lectures as well.

[code] cell 37

question = "what did they say about regression in the third lecture?"

[code] cell 38

docs = vectordb.similarity_search(question,k=5)

[code] cell 39

for doc in docs:
    print(doc.metadata)

[code] cell 40

print(docs[4].page_content)

[markdown] cell 41

Approaches discussed in the next lecture can be used to address both!

[code] cell 42

(empty)

---

## 04_retrieval/04_retrieval.ipynb

[markdown] cell 0

# Retrieval

Retrieval is the centerpiece of our retrieval augmented generation (RAG) flow. 

Let's get our vectorDB from before.

[markdown] cell 1

## Vectorstore retrieval


[code] cell 2

import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

[code] cell 3

#!pip install lark

[markdown] cell 4

### Similarity Search

[code] cell 5

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
persist_directory = 'docs/chroma/'

[code] cell 6

embedding = OpenAIEmbeddings()
vectordb = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding
)

[code] cell 7

print(vectordb._collection.count())

[code] cell 8

texts = [
    """The Amanita phalloides has a large and imposing epigeous (aboveground) fruiting body (basidiocarp).""",
    """A mushroom with a large fruiting body is the Amanita phalloides. Some varieties are all-white.""",
    """A. phalloides, a.k.a Death Cap, is one of the most poisonous of all known mushrooms.""",
]

[code] cell 9

smalldb = Chroma.from_texts(texts, embedding=embedding)

[code] cell 10

question = "Tell me about all-white mushrooms with large fruiting bodies"

[code] cell 11

smalldb.similarity_search(question, k=2)

[code] cell 12

smalldb.max_marginal_relevance_search(question,k=2, fetch_k=3)

[markdown] cell 13

### Addressing Diversity: Maximum marginal relevance

Last class we introduced one problem: how to enforce diversity in the search results.
 
`Maximum marginal relevance` strives to achieve both relevance to the query *and diversity* among the results.

[code] cell 14

question = "what did they say about matlab?"
docs_ss = vectordb.similarity_search(question,k=3)

[code] cell 15

docs_ss[0].page_content[:100]

[code] cell 16

docs_ss[1].page_content[:100]

[markdown] cell 17

Note the difference in results with `MMR`.

[code] cell 18

docs_mmr = vectordb.max_marginal_relevance_search(question,k=3)

[code] cell 19

docs_mmr[0].page_content[:100]

[code] cell 20

docs_mmr[1].page_content[:100]

[markdown] cell 21

### Addressing Specificity: working with metadata

In last lecture, we showed that a question about the third lecture can include results from other lectures as well.

To address this, many vectorstores support operations on `metadata`.

`metadata` provides context for each embedded chunk.

[code] cell 22

question = "what did they say about regression in the third lecture?"

[code] cell 23

docs = vectordb.similarity_search(
    question,
    k=3,
    filter={"source":"docs/cs229_lectures/MachineLearning-Lecture03.pdf"}
)

[code] cell 24

for d in docs:
    print(d.metadata)

[code] cell 25

(empty)

[markdown] cell 26

### Addressing Specificity: working with metadata using self-query retriever

But we have an interesting challenge: we often want to infer the metadata from the query itself.

To address this, we can use `SelfQueryRetriever`, which uses an LLM to extract:
 
1. The `query` string to use for vector search
2. A metadata filter to pass in as well

Most vector databases support metadata filters, so this doesn't require any new databases or indexes.

[code] cell 27

from langchain.llms import OpenAI
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

[code] cell 28

metadata_field_info = [
    AttributeInfo(
        name="source",
        description="The lecture the chunk is from, should be one of `docs/cs229_lectures/MachineLearning-Lecture01.pdf`, `docs/cs229_lectures/MachineLearning-Lecture02.pdf`, or `docs/cs229_lectures/MachineLearning-Lecture03.pdf`",
        type="string",
    ),
    AttributeInfo(
        name="page",
        description="The page from the lecture",
        type="integer",
    ),
]

[markdown] cell 29

**Note:** The default model for `OpenAI` ("from langchain.llms import OpenAI") is `text-davinci-003`. Due to the deprication of OpenAI's model `text-davinci-003` on 4 January 2024, you'll be using OpenAI's recommended replacement model `gpt-3.5-turbo-instruct` instead.

[code] cell 30

document_content_description = "Lecture notes"
llm = OpenAI(model='gpt-3.5-turbo-instruct', temperature=0)
retriever = SelfQueryRetriever.from_llm(
    llm,
    vectordb,
    document_content_description,
    metadata_field_info,
    verbose=True
)

[code] cell 31

question = "what did they say about regression in the third lecture?"

[markdown] cell 32

**You will receive a warning** about predict_and_parse being deprecated the first time you executing the next line. This can be safely ignored.

[code] cell 33

docs = retriever.get_relevant_documents(question)

[code] cell 34

for d in docs:
    print(d.metadata)

[markdown] cell 35

### Additional tricks: compression

Another approach for improving the quality of retrieved docs is compression.

Information most relevant to a query may be buried in a document with a lot of irrelevant text. 

Passing that full document through your application can lead to more expensive LLM calls and poorer responses.

Contextual compression is meant to fix this. 

[code] cell 36

from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

[code] cell 37

def pretty_print_docs(docs):
    print(f"\n{'-' * 100}\n".join([f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]))


[code] cell 38

# Wrap our vectorstore
llm = OpenAI(temperature=0, model="gpt-3.5-turbo-instruct")
compressor = LLMChainExtractor.from_llm(llm)

[code] cell 39

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectordb.as_retriever()
)

[code] cell 40

question = "what did they say about matlab?"
compressed_docs = compression_retriever.get_relevant_documents(question)
pretty_print_docs(compressed_docs)

[markdown] cell 41

## Combining various techniques

[code] cell 42

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectordb.as_retriever(search_type = "mmr")
)

[code] cell 43

question = "what did they say about matlab?"
compressed_docs = compression_retriever.get_relevant_documents(question)
pretty_print_docs(compressed_docs)

[markdown] cell 44

## Other types of retrieval

It's worth noting that vectordb as not the only kind of tool to retrieve documents. 

The `LangChain` retriever abstraction includes other ways to retrieve documents, such as TF-IDF or SVM.

[code] cell 45

from langchain.retrievers import SVMRetriever
from langchain.retrievers import TFIDFRetriever
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

[code] cell 46

# Load PDF
loader = PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture01.pdf")
pages = loader.load()
all_page_text=[p.page_content for p in pages]
joined_page_text=" ".join(all_page_text)

# Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1500,chunk_overlap = 150)
splits = text_splitter.split_text(joined_page_text)


[code] cell 47

# Retrieve
svm_retriever = SVMRetriever.from_texts(splits,embedding)
tfidf_retriever = TFIDFRetriever.from_texts(splits)

[code] cell 48

question = "What are major topics for this class?"
docs_svm=svm_retriever.get_relevant_documents(question)
docs_svm[0]

[code] cell 49

question = "what did they say about matlab?"
docs_tfidf=tfidf_retriever.get_relevant_documents(question)
docs_tfidf[0]

[code] cell 50

(empty)

---

## 05_question_answering/05_question_answering.ipynb

[markdown] cell 0

# Question Answering

[markdown] cell 1

## Overview

Recall the overall workflow for retrieval augmented generation (RAG):

[markdown] cell 2

![overview.jpeg](attachment:overview.jpeg)

[markdown] cell 3

We discussed `Document Loading` and `Splitting` as well as `Storage` and `Retrieval`.

Let's load our vectorDB. 

[code] cell 4

import os
import openai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

[markdown] cell 5

The code below was added to assign the openai LLM version filmed until it is deprecated, currently in Sept 2023. 
LLM responses can often vary, but the responses may be significantly different when using a different model version.

[code] cell 6

import datetime
current_date = datetime.datetime.now().date()
if current_date < datetime.date(2023, 9, 2):
    llm_name = "gpt-3.5-turbo-0301"
else:
    llm_name = "gpt-3.5-turbo"
print(llm_name)

[code] cell 7

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

[code] cell 8

print(vectordb._collection.count())

[code] cell 9

question = "What are major topics for this class?"
docs = vectordb.similarity_search(question,k=3)
len(docs)

[code] cell 10

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name=llm_name, temperature=0)

[markdown] cell 11

### RetrievalQA chain

[code] cell 12

from langchain.chains import RetrievalQA

[code] cell 13

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever()
)

[code] cell 14

result = qa_chain({"query": question})

[code] cell 15

result["result"]

[markdown] cell 16

### Prompt

[code] cell 17

from langchain.prompts import PromptTemplate

# Build prompt
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)


[code] cell 18

# Run chain
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

[code] cell 19

question = "Is probability a class topic?"

[code] cell 20

result = qa_chain({"query": question})

[code] cell 21

result["result"]

[code] cell 22

result["source_documents"][0]

[markdown] cell 23

### RetrievalQA chain types

[code] cell 24

qa_chain_mr = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    chain_type="map_reduce"
)

[code] cell 25

result = qa_chain_mr({"query": question})

[code] cell 26

result["result"]

[markdown] cell 27

If you wish to experiment on the `LangSmith platform` (previously known as LangChain Plus):

 * Go to [LangSmith](https://www.langchain.com/langsmith) and sign up
 * Create an API key from your account's settings
 * Use this API key in the code below   
 * uncomment the code  
 Note, the endpoint in the video differs from the one below. Use the one below.

[code] cell 28

#import os
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
#os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
#os.environ["LANGCHAIN_API_KEY"] = "..." # replace dots with your api key

[code] cell 29

qa_chain_mr = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    chain_type="map_reduce"
)
result = qa_chain_mr({"query": question})
result["result"]

[code] cell 30

qa_chain_mr = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever(),
    chain_type="refine"
)
result = qa_chain_mr({"query": question})
result["result"]

[markdown] cell 31

### RetrievalQA limitations
 
QA fails to preserve conversational history.

[code] cell 32

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectordb.as_retriever()
)

[code] cell 33

question = "Is probability a class topic?"
result = qa_chain({"query": question})
result["result"]

[code] cell 34

question = "why are those prerequesites needed?"
result = qa_chain({"query": question})
result["result"]

[markdown] cell 35

Note, The LLM response varies. Some responses **do** include a reference to probability which might be gleaned from referenced documents. The point is simply that the model does not have access to past questions or answers, this will be covered in the next section.

[code] cell 36

(empty)

---

## 06_chat/06_chat.ipynb

[markdown] cell 0

# Chat

Recall the overall workflow for retrieval augmented generation (RAG):

[markdown] cell 1

![overview.jpeg](attachment:overview.jpeg)

[markdown] cell 2

We discussed `Document Loading` and `Splitting` as well as `Storage` and `Retrieval`.

We then showed how `Retrieval` can be used for output generation in Q+A using `RetrievalQA` chain.

[code] cell 3

import os
import openai
import sys
sys.path.append('../..')

import panel as pn  # GUI
pn.extension()

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key  = os.environ['OPENAI_API_KEY']

[markdown] cell 4

The code below was added to assign the openai LLM version filmed until it is deprecated, currently in Sept 2023. 
LLM responses can often vary, but the responses may be significantly different when using a different model version.

[code] cell 5

import datetime
current_date = datetime.datetime.now().date()
if current_date < datetime.date(2023, 9, 2):
    llm_name = "gpt-3.5-turbo-0301"
else:
    llm_name = "gpt-3.5-turbo"
print(llm_name)

[markdown] cell 6

 If you wish to experiment on the `LangSmith platform` (previously known as LangChain Plus):

 * Go to [LangSmith](https://www.langchain.com/langsmith) and sign up
 * Create an api key from your account's settings
 * Use this api key in the code below 

[code] cell 7

#import os
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
#os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
#os.environ["LANGCHAIN_API_KEY"] = "..."

[code] cell 8

from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

[code] cell 9

question = "What are major topics for this class?"
docs = vectordb.similarity_search(question,k=3)
len(docs)

[code] cell 10

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(model_name=llm_name, temperature=0)
llm.predict("Hello world!")

[code] cell 11

# Build prompt
from langchain.prompts import PromptTemplate
template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template,)

# Run chain
from langchain.chains import RetrievalQA
question = "Is probability a class topic?"
qa_chain = RetrievalQA.from_chain_type(llm,
                                       retriever=vectordb.as_retriever(),
                                       return_source_documents=True,
                                       chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})


result = qa_chain({"query": question})
result["result"]

[markdown] cell 12

### Memory

[code] cell 13

from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

[markdown] cell 14

### ConversationalRetrievalChain

[code] cell 15

from langchain.chains import ConversationalRetrievalChain
retriever=vectordb.as_retriever()
qa = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory
)

[code] cell 16

question = "Is probability a class topic?"
result = qa({"question": question})

[code] cell 17

result['answer']

[code] cell 18

question = "why are those prerequesites needed?"
result = qa({"question": question})

[code] cell 19

result['answer']

[markdown] cell 20

# Create a chatbot that works on your documents

[code] cell 21

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA,  ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader

[markdown] cell 22

The chatbot code has been updated a bit since filming. The GUI appearance also varies depending on the platform it is running on.

[code] cell 23

def load_db(file, chain_type, k):
    # load documents
    loader = PyPDFLoader(file)
    documents = loader.load()
    # split documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    # define embedding
    embeddings = OpenAIEmbeddings()
    # create vector database from data
    db = DocArrayInMemorySearch.from_documents(docs, embeddings)
    # define retriever
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    # create a chatbot chain. Memory is managed externally.
    qa = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model_name=llm_name, temperature=0), 
        chain_type=chain_type, 
        retriever=retriever, 
        return_source_documents=True,
        return_generated_question=True,
    )
    return qa 


[code] cell 24

import panel as pn
import param

class cbfs(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query  = param.String("")
    db_response = param.List([])
    
    def __init__(self,  **params):
        super(cbfs, self).__init__( **params)
        self.panels = []
        self.loaded_file = "docs/cs229_lectures/MachineLearning-Lecture01.pdf"
        self.qa = load_db(self.loaded_file,"stuff", 4)
    
    def call_load_db(self, count):
        if count == 0 or file_input.value is None:  # init or no file specified :
            return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")
        else:
            file_input.save("temp.pdf")  # local copy
            self.loaded_file = file_input.filename
            button_load.button_style="outline"
            self.qa = load_db("temp.pdf", "stuff", 4)
            button_load.button_style="solid"
        self.clr_history()
        return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")

    def convchain(self, query):
        if not query:
            return pn.WidgetBox(pn.Row('User:', pn.pane.Markdown("", width=600)), scroll=True)
        result = self.qa({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer'] 
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query, width=600)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer, width=600, style={'background-color': '#F6F6F6'}))
        ])
        inp.value = ''  #clears loading indicator when cleared
        return pn.WidgetBox(*self.panels,scroll=True)

    @param.depends('db_query ', )
    def get_lquest(self):
        if not self.db_query :
            return pn.Column(
                pn.Row(pn.pane.Markdown(f"Last question to DB:", styles={'background-color': '#F6F6F6'})),
                pn.Row(pn.pane.Str("no DB accesses so far"))
            )
        return pn.Column(
            pn.Row(pn.pane.Markdown(f"DB query:", styles={'background-color': '#F6F6F6'})),
            pn.pane.Str(self.db_query )
        )

    @param.depends('db_response', )
    def get_sources(self):
        if not self.db_response:
            return 
        rlist=[pn.Row(pn.pane.Markdown(f"Result of DB lookup:", styles={'background-color': '#F6F6F6'}))]
        for doc in self.db_response:
            rlist.append(pn.Row(pn.pane.Str(doc)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    @param.depends('convchain', 'clr_history') 
    def get_chats(self):
        if not self.chat_history:
            return pn.WidgetBox(pn.Row(pn.pane.Str("No History Yet")), width=600, scroll=True)
        rlist=[pn.Row(pn.pane.Markdown(f"Current Chat History variable", styles={'background-color': '#F6F6F6'}))]
        for exchange in self.chat_history:
            rlist.append(pn.Row(pn.pane.Str(exchange)))
        return pn.WidgetBox(*rlist, width=600, scroll=True)

    def clr_history(self,count=0):
        self.chat_history = []
        return 


[markdown] cell 25

### Create a chatbot

[code] cell 26

cb = cbfs()

file_input = pn.widgets.FileInput(accept='.pdf')
button_load = pn.widgets.Button(name="Load DB", button_type='primary')
button_clearhistory = pn.widgets.Button(name="Clear History", button_type='warning')
button_clearhistory.on_click(cb.clr_history)
inp = pn.widgets.TextInput( placeholder='Enter text here…')

bound_button_load = pn.bind(cb.call_load_db, button_load.param.clicks)
conversation = pn.bind(cb.convchain, inp) 

jpg_pane = pn.pane.Image( './img/convchain.jpg')

tab1 = pn.Column(
    pn.Row(inp),
    pn.layout.Divider(),
    pn.panel(conversation,  loading_indicator=True, height=300),
    pn.layout.Divider(),
)
tab2= pn.Column(
    pn.panel(cb.get_lquest),
    pn.layout.Divider(),
    pn.panel(cb.get_sources ),
)
tab3= pn.Column(
    pn.panel(cb.get_chats),
    pn.layout.Divider(),
)
tab4=pn.Column(
    pn.Row( file_input, button_load, bound_button_load),
    pn.Row( button_clearhistory, pn.pane.Markdown("Clears chat history. Can use to start a new topic" )),
    pn.layout.Divider(),
    pn.Row(jpg_pane.clone(width=400))
)
dashboard = pn.Column(
    pn.Row(pn.pane.Markdown('# ChatWithYourData_Bot')),
    pn.Tabs(('Conversation', tab1), ('Database', tab2), ('Chat History', tab3),('Configure', tab4))
)
dashboard

[markdown] cell 27

Feel free to copy this code and modify it to add your own features. You can try alternate memory and retriever models by changing the configuration in `load_db` function and the `convchain` method. [Panel](https://panel.holoviz.org/) and [Param](https://param.holoviz.org/) have many useful features and widgets you can use to extend the GUI.


[markdown] cell 28

## Acknowledgments

Panel based chatbot inspired by Sophia Yang, [github](https://github.com/sophiamyang/tutorials-LangChain)
