# Langchain

---

## Lesson Map

- works/L1-Model_prompt_parser/L1-Model_prompt_parser.ipynb → Lesson 1: LangChain: Models, Prompts and Output Parsers
- works/L2-Memory/L2-Memory.ipynb → Lesson 2: LangChain: Memory
- works/L3-Chains/L3-Chains.ipynb → Lesson 3: Chains in LangChain
- works/L4-QnA/L4-QnA.ipynb → Lesson 4: LangChain: Q&A over Documents
- works/L5-Evaluation/L5-Evaluation.ipynb → Lesson 5: LangChain: Evaluation
- works/L6-Agents/L6-Agents.ipynb → Lesson 6: LangChain: Agents

> Generated from `https://github.com/deeplearningai-eng/courses` (subdirectory `course_6`) @ main by ingest_repo.py. Lesson numbers are inferred from notebook order and are a convenience label only — the transcripts under materials/transcripts/ are authoritative for lesson numbering and titles.

---

## Lesson 1: LangChain: Models, Prompts and Output Parsers — works/L1-Model_prompt_parser/L1-Model_prompt_parser.ipynb

[markdown] cell 0

# LangChain: Models, Prompts and Output Parsers


## Outline

 * Direct API calls to OpenAI
 * API calls through LangChain:
   * Prompts
   * Models
   * Output parsers

[markdown] cell 1

## Get your [OpenAI API Key](https://platform.openai.com/account/api-keys)

[code] cell 2

#!pip install python-dotenv
#!pip install openai

[code] cell 3

import os
import openai

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

[markdown] cell 4

Note: LLM's do not always produce the same results. When executing the code in your notebook, you may get slightly different answers that those in the video.

[code] cell 5

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

[markdown] cell 6

## Chat API : OpenAI

Let's start with a direct API calls to OpenAI.

[code] cell 7

def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]

[code] cell 8

get_completion("What is 1+1?")

[code] cell 9

customer_email = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse,\
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!
"""

[code] cell 10

style = """American English \
in a calm and respectful tone
"""

[code] cell 11

prompt = f"""Translate the text \
that is delimited by triple backticks 
into a style that is {style}.
text: ```{customer_email}```
"""

print(prompt)

[code] cell 12

response = get_completion(prompt)

[code] cell 13

response

[markdown] cell 14

## Chat API : LangChain

Let's try how we can do the same using LangChain.

[code] cell 15

#!pip install --upgrade langchain

[markdown] cell 16

### Model

[code] cell 17

from langchain.chat_models import ChatOpenAI

[code] cell 18

# To control the randomness and creativity of the generated
# text by an LLM, use temperature = 0.0
chat = ChatOpenAI(temperature=0.0, model=llm_model)
chat

[markdown] cell 19

### Prompt template

[code] cell 20

template_string = """Translate the text \
that is delimited by triple backticks \
into a style that is {style}. \
text: ```{text}```
"""

[code] cell 21

from langchain.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_template(template_string)

[code] cell 22

prompt_template.messages[0].prompt

[code] cell 23

prompt_template.messages[0].prompt.input_variables

[code] cell 24

customer_style = """American English \
in a calm and respectful tone
"""

[code] cell 25

customer_email = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse, \
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey!
"""

[code] cell 26

customer_messages = prompt_template.format_messages(
                    style=customer_style,
                    text=customer_email)

[code] cell 27

print(type(customer_messages))
print(type(customer_messages[0]))

[code] cell 28

print(customer_messages[0])

[code] cell 29

# Call the LLM to translate to the style of the customer message
customer_response = chat(customer_messages)

[code] cell 30

print(customer_response.content)

[code] cell 31

service_reply = """Hey there customer, \
the warranty does not cover \
cleaning expenses for your kitchen \
because it's your fault that \
you misused your blender \
by forgetting to put the lid on before \
starting the blender. \
Tough luck! See ya!
"""

[code] cell 32

service_style_pirate = """\
a polite tone \
that speaks in English Pirate\
"""

[code] cell 33

service_messages = prompt_template.format_messages(
    style=service_style_pirate,
    text=service_reply)

print(service_messages[0].content)

[code] cell 34

service_response = chat(service_messages)
print(service_response.content)

[markdown] cell 35

## Output Parsers

Let's start with defining how we would like the LLM output to look like:

[code] cell 36

{
  "gift": False,
  "delivery_days": 5,
  "price_value": "pretty affordable!"
}

[code] cell 37

customer_review = """\
This leaf blower is pretty amazing.  It has four settings:\
candle blower, gentle breeze, windy city, and tornado. \
It arrived in two days, just in time for my wife's \
anniversary present. \
I think my wife liked it so much she was speechless. \
So far I've been the only one using it, and I've been \
using it every other morning to clear the leaves on our lawn. \
It's slightly more expensive than the other leaf blowers \
out there, but I think it's worth it for the extra features.
"""

review_template = """\
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

Format the output as JSON with the following keys:
gift
delivery_days
price_value

text: {text}
"""

[code] cell 38

from langchain.prompts import ChatPromptTemplate

prompt_template = ChatPromptTemplate.from_template(review_template)
print(prompt_template)

[code] cell 39

messages = prompt_template.format_messages(text=customer_review)
chat = ChatOpenAI(temperature=0.0, model=llm_model)
response = chat(messages)
print(response.content)

[code] cell 40

type(response.content)

[code] cell 41

# You will get an error by running this line of code 
# because'gift' is not a dictionary
# 'gift' is a string
response.content.get('gift')

[markdown] cell 42

### Parse the LLM output string into a Python dictionary

[code] cell 43

from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser

[code] cell 44

gift_schema = ResponseSchema(name="gift",
                             description="Was the item purchased\
                             as a gift for someone else? \
                             Answer True if yes,\
                             False if not or unknown.")
delivery_days_schema = ResponseSchema(name="delivery_days",
                                      description="How many days\
                                      did it take for the product\
                                      to arrive? If this \
                                      information is not found,\
                                      output -1.")
price_value_schema = ResponseSchema(name="price_value",
                                    description="Extract any\
                                    sentences about the value or \
                                    price, and output them as a \
                                    comma separated Python list.")

response_schemas = [gift_schema, 
                    delivery_days_schema,
                    price_value_schema]

[code] cell 45

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

[code] cell 46

format_instructions = output_parser.get_format_instructions()

[code] cell 47

print(format_instructions)

[code] cell 48

review_template_2 = """\
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product\
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list.

text: {text}

{format_instructions}
"""

prompt = ChatPromptTemplate.from_template(template=review_template_2)

messages = prompt.format_messages(text=customer_review, 
                                format_instructions=format_instructions)

[code] cell 49

print(messages[0].content)

[code] cell 50

response = chat(messages)

[code] cell 51

print(response.content)

[code] cell 52

output_dict = output_parser.parse(response.content)

[code] cell 53

output_dict

[code] cell 54

type(output_dict)

[code] cell 55

output_dict.get('delivery_days')

[markdown] cell 56

Reminder: Download your notebook to you local computer to save your work.

---

## Lesson 2: LangChain: Memory — works/L2-Memory/L2-Memory.ipynb

[markdown] cell 0

# LangChain: Memory

## Outline
* ConversationBufferMemory
* ConversationBufferWindowMemory
* ConversationTokenBufferMemory
* ConversationSummaryMemory

[markdown] cell 1

## ConversationBufferMemory

[code] cell 2

import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import warnings
warnings.filterwarnings('ignore')

[markdown] cell 3

Note: LLM's do not always produce the same results. When executing the code in your notebook, you may get slightly different answers that those in the video.

[code] cell 4

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

[code] cell 5

from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

[code] cell 6

llm = ChatOpenAI(temperature=0.0, model=llm_model)
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)

[code] cell 7

conversation.predict(input="Hi, my name is Andrew")

[code] cell 8

conversation.predict(input="What is 1+1?")

[code] cell 9

conversation.predict(input="What is my name?")

[code] cell 10

print(memory.buffer)

[code] cell 11

memory.load_memory_variables({})

[code] cell 12

memory = ConversationBufferMemory()

[code] cell 13

memory.save_context({"input": "Hi"}, 
                    {"output": "What's up"})

[code] cell 14

print(memory.buffer)

[code] cell 15

memory.load_memory_variables({})

[code] cell 16

memory.save_context({"input": "Not much, just hanging"}, 
                    {"output": "Cool"})

[code] cell 17

memory.load_memory_variables({})

[markdown] cell 18

## ConversationBufferWindowMemory

[code] cell 19

from langchain.memory import ConversationBufferWindowMemory

[code] cell 20

memory = ConversationBufferWindowMemory(k=1)               

[code] cell 21

memory.save_context({"input": "Hi"},
                    {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})

[code] cell 22

memory.load_memory_variables({})

[code] cell 23

llm = ChatOpenAI(temperature=0.0, model=llm_model)
memory = ConversationBufferWindowMemory(k=1)
conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=False
)

[code] cell 24

conversation.predict(input="Hi, my name is Andrew")

[code] cell 25

conversation.predict(input="What is 1+1?")

[code] cell 26

conversation.predict(input="What is my name?")

[markdown] cell 27

## ConversationTokenBufferMemory

[code] cell 28

#!pip install tiktoken

[code] cell 29

from langchain.memory import ConversationTokenBufferMemory
from langchain.llms import OpenAI
llm = ChatOpenAI(temperature=0.0, model=llm_model)

[code] cell 30

memory = ConversationTokenBufferMemory(llm=llm, max_token_limit=50)
memory.save_context({"input": "AI is what?!"},
                    {"output": "Amazing!"})
memory.save_context({"input": "Backpropagation is what?"},
                    {"output": "Beautiful!"})
memory.save_context({"input": "Chatbots are what?"}, 
                    {"output": "Charming!"})

[code] cell 31

memory.load_memory_variables({})

[markdown] cell 32

## ConversationSummaryMemory

[code] cell 33

from langchain.memory import ConversationSummaryBufferMemory

[code] cell 34

# create a long string
schedule = "There is a meeting at 8am with your product team. \
You will need your powerpoint presentation prepared. \
9am-12pm have time to work on your LangChain \
project which will go quickly because Langchain is such a powerful tool. \
At Noon, lunch at the italian resturant with a customer who is driving \
from over an hour away to meet you to understand the latest in AI. \
Be sure to bring your laptop to show the latest LLM demo."

memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=100)
memory.save_context({"input": "Hello"}, {"output": "What's up"})
memory.save_context({"input": "Not much, just hanging"},
                    {"output": "Cool"})
memory.save_context({"input": "What is on the schedule today?"}, 
                    {"output": f"{schedule}"})

[code] cell 35

memory.load_memory_variables({})

[code] cell 36

conversation = ConversationChain(
    llm=llm, 
    memory = memory,
    verbose=True
)

[code] cell 37

conversation.predict(input="What would be a good demo to show?")

[code] cell 38

memory.load_memory_variables({})

[markdown] cell 39

Reminder: Download your notebook to you local computer to save your work.

---

## Lesson 3: Chains in LangChain — works/L3-Chains/L3-Chains.ipynb

[markdown] cell 0

# Chains in LangChain

## Outline

* LLMChain
* Sequential Chains
  * SimpleSequentialChain
  * SequentialChain
* Router Chain

[code] cell 1

import warnings
warnings.filterwarnings('ignore')

[code] cell 2

import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

[markdown] cell 3

Note: LLM's do not always produce the same results. When executing the code in your notebook, you may get slightly different answers that those in the video.

[code] cell 4

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

[code] cell 5

#!pip install pandas

[code] cell 6

import pandas as pd
df = pd.read_csv('Data.csv')

[code] cell 7

df.head()

[markdown] cell 8

## LLMChain

[code] cell 9

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

[code] cell 10

llm = ChatOpenAI(temperature=0.9, model=llm_model)

[code] cell 11

prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe \
    a company that makes {product}?"
)

[code] cell 12

chain = LLMChain(llm=llm, prompt=prompt)

[code] cell 13

product = "Queen Size Sheet Set"
chain.run(product)

[markdown] cell 14

## SimpleSequentialChain

[code] cell 15

from langchain.chains import SimpleSequentialChain

[code] cell 16

llm = ChatOpenAI(temperature=0.9, model=llm_model)

# prompt template 1
first_prompt = ChatPromptTemplate.from_template(
    "What is the best name to describe \
    a company that makes {product}?"
)

# Chain 1
chain_one = LLMChain(llm=llm, prompt=first_prompt)

[code] cell 17

# prompt template 2
second_prompt = ChatPromptTemplate.from_template(
    "Write a 20 words description for the following \
    company:{company_name}"
)
# chain 2
chain_two = LLMChain(llm=llm, prompt=second_prompt)

[code] cell 18

overall_simple_chain = SimpleSequentialChain(chains=[chain_one, chain_two],
                                             verbose=True
                                            )

[code] cell 19

overall_simple_chain.run(product)

[markdown] cell 20

## SequentialChain

[code] cell 21

from langchain.chains import SequentialChain

[code] cell 22

llm = ChatOpenAI(temperature=0.9, model=llm_model)

# prompt template 1: translate to english
first_prompt = ChatPromptTemplate.from_template(
    "Translate the following review to english:"
    "\n\n{Review}"
)
# chain 1: input= Review and output= English_Review
chain_one = LLMChain(llm=llm, prompt=first_prompt, 
                     output_key="English_Review"
                    )

[code] cell 23

second_prompt = ChatPromptTemplate.from_template(
    "Can you summarize the following review in 1 sentence:"
    "\n\n{English_Review}"
)
# chain 2: input= English_Review and output= summary
chain_two = LLMChain(llm=llm, prompt=second_prompt, 
                     output_key="summary"
                    )

[code] cell 24

# prompt template 3: translate to english
third_prompt = ChatPromptTemplate.from_template(
    "What language is the following review:\n\n{Review}"
)
# chain 3: input= Review and output= language
chain_three = LLMChain(llm=llm, prompt=third_prompt,
                       output_key="language"
                      )

[code] cell 25


# prompt template 4: follow up message
fourth_prompt = ChatPromptTemplate.from_template(
    "Write a follow up response to the following "
    "summary in the specified language:"
    "\n\nSummary: {summary}\n\nLanguage: {language}"
)
# chain 4: input= summary, language and output= followup_message
chain_four = LLMChain(llm=llm, prompt=fourth_prompt,
                      output_key="followup_message"
                     )

[code] cell 26

# overall_chain: input= Review 
# and output= English_Review,summary, followup_message
overall_chain = SequentialChain(
    chains=[chain_one, chain_two, chain_three, chain_four],
    input_variables=["Review"],
    output_variables=["English_Review", "summary","followup_message"],
    verbose=True
)

[code] cell 27

review = df.Review[5]
overall_chain(review)

[markdown] cell 28

## Router Chain

[code] cell 29

physics_template = """You are a very smart physics professor. \
You are great at answering questions about physics in a concise\
and easy to understand manner. \
When you don't know the answer to a question you admit\
that you don't know.

Here is a question:
{input}"""


math_template = """You are a very good mathematician. \
You are great at answering math questions. \
You are so good because you are able to break down \
hard problems into their component parts, 
answer the component parts, and then put them together\
to answer the broader question.

Here is a question:
{input}"""

history_template = """You are a very good historian. \
You have an excellent knowledge of and understanding of people,\
events and contexts from a range of historical periods. \
You have the ability to think, reflect, debate, discuss and \
evaluate the past. You have a respect for historical evidence\
and the ability to make use of it to support your explanations \
and judgements.

Here is a question:
{input}"""


computerscience_template = """ You are a successful computer scientist.\
You have a passion for creativity, collaboration,\
forward-thinking, confidence, strong problem-solving capabilities,\
understanding of theories and algorithms, and excellent communication \
skills. You are great at answering coding questions. \
You are so good because you know how to solve a problem by \
describing the solution in imperative steps \
that a machine can easily interpret and you know how to \
choose a solution that has a good balance between \
time complexity and space complexity. 

Here is a question:
{input}"""

[code] cell 30

prompt_infos = [
    {
        "name": "physics", 
        "description": "Good for answering questions about physics", 
        "prompt_template": physics_template
    },
    {
        "name": "math", 
        "description": "Good for answering math questions", 
        "prompt_template": math_template
    },
    {
        "name": "History", 
        "description": "Good for answering history questions", 
        "prompt_template": history_template
    },
    {
        "name": "computer science", 
        "description": "Good for answering computer science questions", 
        "prompt_template": computerscience_template
    }
]

[code] cell 31

from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain,RouterOutputParser
from langchain.prompts import PromptTemplate

[code] cell 32

llm = ChatOpenAI(temperature=0, model=llm_model)

[code] cell 33


destination_chains = {}
for p_info in prompt_infos:
    name = p_info["name"]
    prompt_template = p_info["prompt_template"]
    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    destination_chains[name] = chain  
    
destinations = [f"{p['name']}: {p['description']}" for p in prompt_infos]
destinations_str = "\n".join(destinations)

[code] cell 34

default_prompt = ChatPromptTemplate.from_template("{input}")
default_chain = LLMChain(llm=llm, prompt=default_prompt)

[code] cell 35

MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
language model select the model prompt best suited for the input. \
You will be given the names of the available prompts and a \
description of what the prompt is best suited for. \
You may also revise the original input if you think that revising\
it will ultimately lead to a better response from the language model.

<< FORMATTING >>
Return a markdown code snippet with a JSON object formatted to look like:
```json
{{{{
    "destination": string \ "DEFAULT" or name of the prompt to use in {destinations}
    "next_inputs": string \ a potentially modified version of the original input
}}}}
```

REMEMBER: The value of “destination” MUST match one of \
the candidate prompts listed below.\
If “destination” does not fit any of the specified prompts, set it to “DEFAULT.”
REMEMBER: "next_inputs" can just be the original input \
if you don't think any modifications are needed.

<< CANDIDATE PROMPTS >>
{destinations}

<< INPUT >>
{{input}}

<< OUTPUT (remember to include the ```json)>>"""

[code] cell 36

router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
    destinations=destinations_str
)
router_prompt = PromptTemplate(
    template=router_template,
    input_variables=["input"],
    output_parser=RouterOutputParser(),
)

router_chain = LLMRouterChain.from_llm(llm, router_prompt)

[code] cell 37

chain = MultiPromptChain(router_chain=router_chain, 
                         destination_chains=destination_chains, 
                         default_chain=default_chain, verbose=True
                        )

[code] cell 38

chain.run("What is black body radiation?")

[code] cell 39

chain.run("what is 2 + 2")

[code] cell 40

chain.run("Why does every cell in our body contain DNA?")

[markdown] cell 41

Reminder: Download your notebook to you local computer to save your work.

---

## Lesson 4: LangChain: Q&A over Documents — works/L4-QnA/L4-QnA.ipynb

[markdown] cell 0

# LangChain: Q&A over Documents

An example might be a tool that would allow you to query a product catalog for items of interest.

[code] cell 1

#pip install --upgrade langchain

[code] cell 2

import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

[markdown] cell 3

Note: LLM's do not always produce the same results. When executing the code in your notebook, you may get slightly different answers that those in the video.

[code] cell 4

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

[code] cell 5

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from IPython.display import display, Markdown
from langchain.llms import OpenAI

[code] cell 6

file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)

[code] cell 7

from langchain.indexes import VectorstoreIndexCreator

[code] cell 8

#pip install docarray

[code] cell 9

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])

[code] cell 10

query ="Please list all your shirts with sun protection \
in a table in markdown and summarize each one."

[markdown] cell 11

**Note**:
- The notebook uses `langchain==0.0.179` and `openai==0.27.7`
- For these library versions, `VectorstoreIndexCreator` uses `text-davinci-003` as the base model, which has been deprecated since 1 January 2024.
- The replacement model, `gpt-3.5-turbo-instruct` will be used instead for the `query`.
- The `response` format might be different than the video because of this replacement model.

[code] cell 12

llm_replacement_model = OpenAI(temperature=0, 
                               model='gpt-3.5-turbo-instruct')

response = index.query(query, 
                       llm = llm_replacement_model)

[code] cell 13

display(Markdown(response))

[markdown] cell 14

## Step By Step

[code] cell 15

from langchain.document_loaders import CSVLoader
loader = CSVLoader(file_path=file)

[code] cell 16

docs = loader.load()

[code] cell 17

docs[0]

[code] cell 18

from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()

[code] cell 19

embed = embeddings.embed_query("Hi my name is Harrison")

[code] cell 20

print(len(embed))

[code] cell 21

print(embed[:5])

[code] cell 22

db = DocArrayInMemorySearch.from_documents(
    docs, 
    embeddings
)

[code] cell 23

query = "Please suggest a shirt with sunblocking"

[code] cell 24

docs = db.similarity_search(query)

[code] cell 25

len(docs)

[code] cell 26

docs[0]

[code] cell 27

retriever = db.as_retriever()

[code] cell 28

llm = ChatOpenAI(temperature = 0.0, model=llm_model)

[code] cell 29

qdocs = "".join([docs[i].page_content for i in range(len(docs))])

[code] cell 30

response = llm.call_as_llm(f"{qdocs} Question: Please list all your \
shirts with sun protection in a table in markdown and summarize each one.") 

[code] cell 31

display(Markdown(response))

[code] cell 32

qa_stuff = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    verbose=True
)

[code] cell 33

query =  "Please list all your shirts with sun protection in a table \
in markdown and summarize each one."

[code] cell 34

response = qa_stuff.run(query)

[code] cell 35

display(Markdown(response))

[code] cell 36

response = index.query(query, llm=llm)

[code] cell 37

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=embeddings,
).from_loaders([loader])

[markdown] cell 38

Reminder: Download your notebook to you local computer to save your work.

---

## Lesson 5: LangChain: Evaluation — works/L5-Evaluation/L5-Evaluation.ipynb

[markdown] cell 0

# LangChain: Evaluation

## Outline:

* Example generation
* Manual evaluation (and debuging)
* LLM-assisted evaluation
* LangChain evaluation platform

[code] cell 1

import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

[markdown] cell 2

Note: LLM's do not always produce the same results. When executing the code in your notebook, you may get slightly different answers that those in the video.

[code] cell 3

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

[markdown] cell 4

## Create our QandA application

[code] cell 5

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import DocArrayInMemorySearch

[code] cell 6

file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)
data = loader.load()

[code] cell 7

index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])

[code] cell 8

llm = ChatOpenAI(temperature = 0.0, model=llm_model)
qa = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=index.vectorstore.as_retriever(), 
    verbose=True,
    chain_type_kwargs = {
        "document_separator": "<<<<>>>>>"
    }
)

[markdown] cell 9

### Coming up with test datapoints

[code] cell 10

data[10]

[code] cell 11

data[11]

[markdown] cell 12

### Hard-coded examples

[code] cell 13

examples = [
    {
        "query": "Do the Cozy Comfort Pullover Set\
        have side pockets?",
        "answer": "Yes"
    },
    {
        "query": "What collection is the Ultra-Lofty \
        850 Stretch Down Hooded Jacket from?",
        "answer": "The DownTek collection"
    }
]

[markdown] cell 14

### LLM-Generated examples

[code] cell 15

from langchain.evaluation.qa import QAGenerateChain

[code] cell 16

example_gen_chain = QAGenerateChain.from_llm(ChatOpenAI(model=llm_model))

[code] cell 17

# the warning below can be safely ignored

[code] cell 18

new_examples = example_gen_chain.apply_and_parse(
    [{"doc": t} for t in data[:5]]
)

[code] cell 19

new_examples[0]

[code] cell 20

data[0]

[markdown] cell 21

### Combine examples

[code] cell 22

examples += new_examples

[code] cell 23

qa.run(examples[0]["query"])

[markdown] cell 24

## Manual Evaluation

[code] cell 25

import langchain
langchain.debug = True

[code] cell 26

qa.run(examples[0]["query"])

[code] cell 27

# Turn off the debug mode
langchain.debug = False

[markdown] cell 28

## LLM assisted evaluation

[code] cell 29

predictions = qa.apply(examples)

[code] cell 30

from langchain.evaluation.qa import QAEvalChain

[code] cell 31

llm = ChatOpenAI(temperature=0, model=llm_model)
eval_chain = QAEvalChain.from_llm(llm)

[code] cell 32

graded_outputs = eval_chain.evaluate(examples, predictions)

[code] cell 33

for i, eg in enumerate(examples):
    print(f"Example {i}:")
    print("Question: " + predictions[i]['query'])
    print("Real Answer: " + predictions[i]['answer'])
    print("Predicted Answer: " + predictions[i]['result'])
    print("Predicted Grade: " + graded_outputs[i]['text'])
    print()

[code] cell 34

graded_outputs[0]

[markdown] cell 35

Reminder: Download your notebook to you local computer to save your work.

---

## Lesson 6: LangChain: Agents — works/L6-Agents/L6-Agents.ipynb

[markdown] cell 0

# LangChain: Agents

## Outline:

* Using built in LangChain tools: DuckDuckGo search and Wikipedia
* Defining your own tools

[code] cell 1

import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

import warnings
warnings.filterwarnings("ignore")

[markdown] cell 2

Note: LLM's do not always produce the same results. When executing the code in your notebook, you may get slightly different answers that those in the video.

[code] cell 3

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

[markdown] cell 4

## Built-in LangChain tools

[code] cell 5

#!pip install -U wikipedia

[code] cell 6

from langchain.agents.agent_toolkits import create_python_agent
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools.python.tool import PythonREPLTool
from langchain.python import PythonREPL
from langchain.chat_models import ChatOpenAI

[code] cell 7

llm = ChatOpenAI(temperature=0, model=llm_model)

[code] cell 8

tools = load_tools(["llm-math","wikipedia"], llm=llm)

[code] cell 9

agent= initialize_agent(
    tools, 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

[code] cell 10

agent("What is the 25% of 300?")

[markdown] cell 11

## Wikipedia example

[code] cell 12

question = "Tom M. Mitchell is an American computer scientist \
and the Founders University Professor at Carnegie Mellon University (CMU)\
what book did he write?"
result = agent(question) 

[markdown] cell 13

## Python Agent

[code] cell 14

agent = create_python_agent(
    llm,
    tool=PythonREPLTool(),
    verbose=True
)

[code] cell 15

customer_list = [["Harrison", "Chase"], 
                 ["Lang", "Chain"],
                 ["Dolly", "Too"],
                 ["Elle", "Elem"], 
                 ["Geoff","Fusion"], 
                 ["Trance","Former"],
                 ["Jen","Ayai"]
                ]

[code] cell 16

agent.run(f"""Sort these customers by \
last name and then first name \
and print the output: {customer_list}""") 

[markdown] cell 17

#### View detailed outputs of the chains

[code] cell 18

import langchain
langchain.debug=True
agent.run(f"""Sort these customers by \
last name and then first name \
and print the output: {customer_list}""") 
langchain.debug=False

[markdown] cell 19

## Define your own tool

[code] cell 20

#!pip install DateTime

[code] cell 21

from langchain.agents import tool
from datetime import date

[code] cell 22

@tool
def time(text: str) -> str:
    """Returns todays date, use this for any \
    questions related to knowing todays date. \
    The input should always be an empty string, \
    and this function will always return todays \
    date - any date mathmatics should occur \
    outside this function."""
    return str(date.today())

[code] cell 23

agent= initialize_agent(
    tools + [time], 
    llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = True)

[markdown] cell 24

**Note**: 

The agent will sometimes come to the wrong conclusion (agents are a work in progress!). 

If it does, please try running it again.

[code] cell 25

try:
    result = agent("whats the date today?") 
except: 
    print("exception on external access")

[markdown] cell 26

Reminder: Download your notebook to you local computer to save your work.
