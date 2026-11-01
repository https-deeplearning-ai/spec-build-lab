# AI Agents in LangGraph — Transcripts

---

## Lesson 1: Introduction

Welcome to AI Agents and LangGraph. Built in partnership with LangChain and Tivoli. Taught by Harrison Chase,
co-founder and CEO of LangChain, as well as Rotem Weiss
who is the co-founder and CEO of Tavily. Harrison, it was not quite a year ago
that we're working on our first course on LLM frameworks. And back, then we had an ancient
example, but, you know, it was a little bit of a struggle
to get it to work. Since then, I've seen many teams
successfully build AI agents. What was your view on that? Yeah, that's exactly right, Andrew. We've seen many people successfully
building agentic applications now, and I think there were a couple of key
improvements over the last year. First, function calling LLMs have made
tool use much more predictable and stable. And also specific tools like search
have been adapted for agentic use. Yes. If you think about it,
when you do a query on a search engine, it will return multiple links that you can
then follow to find answers. However, what an agent really wants are answered that you can
then reference to the link. Also, the agent needs predictable
formats for its results. This is exactly what Agentic Search
provides. That makes sense. And by the way, I'm
personally a user of LangChain and Tavily. And the reason for being excited
is of both of you here. And let me start by
describing agents and agentic workflows. let's say that the three of us
are going to write a paper together. Maybe I would start with some planning and try to put together
an initial outline of the paper. Yeah. And I can take it from there
and do some research, maybe run some queries and compile documents
related to our topic. Okay, I guess that leaves me
to write the first draft. I hope it's not a long paper. Yeah, yeah. Short paper. Hopefully. And then
after that, I might veto the paper. Try to make some constructive suggestions
and hand it back to Harrison to see if he wants to make some changes or to Rotem to see
if he wants to do some more research. and so on. And this would be an example of an agentic
or an agent like workflow, in which we iterate
to produce a work product. And, in contrast
to how people often use LLMs to write essays today,
which is served by the prompt and the, write the essay for the first work
to the last word in one shot. This type of iterative workflow
gives a much better work product. In fact, as a person,
I don't write that well. If you force me to just write from start
to finish with no backspacing allowed. So concretely, you can similarly prompt an LLM
to tell it to write an outline, prompt an LLM to write a draft or revise
prompt an LLM to do research and so on. But to dive a bit deeper, let me share
what I think are some of the key design patterns of agentic workflows. First, I think there's planning,
which is thinking through the steps to take like the outline
and what to do after that. Then tool use.
Knowing what tools are available and how to use them, like our search tool.
Reflection, which refers to iteratively improve a result,
possibly with multiple LLMs critiquing and making useful suggestions
to drive that type of editing cycle. Multi-agent communication. So you can think of each of us
as playing a role again to an LLM with a unique prompt to play a unique role
in this process. And then memory, that is tracking the progress and results
over the multiple steps. Now, some of these capabilities
are related to the LLM itself,
like function calling for tool use. But many of these capabilities
are actually implemented outside the LLM by the framework that they operate in. Exactly. And the LangChain framework has
had many of these elements for some time. Memory is available in multiple forms.
Supporting function calling,
LLMs and tool execution are available. And we talked about this in the last DeepLearning class we did, functions tools and Agents course. But LangChain has recently updated
its support for agentic workflows. Here's some examples of agents
that we now better support. So, ReAct agents was an early paradigm
for building agents,
and ReAct stands for reasoning and action. Another example
that we recently added support for is the example presented in the Self
Refine paper, where it does the iterative refinement
that you were talking about. And most recently,
you can see the alpha coding example. Which creates a coding agent
using flow engineering. And from all these diagrams
you can see that these agents and their behavior is defined
by a cyclical graph. And to support directly building agents like this, LangChain
has extended to support LangGraph. In this course, you will start by building
an agent from scratch with just an LLM and Python. Then, you'll learn about the components
of LangGraph by rebuilding that same agent
using the LangGraph components directly. Since search tools are such an important
part of many agent applications, you will learn the capabilities
of agentic search and how to use it. There are two additional capabilities
that are helpful when building agents. First,
is being able to receive human input. This allows you to guide an agent
at critical points. The second is persistence. This is the ability to store
the current state of information so that you can return to it later. This is great for both debugging agents
and for productionalizing them. We will build a project using LangGraph, but you'll have to reach the last lesson
to figure out what it is. And at the end, I'll describe
some of the cool applications and future directions
I see for this technology. Many people have worked
to create this course from LangChain. I'd like to thank Lance
Martin and Nuno Campos. From Tavily, Assaf Elovic And from DeepLearning.AI. Geoff Ladwig. All right. We don't want to keep those agents
waiting. Let's
go on to the next video to get started.

---

## Lesson 2: Build an Agent from Scratch

In this
lesson, we'll build an agent from scratch. You'll see that all agents can do fairly
complex tasks. A basic agent is actually not that hard
to build. As we're building this agent, it will be useful to notice
what jobs fall to the LLM and which are managed by the code
around the LLM. What we call the runtime. Let's dive in. The agent we're going to build from scratch is based on the ReAct pattern. ReAct stands for reasoning plus acting. So in this pattern, an LLM first thinks about what to do
and then decides an action to take. That action is
then executed in an environment and an observation is returned.
With that observation, The LLM then repeats. So, then thinks about what to do again,
decides another action to take, and continues
until it decides that it is done. The code that we will be using to start with, is based on this blog post from Simon
Willison. It's a great introduction
to implementing the ReAct pattern in Python. To get started,
let's import everything we need. We can then initialize the language model. For this, we will use OpenAI. Let's try it out once just to make sure that it's working. We can see that
we pass in hello, world and get back. "Hello. How can I assist you today?" Great. We're set up and running with our language
model. Let's now create the agent. We'll start
by creating a class for the agent. We'll want this agent to be parameterized
by a system message. So we'll allow the user to pass that in. We'll then save that as an attribute. We'll also keep track
of a list of messages over time. This is where we will append
everything that happens in that ReAct loop. And to start it off,
if there is this system message, we're going to append a system message
in this list of messages. Okay great. So our agent can now be initialized. But what exactly is it going to do? Let's implement
the call method for this agent. What we want
this method to do at a high level is to take a message that comes
in, that is a string, and then append that message
to the existing array of messages. We'll then execute a function
will implement that right down below, and we'll then take the result of that
and add a new message into the array of messages. This time, coming from the assistant. So let's implement that execute method. In the execute method. this is where we call the OpenAI client
that we initialized above. So we'll be using this GPT-4 model. We'll be setting the temperature
equals to zero. This will make it very deterministic. And we'll pass in this list of messages
that will accumulate. We'll then have this method return
the content or the string of the message
that it gets back from the model. So, this is our agent. Awesome. Now let's get started
with creating the ReAct agent. The ReAct agent is going to require
a very specific system message. So let's go ahead and write that out. And we can take a look at that in detail
to see exactly what we're doing. Let's take a look at this prompt
in more detail. So we're asking it to run through this loop of, thought,
action, pause and observation. It can then output an answer
when it's finished with that loop. It will use thought to describe
its thoughts about the question it's been asked. It will then use action to run
one of the actions available to it, and it will then return pause.
After that, observation will be used to signal the result
of running those actions. We then tell it what
the available actions are. So we give it access to calculate
an average dog weight. And we'll implement those down below. Finally, we
then provide an example of this in action. This example is really helpful
for helping the language model understand. And a little bit more specific detail
how exactly it should be doing things. And we can see here an example trace. Incoming question
and then a thought and then an action. Then pause. And then it gets back an observation. And then we'll tell it to output. Answer. We now need to provide the two tools
that we mentioned above. So we have a calculate function. And this just takes in a string. And it will eval that string. And then we have this average dog
weight function. And we're going to mock with some returns for Scottish Terrier,
border collie, toy poodle. And then we'll create this
little dictionary that maps the name of the function
to the function itself. And we'll see how we'll use this down
below. Note that
these functions are just a toy example. And in your real use case,
these are going to be more specific to the problem
that you're trying to solve. Let's now try it out. Let's initialize the agent with the
prompt that we created above. Let's then
call it once with this initial question. 'How much does a toy poodle weigh?' We look at the result and we can see that
there's a thought action and pause. So the thought is: I should look up the dog's weight
using average dog weight for a toy poodle. It then outputs an action.
And this is all one string. But the second part is outputting
this action "Average dog weight, toy poodle." And then it says pause. What this means we should do is that we
should look up using average dog weight. How much a toy poodle weighs. And so let's do that. We get back this string, and this is just what we mocked out above. We can now format that into the next
prompt to pass to the language model. And then we can call the agent
with that next prompt. Doing that we see that we get back. Answer: "A toy poodle weighs 7 pounds." If we want to see more details
about what exactly has been going on, we can take a look at the message
attribute on the agent. We can see that
we first have this system message. And this is the long prompt
that we wrote out above. We then have our first question
"How much does a toy poodle weigh?" We then have this response
from the language model, which tells us to take this action. We then have our user message
representing this observation saying how much a toy poodle weighs. And then we have
the final assistant response, which says our final answer
that a toy poodle weighs 7 pounds. Let's
try this again with a different example. In order to do that, we're going to need
to reinitialize the agent in order to clear all the messages
that have already accumulated. We're going to ask it
a more complicated question this time. "I have two dogs,
a border collie and a Scottish Terrier. What is their combined weight?" We can see this
first thought, is a really good plan. It realizes that it first needs to find the average weight of each breed,
and then add those weights together. And so the first action that it takes
is calling average dog weight with Border Collie. Let's execute that action and create the next prompt. I can now
call the agent on this next prompt. I can see that it responds that
we now need to take a different action. We need to call average
dog weight with Scottish terrier. So let's do that. We do that and create another prompt
which we can again pass to the agent. This time it tells us to use the calculate method with 37 plus 20. Okay great. Let's run that action. We run that action
and we get back another prompt, which we can pass yet again
into the agent. Doing that, we get back a Final answer. "The combined weight of a Border Collie
and a Scottish Terrier is 57 pounds." Now that is output the answer string. we know that it's finished.
So this is great. We have a tool calling the agent,
but it's still a little bit manual. Let's automate it. Let's put it in a loop. The first thing I'm going to do is create this regex
for looking for the action string. This is going to let us parse
the LLM's response and determine whether we want to be taking an action,
or whether it's the final answer. Let's now create this query function. This is going to take in a question
and run the same process that we just ran manually. I'll add this max turns parameter
so we can control how long this runs for. We can then start a counter to keep track of how many iterations we've done. We can initialize an agent with the default system prompt. We can then define a query function,
which we'll use to run this loop. It'll take in a question. And we'll also let it take in this max
turns parameter, which will control how many iterations
the agent can run for. We'll start a counter
and we'll set this to zero. We'll create a new agent by initializing the agent class
with the default system prompt. We'll also create this next
prompt variable to keep track of what we should be passing to the agent,
and set this equal to the original question
in order to start. Let's now start our loop. So while our counter is less than max turns,
we'll first increment the counter, and then we'll call the agent
and get a result back. Let's add a print statement just to see what that result is. We'll then use the regex that we created above in order
to parse the response from the agent, and we'll get back a list of actions. Here's where we will decide what to do based on the response. So if there are any actions,
we're going to add some logic to take those actions and get back
a response if there aren't any actions. And this happens
when the agent outputs answer, Then we're going to return
and end the function there. So what exactly are we going to do? If there are actions to take. First, we're going to get the action
and the action input. So the action is the function to call. And the action input
is the input to that function. So we'll get those two things. And then if we see an action
that's not in our list of known actions we're going to raise an exception.
This should never happen. But we'll we'll do this check
and raise this exception just in case. And let's print out what exactly
we're going to be running here. We'll now get the observation. And so we'll do this by first looking up in the action dictionary
the action that we should take. And so this action is a string right here. We're looking it up in this dictionary. And we're going to get back a function. We're then calling that function
on the action input. And the result of
that is what we're saving as observation. Let's print out the observation
just for some debugging. And then let's also create the next prompt
what we'll send to the language model the next time. And this is just a string with observation
and formatted with the observation that we got back from the agent. All right. Let's call this on the complex question
that we had above and see what happens. We can see that
it first thinks about what to do. Outputs in action, calls it, gets back an observation. Thinks about what to do again
and gets another action. Thinks about what to do again,
gets another action. And then finally
it comes up with this answer. That was a lot easier than running it
by hand. That shows how we can create an agent using nothing but the raw LLM API
and some Python code. In the next lesson,
we'll take the same agent and show how to implement it
using LangGraph. See you there.

---

## Lesson 3: LangGraph Components

In the last
lesson, you built an agent from scratch. Now let's implement
the agent using the LangGraph. And along the way, introduce
some of its components and features. All right. Let's get coding. All right, so let's break down
what exactly we did in the last lesson. We had this user message that came in. We then had the system prompt. And this was this very long one. We then called an LLM along with that. This output something like what's right there, a thought and an action. Based on that, we then made a decision. We would either return
or we would call a tool, and we put this all in a big loop. This query function. And we had these two tools that we would
call "calculate an average dog weight." And if we called the tool we would get back an observation. And then we'd loop back in, to the prompt and would put that observation
as a new message. So let's break this down into LangChain
components. First, let's talk about prompts. So prompt templates
allow reusable prompts. And what this basically means is that we
can create something like this, right here, a little string with some formatted
variables that we can replace. And so those formatted
variables can come from user content. So we can have this prompt template
that we format in different ways depending on the user content. If you want to see a bunch of examples
of these prompt templates, you can actually see them in the LangChain
hub. So here is one that's very similar
to the agent prompt that we just used. So you can see here it says "answer
the following question as best you can." You have access to the following tools. And here we don't hardcode
the tools themselves. But we have this little variable. And the same with tool names down here. And then we have the input here. And this is the user question.
And then the agent scratchpad. And these are all the actions it takes. And the observations. If you want to see more prompts
you can go to the hub here. And you can see a bunch of prompts that
people in the community have contributed. The next component in LangChain
that we have is tools. So here's a Tavily tool. And this is the search
that we will be using from here on out. You can see that
we import it from the LangChain community package
which contains hundreds of other tools. Maybe
the biggest part of this application, the most code that we wrote,
was this function that would loop. And that's represented
by all these arrows, here. And that's one way to think about LangGraph. LangGraph helps you describe
and orchestrate that control flow. Specifically,
it allows you to create cyclic graphs, which is exactly what we have here. It also comes with built-in persistence. And this is really nice
for having multiple conversations at the same time, or remembering
previous iterations and actions. This persistence also enables really cool
human in the loop features. If you look at these diagrams here,
and these are all diagrams of agents from academic papers,
these are all represented as graphs. And that realization was
what led us to create LangGraph, an extension of LangChain specifically
aimed at agent and multi-agent flows. Crucially,
it allows for really controlled flows. So in these diagrams
there's really specific arrows
leading from one box or state to the next. We've seen that this controllability
is crucial for creating agents that can perform well. Three of the core concepts of LangGraph are nodes,
edges, and conditional edges. Nodes are agents or functions. Edges connect these nodes,
and then conditional edges are used when you need to make decisions
about which node you should go to next. So let's take a look at an example
of a LangGraph you can create that is equivalent to the function
that we wrote in the lesson before. We can have an agent node.
This is the LLM. We can then have a conditional edge
which takes the result of that LLM call and decides
what to do next. One of those edges can be an action edge
which calls a function node, and that automatically
loops back to the agent node. There's an entry point,
which is where you start, and then there's the end node, which is the other action
available to take after the agent. One of the most important things
to understand when working with LangGraph is the state
that is tracked over time. This is often called the agent state. This is accessible at all parts
of the graph at each node in each edge. It is local to the graph
and it can be stored in persistence layer, meaning that you can resume
with that state at any point in time, later on. Looking at two examples,
we first have a simple state where we just have this list of messages.
Taking a closer look, we can see that this message variable is
a sequence of base message. Base Message is a LangChain type. It's annotated with operator.add. This means that when the state is updated
with new messages, it doesn't override the existing messages,
but rather it adds them to that state. Let's take a look at a more complex state. Here we have input, chat history,
agent outcome, and intermediate steps. They all have their own different type. Three of them are not annotated
in any way. This means that when a new update
is pushed to that variable, it overrides the existing value there. However, intermediate steps is annotated. It's annotated with operators.add,
which means that when a new update is pushed there,
it adds to it. This makes sense because intermediate
steps is what is tracked as the agent action and agent observation
throughout the graph as it executes. And so we want to continuously add to that
as more and more actions are taken. Getting really specific
about the previous agent that we created and how that would map
to a LangGraph object. We can see that we will have one node. We'll call this call OpenAI. And this will call the LLM. We'll then have a conditional edge
which will check for the existence of an action to take. And so we'll call this 'exists action'. And then we'll have another node
which actually executes that action. We'll call that 'take action'. And the state that will track
is pretty simple. It's just this list of messages
to which we add over time. With that high-level overview. Let's dive into the code. Let's first load in any environment
variables that we're going to need to use. This is our OpenAI API key. We're now going to import a bunch of things
that we need to create these tools. Agent state. And the LangGraph itself. First, let's import state graph
and this end node from LangGraph. We'll see how we'll use those later on. These typing imports and operator
are used to construct the agent state. We then have all these different message
types. These are LangChain message types
that we'll use to represent the human in AI and system messages. From LangChain
OpenAI, we're going to import chat OpenAI. This is a LangChain wrapper
around the OpenAI API. This is exposes a standard interface
for all language models, meaning that even though we're going
to use chat OpenAI for this lesson, we can actually switch it out
for any of the language model providers that LangChain supports without having
to change any other lines of code. Finally, we're going to import Tavily,
the search engine that we're going to start
using as the tool. In this example. Let's first take a look at the tool. We'll create the tool by initializing Tavily search results with max results
equals two. This means that will only get back
two responses from the search API. We can see that it's of this type
and it's got a specific name to tavily_search_results_json. This is the name that the language model
will use to call this tool. Let's now create the agent state. This is exactly
what was in the presentation. It's just an annotated list of messages that we will add to over time. Let's now create our agent. As discussed,
we're going to need three functions. We're going to need one function
to call OpenAI. One function to check
whether there is an action present and another function to take that action. These will all be different
methods on this agent class. So let's create those first. And we can then
see how they interact with each other. Let's now create the agent class. We're going to want this agent to be
parametrized by three different things. A model to use, the tools to call, and the system message as before. Let's save the system message
as an attribute. We're
now going to start creating the graph. First, let's initialize
state graph with the agent state. Right now this graph is pretty bare. It doesn't have any nodes or edges
attached to it. We know that we're going to want to create
those three functions before and use them two as nodes
and one as edges. So let's sketch it out and then we'll implement those functions
as methods on the class. So first we know that we're going
to want to create a node called LLM which will execute the LLM. And we can do that by doing graph, add node, LLM. And then we're going to come back here. And we're going to need to pass
in the function that we want to represent this node. We'll add another node, the action node. We'll do the same thing here. Now we're going to add
that conditional edge. This goes after the LLM is called. It checks
whether there's an action present. If there is
then it goes to the action node. If there isn't then
it goes to the end node and it finishes. So let's add this again. We'll have to add
the specific functions later on. The first argument we pass in
is the node where the edge starts. This is from LLM. The second argument we pass in is the function
that'll determine where to go after that. We're going to implement this later on so we'll leave this blank. The third and final argument that we're going to pass
in, is a dictionary representing how to map the response of the function
to the next node to go to. So if the function returns true
then we're going to go to the action node. If it returns false
then we're going to go to the end node. We're now going to add a regular edge. This is going to go from the action
node to the LLM node. So we can do this by calling Add edge. The first argument is
the start of the edge. The second argument
is the end of the edge. We're then going to set an entry point
for the graph. This is at the LLM node. With that done, we can compile the graph. Graph.compile
is just what we need to call after we've done all the setups and we'll
turn it into a LangChain runnable. A LangChain runnable exposes
a standard interface for calling and invoking this graph. Well, we'll see more about that later on. We'll save this
as an attribute on the class. We'll also save the tools
and the model that we passed in. For the tools, we'll create a dictionary
mapping the name of the tool to the tool itself. For the model, we'll actually call bind tools
on the model passing in the list of tools
that we passed into the agent. What this is doing is
this is letting the model know that it has these tools available to call. All right. So we've created this graph. But we still need to create three things. We need to create the function
representing the LLM node. We need to create another function
representing the action node. And we need to create a third function
representing this conditional edge. We'll add all of these as methods on this agent class. For the LLM node, we're just going to create a function
called call OpenAI. It's going to take in this state this
agent state all the nodes and the edges. We'll take this. Then what we'll do is we'll get the list of messages
from the state. We'll then add in the system message
and we'll then call the model. We'll then return this dictionary
with a list of messages. But there's only one message in it. It's the message
that's returned from the model. Again, remember
because we had annotated the messages attribute on the agent state
with the operators.add, this isn't overwriting this. It's adding to that state. We can then go back to the graph.add node
and change that to pass in this method. Let's now do the same for the action node. The action node will also take
in this agent state. We'll get the last message
from the list of messages. We know that if we've gotten to this
state, the language model must have wanted to call some tools. That means that there will be this tool
calls attribute present on the last message in the agent state. Crucially,
this can actually be a list of tool calls. So, a lot of the more modern models support parallel tool or parallel
function calling. What we can now do is
we can loop over these tool calls. We can find the relevant tool
by looking up tool name in the dictionary of tools
that we created. We can then call invoke on it passing in the arguments that we have
from this tool call. We can then append this as a tool message
to this results list. And then we're returning these messages
mapping to these results thing. Again, this is just the new messages
that we need to add. What's happening under the hood
is that LangGraph is adding that to the state in between iterations. Let's go back up and let's put
this here, in the action node. Finally,
we need to define our conditional edge. So, this is what's going to take
in the result after the LLM is called. And return a boolean either true or false,
representing whether we should take an action
or whether we shouldn't. In order to do that,
we're just going to get the last message from the state, which is the most recent
call from the language model, and we're going to return length of that
message dot tool calls greater than zero. So basically if there's any tool calls
we're going to return "True". If there's none, then we're going to return
"false". Let's set this as the conditional edge. And with that we have our agent. So let's start to use it. We create a nice little system
prompt here. We initialize chat OpenAI. So this is the language model
we're going to use. And for our list of tools
that we're passing in, we're just passing in our one,
our Tavily search tool. One of the cool things we can do is we can actually visualize this graph
we just created. So if we get the graph
and then called docket graph and then .draw_png, we actually get an amazing
visualization of the graph itself. This is all done automatically. So let's now call this agent. So let's first call it with this: "What is the weather in SF?" Question. In order to do this, we're going to create this human message
representing a user message. We're then going to put it
in this list of messages. And note that we have to do this
because the state that the agent expects to work with has this messages attribute,
which is a list of messages. So we need to make it conform
with that state. Once we have this input,
we can call the agent.graph.invoke with this
and we can get back a result. So we added some print statements
in the agent. And so we can see that
it printed out what it was calling and it was calling Tavily
search, results, json. And it was calling it with current weather
In SF, San Francisco. And then it prints out back to the model. This means we're going back to the
model. If we look at result. If we look at result we can see that
it's a list of messages. So result, is the final state
that the agent ended up in. If we just want to get the final message
in this list of messages, we can go into the messages attribute. Get the last one
and look at the content attribute. And we can see that
the current weather in San Francisco is partly cloudy,
blah blah blah. Let's now
try this with a more complicated question. So "What is the weather in SF and LA?" We can see that it first calls Tavily
search results json. With the current weather in San Francisco. Then before even going back to the model,
it calls Tavily search results json again,
with current weather in Los Angeles. This is an example of parallel function
or tool calling. Finally, it goes back to the model
and after that, it has all the information, it needs. So it responds. And if we look at the final message. We can see that we get back a response for both San Francisco and Los Angeles. Let's
try an even more complicated question. "Who won the Super Bowl in 2024?" "What is the GDP of that state?" We can see first, it calls Tavily with the query
2024 Super Bowl winner and then goes back to the model. It then calls Tavily again, this time
with the query "GDP of Missouri 2023." Then goes back to the model. And finally, it's done. And if we look at the final response,
we can see that we get. "The Kansas City Chiefs won the Super Bowl
in 2024 for the GDP of Missouri, where the Kansas City Chiefs are
based, was 400 something billion. And the third quarter of 2023." So the difference here
is that in order to make the second query, it actually had to know
the result of the first query. So it calls one tool, then goes back to the model in order
to enable it to call the second tool. This is a little bit different
from parallel function calling. And it's not happening in parallel.
It's happening sequentially. And the reason it's happening sequentially,
is it actually needs the result of the first query,
in order to make the second query at all. With this, we've seen how we can take that raw LLM and raw Python example
with some fake tools and turn it into a real agent
that can answer complex questions. Under the hood, it's
using the Tavily search API. In the next lesson,
we'll learn a lot more about that.

---

## Lesson 4: Agentic Search Tools

A frequently used tool in agents is search. This lesson is going to dive into
how agentic search is different from standard search
and how to use it. Let's try it out. All right,
so before diving into what an agentic search does, let's understand
how an agent might use it. In a zero shot learning an agent
would receive a prompt and will produce an answer
based on its static weights of the model. As powerful as it's proven to be, there are many limitations
to this process. First, the data on this is dynamic. So we couldn't, for instance, ask
about the scores from the game last night. Secondly, in many use cases,
we would want to know the sources of the information provided in
the result. This can reduce hallucinations and smooth the friction of this human-computer
interaction. Looking at the slide, we can see
the prompt is received by the agent,
which then decides to call the search tool. Then the information found
is returned to the agent. Now, let me show you what happens inside. This is an example of a very basic search
tool implementation. Let's go over it step by step. If the agent decides
it will send the query to the search tool, the first step would work on
understanding the question and divide it to sub-questions if needed. This is an important step
because it can handle complex queries. Then, for each subquery, the search tool
will have to find the best source. Choosing from multiple integrations. For example, if an agent would ask
"How is the weather in San Francisco?" The search tool should use the weather API
for best results. the job doesn't end
with finding the correct source. The search tool would then have to extract only the relevant
information to the subquery. A basic implementation of this
can be achieved through a process of chunking the source, and run
a quick vector search to retrieve the top-K chunks.
After retrieving the data from its source, the search tool would then
score the results and filter out the less relevant information. Okay, so let's test it out. Okay. So first, let's import some libraries and do the initial connection
to the search tool. Here we loaded Tavily
API key from the environment variable. And then we created the Tavily client which we imported from the Tavily library. All right, so after creating
the initial connection, let's test it out. Here, I'm going to run this search
asking about Nvidia's new Blackwell GPU. And let's see what's the answer. All right. As you can see there's
a pretty simple answer but very accurate. Okay, so let's do a simple example
to see the difference between a regular search tool
and an agentic search tool. I'm going to create a simple query
about the weather in a certain location. Feel free
to change the location to your location. I'm going to do it with San Francisco. So, the query is "What is the current
weather in San Francisco? Should I travel there today?" Now, let's try to attempt
it with regular search. Here, I'm going to import the DuckDuckGo
search. I'll try to run a regular search
and get the links. The links
that might lead me to the answer. Okay. So as you can see, we did get the results,
but it's not what the agent meant. Now we're going to have to get
some answers from these results. Let's do that. Okay. So now we're going to create the function that can scrape the data
from the first URL. We're going to use Beautifulsoup
to extract the html. As you can see that's a beautiful output. And if you want
you can keep scrolling down. But let's try to clear it up. Okay. To clear it out,
I'm going to use some parsing. I'm going to extract the headers
and some content. I'm going to strip it down
and use a join to get the text. As you can see, the output is much,
much better, but still not concise enough. Okay. After seeing this let's try to run
it using the agentic search tool. We're going to do the same query
and call the Tavily to get the results. As you can see, we got a simple json with a lot of information
about the weather in San Francisco. Let's clear it out
so we can see a formatted json. Okay, now we'll parse it and highlight the json just so we can see it clearly. As you can see, this is not the answer
I would want to see as a human. But this is the exact answer an agent would want, a structured
data. Okay I'm going to load the sample from Google Search so you can see the difference. Here. I get exactly what I want to see as a human. A nice image showing me the temperature,
the humidity, the wind. But not unnecessary data. That's exactly the difference between
what a human needs and what an agent needs. Okay. That was an introduction
to agentic search. In the next lesson, Harrison will discuss
persistence and streaming.

---

## Lesson 5: Persistence and Streaming

When building agents, they're often
working on longer
running tasks. For these types of tasks, there are two really important concepts. Persistence and streaming. Persistence lets you keep around the state of an agent at a particular point in time. This can let you go back to that state
and resume in that state in future interactions. This is really important for long
running applications. Likewise, with streaming, you can emit a list of signals
of what's going on at that exact moment. So for long running applications,
you know exactly what the agent is doing. Let's see these concepts in action. So to get started, let's create our agent as we did before. We'll load in the appropriate environment variables. We'll make the necessary imports. We'll create our Tavily search tool again. We'll create our agent state. And finally, we'll create our agent again. Now we're going to add in persistence. In order to deal with persistence, we've added the concept
of a check pointer into LangGraph. A check pointer basically checkpoints the state after and between every node. To add in persistence for this agent, what we'll do is we'll use a SqliteSaver. So this is a really simple check pointer
that we've added that uses Sqlite, a built in database
under the hood. And we'll just use the in-memory database. So if we refresh this notebook
it'll disappear. But you can easily connect this
to an external database or we also have other check pointers
that use Redis and Postgres and other more persistent
databases like that. Once we initialize this check pointer,
the way that we can use it, is we're going to pass it in
to graph.compile. So in order to make this easy,
let's add another parameter to agent. That is check pointer. And then we're just going to pass check
pointer equals check pointer right here. And we've modified our agent. This is all we're going to need to do. We can now create our agent. And we're going to pass
in checkpoint equals memory. And remember memories. The object that we initialized above. When we use our agent now, we're also going to add
the concept of streaming. And there's two things that we might care
about. Streaming. First, we might care about streaming the individual messages. So this would be the AI message
that determines what action to take. And then the observation message
that represents the result of taking that action. The second thing we might care about
streaming is tokens. So for each token of the LLM call
we might want to stream the output. To begin we're just going to start
by streaming only the messages. We'll do the tokens
later on in the lesson. So we're
going to create our human message. "What is the weather in SF?" This is the one we ran before. We're now going to add
this concept of a thread config. So this will be used to keep track
of different threads inside the persistent checkpointer. This will allow us to have multiple
conversations going on at the same time. This is really needed
for production applications where you generally have many users. This thread config is simply a dictionary
with a configurable key. And as part of that, we have a thread id
and we can set that equal to any string. Here we're going to set that equal to one. We're now going to call the graph not with invoke, but with stream. We're going to pass in the same messages
dictionary. And we're also going to pass in this
thread config as a second parameter there. We're then going to get back
a stream of events. These events
represent updates to that state over time because we know our state
only has one key, the messages key. We're just going to loop through it
and print that out. So let's run this and see what happens. We can see that we get back a stream of results. First, we get back an AI message. This is the first result
from the language model. And it's telling us to call Tavily. Next, we get back a tool message. This is the result of calling to Tavily. And it has the results from the search. And finally,
we get back a third AI message. This is the final result from the LLM
answering our question. With this stream method, we get back
all of these intermediate results, and we have really good visibility
into what exactly is going on. Let's now call it with another message. This time we're going to say
"What about in LA?" So this is continuing
the same conversation that we had before. It's asking a follow-up question. We don't say anything explicitly about the weather,
but based on it being a conversation, we would expect it to realize
that we're asking about the weather here. In order to make sure that we're
continuing from that same point, we're passing in the same thread ID here. If we run this, we can see that it returns
first a function call, where it's looking for current weather
in Los Angeles. Again,
it's knowing that we asked about the weather because it has this persistence
from the checkpointer. We can then see that it's getting back
results from Tavily. And finally, that is responding
with an AI message that says the current weather in
Los Angeles is blah blah blah. We can call this yet again using the same thread ID with the message,
"Which is warmer?" Here it has access to the full history
so it can accurately respond. Los Angeles is currently warmer
than San Francisco. Just to demonstrate
the importance of this thread ID. Let's change this to be two. If we run this now. we can see that
the language model is really confused. "Can you please
specify the two or more items you are comparing to determine
which is warmer?" That's because it doesn't
have access to any history. And that's
because we're using a separate thread ID. So we've
covered the importance of persistence. And we've showed
how you can stream events. But what about streaming
tokens themselves. For that,
we're going to want to use the A-stream events method that comes on all LangChain
and LangGraph objects. A-stream event is an asynchronous method, which means that we're going
to need to use an async checkpointer. In order to do this. We can import async SqliteSaver
and pass that to the agent. This is very similar to before. It's just swapping out a synchronous SqliteSaver
with an async SqliteSaver. This allows us to use async methods on the graph. We'll use a new thread id, so this will start the conversation
from fresh. We're also going to be iterating
over a different type of event. These events represent updates
from the underlying stream. What we want to do, is
we want to look for events that correspond to new tokens. These kind of events are called
on chat model stream. When we see these events happening,
we want to get the content and print it out. And we'll print it out with this type
delimiter. When we run this, we should see it
streaming real time into the screen. So we can see a few things here. First, we can see that
it called the function under the hood. The reason it didn't stream out
anything there, is there's actually no content to stream. It was just a function call. But then we can see that when it did
get to the final response and it is returning a final answer,
we stream out those tokens one at a time. We can see that we've got this
little funny pipe delimiter here, but we could easily remove that in our
production application if we wanted to. So that's it
for persistence and streaming. Pretty simple to get started with,
but really powerful for building production applications. You're going to want your agents
to be able to have multiple conversations at the same time, and have a concept of memory
so they can resume those conversations. And you're also going to want them to be
able to stream both the final tokens, but also all of the messages
that came before. Persistence is also really important
for enabling human in the loop type interactions, and that's exactly what
we're going to cover in the next lesson.

---

## Lesson 6: Human in the loop

There are many occasions when
you would like to put a human in the loop to keep tabs on what an agent is doing. This is pretty easy to do with LangGraph. Let's see how this works. We're going to resume
from where we left off in the last lesson. So let's start
by setting up our environment variables. From there, we can make all the relevant imports
and set up our checkpointer. We're now going to set up our agent state. And we're going to make
one small modification. In the previous example, we annotated the messages list
with the operator.add. That added messages
to the existing messages array. However, for these human-in-the-loop
interactions, we may want to actually replace
existing messages. In order to do that, we're going to write
a custom reduced messages function, that basically looks for messages
with the same ID, and if it sees that you're inserting
one with the same ID as one that already exists,
it's just going to replace that. Otherwise, it will append them. After that, we create our same Tavily
tool that we've been using. And we can create our same agent. We're actually going
to make one small modification. So when we compile the graph, in addition to passing in the checkpointer, we're also going to pass this interrupt before equals action parameter. What this is going to do is it's going to add an interrupt
before we call the action node. So the action node is
where we call the tools. And so the reason that we're going to do this, is we're going to add something
that requires manual approval. Before we run any tools. This is useful when you want to make sure
that tools are executed correctly. This interrupt happens before we call the action node
where all tools are called. Sometimes you may only want to interrupt
if a certain tool is called. That's covered
in other parts of the documentation, and I encourage
you to check that out later. What's
initialization with the same system prompt and model and checkpointer
that we've been using. We now call it. And we'll pass in this thread config
using the thread ID of one. Because this is a separate
notebook, it'll start from fresh. We stream back responses
and we stop after this AI message. This is because this AI message
is saying that we should call it "tool", but we have that interrupt
before parameter which stops it there. One thing we can do from here is get the current state of the graph
for this thread. So, in order to do that
we'll pass in this thread config. We'll get back this configuration object
which has a few parameters. We can see that the largest ones
are this list of messages here. This is the state of the graph. At this point in time. We can
also see that it has a next parameter. This is the node
that is to be called "next". We can see here that it's action. This means that we're about
to call the action node. In order to continue,
we can call stream again with the same thread config
and just pass in none as the input. This will stream back results
and we will see that we get the tool message
from calling the tool. And then we also get the final AI message. Notice that there was no break
in between the action node and the LLM node, because we didn't
add any interrupt there. If we now get the state, we can see that the messages
list contains the full list of messages. And if we get the next parameter,
we can see that it's empty. There's nothing left to be done. For fun, we can write some code
that runs this in a little loop and prompts us for input
about whether to continue or not. We'll pass in a new thread ID,
so we start afresh. We get this little input box here
asking us whether we want to proceed. We can hit yes. And then the agent continues on its way. This is a good time to stop
and try it out with other inputs. Try adding different places
to interrupt before and see what happens. Before we get to the next section, let's talk
a little bit more about state memory. As a graph is executing, a snapshot
of each state is stored in memory. What's in that snapshot? Well there's the agent state
which you've already defined. And then there's some other useful things. For example, there's a thread and a unique identifier
for each of the snapshots. That's the thread TS right there. You can use that to access the snapshots. There's some commands to access memory. There's get state
which you've already seen. If you provide the thread
without the unique identifier and just return that thread ID,
it will return the current state. There's also get state history,
which returns an iterator over all of the state snapshots. You can use the iterator to get access to all of the unique identifiers
for each of the states. What can you do with that? Well, here's an example. Given the thread identifier, or rather
that thread TS the unique identifier, you could, for example, access
that first state, state one, and use that in an invoke command.
That will use state one as the current state or the starting point
for the rest of the graph. This is effectively time travel. Conversely, without that thread TS,
if you just pass in the thread ID, it will use the current state
of the thread as the starting point. You can also use that unique identifier to access a particular state. You can then modify that state, and then you can use update state,
to update the state and store it back into memory
in the location of the current state. From there, if you run Stream or Invoke, it'll use the new state,
the modified state as a starting point. All right. You'll be seeing some examples of these
in the upcoming section. So let's get back to it. Now let's
show an example of modifying the state. So let's start a new thread
and let's ask it what's the weather in LA? At this point in the thread we have two messages the human message
and then the AI message which is saying to search Tavily
for current weather in Los Angeles. But let's modify this. Let's pretend we were instead
asking about the weather in Louisiana, not Los Angeles. So how would we modify this to correct the agent action? First,
let's save the current state of the graph to a variable called current values. The last message we have in
this state is this AI message, which is saying to search
for a particular search term, in this case,
current weather in Los Angeles. We can drill in even further into see the list of tool calls
associated with this message. Let's now update these tool calls. In order to do that, we can first
get the ID associated with the tool call. Well then update
the tool calls property to be a list. This list will have one element. It's a dictionary. It's got one tool call. It's calling the Tavily
search results json. That's the same as before,
but the arguments are different. This time we have query
with current weather in Louisiana. This doesn't actually do anything
until we call: update state on the graph. We're going to pass in the thread config. And this is so we know
which thread we're operating on. And we're going to pass in the new values
that we want to override with. If we get the current state of the graph now we can see that
we have this search term here. Current weather in Louisiana. If we continue from here,
we can see that it calls Tavily with the current weather in Louisiana and gets back some response
and then responds accordingly. The current weather in Louisiana shows
sunny conditions. We've now shown how we can modify the state of the graph
in order to control what the agent does. One important thing to note, is that we're actually keeping
a running list of all these states. So when we modify the state,
we actually created a new state. And that became the new state. And then every time we update it
with results from the nodes, it's actually creating a new state
one after the other. This is really nice
because it actually allows us to go back and visit previous states in
something we're calling time travel. So in order to do this, we can call get state history
on the graph passing in again the thread ID. We'll then start building up
this list of states over time. If we get the last state in this list, we can see that it's
actually the earliest one. And so this is the one where
it was looking up the current weather in Los Angeles. This was the original state update
that was made based on the first language model call. If we wanted to go back in time
and resume from this checkpoint, where it was looking for Los Angeles,
we easily can. In order to do that, all we have to do, is call graph dot stream again,
pass in none. And now notice that we're passing in to
replay dot config. So to_replay
is the state where we want to resume from. And config
is just the configuration parameters that tell us
that we're resuming from this state. So if we run this, we'll start to see that it's searching
for the current weather in Los Angeles. It's getting a result back from Tavily, and then it's generating a response. And that's our final answer. One thing we can also do, is go back in time
and then edit it from there. So here we have this to_replay config. And this is where it's
the current weather in Los Angeles. So we can do the same thing that we did
before where we modify the state. And so we'll modify this
to do current weather and LA AccuWeather presuming
that we want a response from AccuWeather. And the reason
this is different than before is that here, we're going back in time
and then editing as opposed to before where we were editing
from the most recent state. We can update the state of this to_replay
and we'll get back this branch state. What we've branched off
with this modification. If we now call graph dot stream
with none on this branch state, we can see that we're looking up AccuWeather
and getting a result from there. And we're getting back a new answer. And then we're responding from the AI. Another thing we can do, is add messages to a state
at any given point in time. So here we have this to replay config
which we've modified to have the current weather
in LA, AccuWeather. Now let's presume that instead of actually
calling Tavily, we wanted to mock out a response. We can do that
by appending a new message into the state. We're going to grab the ID of the tool call
that we're supposed to be making. And we're going to create this state
update, which is a list of messages. And it's a new message this time. It's got a tool call ID of this. It's got a name of Tavily Search. And it's got a content of 54°C. So here this is a new message. So when we update the state in the graph,
it's not going to replace an existing message, it's going to append
it to the list of messages. We're now
going to update the state of the graph. But because we are actually adding
and pretending that an action has taken place, as opposed
to modifying the existing state, we need to do an additional thing. we need to add this as node equals action
parameter here. What this is basically doing
is it's saying that the state update that we're making isn't
just a modification. We're actually making this update
as if we were the action node. The reason that this is relevant
is because before we add this message, the current state of the graph
is about to go into the action node. But after we add this message,
we don't want it to go into the action mode anymore. So we're basically saying that
when we update the state, we're acting as
if we were the action node. If we now call stream on this new configuration, we can see that
it doesn't take an action anymore. Rather, it just calls the model
and responds with this AI message. The current weather in Los
Angeles is 54°C. This is what we pretended
that the tool had responded with. This has shown off
a lot of really advanced and complicated human-in-the-loop
interaction patterns. So you've learned how to add a break
before a node takes place. This allows for humans to approve
or deny specific actions. You've also shown
how you can go back in time and how you can modify the state, either
the current state or the past state. Additionally, you've also shown
how you can update the state manually. This allows you to manually give the agent the result of calling a tool, rather
than actually calling the tool itself. All of these human-in-the-loop patterns better serve to facilitate
how you interact with agents. They give you more control over
what it's doing. It allows you to go back
to a previous point in time, and by editing,
it allows you to correct what it has done. So far we've
been working with a pretty simple agent. It's got one LLM, one prompt,
and it's got a pretty simple state. Just a list of messages. And the next and final example in this course, we're going to create
a much more complicated agent made up of multiple LLM calls
that has a pretty complex state. See you there.

---

## Lesson 7: Essay Writer

In this lesson, you'll build a project
with a bit more scope. We'll build a compact version of an AI
researcher, in this case, an essay writer. Let's get to it. So we're going to create an essay writer. This is going to be broken down
into a few different substeps. So first we're going to generate a plan
for the essay. This is going to happen once upfront. Then based on that plan
we're going to do some research. This involves calling Tavily
and getting back some documents. From there we're going to go into generate,
and then generate. We're going to follow the plan
using the documents that we researched. And we're going to write the essay. From there, we're either going to finish
or we're going to continue. If we continue, we're
going to go into a reflect node where we're going to generate
a critique of the current essay. Then based on that critique,
we're going to do another research step with Tavily,
and get another set of documents. We're going to append those
to the existing set of documents and go all the way
back to the generate step, where we're going to once again
try to write this essay. And we're going to continue this
until some criteria is met and we exit. Let's see this in code. We're going to start with again importing all our environment variables. We're
then going to make some standard imports and set up our in-memory
SQLite checkpointers. Now we're going to create the agent state. And it's going to be a little bit
more complicated than before. So we're going to want to keep track
of a bunch of different things. First, we're going
to keep track of the task. This is the human input. This is what we're trying
to write an essay about. Then we're going to have a key
to keep track of the plan. This is the plan
that the planning agent will generate. Then we've got a key for the draft. This is a draft of the essay. And then we've got a key
for the critique part. So the critique agent will populate
this key. We're also going to add in content. This is a key to keep track
of the list of documents that Tavily has researched
and come back with. And then we're going to have two arguments
that keep track of how many times we've gone through this. So revision number,
which is going to keep track of the number of revisions we've made and max revisions,
which is keeping track of the maximum revisions
that we want to make. We're going to use those last two things and the criteria to decide
whether to stop or not. Let's create our model. We're going to be using OpenAI. And now let's write some prompts
for our agents. First, we have this planning prompt. This is the prompt for the LLM
that's going to write out a plan for our essay. Next, we have the writer prompt. This is the one who's writing the essay. Given all the content that was researched. We now have the reflection prompt. This is the prompt that's going to control
how we're critiquing the draft of the essay. We now have a prompt
that we're going to use for the agents that's doing research
after the planning step. So given a plan, we're going to generate
a bunch of queries and pass these to Tavily.
So this is the prompt that does that. And then we also have this research
critique prompt. So after we've made the critique
we're going to generate a list of queries to pass it to Tavily. So this is slightly different
than the planning prompt just because it's working on a critique
versus a plan. But it serves a similar purpose. For generating these lists of queries
to pass to Tavily. We're going to use function
calling to ensure that we get back a list of strings from the language
model. In order to do that,
we're going to set up this pydantic model that just represents the result
that we want to get back from the language model,
which in this case, is a list of strings. We're going to import the Tavily client
instead of the tool, because we're working with it
in a slightly unconventional way. Now we can start to create all our different agents,
all our different nodes. Let's go in order. So first we're going to start with
the node or agent that does the planning. What this node is going to do
it's going to take in the state. It's then
going to create a list of messages. One of them is going to be
the planning prompt. That's going to be the system message.
We're then going to create a human message. That is the task that we want to do. We're going to pass that to the model. We're going to get back a message. And then we're going to take the content of that message
and set that equal to plan. And so this is going to update the
plan key to be this response. The next
node that we're going to want to do is the agent that takes in the plan
and does some research. So for this, we're going to create
the research plan node. This is going to take in the agent state. And we're first going to generate
some queries. So we're going to do model. And this is the OpenAI model. And then we're going to say
with structured output and put queries right there. And so this is basically saying
that the response of what we're going to invoke
this with is going to be that pydantic object that we had,
which has that list of queries. So we're going to call invoke
and we're going to call invoke on a list of messages. We've got this research planning prompt. And then we pass in this human message
this task. And so for this part, we're generating
the queries based on the task. We're then going to get our list
of current documents, the content documents that we're going
to use to write this essay. So we're going to look in the state
for content if it exists or if it doesn't exist. We're just going to create
an empty list of documents. We're then going to loop over the queries
that we generated and search for them in Tavily. We're going to get back the results and
we're going to append them to the content. We're then going to return this content
key equal to the content that is the result of the original content,
plus the accumulated content. Okay. So we've made a
plan and we've done some initial research. Now it's time to write the first draft. So for the generation node,
the first thing we're going to do is to prepare the content. So we're going to take this list
of strings and join them into one big one. We're
then going to create the user message, where we're going to combine the task
and the plan. So we create a user message,
that's basically like "this is my task. And then here is my plan." The plan, remember,
this is what we generated two steps before. The task is the original user input. We're then going
to create a list of messages. This is a system message with the writer
prompt where we format in this content. We format in the documents
that we fetched. And then we're going to pass
in this user message, which is a combination of the task
and the plan. We're going to pass this to the model
and get back a response. We're then going to update two things
in the state. First, we're going to update the draft. So we're going to take the response
from the model and use that as the new draft version. Then we're going to update
the revision number. So this keeps track
of how many revisions we've made. And so here we're going to add one to the current
revision number in the state. After generating we now need a reflection node. This reflection node is going to take the reflection prompt
as a system prompt. And it's going to take the draft. This is what we just generated. We're going to have these two messages. And we're going to pass them
into the model and get back a response. And this is going to generate the critique
that we're going to update the state. The last agent we need, is the agent that's going
to take the critique and do some research. So we're going to do a very similar thing
that we did with the research plan node. We're going to take this model we're going
to do with structured output with query. So that's returning
queries. We're going to invoke it. This time we're passing in the research
critique prompt. And we're also passing in the critique
from before. Based on that we're going to get
the current content list. And we're going to start appending to it
the Tavily searches. We're then going to return
this updated content key. The final thing
we need is this 'should continue' condition. This is going to look
at the revision number. And if it's greater than the number of max
revisions, we're going to end. If not, we're going to go on to reflect. Remember this is getting run
after the generation step. So after the generation step
we're either going to finish or we're going to go into this critique
loop. Okay. We made all our agents
all our little nodes. We made our conditional edge. Now let's put it together into one
big graph. First, let's initialize the graph with the agent state. Let's then add in all the nodes that we created. We then need to set an entry point. So the entry point here is going
to be the planning node. Let's then add in our conditional edge. So after generate, we're going to call
the should continue function. And we're either going to end
or we're going to reflect. And so here, if the should continue
condition returns and we're going to end. If it returns reflect
we're going to go to the reflect node. We now need to add in the basic edges. So after planning, we're going
to go to the research plan node. After research plan, we're going to go to
generate generates already covered above. then after reflect
we're going to go to research critique. And after research critique
we're going to go back to generate. Let's now compile it. And we'll pass in the checkpointer
that we created before. We can visualize this. Same as before. It's a much more complex graph. All right. So let's use this writing agent. Let's call graph.stream. So we can see all the steps
that are happening. Because this is going to take a while. And we really want that visibility.
Let's pass in a task. Let's ask it what is the difference
between LangChain and LangSmith. I don't think GPT-3.5
knows about any of these. And then let's pass in max revisions
equals two. And let's passion
revision number equals one. So it is starting on the first revision. And we want it to make two revisions
of what it's going to do. Let's call this and it's going to start
getting to work. So we can see that it generates a plan. First. It then does some research. It gets back a bunch of documents. It's now got a first draft. So we can see that it generated a title
unveiling the distinctions LangChain versus LangSmith. And it started writing. Here we can see the critiquing
that the agent did. The essay provides
a clear overview blah blah blah, with here are some recommendations. It would benefit from a deeper analysis
of the strengths and weaknesses. Okay, great. Now we can go to planning. So here
we have the research critique node. This is done research
based on the critique of the agent. Here we get to generate again. This is the second draft. And we've only told it to do two drafts.
So this is the final one. It ends after this. And we can see the final essay
that we get. LangChain versus LangSmith. We can see some more details on what LangChain
is, what LangSmith is. Some talk about scalability,
incorruptibility, performance. We've now created this writer agent. This is a great time to go back
and try it out with different questions. Maybe have it
write a few different revisions, see how it performs, mess
around with the prompts. There's a lot that you can change here
to see how this overall writing agent responds. We built a little GUI that you can use
to try out the Essay Generator. Here's how it works. You can put in a topic here, and then you can hit this
button, Generate Essay. That will invoke your graph. And it will go and it will run off
and it'll start the generation process. And as you can see we stopped. We stopped at the planner node. Last node was planner. Next node was research. We're in thread zero. We're doing our first draft
with a count of one. We've taken one step in our graph. So why do we stop? Well if you look in "manage agent"
we have this interrupt after state set. So you may recall from code
what that looks like. So when we're compiling the graph, we have "interrupt
after set" for each of the states. after each state it'll stop. And what we'll do is in the GUI logic it'll come back
and it'll to see if that state is checked. And if it is, it will stop. And if it's not, then it will continue. And so you can uncheck these and continue
all the way through the process. Now we stopped the planner. So we should have a plan at this point. Let's take a look. Sure enough there's our introduction. But if we look at our research content
for example we don't have any. And same for draft
and for critique. There's also this tab the state snapshot. So this is giving us a view
into the current memory. This just lists all the things in memory. We can see that there were two initial
states inserted by the graph logic. And then there was this state
that we just inserted. It was the tasks, the pizza shop. The last node we're in and the values
of the agent state at this point in time. The last node is planner. Our plan was "briefly introduce the topic of pizza shops
and the popularity" and so on. We don't have any drafts, etc. So that's our current state. Now you may want to do something a little
bit different than this introduction. Let's say
what you really wanted to talk about was discuss the importance of jelly donuts in pizza making. Now, this is a bit nonsensical,
but you can now update the state if you hit this modify button, that will run the update state command
that we had seen earlier. And we can go in and take a look
and see what happened. So we can refresh our state snapshots. And here's the state
we were in previously. And now we have a new state. The current state. And here we have our plan is "discuss The importance of jelly donuts
in pizza making". And so we can continue from here
if we go back to the front end, and if we hit Continue Essay. as opposed to generate, then we continue on the path of the thread
that we've already started. Okay. So now we're at the research plan. The next note is generate. Let's go ahead and click continue
and we'll generate a draft. Let's take a look at the draft. And if we refresh we can see the last node which generate
the thread IDs zero there in one. Step four. And so if we read this
we can see "Jelly donuts. A beloved treat in many cultures
hold a surprising significance in the world of pizza making. What a surprise". Let's go back to our agents. Well, we could continue this, but you may have had second thoughts about this whole pizza
making and jelly donuts connection. So maybe we want to go back
to the beginning. So with this update state from Tab, you can go back
to the original planner state. And that just didn't update the state. So if we go take a look at our state
snapshot, that pushes onto the memory, the state that we had selected. And that's back to our original plan. "The briefly introduced the topic
of pizza shops and their popularity". So we can go back to there and then we can then run from there. And so let's unclick those two things
and run all the way to generate. Click continue essay and see what happens. All right. So the last note is generate. So now we can look at a draft. Let's refresh. "Pizza shops have become a staple in the food industry
offering a wide variety of options". Blah blah blah. And so we don't have any more references
to jelly donuts and pizza making. If you decide to do a different topic, for example, let's say you want to do a topic
on New England IPAs. So you can change that value
and then hit Generate Essay. Now you're starting a new topic. So you start a new essay. What happens here, is we get the live agent output down here. And we're going to go
all the way to generate, because we didn't have those to interrupt. After states selected. Now you'll notice that we have two different
threads to choose from. We have thread zero
which is a pizza shop, and then one which is the New England IPA topic. And our New England
IPA, only has a couple of states here. So you can explore essay
making with this GUI. More importantly, is to understand
what's happening to memory state and how the graph is being run. If you want the details, you can go into the helper.py file
and all the code is there. It's a little long, but you can use that as the
basis for your own project. We've covered a lot in these past
six lessons, but it's honestly
just the start of building agents. In the next section,
we'll do a quick overview of some resources that you can peruse
in your own time after the course to get an even deeper understanding.

---

## Lesson 8: LangChain Resources

Look, we have only
covered some of the basics here today. I want to point out where you can find
some more information to continue your agent journey. We've covered a lot of info. Here are some of my favorite resources for diving deeper into all that
we just talked about. The LangChain documentation
is a great place to start. Specifically,
it provides a great high level overview of all the packages
and services in the LangChain ecosystem. So we break down the different LangChain core packages as well as all the LangChain
community packages. So we used Tavily as part of LangChain
community. And then we also use LangChain OpenAI
which is a separate partner package. But we have a ton of other integrations
and you can explore those here. LangChain itself is more high
level and covers agents and other chains and different retrieval strategies
that are good high-level entry points. If you just want to get started. We also have a bunch of templates
that can be deployed easily with LangServe LangServe's just a really easy way to turn your LangChain
application into a web server. Helping out with all of this is LangSmith
from the beginning, LangSmith can help with debugging,
and then it can also help with monitoring in production. And it also has a playground
which we saw earlier. Looking at a few other sites. The LangChain GitHub
repo has a lot of good resources, a lot of good cookbooks, and
a lot of templates for getting started. The LangGraph repo, of course, has in-depth documentation on LangGraph,
everything that we just covered. So great reference docs,
great tutorials, and great how-to guides. We've also done
previous courses on LangChain with DeeLearning.AI,
that I'd highly recommend checking out. In particular, Functions,
Tools and Agents with LangChain, is a really good precursor
to this lesson. We already saw the prompt hub once, but
just to reiterate, this is a great place to go to get inspiration and see what
other expert prompters are doing.

---

## Lesson 9: Conclusion

Congratulations. You now have a good hand
on how to build your own agents. With what you have learned today, you can build simple
or quite complex agents. But before we go,
I wanted to cover some of the agent flows that we couldn't build today, but I think you should know about. The first architecture I want to talk about is a multi-agent architecture. And we covered this a little bit
with the writing agent. But just to make it a little bit
more concrete. A multi-agent architecture
is when multiple different agents work on the same shared state. And so these agents could be just a prompt
and a language model as they were in the writer. They could also have different tools
that they could call this. And that could be a prompt,
a language model and tools. And they could actually have
their own loops inside them. The crucial thing here, and the differentiator
between the next thing that we'll see is that they all work
on the same shared state. So they're passing that around from one
agent to the next. Let's contrast
that with a supervisor agent. So here we have a supervisor
which is calling into some sub-agents. And here the supervisor will actually
determine what the input to that agent is. And those agents themselves
could have different states inside them. There are graphs. And so there's not necessarily
the same concept of a shared state. Other than that this is pretty similar
to the multi-agent framework. It just really emphasizes
that there's this one supervisor that's in charge of routing
and coordinating these other agents. This is often good when you can use a really powerful
language model as the supervisor. Because doing this supervision, doing this
planning requires a lot of intelligence. One term that's popped up
a bunch recently is flow engineering. This comes from an AlphaCodium paper, where they achieve
state of the art coding performance. And they do it with a very graphical
like solution like this. And so looking at it you can see that
it's basically a pipeline. But there are a few key nodes
where there's actually a loop. So there's loops on the initial code
solution. There's loops
when you iterate on public tests and there's loops
when you iterate on AI tasks. And so this is an interesting graph
because you have this very directed flow
up until a certain point. And then you have these iterations. This is a really bespoke architecture
for a particular coding problem. But the concept of flow engineering
extends more broadly, and it generally refers to thinking of
what is the right information flow for your agents
to take action and think. In that vein. A common paradigm is to have a plan and execute style flow where first, you do an explicit planning,
step upfront and then you start to execute
on that plan. So you may come up with a few steps
that a sub-agent should go do. It can then go do one come back. Maybe you update the plan,
maybe you don't. This is where
there are some different variants, but then it goes on to the next thing
and it does that and it comes back
until it finishes the plan. Then you maybe check to see if the plan is successfully accomplished
or whether you need to replan. And then if all is good,
you return to the user. The final one I want to touch on
is a really interesting paper called Language Agent Tree Search. So this basically does a tree
search over the state of possible actions. And so it first generates an action. It then reflects and then goes down
based on that action and generates
some other sub-actions reflects on that. And throughout all these reflections
it can basically reflect on where in the tree of action states
it wants to jump back to. So it can backpropagate and update
parent nodes to have more information, which may inform future directions
from that previous state. For this in particular, you can really see
why persistence is really important, because you need to be able
to go back in time to previous states. These are just some of the emerging paradigms
for creating more complex agentic flows LangGraph is really aimed
at being highly controllable and allowing you to create these cyclical
or non cyclical flows. This degree of controllability
is really what differentiates it from other frameworks, and it's what
we're really excited about going forward as we view this to be crucial
to creating agents that actually work.
