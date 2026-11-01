# Evaluating AI Agents — Transcripts

---

## Lesson 1: Introduction

Welcome to Evaluating AI Agents
built in partnership with Arize AI. Say you're building an AI
coding agent, you might have to carry out a lot of steps to generate good code such
as plan, use tools, reflect, and so on. And using an evaluation driven development
process would make your development much more efficient. In this course, you'll learn how to add observability
to your agent-based applications. Said this, You will see what it is doing
every step of the way, so you can evaluate it components wise and efficiently
drive improvements at the components. And then also at the whole system level. So if you're asking yourself questions
like should you update a prompt at the last step, or should you update
the logic of the workflow, or should you change the large language
model you're using? Having a disciplined, evaluation
driven process will help you a lot in terms of making these decisions
in a systematic rather than random try a lot of things
and see what works, kind of way. If you've heard of the idea of error
analysis, which is a key concept to machine learning,
this teaches you how to do that in the agentic workflow
development process. If you haven't heard of error analysis,
that's fine too. But in this course it takes
an important set of ideas and shows you how to do it to develop agentic workflows
efficiently. The instructors of this course
are John Gilhuly, whose head of developer relations and Aman Khan,
who is director of product at Arize AI. It's been fun working with you
on this course. Thank you. Andrew.
We're excited to teach this course. Thank you. Say you're building a research agent
that searches the web, identifies sources, collects content, summarizes findings,
and then maybe iterates if it identifies
any weaknesses as an output. When you're building this complex system,
you need to evaluate the quality of each step's output. For example, for source selection,
you might create a test set that comprises research topics and the corresponding
set of expected sources, and then measure the percentage of times
that the agent chooses to correct sources. Or for open
ended tasks like summarization, you can prompt a separate
large language model or apply what we call large language model
as judge. In order to evaluate the quality of this
more open-ended output of a text summary. Apart from testing and improving
the quality of your agent's output, you can also evaluate the path taken
by the agent to ensure it doesn't get stuck in a loop
or repeat steps unnecessarily. And so, in this course, you'll learn
how to structure your evaluations to iterate on and improve both the output
quality and the path taken by your agent. You'll do this by creating a code based
agent that operates as a data analyzer. The agent will have access to a set of tools that allow it to connect
to a database and perform analysis. A router that identifies
what tool to use, and a memory that keeps track of the chat history. You'll
collect and evaluate traces of the steps taken by your agent to process
a query and visualize the collected data. You'll then learn how to evaluate each tool in your agent workflow
using different types of evaluators. You also evaluate if the router chooses
the right tool based on the user's query, and if it extracts the right parameters
to execute the tool and assess
the trajectory taken by the agent. Finally, you put all of your evaluators
into a structured experiment that you can use to iterate on
and improve your agent. While the course focuses on
applying evaluation during development. You'll also learn how you can monitor
your agent during production. Many people have worked to create this
course. I'd like to thank Mikyo King,
Xander Song, and Aparna Dhinakaran from Arize AI.
And from DeepLearning.AI Hawraa Salami has also contributed
to this course. John and Aman are both experts
on the important topic of how to evaluate AI agentic workflows. Let's now go on to the next video,
and I hope you enjoy the course and learn a lot from John and Aman.

---

## Lesson 2: Evaluation in the time of LLMs

AI agents are software applications
powered by LLMs. In this first lesson,
you'll learn how evaluating LLM-based systems differs
from traditional software testing. We'll then examine what agents
mean and discuss what you need to consider when evaluating agents. Let's dive in. When you think about evaluation in
general, there are typically two layers. On the left-hand side,
you have LLM model evaluation. This focuses on how well a large language
model performs a specific task. You might have seen benchmarks
like MMLU for questions spanning math, philosophy, medicine and more,
or human eval for code generation tasks. Providers often use these benchmarks
to showcase how their foundation models stack up. On the right-hand side, you have an LLM system
or application evaluation. This zeroes
in on how well your overall application, of which the LLM is just a part
of, performs. Here, the data sets being used for
evaluation are created either
manually, automatically, or synthetically, using real-world data. When you incorporate an LLM into a broader system
or product, you'll want to understand if the entire system
including the prompts, tools, memory, and routing components are delivering
the results that you expect. You may have experience
with traditional software testing,
where systems are largely deterministic. You can picture that
like a train on a track. There's usually a well-defined start
and end, and it's often straightforward to check whether each piece, the train
or the track is working correctly. LLM-based systems, on the other hand, can feel more
like driving a car through a busy city. The environment is variable
and the system is non-deterministic. With software testing, you rely on unit tests
to check individual parts of the system and integration tests to make sure
they fit together as intended. And the results
are usually pretty deterministic. Unlike traditional software testing,
when you give the same prompt to an LLM multiple times, you might see
slightly different responses. Just like how drivers
can behave differently in city traffic. You're often dealing with more qualitative
or open-ended metrics, like the relevance
or coherence of the output, which might not fit neatly into a strict pass/fail
test model. There are a number of common
evaluation types for LLM systems. We have hallucination. Is the LLM accurately using provided
context or as in making things up? Retrieval relevance. If the system retrieves
documents or context, are they actually relevant to the query? Question answering accuracy. Does the response match the ground truth
the user needs? Toxicity. Is the LLM outputting harmful
or undesirable language? And overall performance. How well is the system
performing at its goal? There are many open-source tools
and data sets that can help you measure these aspects, as well as help
you develop your own evals. And we'll cover a few
of these later in the course. As soon as you move from an LLM-based
app to an agent, you're adding an extra layer
of complexity. Agents use LLMs for reasoning,
but they also take actions on your behalf by choosing among tools, APIs,
or other capabilities. an agent as a software-based system that can take actions on behalf of a user
utilizing reasoning. An agent
typically has three main components. We have reasoning,
which is powered by the LLM. Routing, which is deciding which tool or skill
to use. And the action, which is executing the tool call, API call, or code. You may have already seen
examples of agent use cases, like personal assistant agents that help you take notes
or transcribe information for you. Desktop or browser-based agents
that help automate repetitive tasks. Agents for data scraping and summarization
and agents that can conduct search and compile research. Let's use an example use case
to illustrate how an agent actually works. Suppose you want an agent to book a trip
to San Francisco. There's a lot going on behind the scenes. First, the agent has to figure out
which tool or API it should call based on your request. It needs to understand what you're really asking for
and which resources will help. Next, it might call a search API
to check available flights or hotels, and it could decide to ask you
follow-up questions or refine how it constructs the request
for that tool. Finally, you wanted to return a friendly
and accurate response, ideally with the correct trip details. Now, let's think
about how you'd evaluate the step by step. Did the agent pick the right tool
in the first place? When it forms a search or booking request
that it call the correct function with the right parameters? Is it using your contacts, for instance, the dates, preferences,
and location accurately? How does the final response look? Does it have the right tone
and is it factually correct? In the system,
there's plenty that can go wrong. Maybe the agent returns flights
to San Diego instead of San Francisco. That might work for some people. Then those folks would be unhappy if they wanted San Francisco
and ended up with San Diego. This highlights why you need to evaluate
not just the LLMs raw output, but also how the agent decides
on each action along the way. You might see issues like the agent
calling the wrong tool, misusing context, or even adopting a snarky
or inappropriate tone. Sometimes users
also try to jailbreak the system, which can create even more unexpected
outputs. To evaluate each of these factors. You can use human feedback
or human in the loop or in less an LLM itself
as a judge to assess whether the agent's final response
is truly fulfilling your requirements. We'll dive deeper into how LLM
as a judge works with agent evaluation later in this course. Finally, remember
that even small changes to your prompts or code can have unexpected
ripple effects. For instance, adding a simple line
in like "remember to respond politely" might help you improve
on a number of use cases, but can also cause a regression
in test cases that you may not expect. That's why you want to maintain
a representative set of test cases or data sets that reflect your critical use cases.
Each time you adjust your system, you can rerun evals on these data
sets to catch regressions and keep building out
new agent capabilities over time. This approach is key to developing robust
agent evaluations. Just like you do
with traditional software. You want to iterate on an agent's
performance. However, you can't rely on purely
deterministic checks. Agents themselves are non-deterministic,
and take multiple paths, and might regress in one scenario
even as they improve in another. To handle this,
you want a consistent set of tests covering different user cases
that get run every time you make a change. These tests
often loop back from production data, like real-world
queries and real user interactions. Back to development, where you can refine
on prompts, tools, or your approach. This can help you catch regressions
when your agent is deployed in production, and continuously expand your test coverage
to improve on your system over time. A few of the tools that we're going
to be covering in this course are: trace instrumentation to understand
what's happening with your agent underneath the hood, an eval runner
which contains LLM as a judge, data sets which you can use to rerun
experiments, human feedback that allow you to capture
human annotations and production, and a prompt playground you can use
for your data for iterating on your data. In this lesson, you took a broad
look at how LLM model evaluation compares to system evaluation,
why LLM-based apps require different testing approaches
than traditional software, the extra complexity that agents
bring with reasoning, routing, and action. Common pitfalls with agents like
wrong tool selection for context usage and the importance of iterative testing
using a single set of tools for development to production. You'll get to see all of this in action
and dive into practical code soon. In the following lessons,
you'll look even more closely at how to evaluate an agent,
what data to collect, and how to structure these evaluations to keep your agent
on track in the real world.

---

## Lesson 3: Decomposing agents

In this course, you'll build an AI agent
from scratch and learn how to evaluate it. In this lesson, we'll dive
into the details of this agent structure and then go through an agent example
that can perform data analysis. You'll then learn how to code
such an agent in Python. All right. Let's go. Agents are typically made up
of three main types of components: a router, skills,
and then memory and state. The image on the right here
shows an example of an agent with a router in black, the state
as the dark purple at the bottom, and then a set of three different skills
that that agent can call in this case track package,
look up item, and answer a question. Each of those different components
can interact with the state, and the router is responsible for handling user input
and then output back to the user. Looking first at the router, the router is
the main planner of the agent. Sort of the agent's brain in a way. The router is responsible for deciding
which skill or function the agent will call to answer
a user's question. So when the router receives user
input or a response back from a different skill, the router will
then decide which other skill to call from there. Routers can take a few different forms. They can either be an LLM equipped with function calling,
as we'll use in this course, or a more simple NLP classifier,
or even just a rules-based code. Generally,
the simpler type of router that you have, the better your performance will be in, the more consistent
your performance will be, but you'll also scope down
the capabilities of that router. Something like an LLM with function
calling has a very broad ranging capabilities, but is a little bit
more unreliable than rules-based code. That's also where evaluation can help
you close the gap. Some agents,
instead of using a single router step, will distribute that logic
throughout the agent. Popular frameworks that use this are line
graph as well as OpenAI swarm. They still have routing logic,
but instead of having one single router step, they distribute that responsibility
throughout the agent itself. Next, skills are the individual logic blocks and capabilities
that an agent has. So, skills are what allow the agent
to actually do anything that would allow it to connect with the outside world
through APIs or call databases, or really do any of the different tasks
that your agent can accomplish. Every agent will have either one
or more skills. An agent without any skills
doesn't really do anything. Not a real use case there. Skills are made up of individual steps.
LLM calls, application code, API calls, or really
any other code that you want to use there. One example of a skill
that's very common is a RAG skill. So in this case, you could have a retrieval augmented
generation capability within your agent that would handle everything
from embeddings to looking up data from a vector database to making an LLM
call with retrieved context. And all of that is encompassed
in a single RAG skill. So you can see how skills can encompass
multiple different steps, and entire LLM applications can be thought of as skills in the context of agents. Once skills is complete,
they'll also return back to the router in most agent contexts so that they can choose either
to return to the user or call another skill from there. Memory and state are also used by agents to store information that can be accessed
by every component within the agent. Typically, memory and state are used
to store things like retrieved-context, configuration variables, or very commonly,
a log of previous agent execution steps. This last one is probably the most common
that you'll see. Many LLM APIs actually rely on being passed in a whole dictionary or list of messages about what the agent has done previously,
before choosing the next step to call. The OpenAI function calling router
that you'll use throughout the course uses this approach, so you'll get
very familiar with that approach. Turning to your example agent that you're
going to build throughout this course. The example agent that you're going to
create is a data analysis assistant that can help you understand
and ask questions over a sales database that you have. That agent has a few different skills. It has a data lookup skill that can query
information from that attached database. It has a data analysis skill
that can draw conclusions from that data, spot trends and make calculations. And then finally,
it has a data visualization skill that can generate Python code
and create graphs through that code and visualizations. Looking
at your example agent visually here you see you have a user who's
sending in queries to a router in this case
GPT-4o-mini call with function calling. And then that router will call
one of three different tools here, the lookup sales data tool, data
analysis tool or data visualization tool. And then those tools will return
back to the router, which then decides to either return to the user
or call another tool from there. Now we're using the word tool here
because that's what's expected by GPT-4o-mini. That's analogous to skills in this case. So your lookup sales data tool would be
analogous to a lookup sales data skill. Diving into each of these skills
a little bit more deeply, you see that each
skill has a few different steps that it can actually go through
to accomplish its task. The Lookup sales data tool, for example,
first prepares a database so it loads in a local database
and make sure that it's ready to query that database. Then it will generate SQL using another
LLM call to query that database, and then finally execute that SQL
and return the result all the way back to the router. Similarly, the data analysis tool makes a single call
to generate an analysis. So it just makes a single LLM call
and then returns that response back to the router. And finally, the data visualization tool actually
makes two sequential LLM calls. First, to generate a chart config and then to generate Python code
based on that config. The reason for the two calls in that case
is that while you could just ask an LLM to generate code straight away
and do both steps at once, you'll get more unreliable responses
that way. And because chart visualizations in Python
are somewhat formulaic, it helps to first generate this chart
config with a few key variables and then generate the Python code
based on that chart config. So splitting up the task into two simpler
tasks instead of asking for the LLM
to complete one more difficult task. In this lesson, you've learned about the major components
of agents, routers, skills, and memory, and you've examined the example agent
that you're going to build. In the next video, you're going to go through a notebook
and actually implement and build this example agent.

---

## Lesson 4: Lab 1: Building your agent

In this notebook, you're going to build
the agent that's going to be used
throughout the rest of this course. As you've seen, this is an example agent
that uses a few different tools and a router to answer questions
about a data file that's attached. So first thing you want to do is import a few different libraries
that are going to be used by this agent. So you have an OpenAI
library, Pandas, Json, and then a library called duckDB,
which gets used for some of the SQL code that you're going to run, as well as pydantic,
some markdown displaying, and then some helper methods
that are used to gather the OpenAI key and a few other kind of things
specific to your environment here. And then next thing you're going to do
is you'll want to set up your OpenAI client
that will be used throughout this agent. In this case, using GPT-4o-mini. And then you're ready
to start defining the tools. So as mentioned there's three tools
that the agent is going to have. The first is a database
lookup tool that it will use. And so there's a local file
in the notebook that is store sales price
elasticity promotions data file. So, here's a path to that file
that's going to be used. And this is a parquet file
which is just a file that's going to be used to simulate the database
that your agent can interact with. And this file contains a bunch of
transaction data of different store sales. So you can imagine every time there's a sale in a particular store,
one new entry gets added to this file with the product skew
and with the any promotions attached to it, as well as the
price and the cost of that sale. So now,
there's a few steps to this first tool. First, the tool needs to generate SQL that can be run on this database
that you have locally. And then it needs to actually run
that SQL command and get the result back. So to generate
the SQL you're going to use a prompt here. So you'll need a prompt
to actually generate the SQL code. And so you can see that here
generate a SQL query based on a prompt. Do not reply with anything
besides the SQL query. And you can see the prompt
is going to be passed in as a variable, as are the columns for the table
and the table name, so that the LLM knows what available columns there are. What the table is,
which is critical when it creates the SQL code that's going to run. So now you can set up a method
to actually generate the SQL code itself, using that GPT-4o-mini model
that you established. So here is the generated
SQL method that you might use. So it takes in a prompt list of columns
and then table name. And then it formats
this SQL generation prompt that you have up here
with those different variables. So you'll see the prompt, columns
and table name passed in. And then that formatted prompt
will be sent over to GPT-4o-mini as a user message. And then that response will get returned.
And now you need to incorporate that SQL generation code into a tool
that can be used by the agent to actually run the code
after it's been generated. And so for that you'll find another method
here. In this case, this is going to
be called lookup sales data. And so what this method will do
is it takes in a prompt. And then it will try to first create the database from that local parquet file. So you can see it creates a data frame
here using pandas with that local file. And then it uses the DuckDB library here
to say create this table
if it doesn't exist already, which will create a SQL database table
based on that data frame that you have. And then next, you'll use the generate SQL
query method that you just created
to create an SQL query here. And that can then be slightly modified
here to remove any extra trending white spaces
or any other extra characters here, and then run
using duckDB to receive a result. This step right here can be useful
because oftentimes you'll have the LLM respond with SQL at the top
to kind of format the response there. It doesn't just respond with code. Sometimes it includes that extra SQL bit, which is why you're removing
some of those characters here. DuckDB here is used to take the data frame that you have
and turn it into, a corner database in memory
that you can access. And that will make it easier to run
any kinds of, queries across that database and will work
fairly efficiently and very quickly. And it also allows you to use generated
SQL code and query that database
using SQL code in a very easy way. Now that you have your tool defined here, it's always good to make sure
that the tool is actually working. So you can put in an example query here,
print out the result, say example data and call your method
with show me the sales data for store 1320 on November 1st, 2021,
and you can run that. It might take a second to run
and you should get a response back. Should get a response
back that looks something like this. So you see data that's been retrieved
from your SQL database. Great.
That's one tool down. Two more to go. So next tool is a data analysis tool. And so this is a tool
that can take in data and then makes an LLM call to conduct analysis
and capture trends from that data. So, similar to before you're going to want to have a prompt
for that particular tool. In this case, it's pretty straightforward. It's analyze the following data. And there's a variable for data. And then your job
is to answer the following question. And there's a variable for the prompt. Now you'll have a method
to actually make that call. So you can have an analyze sales data
method here that takes in a prompt and some data. And then similar to before, you're going to format the prompt
you just created with those parameters, make a call to your OpenAI client and get a response back as the analysis. And then you can always do
some little bit of error checking here
to see if the analysis doesn't come back for whatever reason,
then you can still return within no analysis could be generated. This kind of thing
is especially helpful in agents because if you have a response
that breaks halfway through your agent, you want to make sure that that doesn't
cascade and break everything else
inside of your agent. So, good error checking is almost more important
in agents than it can be in other tools. And now, with your analyze sales data method defined, you can test
and make sure that that's working. So you can call analyze
sales data the prompt: What trends do you see in this data? And you can pass in the example data
that you retrieved with the previous tool. And you should get back
something that looks like this, which is some markdown
formatted response from your model. And moving on to the third and final tool
that the agent will use here. This third tool
is a data visualization tool. And if you think back to the previous
lesson, you'll remember that
this works using two different steps. So at first generates a chart config
or what we're calling a chart config. And then it will use that chart
config to generate some Python code
to generate a visualization. So starting with the chart config here. You're going to again have a prompt that
you want to use to generate that config. You'll see it says generate a chart
config based on some data. Your goal is to show a visualization goal. And then here, you're going to use a tool
called pydantic along with a feature of OpenAI
called Structured Output. So that you can ensure that when you make
a call to generate a chart config, it matches a very specific format
that you're defining here. So first thing to do that is define
the actual format that you want to use. So in this case this visualization config is a set of a dictionary
with four different variables here. Chart type x axis, y axis, and title. And then you can see there's a description of what
each of those different variables are. And you'll use that in just one
sec here with your OpenAI call in order to make sure that the output
matches that format exactly. So now you can define a method for extracting the chart config
and creating that chart config. It'll take in some data
as well as a visualization goal. And then again, it's going to format the chart
config prompt that you set up above. And then there's going to be slight
difference in this call that's made here. Because now you're using that structured output feature
to tell OpenAI that it should respond in a format that matches that visualization
config that you just created. So one important thing to note is there's
a slightly different message string here to allow you to include that response
format variable for visualization config. And again
what this will do is it will make it so that when OpenAI responds,
when GPT-4o-mini responds, it will be in the format
that matches your visualization config. So you'll be able to access things
like the content dot chart type
or content dot x axis, or y axis, or title. And the broader goal of this approach
is you're really scoping down the first thing you ask the model to do to say
instead of just generating Python code, it really just has to pull out, okay,
what's the chart type I should create? What's the x axis, y axis and title
that I should give to my chart? And then you can pass that into an LLM
in the next step of this tool. Do you have a more defined goal
for that LLM to generate code for. So moving on to the next step within
this third tool is to actually create the chart code
itself. So similar to before, you're going
to create a prompt to start off with. It says write Python code
to generate a chart based on this config. And it's passing in this config here. And then you can define a method to use that particular prompt
to generate Python code. So you'll see this create chart
method here takes in a dictionary which is that config. So that's what it was
generated by the last step there. And then it formats
your create chart prompt here. With that config. Makes your standard
OpenAI call gets its response back. And then similar to what you did
with the SQL code, it's always a good idea to make sure that, any sort of prefix here
that gets added by the model like this Python one you see here, is getting removed and replaced so that
you're only left with a runnable code. And now the last thing to do with
this tool is just compose those two different steps
together into one method. So now this generate visualization method is going to take in some data
and a visualization goal. It's first going to create a config
with the extract chart config method. And then it will create some Python code
using the create chart code. And finally, you can test and make sure
that this is actually all working correctly. So you can say generate visualization
with some example data and then a visualization goal. In this case, that's similar to the prompt the user might have. And we'll print out the response as well. And you should now see some Python code
that's been printed out here that will generate
a particular visualization for you. And you can actually take it
one step further and run the code here using the command execute code. And you'll see a visualization. In this case it looks like
the code was created correctly. But the visualization
looks slightly off here. So, this is where evaluation
is going to come into play later on because you'll be able to catch cases
where maybe the visualization is slightly off. One important note is that you always have the option to include
the ability for your agent to run code, but it's something you have to be
a little bit careful with because if you just run code that's been
created by an LLM, it could have errors. It could do things that you don't expect
it to. So it's always good to run code
within an enclosed environment if you're giving your agent
that capability. In this example agent, you left that
capability out just to keep things safe. But something good to know if you're incorporating the ability
to run code into future agents. Now, with all of your tools defined,
the next step is to put those tools into a format
that can be understood by your router. In this case, you're using an OpenAI,
GPT-4o-mini router with function calling. So there's a very specific format that
OpenAI expects to be pass those tools in. You can add that in here. And what you'll see is that each object
within this array of tools has a specific Json format
that's been defined. So in this first one, this first tool here
is your lookup sales data tool. So this is a method
that you defined earlier. And you'll see there's a description
in here of what that tool does. Or it can do lookup data
from this particular file. And then you'll see
that certain properties have been defined for things like the prompt parameter
that needs to be passed into this tool. And so this is what tells the router
how to choose this function. And if it chooses this function to call
what parameters need to be passed into it. So these descriptions are really critical both for the description of the function
as well as descriptions of the parameters. Because if you get these wrong, the router
may choose not to call your function. It may not understand
what that function does, or it may think the function can do things
that it actually can't do. So this is often
something that you end up changing a lot of times when building an agent
is getting the description and the parameter
descriptions exactly right. So there'll be an entry here
for each of your different tools. As well as a mapping at the bottom here to say this name here
matches this particular function, which I got used in a second. Awesome. You're now ready to define your router. To define your router
you can use a few different approaches. Let's walk through the code here. So in this case, this run agent function
that you have it's going to be what runs your router. Oftentimes, people will set up routers
to either work recursively where you continually call a function
that represents your router. Or in this case, you could go for something
even simpler and just use a while loop here that you break out of
when the agent completes its task. Looking through the code that you see
here, you have the messages object
that's passed into this function here. And then first we'll make sure that that messages object
matches the right format that we expect. So in this case
you want to have it as a user message. And this is a format that's expected
by OpenAI in this case. So you want to check for cases
where maybe you've passed in just a string as opposed to a dictionary of
these messages and correct for that case. And then if the system prompt has not actually been added
into this already, then you'll want to make sure
that that's been added. We'll define
that system prompt in just one moment. And then to actually run your agent,
it's going to follow a similar loop here where you first make a call to OpenAI
with your tools object that you just set up up there,
as well as the messages, and then you'll receive a response back to look for if there's any tool
calls inside that response. And then if there are, you're
gonna want to handle those tool calls. So you'll need to define
what that means in just a second. And then if there's no more tool calls
then you can return the response back to the user. So there's a couple more pieces
you need here for the router. First, you need this system prompt variable. So your router needs
some sort of system prompt. So you can define that
a very basic version of this is just you are a helpful assistant that can
answer questions about this data set. And the last piece you'll need is a way to handle the tool
calls that get made by your router. And so you can add in a method
to handle those tool calls. So here this is just looping through
each tool call that gets made. And then for that tool call
looking up the corresponding function name parsing out any arguments
that have been included in the tool call, and then calling that function
with those arguments and appending the result
back to the messages object. One other important thing to note here
is that OpenAI specifically,
as well as some other models, rely on a behavior where if they tell you
to call a particular tool, if that's the response you get back
from your router, then in the next call that you make to them, you need to include
a response of that particular tool. So they'll give you a tool call ID, and if you don't include back a tool message here
with that particular tool call ID, then they'll actually error and say,
hey, you need to call this particular tool and you need to give me a response for
that tool call that I asked you to make. And now with each of these
you are ready to go and run your agent. Pull in an example here. You can ask it a question like "show
me the code for a graph of sales by store. In November 2021
and tell me what trends you see." And you'll see it start to run, and you'll start to get
some print statements from your router there
where it's making calls to OpenAI, it receives some tool calls back,
it's going to process those tool calls. Then go back to the router
and you'll see that loop complete a few times as the code
runs here. And once you see a message saying that
there's no more tool calls to make and it's returned, the final response,
you can print out your result. And you should see in this case some code to generate that graph. As well as some of the trends that were
gathered by the data analysis tool. Congratulations. You now have a working agent
that can answer questions based on this local database
of sales data that you captured.

---

## Lesson 5: Tracing agents

Now that
you understand your agent example, the next step is to add
observability to your agent code. This will give you insight
into the trajectory or sequence of steps your agent takes to respond
to a user's query. You'll learn how to instrument your agent, which means adding code
to track your agent steps, and then visualize the collected
information or traces in the Phoenix UI. All right. Let's have some fun. When it comes to observing your agent, there are a few key concepts
that are important to know. The first is observability. Observability is a general software
concept that refers to having complete visibility
into every layer of your application. In the context of LLM applications, that's
often tracking things like the prompt, the response, token usage,
and then any calls that happen around the calls
that you're making to LLMs. Observability
is typically made up of traces and spans. Traces refer to full run
through of your application, so a single trace would be one and end run of your application from an input
all the way through to an output. And then traces are comprised
of multiple spans. Spans are individual steps of calls to LLMs or code, or lookups to databases
or whatever might be. So one trace is made of multiple spans,
and they're typically presented in this hierarchical way where spans
can be nested underneath each other to show that they're operating
within another span. And then a set of spans
will make up one trace hierarchy. Spans are typically presented
in this hierarchical manner here where you have individual spans
that are nested within each other,
all making up one trace. And you might have spans for LLM calls
as you see in the image here. You might have spans for tools. You might have chain spans which are just general logic steps
that happen within a trace. Traces and spans come from a framework
called OpenTelemetry. OpenTelemetry is often
abbreviated to OTEL, and it's one of the most widely used
standards for application observability,
even outside of LLMs and AI agents. OTEL includes the idea of traces and spans
that are captured within your application, as well as some standards
for how to capture those traces and spans. Often this process is referred to as instrumentation,
which you'll learn more about in a second. And then OpenTelemetry also includes
the concept of collectors and processors to receive those traces and spans,
and then enumerate them in a platform that allows you to visualize those traces
and run later evaluation on them. Throughout this course,
you're going to use a tool called Arize Phoenix,
which serves as one of those collectors to allow you to receive,
visualize, and evaluate traces. This is
what a trace looks like in Phoenix. You're going to see a lot more of this
throughout the notebooks as you start
implementing some of these techniques. But you'll notice
there's one trace here of Agent Run in the image
that's made up of multiple spans. You have an LLM span in orange. You have your chain spans in blue. And then your tool spans in yellow. Traces and spans are captured
in your application through a process called instrumentation. Instrumentation refers
to the practice of marking which functions or code blocks within your code you want to track as spans
and what attributes you want to attach to those spans. You can do this
manually with clauses or decorators, as you'll see
in the next notebook as well. However, tools like Phoenix do automate
some of this process for you, especially if you're using popular libraries
like OpenAI or LlamaIndex or LangChain. Observability
is important for a few different reasons. First, when you're getting off the ground
and building your application, observability
really simplifies the debugging process. As you're building. It's much easier to debug
by going through a nice visual trace than it is to pore over print statements
and logs in your application, so it makes it easier to get going. But then, as you start
launching your application to multiple different users, you start moving towards
production or testing even. Then, it gives you a detailed log
of all of the calls made to your application and all of the different
inputs that you're receiving. So it gives you a large database
of information of all of your different application runs,
so you can monitor how it's performing. And then these traces will become the
bedrock that is used to run evaluation. So later notebooks will have you export
data from Phoenix that you can then use for evaluations at scale across
multiple runs of your application. Finally, putting these together, observability helps
you really start to understand and eventually control some of the more
unpredictable behavior of LLMs. LLMs are by their very nature,
unpredictable in some cases, and the best way to deal with that is by monitoring them and later
evaluating them within your application. In this lesson, you've learned
what observability is, how it works, and why it's important, as well as some of the basic building
blocks of observability like traces and spans, and how those traces in spans
are collected. In the next notebook, you'll implement
some of the instrumentation techniques that you saw in these slides, and you'll set up your first Phoenix
instance here to collect those traces.

---

## Lesson 6: Lab 2: Tracing your agent

In this notebook, you're going to add
tracing and observability into the agent that you previously built
in the last notebook. So you'll start from the agent
that you've already built. And then you're going to add a few things in here to allow you to trace
that agent using Arize Phoenix, and then get some better observability
into what your agent's doing. So as before, you're going to start out
by adding some new imports here that will be used for Phoenix. So importing here Phoenix
as well as some basic libraries, and then importing a few things
from Phoenix here to set up some of that tracing observability registering here as well as some libraries
from OpenTelemetry, which you just learned about in the previous slides,
and then a library called Open Inference. Open Inference is a library
that's used and created by the Arize team, and it helps translate some concepts
in OpenTelemetry to work better with LLMs. So those are your libraries there
that you're going to be using. Go ahead and import those. And then as before, you're going to set up
your OpenAI model and client that you want to use. And now you can launch and connect
to an instance of Phoenix. So Phoenix is an application
that can receive the traces that you're going to send
from your agent here. And then can visualize those in a UI. And so in this environment you've already
got an instance of Phoenix running. There are a few ways that you can
launch Phoenix. You can either use this command
to launch Phoenix inside of a notebook. Alternatively,
you can run it on your own local machine, or you can access it through a web
app on the Arize website. In this case, in these notebooks,
Phoenix has been launched for you, so you don't actually have to run anything
here. You've already got an instance
that's running. Now, Phoenix has a concept of projects, and so projects are used to separate out
some of the traces that you're sending. Maybe you're tracing multiple
different kinds of applications or agents. You might want to group some of the
tracing into different projects. So here
you want to define the project name. And then you can use the register
method from Phoenix to connect your application
here to your Phoenix instance. So this register method here will take in
the project name as well as an endpoint. This endpoint is just
where your Phoenix instance is running. And that will be
where any traces get sent to. So again
you have it running in your notebook. And so this helper method here
get Phoenix endpoint. It's in the utils function. You can take a look
and see what that's doing if you want to. And that will give you an output that looks something like this where you can see OpenTelemetry
tracing has been set up. And so now any openTelemetry traces
that you capture or you instrument will be sent through
into your Phoenix project. So, next step that you'll go through here
is you've made this connection to Phoenix, but you still need to instrument
your application and mark which calls and which methods should be sent
through into Phoenix. And with what attributes. You can do this manually. However, libraries like Phoenix also have tools to do
some of this automatically for you. So this OpenAI instrument or for example, is part of the open inference library
that we mentioned. And what this will do is if I run that,
it will take in the tracer provider
that we set up here, and it will actually make it
so that any calls you make to OpenAI's library from this point on in the project
will get sent through into Phoenix traced properly. So if you're just using OpenAI calls
this would be all you would need to do to actually set
up tracing for those calls. In this example agent,
you have some stuff beyond that as well too. So you have tool calls that get made. You have some other logic
that's happening. So you're actually going to combine
this automatic instrumentor here with some more manual tracing. And so, to set up your manual tracing,
the first thing you want to do here is you want to get a tracer object from that tracer provider. And then this is what's going to be used
to mark any of those methods that you want to send through into Phoenix
as well. Now with all of that set up, make sure that you've also run
the different cells of your agent so that you can then run and test
your agent as we trace it. Now when it comes to setting up manual tracing for your agent
or really any project, it's always helpful to start from the outermost
layer that you want to trace. The outermost tracer span,
and then work your way down in terms of the detail
that you want to go to. This just helps make sure that you're
capturing the right information, and you give yourself a holistic view
of what's going on. So in this case,
you have your run agent method that's going to be used here
to start your agent. However, this method has a loop in it. And as we mentioned
in the previous notebook, sometimes you might want to use more of a
recursive call here where you're calling this method multiple times
for one given run of your agent. So it's helpful
sometimes to create an actual another outer layer
that you can use, or outer method that you can start
as that very top level trace or span here. So in this case
you're going to create a new method. In this case the start main span could just be called start agent
or whatever you want to use there. And really all this method is doing aside
from some of the tracing stuff, is just calling this run
agent method that you have already. So it's just calling that run
agent method. And again,
if you had that as a recursive method, this would be the initial call
that you would make to that method. And then beyond that it's adding
in some calls to set up tracing here. So this is your first manual tracing call
that's being added. So you'll add in using this tracer object. You'll start the span here with the name
Agent Run. You can make the name whenever you want. And then the open inference span
kind, agent. The span kind is just
what kind of category is the span. It'll map to some of the colors and things like that in the Phoenix
UI that you'll see in a second. So in this case, agent is the example. You'll see some for
tools and for chain later on. And then
that will start that current span. And anything within that with clause block
will be treated as part of that span. You can also set some attributes
for the span. So in this case setting the input to
what's the input value for that given span. In this case it'll be the messages object. And then when the agent completes
you can set the output here. This will be the value
of the return of the agent. And then you can set a status code
if you want to to say this was a completed call correctly.
There was not an error on this call. So you can define that method. And then from there you can start to work your way down
into the agent adding tracer. So next step can be done here is going into your run agent method. And there's maybe a few places
that you might want to start spans here. The most obvious one
is that each time you call your router, you may want to have a span
representing that router call. So here's what you can add to do that. So there's been a couple updates
to the method here. Everything up here is the same. No changes
there as you get down to your while loop. Here's the first change that you'll see. So adding that same call from before
tracer start this current span. This time calling it router call and then
adding in the open inferred span kind. This time adding in chain as the span kind.
Chain is just a basic logic step. There's no LLM call or tool call or it's
not an agent, it's just a chain. Chain is almost the default in a way. So you can start that
and then add in the input. Once again you'll keep your OpenAI call the same here. Add in your status as well. And then you can add in the output either
the tool calls or if you have all the tool calls completed and you're
going back to the user, you can add the eventual response of your agent here
to final response. So you can update that method here.
And then you can add a couple more pieces and then take a look
at what this looks like in Phoenix. So one other area
that you might want to add another span is when you go to handle the tool
calls, you might want to have a span
that captures that particular method and tracks that method. So here's how you can do that. You can go up to your handle tool
call method. And in this case you can use a different
technique for actually marking a span. So instead of using the with clause
you have another option which is to use a decorator
for this method. And this is really useful here
because really this method is totally self-contained. If you just said everything in this
method can be one span and that would work well for the instrumentation
you want to set up. So here you can just mark @tracer.chain. You could do @tracer agent
or @tracer tool for the different kinds of tool spans
or spans that you would want to track. And then what that will do is
it will treat any calls to this method
right here as a single span in Phoenix. And then it will take the inputs to this
method as the inputs, and then it will take any return from this
method as the output value. So if you saw before you were marking
the input in the output manually, this is a kind of convenience way
that makes it so that you don't have to define
those manually. It'll just happen automatically. And so now's a good moment. You've added a few different kinds
of instrumentation spans and traces. It's a good opportunity to take a pause,
run your agent and see what that looks like in Phoenix. So if you're going to run your agent here,
make sure that you're using your newly created start main span method and you can run that. But if you switch over into Phoenix, it should now see
you have some data in Phoenix to review. So if you open up Phoenix
and to open up Phoenix, there'll be a URL provided in the notebook
that you're working in. You open up Phoenix,
you'll start on this projects page. And if you remember,
you set the project name of Tracing Agent. So you should see there's now one trace inside
that you can click into that project. And you should see something that looks like this,
where one row here is your trace. You've named it Agent Run. You can click into this and see a few
different spans that have been marked. I'm going to expand this so you can see those. So each row here within
your trace is one span. And so your first one is this agent Run. So this was what was set with the with
clause inside of start main span. And then you have
the router call as a span. And so this was what was set with the
with clause inside of your start agent. And then you'll also have this tool
called chain span here which is the one that you created using that decorator
on your handle tool calls method. You'll also see these orange calls here,
which are LLM calls that are made to OpenAI. And so these are all coming
from the automatic instrumentor that you used at the very beginning of this video,
where you added the OpenAI instrumentor. So those are automatically
getting captured without doing any of
the manual instrumentation. And if you expand this a little bit you can see
some of the values that are captured here. So, starting in your agent run you have your input and output values
that are coming there. Similarly for router
you'll have your input and output as well. And then if you look at your LLM spans
you'll have a little bit more information. You'll have things like the user prompt,
the system prompt, the output. And then you also have
all the tools that were supplied. So you can see the tool definitions
that were supplied to your agent as well. And in any of these spans you can also
always go into the attribute section and see all of the information
that was sent to that particular span. So this is where you have all of the info. If you want to really
deep dive into some of these. Great. So, so far you've got your agent router and your handle tool calls method, as well
as some of your LLM calls being tracked. But you also have some tools
inside of this agent. And it would be helpful to understand when those tools are actually being called
and what the responses are there. So you can add in some tracing
for those tools as well. So to add tracing to some of your tools,
you have a few different options here. First, you can use those decorators
that you used for your handle tool calls method.
And that's probably the simplest way. So usually the recommended way
to go about doing that. So starting here
you have your lookup sales data method which is your first tool. And so you can add in a decorator
at the top to say tracer dot tool. And then again that will treat this as a single span
whenever this method is called. And then it will take the input
as this prompt value and the output as whatever the return of this method is. Now this particular tool actually calls
some other kinds of methods inside of it. It calls this generate SQL query method. And so it might be helpful to have
that as a separate span to say okay, first you want to have a span
for generating the SQL code and then a separate
one for running the SQL code. So what you can do is
if there's part of a method that you want to actually track
as an individual span, you can use the with clause
that you saw before. So you can add in here
before your SQL query is run. You can add in a with clause to say
start_as_current_span. In this case
you can call it execute SQL query and set the open inference
span kind as chain once again. And then you'll want to make sure
that this is indented so that it's part of that span
that you've created there. And then it's would be good to add
in some of the input and output values that go along with that as well. So, right before this
you can add in the input value. And so you can do span dot set input. And in this case the SQL query that's going to be called
would make sense as a good input. And then after your call is made you
You can say span set output and set status. With the result of that SQL query. And in this case you're defining it
using the parameter name. You can also just define it
by sending the parameter itself whichever way is easier for you to use. And then so now if you run this then that tool will have two spans
that it creates whenever it gets run. And we'll have one for the method itself
using this decorator here. And then it will have a separate span
within that other span nested below for specifically
the SQL query running itself. And it makes sense to do that in this case
because you might generate correct SQL, but then there might be some connection issue or something else
that prevents it from being run correctly. And it's helpful
to see where that error might be. So if you see that the internal span
here fails but the external one succeeds, then you know that there was an issue
with connecting to your SQL database in this case. And so finally you can add in similar
tracing to your remaining tools. And then that'll probably cover all the
tracing that you need for the agent here. And so this is fairly straightforward
to add in here. Your next method here
is pretty simple in this tool. So you can just use the decorator
to say trace this as a tool. Again
it will grab the input and output for you. Nothing really more that you need to do in
this case to trace that particular tool. And then for your data visualization tool, again, you can use the decorators as well. This is another case
where you have a two-step tool. But in this case you have multiple steps that are split
across two different methods. So you can keep things simple
and use the decorators because those contain
all of the logic for that particular step. So here for this extract chart config. This in itself is not a tool. This is just part of a tool. So it makes sense to call it chain here. And so you can say @tracer dot
chain as opposed to @tracer dot tool. For this extract chart config method. And then you can do the same kind of thing for the other method that gets called here
which is your create chart method in your @tracer dot chain. And also make sure that you run
any of these cells again as you added things to them
just to update that. And then finally
you can go to your last method here this generate visualization
and mark this as a tool. So you've marked three different tool
spans for your three different tools. You've marked a few different chain spans
within those tools. And you've marked your agent
and router spans as well. Now you've added
all the tracing that you need to so you can go back down
and run your agent again, and you should see some
more detailed information. And so
now if you jump back over into Phoenix, you should see you have a new trace
that's been run. So you should now have a second entry. And if you click into that, it'll look
slightly different than the one before. You'll have a few more spans here. Notably, you'll have this yellow
one of your lookup sales data tool. So that was one that you captured with
that decorator on your lookup sales data. And then within that you'll also have
a chain span for executing the SQL query. And look at the inputs
and outputs of those. this is the one that's been captured
using the with clause inside of your lookup sales data method. And if you ran more complicated queries
that you used other tools, you would see those tools
appearing as well too. So now you have all of the information
that you need to understand what's happening
inside of your agent at any given step.

---

## Lesson 7: Adding router and skill evaluations

Now it's
time to start setting up your evals. In this lesson, you'll focus on evaluating
each of your agent's skills, as well as the router's ability to choose the correct tool and execute
it correctly given a user's request. You will learn about three types
of evaluators: code based evaluators,
LLM as a judge, and human annotations. You will then apply the appropriate
evaluators to your agent example. Let's get to it. There are three main techniques
used for running evaluations. The first is code-based evals. Second is LLMs and judge evaluations. And finally, human annotations. Each of these techniques
can be applied to agents to measure and evaluate
different parts of your agent, but they can also be applied to other LLM
based applications. So each of these techniques
works for both agents and your more traditional LLM
applications as well. Code-base evaluations
are the simplest kind of evaluations when it comes to LLM or agent evals,
and are the most similar to traditional software
integration tests or evaluations. Code-based evaluations involve running some sort of code
on the outputs of your application. Some common
examples of these are checking to see if your output matches a certain regex. So maybe you want a response
to only contain numbers or no alphanumeric characters. You can use a regex to check to make sure
that your response matches that filter. You might also want to make sure
that your response is Json passable. or a very common
one that you see, especially in chatbots, is checking to see if the chatbots
response contains certain keywords. Like most often, companies don't want
their chatbots to mention a competitor, so you can do a code-based eval to see if that competitor name is ever
in one of the agent responses. But perhaps, maybe the most common type
of code-based eval is to use these evals to compare your applications outputs
to expected outputs. So if you have ground truth data of what
the expected output is for an input, then it's very effective
to use code-based evals to either directly compare the output of your application
to that expected output, or to use something like cosine similarity
or cosine distance to do more of a semantic match
between those two different values. The next technique for running evaluations is called
LLM as a judge. LLM is a judge,
as the name implies, involves using a separate LLM to measure the outputs
of your application. Typically,
the way that it's done is by grabbing the input and output of your application,
as well as potentially a few other key pieces of information
from one run of your application. Constructing a separate prompt
that's going to evaluate a specific criteria
based on those inputs and outputs. Sending that prompt over
to a separate judge or evaluator LLM, and then having that a LLM, assign a label on a specific access to that response. For one more example of how that works. You can examine this case
of evaluating the relevance of a document that was retrieved in a RAG system. The retrieval span in this case
is made up of a user query. And then the documents
that were retrieved for that given query. That query and then the reference documents are then sent into the separate,
eval template that you see here and then populated
so as to ask another LLM, "Are these reference retrieved documents
relevant to the user's question?" And then that separate
LLM will either say those documents are relevant or irrelevant. An LLM as-a-Judge is really powerful
because you're able to run large-scale evaluations across
both quantitative and qualitative metrics. However, it's important to keep a few
things in mind when using LLM as a judge. The first is
that only really the best models actually
align closely with human judgment. So if you're going to run LLM as a judge,
you often need to use a GPT-4o or Claude3.5 Sonnet
or similarly high-end model to do so. Even with these, though, a LLM as a judge
is never going to be 100% accurate. There will always be some margin of error,
because at the end of the day, you are using an LLM
to assign that particular label. You can mitigate some of this by tuning
either your LLM judge prompt or even your LLM judge model, and you'll learn a little bit more about
these in later modules in this course. Finally, it's always important to remember
to use discrete classification labels as opposed to undefined scores when
setting up the outputs of your LLM judge. So you should always use things like
correct versus incorrect, relevant versus irrelevant, and never a measure like "score
this response on a scale from 1 to 100." The reason for that is that LLMs
don't have a great sense of what constitutes an 83 out of 100 versus
a 79 out of 100, especially when they're evaluating
each case independently. So always use discrete
classification labels wherever you can. The third evaluation technique that you can use
is using annotations or human labels. The idea here is that you can use tools
like Phoenix or other observability platforms to construct a queue of lots
of runs of your application to construct an annotation queue,
and then have human labelers work their way
through that queue and attach feedback, or judge
the responses of your application. The other method that you can use
is actually gathering feedback from your end users. So you might have seen cases in the wild
where LLM systems have a thumbs up, thumbs down response system
where you can rate the responses of that LLM system. And you can use the same technique
inside your application to gather some feedback or evaluation metrics
about how your app is performing. When you
have these few different techniques it can be tricky to decide
which one to use for a given evaluation. One way to think about
this is how qualitative versus quantifiable or quantitative is the metric
that you're trying to measure. If you have something like evaluating
the quality of a summarization or evaluating the clarity of analysis,
that's a very hard metric to assign, quantitative
or code-based measurement to. So that's where you might want to rely on
LLM as a judge or human labels
to understand that qualitative metric. If you have something that's a little bit
more flexible or can be defined in code, like whether an output matches
a certain regex, then a code-based evaluation will work
in that case. The other way to think about these
is whether the evaluation needs to be 100% accurate, or if it can afford
to be less than 100% accurate. If you remember, LLM
as a judge is never going to be 100% accurate
or 100% deterministic kind of technique. So if you need 100% accuracy,
then you'll need to rely on either human labels or code-based evals. What you might notice here is that human labels
is sort of the best version of evaluation. In this case, it's
flexible and it's deterministic. However, in practice it can be hard
to get human labels at scale because it's a very labor
intensive process to do lots of labeling on your data. And if you rely on end users to provide
feedback, there is some selection bias there over
who chooses to supply feedback to your application.
So it's generally not advisable to use that as a large scale
evaluation technique. Now that you understand
that the techniques that you can use to evaluate an agent or really
an LLM application, now you'll learn about the different pieces of your agent
that you can apply these techniques to to run these evaluations. This lesson we'll go through evaluating the router
and the skills. And you'll have a future lesson in this course that goes into evaluating
the path in detail. Starting off with a router. Routers are typically evaluated
in two different ways. First, you'll evaluate the function
calling choice, aka did the router make the right choice
and choosing a function to call. And if you're using an NLP-based classifier
as opposed to an LLM with function calling, you can still evaluate
the function calling choice. And you still use this
sort of evaluation metric. The second kind of thing that gets evaluated in routers is typically
the parameter extraction. So once the router chooses
which function to call, does it extract the right parameters
from the question to pass those into whatever function
it's decided to call. One way to evaluate
a router is by using an LLM as-a-Judge. This is an example of the prompt,
the template that you would use for your LLM as a judge
to evaluate a router in this case. So you'll notice at the top
you have some instructions for the LLM judge
to say what it's going to be evaluating. You have some places where data will be
added into the prompt, in this case the user's question,
and then the tool call that was chosen. And then you have some instructions
saying the LLM judge should respond with a single word,
either correct or incorrect. And then you have some more details on what incorrect means
and what correct means in this case. And finally,
you have some tool definitions information so that the LLM judge knows
all of the possible options that your application had
when choosing which tool to call. Looking at the example here,
you might have a case where a user asks your agent, can you help me
check on the status of my order? Number 1234. And the agent says
"definitely" makes a tool call. In this case, choosing to call an order
status check method and then extracts that one two, three,
four and says this is an order number. So it passes it through as an order number
to that order status check method. And this all looks good. And it gets back a response
saying the order has been shipped. It goes back to
the user says your order has been shipped, and the user follows up and says
"okay, when will arrive?" And the agent decides
to make another call here, this time using the shipping and status
check method. That all looks good so far,
and then it takes that same one, two three, four and this time
as it has a shipping tracking ID in this case that's an order number
and not a shipping tracking ID. So here the agent actually failed
in the parameter extraction task, even though it succeeded in the function
calling task that it had. Now, when it comes to evaluating skills,
you can use a few different techniques to evaluate skills either
standard LLM-based evaluations or LLM as-a-Judge evaluations
or code-base evals. And one important thing to call out here
is that skills themselves are really either just other LLM applications
that have been composed into a skill. The agent can use, or other software
applications like API calls or application code that have again
been compressed into a skill. So all the techniques that you can use to
evaluate skills are really just the same techniques
that you can use to evaluate either standard software
applications or LLM applications. So you might use an LLM as-a-Judge
to evaluate things like relevance, hallucination, question
answer correctness, generated code
readability, or summarization. And then you might use code
based evaluators to evaluate regex matches Json parse ability in your response
or comparison against ground truth. Looking at your example agent,
you have three different skills here. You have a database
lookup skill, a data analysis skill, and a data visualization code gen skill. I invite you to pause the video here
and think of a few different evaluations that can be used to evaluate
each of these three different skills, whether the entire skill
or one single part of the skill. As in the case of this lookup sales
data tool, you have a step to prepare the database,
generate SQL, execute SQL. So you might have evaluations
on the full lookup sales data tool, or on one step of that process. So here are a set of evaluators
that you could use to evaluate each of those different tools. So for the database lookup tool
you could use either LLM as-a-Judge or a code-based eval
to do SQL generation correctness and see if the SQL that's generated
is correct. For the data analysis tool, you could use an LLM as-a-Judge
to check for clarity in the analysis, and make sure all of the entities
that are mentioned in that analysis are correct and match back to entities in the input
or other sections of their data. And for the data visualization
code gen tool, you can use a code-based eval to make sure
the code is runnable. Fairly straightforward eval
that you can run there. Now, it's important to mention
that you could have come up with different evals to use here. And again, eval is sometimes
more of an art than a science. And so if you came up with different ideas
don't be discouraged. Those could be just as correct
or in some cases more correct here too. The last thing
to mention is that you have SQL generation correctness being run with either LLM
as-a-Judge or code-based evals. You'll see what both
those look like in future notebooks. You can either use an LLM
as-a-Judge to judge whether this equals correctly generated, or you can use a code-based
eval to compare the SQL that's generated
against some ground truth data, or the result of that SQL
against some ground truth data. In this lesson, you've learned three
different techniques to run Agent evals: LLM as a judge, code-based
evaluations, and human annotations. You've also learned common types of evaluations
to run using each of these techniques. And finally, which pieces of your agent
should apply these techniques to you to evaluate. In the next notebook, you're going to apply an LLM
as-a-Judge and code-based eval to understand how these work in detail
with your example agent.

---

## Lesson 8: Lab 3: Adding router and skill evaluations

In this lesson, you're going to take the agent
that you've already built and traced, and now add some evaluations
to measure its performance. Similar to before, you're going to start
by importing some libraries that'll be used here. So there's some that you've seen
before like Phoenix and some other libraries here. And then you're adding in some new ones. So, specifically from Phoenix evals, importing some things like an LLM
as-a-Judge prompt template that's going to be used,
and some methods like LMM classify that are going to help you run
LLM as-a-Judge, evaluations. One other one that's important
to call out here is this nest_asyncio you might see.
This is used to run multiple calls asynchronously and simultaneously
to speed up some of your evaluation. You'll see where
that comes in in a second. Now again
in Phoenix there's a concept of projects. And so just to separate things out
from a previous notebook, you may want to use a different project
name here. So in this case
you could use evaluating agent. And then in this notebook
just to keep things simple, what's been provided for you
is the entire agent that you run that you set up previously is in the utils file
that's attached to this notebook. And so you're going to import
a few different methods from there. But if you run this you'll see
the same output that you saw before in the previous notebook saying "tracing
has been connected and set up there." Again this is all the code
that you created in the last notebook. It's just a pretty long notebook already, so it's been separated out
into a utils file for you. But this has been set up with your agent to run and connected
to the Evaluating Agents project. So here, anything that you call to run
an agent, start main spans either of those methods will be traced and
sent through into the Evaluating Agents project within Phoenix. It just lives in that separate
utils file to keep things clean here. You've also imported tools which are going to be used
for one of your evaluations as well too. So now when you're evaluating your agent, you can go for two different
kind of approaches to start evaluating it. One starts from a data set of examples. You can run through your agent and you'll learn more about that in the next modules
where you'll cover experiments. The other way is to run
real-world examples through your agent. Trace those examples
and then evaluate the performance of the agent using those traces. So, in order to do that, you can set up
some basic questions for your agent. Things like what was the most popular
product skew, total revenue across stores, some other kind of queries
that are going to come through there. And then you can loop through your agent
and call the start main span method that you imported above
with each of those questions. So this will just loop through each of those questions to your agent
and have those traced in Phoenix. So this cell will take a minute or two to run. Go ahead and kick off. Great. Now once your calls have all finished
running, you can jump back in to Phoenix and see the traces
for all of those different runs. If you start from the projects view, you should now have a new project
that says Evaluating Agent. And you got six traces in there. So you'll see a row
for each run of your agent. And you could click into those and see
more details on what that agent executed for that given step, including some calls that are using multiple different tools
that you can trace. Now, in order to evaluate your agent,
there's a few different pieces of the agent that make sense to evaluate
as you learned in the previous slides. So, one of those is the router. So you could evaluate this router call
that's being made where it's deciding
which particular tool to call. So that would be one thing to evaluate. Or you can evaluate
some of the skills like the sales lookup data skill
or the generate visualization skill. And now the pattern of evaluation
in Phoenix typically involves exporting spans
from your Phoenix instance, either using LLM as-a-Judge
or a code-based eval to add labels to each row of those spans
and then uploading them back into Phoenix. So let's start
by evaluating the router itself and using an LLM as-a-Judge to do that
router evaluation. So you're going to want to export
some of these spans from Phoenix. You can do that using code. But just to show how you would filter down
to the spans that you care about. For the router here
you really care about within the router call this first LLM call
that's being made. So if you look at this first
LLM calling, you can see
this is where you have a users question. And then you have the response here, is one of these tools. So in this case the lookup sales data tool. That was the response
back from the router. So this is all the information that you want to be able
to grab and export from Phoenix. And you can actually look at some of
the attributes here to see the information associated with these. The first is that you can see that there's
an open inference span kind of LLM. So that's one way
that you could filter by this. Or you could use any of the other
information inside of the attributes here to filter for this particular
kind of span that you want to use. Now back in your notebook to evaluate
your router using an LLM as-a-Judge. There's a template that's provided
as part of the Phoenix Library for this kind of evaluation, because this is a very common evaluation
that oftentimes people want to run. So this tool calling Prompt template is an
LLM as-a-Judge template that you can use to evaluate your function
calling of your router. So if you look through
what this is looking for, you can see all of the instructions
given to the judge. And one thing that you see here
is that there's two variables in this case up here, and one variable down below
that need to be passed in to the template. So, first is the question the user asked
and then the tool call that was made. It also looks for the tool definitions, which is a set of
all of the possible tools and their definitions
that could be called so the LLM can compare against that. So, next you can export the required spans
from Phoenix using some of those filters
you just saw in Phoenix. So there's a few things
that you can do here. So, first off you can use this span query method to set some sort of filter
that will filter down the spans in your project and export
any spans that match the filter. Here, you can use span kind of equals LLM. And this will give you all of the LLM spans
for both the router calls as well as other LLM spans. So you're going to do a little bit
more filtering in a second there. And then you can choose
which columns or attributes you want to export as part of that call. And so here you want to export import dot value and LLM dot tools. And you want to export them
using the headers question and tool call. Those headers are important
because they match, you scroll up a bit, they match what's going to be looked for
by your template. So question and tool call and then ask for
the input dot value and LLM tools. Those are attribute
names inside of Phoenix. So if you want to quickly jump
in over to Phoenix one more time, you can see in this case in your attributes. You can see input here dot value will give you the full messages
object that was input there. And if you scroll down further, you can see LLM dot tools here, you can see the tools
that that were chosen. So now you can export
those different values. Run this query on your Phoenix client and that will export
those particular spans. You can see
they're also passing in the project name. And then one other thing
that's being done here to filter down. Because again this will pull up all of the
LLM spans, even those that are not to do with tool calling or routing in this case. So you can also just use this dropna
method to remove any spans that were exported
that don't have a tool call. So they have no value here for LLM tools. That's an easy way
to just filter down to just the LLM spans that have to do with routing. So if you run the cell now you should see your tool calls
data frame. It's been exported. Should have two columns
question and tool call. And again those match what
the template above is going to look for. And then you'll have the question from the user
as well as the tool calls that were made. You'll also have this context dot span
ID column. This is what corresponds
to the particular span inside of Phoenix. And it's going to be what allows you
to upload the data back into Phoenix and have it
match up in a little bit here. So now you have this data frame. The next step is to add labels
to each row of that data frame based on your template above. So here's how you can do that. There's a few things going on here. First, the LLM classify method is a method
that's supplied by Phoenix that will take each row of your data frame
and run it through some provided template. So in this case
your tool calling prompt template. And then it will take a response. And in this case it will snap it to either
a correct or incorrect value. That just ensures that you have really
specific labels that are being used. Sometimes the LLM might respond
with correct with a capital C as opposed to lowercase. And so this rails function here
will snap it. So all the values are consistent. And then providing a model that's going
to be used to actually run this prompt. So this is your judge model
in this case using GPT-4o. And then this variable here will allow to provide an explanation
for why it shows that particular label. There's a couple other things
going on inside the code here. One is that this suppress tracing
tag up top. This has been added
because if you remember, your agent is set up to trace
any calls that are made to OpenAI. So if you didn't have this method saying, hey, turn off tracing
for everything happening inside here, then you would actually see some spans
tracked to your project for all of the evaluation calls
that are being made. So you want to make sure your LLM
as-a-Judge spans themselves don't get traced. So you're suppressing training there. And then on the template row here, there's
some kind of wizardry going on here to add in and replace the tool definitions
with your tools object. That's the idea here. So if you quickly
see your template from earlier, it's being passed in this tool's
definition, which is a definition of all of the possible tools
that could be called. And you want to make sure that that's
being replaced with the Json dictionary of tools
that your agent is using, so that your LLM judge knows
all the possible tools that could have been called,
so it can make its judgment appropriately. And finally, one other thing
that's happening here after your LLM judge runs, is you're also adding
in a score column that is just one if the LLM judge
label is correct, zero otherwise, that's used to have a numeric value
attached to your LLM judge, which is used in
some of the visualization. So now you can go ahead and run that and you'll see some LLM classified progress
bar being made. These calls are made asynchronously
because of the nest_asyncio library you imported all the way
at the beginning of this notebook. And then you should see a response
that looks like this, where you have some labels
as well as explanations. And then if you scroll to the right you'll also see
you have some scores, values 1 or 0. So now you've appended some labels onto your span IDs. The last thing to do
here is upload these back into Phoenix so you can visualize the data there. So you can use this log evaluations method
which will take a couple things here. It'll take the name of the eval
that you want to use as well as the data frame that you just created with
all of those labels and context dot span IDs. Now, if you jump back into Phoenix,
you may need to refresh your project, and then you'll see there's a new value
at the top here of your tool calling eval. And so you'll see a numeric value. Again
because you added that score and it's able to have a numeric
and a percentage value here. And then if you start
going into any of your runs and you click on your router span right here, you'll now see that
the feedback tab here has a new entry. And you'll see it's now labeled either
correct or incorrect. And then it has an explanation as to why
that particular label was chosen. And so you can use these to get some more information about what's
happening inside of your application. And you can actually filter down as well
if you want to go to spans as opposed to traces,
to see all of your spans in Phoenix. And then you can set a filter
for your evals to be tool calling eval, as a name of your eval. And then let's look at just
the incorrect ones. You can look at... And now you'll see there's cases
where your router was incorrect there. And you could click into those
and see the feedback as to why that particular run
was incorrect. Awesome. So now you've evaluated
your router using LLM as-a-Judge. You can add in some evaluations
for your skills as well. One that might make sense to do
would be evaluating your generated code
for your generate visualizations. And so one way you could do this
you can say okay I've got my tool here,
called Generate visualization. Why not export all of the spans for that Generate visualization. And then you can evaluate the code
that's been generated there. So you'll follow the same kind of pattern
as before. Start by exporting the spans
that you want to evaluate. And in this case
you can just use the name of the span equals generate visualization. Super easy there. And then you'll want to export
the output of that span. So you can run this. You probably just have one entry here
given the examples that have been run. And then instead of using LLM
as-a-Judge here, you can define a
code-based evaluator instead. So in this case you
can do a very simple evaluation of just: Is the generated code runnable? And so you could say okay
here is a method that will check for that. It will take some generated code. And it will do some quick checks
to make sure it doesn't have any extra string values inside of it. And then it will try to execute that code
returning true or false
depending on if there were exceptions. And now you can take that method and apply it to your code
gen data frame that you exported above. So you can apply the code as runnable method
here to your generated code column, and then map to the return values of true to runnable and false to not runnable. And then again, you want to add a score. So you can say that one is runnable
and zero is not runnable. And now if you run that method
you'll add in some labels there. You can
take a look at your generated data frame. And now you have some labels and scores. And finally you can upload this data back into Phoenix
using that same log evaluation method. And now if you look in Phoenix
you'll have a new entry at the top this time for runnable code. And it looks like the generated code
wasn't runnable. So in this case it's good eval
caught that for us. So you could use this at scale to run
more checks of your runnable code, this time using a code-based evaluator
as opposed to an LLM as-a-Judge evaluator. And there's a couple other tools that
you had that might make sense to evaluate. Another good example would be the data
analysis tool that you're using to generate analysis on top of any data
that's been exported. And so this one's another good one to use
LLM as a judge for. However, there's not actually a template
built into Phoenix for clarity of analysis. So you might wanna actually
define your own template in this case. So you can actually just define
your own template as text using whatever variables make sense here. And so in this case
you can create your own template and then follow the same pattern
as before. Export the information you care about. And in this case, one way you could export
relevant information is that you could look
for all of your agent spans, which are that top-level span,
and just look at the overall output value, because that's what you can evaluate
whether or not that was, correctly and clearly communicated. So you can export your top-level
agent spans. And then again make sure that when you're doing this,
you're matching any of the names here or the column headers here to whatever
is expected by your LLM as-a-Judge prompt. And now you can use the same LLM classify method, with tracing
suppressed this time using your manually defined
prompt to run your LLM as-a-Judge. And then once that completes, you'll have your new data frame
that you can upload back into Phoenix. You can call this one
a response clarity eval. And you should see that appear in Phoenix
under response clarity. In this case, it looks like 100% out 100%. And you had one third and final tool, which is your SQL code
generation and database lookup tool. So you can add a similar evaluation
for that. Again, defining an LLM as-a-Judge prompt. So in this case
you can see a SQL eval gen prompt. And then you can export relevant spans. So again in this case
you can export your LLM spans. And then you can later
filter down a little bit more specifically here to filter whether the question
that's being asked contains this: generate
a SQL query based on a prompt method. Oftentimes the hardest part of setting up
the evals is filtering down the right set of spans
and coming up with the right criteria. So just know that you can filter
based on anything inside of the spans, including string manipulation here,
or just looking to see if the prompt contains
a certain kind of value. Export your data there. Once again, run your LLM as-a-Judge prompt. And then finally upload
that data into Phoenix. And so now you should have four different
evaluators in Phoenix. You have one evaluator for your tool
calling and your router. You'll have one evaluator
for your SQL code gen, your response clarity
and your generated code visualizations. So at this point, you now have at least one evaluator
set up for each main part of your agent. And you can use these
to get some directional indications of how your agent is performing
across different types of queries.

---

## Lesson 9: Adding trajectory evaluations

In addition to testing your agents
skills and router capabilities, you need to ensure that your agent can respond to a user's query
in an efficient number of steps. In this lesson,
you'll learn how to assess this by computing a convergent score
and apply the test to your agent example. Let's go. Now what is an agent trajectory? A trajectory is simply the path
the agent takes through different router, tool,
and other logic steps for a given input. Looking at your example agent,
you can examine a few different trajectories
to get a sense of how these work. First, you can examine a query like:
"Which store had the most sales in 2021?" In this case, the agent would go from
the user to the router and then would go from that router to,
in this case, the lookup sales data tool,
as well as the data analysis tool. Back to the router
and then finally back to the user. Now one important thing to call out here
is that in this case, the agent has been built to allow for
multiple tool calls from one router step. So that's why you see both the Lookup
sales data tool and the data analysis tool being called together
in the one step between routers. Some agents limit their routers
to only call one tool at a time. That's just an architectural decision that
you can make when building your agent. To look at a more complicated trajectory. You might have a query like plot sales
data volume over time. In this case, your agent would go through
a user to the router to your to look up sales data and data analysis tools
back to the router, which then decides to call the data visualization tool
to generate that visualization code that would then return back to the router
and finally go back to the user. So these are pretty straightforward
trajectories so far. All told. But you can imagine that trajectories
get very complicated very quickly. Your example agent has three tools. But agents in production can have ten, 20,
30 different tools that they use. And even some systems will start
to compose multiple agents together. So those agents can work together
with each other to accomplish some sort of goal. In these multi-agent systems you can have trajectories getting
very complicated very, very quickly. Now you might be asking
if your agent's output is correct, does the trajectory really matter
all that much? And the answer is yes,
because efficiency matters in this case. Now, you might have a certain use case,
like if you're working on a hobby project or you're doing some research
where the efficiency of your agent doesn't matter.
That might be okay. But in most production agents or real world
agents, some amount of efficiency matters. If you can answer a user's question
in six steps as opposed to 11 steps,
that means fewer LLM calls. That means less variability. That means lower cost
and lower latency for the user. So how can you track and measure
trajectories? One way to do
that is using a tool called Convergence. Convergence as a measurement
for how closely your agent follows an optimal path for a given query. So you can think about this
as a measurement of how much your agent has converged towards an optimal path
for a certain type of query. So how do you test for convergence? Well, one way to do
it is using the following technique: You can run your agent
on a set of similar queries. In this case it could be
a bunch of questions that ask your agent to retrieve sales data from November 21,
and then construct a set of different graphs
or visualizations on that data. And the idea here is
you want questions that are similar enough where your agent really should take
the same path through each of them, but different enough
that there could be some variation that you can improve upon
within your agent. Next, you run each of these queries
through your agent and record the number of steps
taken for each of those queries, and then find the length
of the optimal path taken. In this case,
that's the minimum number of steps that your agent
took to get through one of these queries. Then you
can use all of those different numbers to calculate your convergence score,
which is a numeric representation of how often your agent
is taking that optimal path. Another way to think about the convergence
score is what percent of the time is your agent taking the optimal path
for that given set of inputs? So a convergence score of one means
that your agent's taking the optimal path 100% of the time, and your convergence
score will always be between 0 and 1. There's a couple things to keep in mind
when running convergence evaluations. First is that convergence evaluations
will typically not catch situations where your agent takes an unnecessary step every time
for every query in your test set. And the reason being here
is that the optimal path in a convergence eval is typically the minimum number of steps
the agent took to get through one of the queries. So again, if you have an unnecessary step
that's taken by all the runs of your agent, typically convergence evals
won't catch that situation. Second, you want to make sure
when running convergence evaluators that you're only running them
using four completed runs of your agent. If your agent takes three steps
to get into a problem and then errors out, you don't want to track those three steps
because that will skew your convergence evaluation data. In this lesson, you've learned
what trajectory and convergence are, why they're important
to track and measure. And then one way to measure
and calculate convergence. In the next notebook, you'll implement
this convergence measurement and evaluation technique.

---

## Lesson 10: Lab 4: Adding trajectory evaluations

So now that you've added some evaluations
to your router and skills for your agent, the next step is to evaluate the path or understand if it's taking an efficient
path for a given query. So in order to do that, again,
you're going to start by importing a few libraries
that will be useful here. Most of the things
you've already seen for Phoenix. And then now you've got some new things
from Phoenix for what's called experiments, which
you'll learn about in just a second here. So you can import those libraries.
And one other thing to call out is that, again, the agent's been imported
from your utils method here. So, you have the same agent that you've
been working with the whole time. You're importing that run agent method. So just know that that code
is sitting in the background. And then here you're still going
to need to connect to the Phoenix client. So in this case I'll just save that
Phoenix client variable. And then the way that you can evaluate
your trajectory as you learned in the previous slides, is by running
a set of queries through your agent and then tracing the number of steps
taken by each of those queries. So in order to evaluate the trajectory
here, you have to actually compare multiple
runs of the agent together. So in order to do that, you're going to use a tool
called a run experiment within Phoenix, which allows you to run
multiple different runs of your agent and then compare those
to each other in certain ways. So here's a good point to pause
and dive a little more into experiments and how they work. Experiments in Phoenix
are made up of a few different steps. First, it's taking a data
set of different test cases, then sending those into a particular task
or job to run and then evaluating
the results of that task. So a data set of test cases
is going to have a bunch of different queries or questions
that you might run through your agent. And typically you'll have an input value
inside of those. examples
as well as maybe an expected output. In this first case,
you won't have an expected output. You'll just have an input. Sometimes you have expected outputs,
sometimes you don't. And that dictates some of the evaluators
you can use later on. So you have a set of examples here. And then you'll run those
through a version of your agent. So in this case just going to use
one single version of your agent. You'll get the outputs
from that particular round. And you'll see actually that you made
some slight modifications to your agent to actually track the number of steps
taken as well as part of that task. So you can define the task
for your experiment. And then once you've collected
all the results of each example through your task, you can
then send those to a set of evaluators. And those evaluators could be
the ones you set up in previous rounds. Or in this case you can do
more of a comparative evaluator, comparing different runs of your agent. And so in this case, there's another variable
that will be added to each example, which is the output of that
particular example through the task. And you'll learn a lot more
about experiments in the next lesson as well too. This is sort of
just your primer for them in this case. So step one there is creating a dataset of test cases. So the way that you can do that
is you have a set of questions. In this case convergence questions. And if you think back to the slides, one of the ways that you test
for convergence here is you send a lot of different
variations of a similar type of query through your agent
and then track the number of steps taken. So notice
that each of these different examples here is all about the number or the average
quantity of items per transaction. So you see the average quantity sold per
transaction mean number of items for sale. Calculate
the typical quantity for transactions. You see these are all kind of variations
on the same question. So the agent should take the same path
for each of these. But sometimes there's variation. So you can take this list of questions,
create a data frame out of them and then upload
that data frame into Phoenix. So now you have a data
set that lives in Phoenix. If you want to,
you can quickly visualize it here Now, if you want to look in your Phoenix window, you can actually see
under the datasets tab here, you'll now have an entry for the data
set that you have just uploaded. You can click into that. And you can see all of the different
examples that you've uploaded. And now you can use this data
set to start running experiments. So for the next step here you have to
define the task for your agent. Now you could just run these examples
through your agent. But again you want to have some count
of the number of steps that were taken. You might want to format
some of the messages so you can make slight tweaks
to your agent as well. When you're setting it up as a task. So in this case, I do a couple of things
here. One is actually create
a method that will format some of the message steps
which you can come back to in a second. And then you'll create a task here
that is run agent and track path. So starting with this task
you'll see it takes in an example. So if you remember each row of that data
set is an example. So you can see in this case
you're taking in an example variable. And then it's calling. It's taking the input value
from that example. And then calling the run agent method
on that particular example. And then finally calling
that format messages step. So the return from this run
agent and track path, it's going to be the length of the messages
inside the agent as the path length. And then the actual message is object. And then this format message step really
just is going to go through all of the messages
in your agent's log. And it's going to format them in
a little bit easier to read sort of way. So you can see the two calls that are made
and make it a little bit easier to compare here. So now with your task ready and your data set defined,
you can start an experiment. So to do that
you'll call this run experiment method. And then what this will do is it'll take
in your data set as well as your task or your function that gets applied
to each row of that data set. And then you can come up with a name. So in this case convergence eval
and a description. So if you run that now,
each row of your dataset will be run through the run
agent and track path method. And you'll get results back. That'll take a second to run because
it's equivalent to 17 runs of your agent. So give that a second to complete. Now you should have some results
that look like this. You'll see all those runs completed. And you can actually click
and see the results of that experiment inside of Phoenix. So if you click into that,
what you'll see is in your dataset, you now have an entry for experiments. And you have this first run
of your experiment that you named convergence eval. And you can actually click and see
all of the outputs for you to run there. In this case looks fairly successful
on each of our runs. And so now what you can do is
you can actually go back into the code and you can apply evaluators to each of
those different experiment runs. And so here's where you can essentially
implement your convergence evaluator. And so because you just run
your experiment, you have written that experiment has something that
you can apply and access in your code. So you can always view the results
of that experiment as a data frame where you have the output, input
and other various columns there. And so that's one thing that you can actually use
to run your convergence eval as well. And so in order to calculate the convergence
first you need to calculate the minimum number of steps that was taken
by all the runs of your agent. And so to do that add in code here to first take your experiment as a data
frame like you've just done above. And then look at the output column
and turn all of those different, variables into values that you can access,
and then calculate the minimum or optimal path by using the minimum
function on the path length variable
within each of those different outputs. So this is just going to give you a number
for the minimum path length taken. So if you run that you should get something says the optimal path length is
you should probably see five in here. That's a that is the optimal path length
that's being used. And one important thing to note
is just the way that this has been set up so far is it's counting. Every message has the path length. So it is including things like
the system message and the user message. That's fine in this case because you're
comparing a bunch of different examples that all include both those variables
or both those messages. You just want to make sure
that you're consistent. So if you include the user message
in the system message again that's fine. You just got to make sure that you do it
on every example that you're testing with. So now you can create a method to use as your evaluator. And in this case you can use
this, evaluate path length method which is going to take an output
and compare it, the path length of that output to the minimum or optimal
path length that you calculated earlier. You're also you're going to use this
create evaluator decorator here. This is totally optional but it allows you to name the evaluator
that you're going to run here and see. Or it'll mark
how it shows up inside of Phoenix. And so now you can take the experiment
that you've already run and use this evaluate experiment
method to take in the experiment. And then this evaluate path length
method that you run above. And that will take all of the results
from your experiment and run them through any evaluators that you add in here. AKA in this case, the evaluate path length and it will give
you a score at the end of it. That'll go pretty quick
because it's just a basic code-based eval. And if you jump over into Phoenix now, you'll see that your experiment,
if you go back to your dataset, you'll now have a column here
for convergence eval. It's named that because of the decorator
that you attached. And in this case
we've got a perfect score of one. Our agent has taken the correct path. Every example here. You might see a different value here. Every time we've run
this we've gotten a different value. So you may see a different value
here for one. And that'll give you an idea of whether or not your agent
is converging towards the correct path.

---

## Lesson 11: Adding structure to your evaluations

So far you've learned
how to evaluate your agents skills, router and path convergence. You'll now
learn how to combine your evaluators into a structured experiment to iterate on
and improve your agent. Let's dive in. Evaluation-driven development is a concept
that involves using evaluations and measurements from your agent
to help guide where you spend your time improving and iterating on
and developing your agent. Evaluation-driven development
is made up of a few different steps. First, you curate a data set of test cases
or examples that you can send through
different variants of your agent. Next, you send each of those different test
cases through those different variants of your agent,
each time changing things like the model you're using, the prompts you're using,
or the agent logic. And then once you run those different test
cases through those different variations of your agent,
you take the results of all of those different experiments
and run them through your evaluators. Those evaluators
will give you a set of scores that you can then use
to compare the different iterations of your agent on an apples to apples
basis. Now, this is presented
linearly in the visualization here, but in practice
this tends to be more of a cycle, especially as you move
your agent into production. LLM apps require kind of iterative
improvement as you're working on them. And so typically what will happen is
you'll you'll go through this full process, your release or agent or you'll
get it into some other people's hands. And then you'll realize that you wanted to add in different test cases
or different evaluators. And so you can always update
and change each of these different pieces as you're going. And then you can create a flywheel here,
where you're incorporating information from production back into your development process
using evaluation-driven development. Diving into each of these steps
in a little bit more detail. You start by curating a data set test
cases. And the idea here is to be
more comprehensive than exhaustive. You can have a set of examples that are representative of the inputs
that you expect your agent to receive. And you just really need 1 or 2 examples from each of the different types of inputs
that you might get. You don't need to have hundreds
and hundreds of examples, especially if there's
similar types of examples. And these examples can come from either
live runs of your agent or can be constructed
beforehand, manually, or even in some cases,
and generated using another model. In practice,
you often start by constructing the examples yourself,
and then add to them from live data. As you release your agent. And then wherever possible, it's always good to include expected outputs
along with your test cases. You may not always have expected outputs,
but if you can include those, it unlocks different types of evaluations
that you can run. LLM as-a-Judge, evals can be used
even if you don't have expected output. But certain code-based evals do require
an expected output to compare against. With your data set in place
and your test case is in place. Then you can start to make changes to your
agent and track each of those changes. So, some tests that you can often do are changing things
like your prompts used by your agent, changing the tool definitions
that you're passing into your router, changing the router logic itself,
changing some of the skills or the skill structure, or just swapping
in a new model that you want to test out. And the
practice of sending each of your test cases through a variation of your agent
is often referred to as an experiment. We are experimenting
with a certain version of your agent. And you can use those experiments
to record and measure results from each of those different runs. Once you have all your experiment
data collected, then you can use all of your evaluators from the previous lessons
that you've built and apply them
to the results of those experiments. So you can use your code-based evaluators,
your comparison against ground truth, or checking if generated code is runnable,
as well as the convergence evaluators that you run. And you can use your LLM
as-a-Judge evaluators, like function calling,
analysis, clarity, and entity correctness. Now, how can you apply this to your agent? As a quick reminder, your agent is set up
to use this OpenAI router with function calling and then three
different skills that you can evaluate. First, taking an example of how you would set up an experiment
around with a router. You might have an example test case that looks something like this
where you have an input, which is which stores
have the best sales performance in 2021 and then an expected output. In this case, the database lookup tool is
the tool should be chosen by the router. And then you might want to experiment
with trying different tool descriptions. So if you think back to the Json object
that you pass into your LLM router, you might want to modify the description
that's given to each tool to see if that improves
your router performance. And then once you have
those experiments run, you can evaluate the results
using either code based comparison against ground truth. Because here you have
that expected output. You have that ground truth data. Or you can use a function
calling LLM as-a-Judge. Taking another component of your agent. You have your database
lookup tool or skill, and you might have a test case
that looks something like this, where you have the same input
from the previous round. And then in this case, the expected output
is some SQL code that you see there. And so if you notice here that SQL code is an intermediate step
within your database lookup tool. First, it generates SQL and then it runs
that SQL and gets an output. So that's one thing to keep in mind here
is that again you can evaluate just the SQL generation
part of your database lookup tool. Invite you
to pause the video here for a second, and see if you can think of an experiment
and some evaluations that you could run on this database lookup tool. So one experiment you could do would be testing
different SQL generation prompts. You could also test different models
or other pieces of that as well. And then you can use your code based
comparison against ground truth evaluator, similar to what you had looked at in
previous notebooks as well, because you have that ground truth
to compare against. Next, you look at the database
analysis tool. In this case, you might have a test case
like the one you see here where you have a message from a user,
and then you actually have some retrieved data. Because the database analysis tool takes in both a user question
as well as some data to analyze. So you'd have to have both
those pieces in your test case, and then you don't actually
have an expected output in this test case. So once again,
I invite you to pause the video and see if you can think of an experiment
and then an evaluation that you can run in this case. So here you want to experiment could be testing different
LLM models. You could also test different prompts
or other kind of logic changes there too. Then you can use the analysis
clarity and entity correctness LLM as-a-Judge evaluations from previous slides and notebooks
that you've seen to evaluate the results. And as you structure
all of these together and start to run multiple iterations of your agent
with multiple different evaluators and create a whole process around this,
you can end up with, a dashboard or a heads-up display
that looks something like this. Each row has one run of your agent, and then all of your evaluators,
those different columns here, and you can measure, okay,
what are the effects of each change that I'm going to make to my agent across
not just one part of the agent, but each part of the agent holistically. And then again, as you
start to move your agent into production, you'll find that you're going to come up
with new test cases, new evaluations, and new changes
that you want to make using some of that production
monitoring data that you have. And then you can bring that back
into your testing and development process. So this whole experimentation framework
and this whole evaluation driven development framework enables you to not just create
a strong application in development, but also incorporate production learnings
that you have into your development process
and create a large flywheel here that you can use to create a better
and better agent over time. In this lesson, you learned the purpose
of evaluation-driven development, what it is and how it works,
and you learned how you can structure experiments around your evals
to scale them as you continually improve your agent. In the next notebook, you're going
to implement some of these techniques and create the visualization
that you saw just a few slides ago by adding lots of evaluations to the agent
you've been working on so far, and structuring them into an experiment.

---

## Lesson 12: Lab 5: Adding structure to your evaluations

In this final notebook here, you can take everything
that you've learned and compose it all together
to create one large experiment, to be able to test out all the different parts
of your agent at once. So you'll combine some of the evaluators
that you created in previous notebooks, along with the experiment structure here, to create an easy
way to iterate on your agent. As before, import some different libraries
that you're going to use. These should look familiar
at this point in your LLM classify by some of the experiment functions
that you might use. And then from utils some functions
including the agent that you've been working on so far. Now, you're going to run a few different
evaluators. So it's helpful to define a few eval model
at the beginning saying this is the evaluator LLM judge model
you're going to use throughout. And then you're also going
to be accessing the Phoenix client. So you can go ahead and add
in the Phoenix client. Now, you're going to use one big experiment
to actually structure this code here. And so the first step is creating the data set that will be run
through for that experiment. So to start out with
you can create a data set here. and this is a pretty big data set. Here you have the questions
that are being inputted. You also have some ground truth data
like the SQL results that you expect for those questions, as well as some ground truth data
about the SQL generated for some of those questions. Because you're combining multiple
different evaluators here, you have some multiple examples
of ground truth data that's being added. But again, you'll use the same syntax
as you used previously to create a data frame out of those examples
and then upload that data frame into Phoenix
under the name Overall Experiment Inputs. Now, one of the thing that's important
to note is because you have multiple keys this time, when you upload a data
set into Phoenix, you define which of those keys are input values, so in this case just the question. And then which of them are output values. So these are your expected outputs. So your SQL result and SQL generated keys. Run that and your
data set will be uploaded into Phoenix. You can take a look in Phoenix
within the data sets section. You may need to refresh your Phoenix
to have that appear. And then you'll now see you have this
overall experiments input data set. And if you click into any of these examples you'll see that
each one has input keys for question and then expected output keys
for SQL result and SQL generated. Now you might be asking why we just have ground truth data
for the SQL result in SQL generated. The reason for that
is that you can still use LLM as-a-Judge when you don't have expected ground
truth data to compare against. So for some of the other tools
you can use LLM as-a-Judge approach where you don't need that expected value. So on the subject of LLM as-a-Judge, now it's time to define all of your different
evaluators that you're going to use. And there's two different LLM as-a-Judge
prompts that you might want to use here. And these should look familiar
from the previous notebooks that you run. So if one is your LLM as-a-Judge
for clarity and your response. And then another here is for what
we're calling entity correctness. So in this case,
this is another type of LLM as-a-Judge that you can run on the output
of your model or your data analyzer step to check to make sure that any, any variables that are mentioned,
any SQL columns or anything like that are mapped correctly in the input,
the data throughout the run, and then the output. This is basically making sure
that your agent doesn't start referring to SKU or skew columns as store IDs, or something
along those lines. Now you can define
your evaluator functions. And so you can go one by one for these
starting with the router. So, for your router
you're doing a function calling eval. And because you're using this
in the context of an experiment, you can expect that
this is going to be sent an input. And then an output. In some
cases you also have expected output. In this case you don't have ground truth
data for function calling. So you just have an input
and then the output. This is the original input that agent got. And then this is going to be your output
from running your agent. So what you'll do is from that output grab
some of the tool calls that were made. That'll be one of the entries
in the output. And then you can construct together a data frame using the question as one key. And then any of the different function
calls as the other rows here. And the reason that you're constructing
a data frame is one so that it works nicely
with the LLM classify method. And two, because you might actually have
multiple tool calls per question here. So you might have a case where a question came in and your agent
decided to call two different tools. So this structure here
will create a data frame that's two rows with the question
and the tool call column. And then you're going to use your LLM
as-a-Judge, LLM classify method here again
using that data frame. The tool calling prompt template as before
exactly the same code that you ran. Previously to run your LLM
as-a-Judge for function calling. A couple notebooks I got there. So you can define that method, and
then here you're returning back the score. This is going to be the mean score here. Because again, you could have
two different LLM as a judge or two different functions
that were called by your agent. So you're going to have to have some way
of reporting back the overall score for this run. Now, you can start evaluating your tools. So one of those tools is going to be
your database lookup tool. And so you can grab a method to evaluate your database
lookup tool. And so in this case
it's evaluating the SQL result. And now if you think back to the data
frame, you'll remember that you have some ground
truth data. You have some expected responses
for SQL generation. So in this case you will still have
the output of your agent. But then you're also going to ask
for the expected value. So these are going to be
the expected ground truth responses that you have
that you defined in your data frame. And so first it's
checking to make sure the outputs there. And then it's grabbing
any kind of SQL result from the actual output that was run. And in this case it's going to grab
all the two responses from the output. And then this code here will actually loop
through all the different tools that were called
in that particular run of the agent. And then it's going to look for one
that matches the name lookup sales data. And the idea there is
you want to make sure that you're just looking at the tool
call responses here that are for that lookup sales data
method. You don't want to look
for your other two tools in this case. And then once you have
that as your SQL result, then you're going to grab the actual response
from that particular tool. So all of this code here is just getting
you to a point where the SQL result equals the SQL that was generated by your agent
when it ran. And now you can do one more step here,
which is to pull the numbers, specifically the numerical values
out of that SQL result. And then also out of the expected
target SQL result. So this here is your expected value
that's in your data set. And the reason to pull out
just the numbers is because in SQL you can define columns in your responses
and things like that using different names. And this just allows you
to make sure that you're not having a case where your agent use a slightly different
column name in its response. And still got
the correct numerical result. And then this will return true or false,
depending on if those numbers match. Now, one thing you'll notice here
is that in this case, you're using a code-based evaluator
to evaluate your SQL generation. If you think back to a couple notebooks
ago, you actually used an LLM as a judge to evaluate your SQL response. Either of those approaches can be used.
If you think back to the slides, LLM as-a-Judge will work. It may not be 100% accurate. So the method you're looking at here
to compare against ground truth is generally going to be a more accurate
kind of evaluation. But at the same time it relies on
you having some of that ground truth data. So it relies on
you having those expected values which you may not have in large amounts
or large scales. Okay. Now moving on to your second tool. You have your data analysis tool. And there's actually
two different evaluations you can run for your data analysis tool
that match the two prompts you saw above. One is to evaluate
the clarity of the response. And so in this case you can use
an evaluate clarity method here that takes in the output of your agent
and the original input to your agent. And then it will construct a quick data frame out of those
using the query and response columns, because that's what's expected by your
LLM as-a-Judge prompt. And then it will call the LLM classify
method. And classify the result of that particular
run of your agent. So this one is exactly the same
as the previous LLM as-a-Judge that you ran
a couple notebooks ago for clarity. It's just now put into this function
that you can call that knows to expect things like the input in the
output from different steps. Similarly, you can add another evaluator here
for entity correctness. Again, same exact kind of flow. So you'll have a method. You'll create a data frame
out of the input and the output. And then you'll call LLM classify
using your LLM as-a-Judge prompt. So now you've got evaluators
for your router your tool one. Your tool two. Finally, the last piece here is your tool
three. Which again you can use one that you've used previously here to check
if the generated code is runnable. To evaluate tool three
you can use a code is runnable evaluation here
this time you don't need the input. You don't have any expected values
to compare against. You just have the output. So what you can do is
you can take that output and you can again
pull out any tool call responses. This is similar to what you did
for the database lookup tool. So all of this code here is just getting
you to a point where generated code equals the code that was generated
when the tool name equals generate visualization. And then you can take that and make sure that you have stripped away
any extra characters that are used there. And then at the end here, you can just run
your execute on that generated code. If it executes correctly, return true. If not, return false. So this is the same evaluation
that you used a couple of notebooks ago, just with some extra manipulation to get it to look for the specific output
here. Great. And now you have your data set, as well as all the evaluators
that you want to run on your experiment. The last piece that you need is your task. And so you can define a task method here. In this case run agent task. And it's going to take that example. Grab the input question from it
and then run your agent on that. Now you can define that. And one other thing to call out here
is there's this process messages method that's called. This is also in your utils function. And it's just going to take the output
of your agent and process the messages to match
a little bit cleaner of a format to read. Now with your data set and your task
and all of your evaluators defined, you're ready
to run your giant experiment here. So you can use the run experiment method. You're passing in the data
set the run agent task. And for evaluators, you can pass in all
your different evaluator functions here. And what will happen is now each row of that data
set will be run through that agent task. And then the outputs of that will be run
through all of your different evaluators. Go ahead and run that. And that will take a second to run. So once that completes
you'll see that you run seven different tasks through your agent. And then you'll see a bunch of output here
around all of the different evaluations. So you'll see again, you're running
35 evaluations here total because it's five evaluations
for each seven case. So you'll have quite a bit of output here. That's all normal
and it's all looking good. You'll have some graphs and then you'll finally have some scores at the bottom
for some of those different runs. And now if you jump over into Phoenix
you'll see a detailed view there as well. To make sure you go
to your overall experiments input here. And then you'll see a bunch of different
columns for all those different evals. So it looks like all the code is runnable. The evaluation analysis is clear. The entities are correct. It looks like some issues with
SQL generation and then function calling. So you could jump into this experiment
and see it in more detail. So you could see all the tool calls and all the format of response that
you have here for some of these pieces. So you could click into those and see more
if you wanted to. And now the question becomes
what do you do with this information? How do you improve your agent? And so you've got really two options here
for how to improve your agent. One is in code. You can go in and start
making some changes to your agent and running different versions
of your agent using the experiment. So SQL generation was a little bit
tough there. So why not start with changing up
the SQL generation prompt. So this is your base SQL generation prompt
that's being used by our agent. We can add something here like think
before you respond. You might make bigger changes to it. This is just a pretty basic change. But one you could try out. And then we have a helper function here to just update that SQL generation prompt. In practice,
you probably go into your agent code. You would actually make the change
in the agent code. This way, we'll do that
same kind of thing here. And then you can rerun your experiment and you'll because you've updated
your agent, that task is now a new task. So you might want actually change
this experiment name to say V2 and evaluating the overall experiment with changes to SQL prompt. And then you can run that experiment again
and you'll get a comparable line. And so now if you scroll
through those results, you'll see similar kinds of outputs before. And then you can continue going down,
see all the results that were run. And you'll have your same scores
from before. You can jump over into Phoenix
to see those in detail. And now you may have to refresh your page. You should see a new entry for your
in second experiment for your V2
and then changes to the SQL prompt. And so it looks like
if you look at the scores there, looks like SQL didn't
really have the change that you wanted. So you might have to have
some more changes from there. And one of the things it looks like
some of the responses that came back are less clear or correct
this time. That could be due to the change you made. It could be due to just the fact
that you're running with seven test cases here,
which is a sort of small amount. So it's always good to do
multiple runs of each experiment to get some more statistically significant kind of data back as you're
testing your agent's performance. So you can continue to make changes
inside of your agent, either to one part of your agent or multiple parts of your agent
to try to boost these scores over time. And you could continue
to make those code changes until you get to the results
that you want with your agent. There is one other approach that you can
use as well too, which is in Phoenix, there's a tool called playground
where you can jump into the playground button here, and that will bring your data
set into a playground environment where you can make whatever queries
you want over your data set. And so you could actually take that
same SQL generation prompt and run it directly here on your data
if you want it to. So you could copy over your prompt
from your notebook and paste that in here. And then in this case,
you might want to have it look for specific variables
from your inputs and outputs. So in this case if I use curly braces
you can add these curly braces. And then you'll actually pull
in the question from that particular row. So you could use this. And if you then ran this you would then have results for each row
that you could look at. You can use the compare button that will
add a second iteration of the prompt. In this case you're using GPT-4o-mini. So you can switch that to 4o-mini. And then similarly over here
have consistency there. And so you could actually make your changes
to your prompts directly in the UI here. And then this will give you a side by side
comparison of the responses. So you could always make the changes
to your agent in your code itself and then run them as a new experiment. Alternatively, you can use this
prompt playground tool to run changes directly in the UI and have a little bit faster
of an iteration cycle as you change them. No matter if you
use either of these different techniques, you can make changes to your agent and use
your new experiment that you've created to have a really easy apples
to apples way to compare what are the actual facts
of each of those changes, so that you're not just moving
things around without understanding what the effect of each change situation
might be. So you now have a structure
that you can use to iterate on your agent and compare
all of those different iterations to each other in a structured way.

---

## Lesson 13: Improving your LLM-as-a-judge

For this lesson, you'll dive into
how you can improve your LLM evaluators and LLM as-a-Judge
evaluations within your agent. The idea here is that as you use
LLM as-a-Judge, you may want to improve the evaluators themselves, as
those are never going to be 100% accurate as you've learned in previous lessons. So this serves as a bonus lesson here
where you can learn how to improve those evaluators as you go through the process
of improving your agent itself. So if you think back to the previous slides lesson,
you might have noticed a case where you used both a code-based comparison
against ground truth and an LLM as-a-Judge function calling evaluation
to measure the performance of your router. And you might be thinking, why would you need to use two different
evaluators to evaluate the same thing? Especially because the code based
evaluator is going to be 100% accurate. So why would you add in the LLM as-a-Judge evaluator? Well, the answer there is
that you can use this technique to actually measure how effective
and how closely your LLM as-a-Judge evaluator aligns to your 100% accurate
code base comparison against ground truth. Because as you remember, LLM as-a-Judge is not 100%
accurate method. However, it can scale a lot further beyond
the comparison against ground truth. You could apply an LLM as-a-Judge eval
to all of the runs of your application if you want it to,
but it pays to know how accurate that LLM as-a-Judge is compared
to your 100% accurate evaluation method. So you can use experiments to actually
improve your LLM as-a-Judge itself. The experiments that you just learned about in a previous
lesson, can still be applied this time to your LLM as-a-Judge,
as opposed to to your agent itself. It's a little bit meta, but you can use the same techniques
to judge your judge in this case. So you could set up an experiment on the function
calling LLM judge. And you might have an example test case
that looks something like we see here where you have an input. That's which stores
have the best sales performance in 2021 and then an output in this case
the database lookup. And the important thing is that everything in red
there is the input to your LLM judge, because you're having your LLM judge
judge the performance of that agent. So everything in red there is the input. And then you'd have your expected output
in this case is correct. So that expected output
is your ground truth data. And then you could set up the experiment
to test different versions of your LLM as-a-Judge prompt. You might change
some of the wording there. Or you could add things
like few shot examples. So you could add in some examples
of previous judgments made that were correct to help align
the judge into that prompt as well. And then you can evaluate
the performance of your LLM as-a-Judge using the code-based comparison
against ground truth. In this case, comparing to that correct
or incorrect expected output label. And you can use the same approach
for another LLM as-a-Judge that you're using, in this case
the one you're using to evaluate analysis clarity. And so in that example, you might have an input
that looks something like you see here: in 2021 the stores that perform the best,
yada yada. And then the expected output of the
analysis is clearer because of x, y and z. And this time
you might judge different types of models that are being used to create that
judge label. You could also test different LLM as a judge prompts similar
to what you did in the previous example. Now the question here though becomes
how do you evaluate that output? Because while you have expected output,
it's no longer a clean just correct or incorrect label. It's this expected output of the analysis
is clear because of something. And so what if your LLM as-a-Judge
comes back with the analysis is easy to understand
because of x, y, and z. That should be correct. But you can't just compare
those strings exactly. That's where you can use something
like semantic similarity to compare the meaning
of each of those strings in a numeric way, as opposed to doing a direct comparison
between output, unexpected output. So in this lesson, you've learned
how you can measure and improve your LLM as-a-Judge evals using structured experiments. And your next and final lesson,
you'll learn about moving your agents into production
and monitoring those agents in production, as well as wrap up all the lessons
that you've learned here in the course.

---

## Lesson 14: Monitoring agents

After
you develop your agent and improve it until it's production ready,
you need to apply the same techniques of tracing evals and experimentation
to your agent in production. During production, things like code changes or model updates can degrade the performance of your agent. You can use your evals and run experiments
to continuously monitor and improve your agent. Let's get to it. As a quick recap, you've covered
four main steps that take you from an initial agent prototype all the way
through to a production-ready system. Choosing the right architecture, you need to decide on an agent framework
that matches your use case. Deciding which eval to use. Figuring out which metrics really matter
for your system, such as accuracy, latency,
and convergence. Building your evaluation structure,
which includes the prompts, tools, and data
you'll use to measure performance. Iterating with your data,
you keep refining your agent by analyzing results, adjusting prompts
or logic, and testing again. This cycle repeats as you move
from development to production and back again, so you can catch issues early
and refine based on real-world feedback. When you actually reach production,
you may find that the simple agent designs you use
initially need to scale up and complexity. You might end up
adopting a multi-agent system where agents can call
other specialized agents, or a multimodal system where your agent
handles different types of data, like text or images or audio,
or a continuous improving system where your agent learns
from user interactions in real time, either through manual updates
or automated processes. So, what's different about production? Well, you can often discover new failure
modes. Users might ask you questions
that you never saw in development or they reference something
that your system doesn't know about yet, like a brand new product. If your agent now calls out
to additional APIs or other agents, there are more chances for errors
or unexpected outputs. You might also try A/B testing
or different model strategies that introduce surprising regressions that you didn't anticipate
in a controlled environment. The encouraging part here is that a lot of the tools
you use in development, like instrumentation and feedback
loops, are just as valuable in production. You'll continue to collect metrics
that you define for evaluation, and you'll rely on continuous integration
and continuous delivery flows and ongoing experiments
to keep tabs on your agent's performance. In other words, you can use those
same tracing and annotation methods you had in development, only
now, they're enriched by real user data. You'll gather
feedback from actual interactions, label any problematic outputs, and identify
where your agent might be struggling. Collecting user feedback
for evals is crucial in production. You can take real usage data, for example,
every user query or interaction, and attach human-labeled annotations
to highlight issues or successes. If your eval metrics disagree
with what real users say, that's a sign you might need to recheck your system
or your eval. Maybe you're measuring the wrong metric. Or maybe there's a deeper logic
flaw and the agent's flow. You also want to keep track of metrics over time to understand efficiency
or execution dependencies. For example,
if you're using convergence evals, you can see how many steps it takes
for the agents to reach a correct answer. If that number grows after you tweak
your prompts, it can indicate a regression since you're likely calling external
LLM APIs, you should track those calls, too. They can have a significant impact on latency and costs,
which can impact your end user experience. Your choice of model, perhaps a large reasoning model versus
a smaller, faster one may vary based on the complexity of tasks
in production. Keeping an eye on those decisions
and their downstream effects is part of robust production
monitoring. When you gather human feedback
and run your evals on real traffic, you'll gain a clearer picture
of how changes like swapping out a model or updating a prompt, impact
the overall system. You can rerun the same experiments
you used in development, but now on new data or new failure modes
that you've discovered in production. This is why you'll want to maintain
consistent data sets and keep augmenting them
with production samples. One effective approach is curating golden
data sets that capture your most critical use cases
and known failure modes. Each time you push a change,
like adjusting a prompt or logic, you can recheck these data sets to be sure
you haven't broken something you've already solved. Experiments can act like gates
for shipping changes, so you can decide whether to roll forward
or roll back a change. Let's imagine you have a self-improving
agent that collects feedback automatically whenever a user interacts
with your system. You can add those user examples,
both successful and failed interactions,
to a continuously updated data set. Then you run
CI/CD experiments on this data set, checking
if new versions of the agent do better or worse on the very latest
real-world scenarios. When you refine the agent logic
or tweak prompts, you can also incorporate few shot examples
from the newly collected data. This lets your system learn from mistakes
and gradually converge towards better performance
on exactly the tasks that matter most in a self-improving and automated manner. What you're doing here
is essentially applying evaluation driven development in production. You're watching for new failure modes, monitoring how well your agent
handles them, and automating feeding production
feedback back into your evals. In this lesson, you've learned what to watch out for new queries,
complicated architectures, and unexpected user behavior,
and how to keep your agent on track by continuously measuring
and refining its performance. You've also seen how the tools and data
you used in development carry seamlessly over to production,
and how you might scale those approaches for even more robust agent systems, by using CI/CD pipelines
with consistent experiments, you can ensure that every update
to your agent maintains or improves on the quality
you've already achieved. Now, you have a solid foundation
for monitoring your agents in production and continuously refining their
performance based on real-world data.

---

## Lesson 15: Conclusion

Throughout this course, you learned how to trace, evaluate,
and improve a code-based agent. You can now take what you've learned
and apply it to any other agent framework. Please check out the resource section
that we've included after this lesson. And I can't wait to see what
you'll build on your own.
