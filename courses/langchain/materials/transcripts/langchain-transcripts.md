# LangChain for LLM Application Development — Transcripts

---

## Lesson 1: Introduction

Welcome to this short course on
LangChain for large language model application
development. By prompting an LLM
or large language model, it is now possible
to develop AI applications much faster than ever before. But an application
can require prompting an LLM multiple times and parsing
its output, and so there's a lot of glue code
that needs to be written. LangChain, created by Harrison
Chase makes this development process much easier. I'm
thrilled to have Harrison here, who had built this short course in
collaboration with DeepLearning.ai to teach how to use this amazing tool. Thanks for having me. I'm
really excited to be here. LangChain started as an open source framework
for building LLM applications. It came about when
I was talking to a bunch of folks in the field who
were building more complex applications and
saw some common abstractions in terms of how they were being developed. And we've been really thrilled at
the community adoption of LangChain so far. And so look forward
to sharing it with everyone here and look
forward to seeing what people build with it. And in fact, as a sign of LangChain's
momentum, not only does it have numerous users, but
there are also many hundreds of contributors to
the open source, and this has been instrumental for its
rapid rate of development. This team really ships code and features
at an amazing pace. So hopefully,
after this short course, you'll be able to quickly put together
some really cool applications using LangChain, and
who knows, maybe you even decide to
contribute back to the open source LangChain effort. LangChain is an
open source development framework for building
LLM applications. We have two different packages,
a Python one and a JavaScript one. They're focused on composition
and modularity. So they have a lot
of individual components that can be used in
conjunction with each other or by themselves. And so that's one
of the key value adds. And then the other key value add is a bunch
of different use cases. So chains of ways of combining
these modular components into more end-to-end applications making it
very easy to get started with those use
cases. In this class, we'll cover the common components of LangChain. So
we'll talk about models. We'll talk about prompts, which are how
you get models to do useful and interesting things. We'll talk about indexes, which
are ways of ingesting data so that you
can combine it with models. And then we'll talk about chains, which are
more end-to-end use cases along with agents, which are a very
exciting type of end-to-end use case which uses the model as a reasoning engine. We're also grateful to Ankush Gola, who
is a co-founder of LangChain alongside Harrison Chase, for also
putting a lot of thought into these materials and
helping with the creation of this short course. And on the DeepLearning.AI side, Geoff
Ludwig, Eddy Shyu, and Diala Ezzeddine have
also contributed to these materials. And so with that, let's
go on to the next video, where we'll learn about LangChain's models, prompts, and parsers.

---

## Lesson 2: Models, Prompts and parsers

In lesson one, we'll
be covering models, prompts, and parsers. So models refers to the
language models underpinning a lot of it. Prompts refers to the style of creating inputs
to pass into the models. And then parsers is
on the opposite end. It involves taking the
output of these models and parsing it into
a more structured format so that you can
do things downstream with it. Yep, so when you build
an application using LLM, there'll often be reusable models. We
repeatedly prompt a model, parses outputs, and so LangChain gives
an easy set of abstractions to do this type of operation. So with that, let's
jump in and take a look at models, prompts, and parsers. So to get started, here's
a little bit of starter code. I'm going to import OS, import OpenAI, and load
my OpenAI secret key. The OpenAI library is already
installed in my Jupyter Notebook environment. If you're running this
locally, and you don't have OpenAI installed
yet, you might need to run that. Bang, pip install OpenAI, but
I'm not going to do that here. And then here's a helper function. This
is actually very similar to the helper function that you might have
seen in the ChaiGPT prompt engineering for developers course
that I offered together with OpenAI's Iza Fulford. And so, with this
helper function, you can say get completion on what
is 1 plus 1, and this will call ChatGPT, or technically
the model, GPT 3.5 Turbo, to give you
an answer back like this. Now, to motivate the
line chain abstractions for model prompts and parsers, let's
say you get an email from a customer in a
language other than English. In order to make
sure this is accessible, the other language I'm going to use is
the English pirate language, where the consists are, I'd be
fuming that me blender lid flew off and
splattered my kitchen walls with smoothie. And to make matters worse,
the warranty don't cover the cost of cleaning up me kitchen. I
need your help right now, matey. And so, what we will do is,
ask this LLM to translate the text to
American English in a calm and respectful tone. So I'm
going to set style to American English in
a calm and respectful tone. And so, in
order to actually accomplish this, if you've seen a little bit of
prompting before, I'm going to specify the
prompt using an f-string with the instructions, translate the
text that is delimited by triple
backticks into style that is style, and then
plug in these two styles. And so, this generates a prompt
that says translate the text and so on.
I encourage you to pause the video and run the code,
and also try modifying the prompt to see if you
can get a different output. You can then prompt the Large Language
Model to get a response. Let's see what the response is. Says
translated the English pirate's message into this very polite, I'm really frustrated
that my blender lid flew off and made a mess of my
kitchen walls with smoothie and so on. I could really use your help right now,
my friend. That sounds very nice. So, if you have
different customers writing reviews in different languages,
not just English pirate, but French, German, Japanese, and so on,
you can imagine having to generate a whole sequence of prompts to
generate such translations. Let's look at how we can do
this in a more convenient, way using LangChain. I'm going
to import chat OpenAI. This is LangChain's abstraction for
the chatGPT API endpoint. And so, if I then set
chat equals chat OpenAI and look at what chat is,
it creates this object as follows that uses the chatGPT model,
which is also called GPT 3.5 turbo. When I'm building applications, one
thing I will often do is set the temperature parameter
to be equal to zero. So the default temperature is 0.7. But let me actually
redo that with temperature equals 0.0, and now the temperature is
set to 0 to make this output a little bit less random. And now, let me define the
template string as follows. Translate the text delimited
by triple vectors into style that is style, and then here's
the text. And to repeatedly reuse this template, let's
import LangChain's chat prompt template, and then, let me create
a prompt template using that template string that we
just wrote above. From the prompt template,
you can actually extract the original prompt,
and it realizes that this prompt has two input variables,
the style and the text, which were shown here
with the curly braces. And here is the
original template as well that we had specified. In fact, if I print this out,
it realizes it has two input variables, style and text. Now, let's
specify the style. This is a style that I want the customer
message to be translated to, so I'm going
to call this customer style, and here's my same customer email as before. And now, if I create customer messages,
his will generate the prompt, and will pass this
large language model in a minute to get a response.
So if you want to look at the types, the customer message is actually a
list, and if you look at
the first element of the list, this is more or less
that prompt that you would expect this to be creating. Lastly, let's
pass this prompt to the LLM, so I'm going to call chat, which we
had set earlier, as a reference to
the OpenAI chatGPT endpoint, and, if we print out
the customer responses content, then, it gives you back this text
translated from English pirate to polite American English. And of course, you can imagine other
use cases where the customer emails are in
other languages and this too can be used
to translate the messages for an English-speaking
to understand and reply to. I encourage you to
pause the video and run the code and also try modifying the prompt
to see if you can get a different output. Now let's hope our customer
service agent replies to the customer in their original
language. So let's say, English-speaking
customer service agent writes this and says, "Hey
there customer, warranty does not cover
cleaning expenses for your kitchen because it's your
fault. You misused your blender by forgetting to
put on the lid. Tough luck. See ya." Now they're polite message, but let's say this is what a
customer service agent wants. We are going to specify that the service message
is going to be translated to this pirate style.
So we want it to be in a polite tone that speaks in English pirate. And because we previously
created that prompt template, the cool thing is, we can now reuse
that prompt template and specify that the output
style we want is this service style pirate and the text is this service reply. And if we do that, that's the prompt. And if we prompt, ChaiGPT, this is the response it gives us back.
"Ahoy there, matey! I must kindly inform you that the warranty be
not covering the expenses or cleaning your galley." And so on. Aye, tough luck.
Farewell, me hearty. So, you might be wondering,
why are we using prompt templates instead of,
you know, just an f-string? The answer is that as
you build sophisticated applications, prompts
can be quite long and detailed. And so, prompt templates are
a useful abstraction to help you reuse good prompts when you can. This is an example
of a relatively long prompt to grade a student's
submission for an online learning application. And a prompt like this can be quite
long, in which you can ask the LLM to first solve the problem,
and then have the output in a certain format,
and the output in a certain format. And wrapping this in
a LangChain prompt makes it easier to reuse
a prompt like this. Also, you see later
that LangChain provides prompts for some common operations,
such as summarization, or question answering,
or connecting to SQL databases, or connecting to different APIs.
And so by using some of LangChain's built-in prompts, you can quickly get an
application working without needing to, engineer your own prompts. One other aspect of LangChain's
prompt libraries is that it also supports output parsing,
which we'll get to in a minute. But when you're building a complex application
using an LLM, you often instruct the LLM to generate its output
in a certain format, such as using specific keywords.
This example on the left illustrates using an LLM
to carry out something called chain of thought reasoning using a framework called the React
framework. But don't worry about the technical details, but
the keys of that is that the thought is what the LLM is thinking, because by giving an LLM space to think,
it can often get to more accurate conclusions. Then action as a keyword
to carry the specific action, and then observation to show what
it learned from that action, and so on. And if you have a
prompt that instructs the LLM to use these specific keywords,
thought, action, and observation, then this prompt can
be coupled with a parser to extract out the
text that has been tagged with these specific keywords.
And so that together gives a very nice
abstraction to specify the input to an LLM, and then also have
a parser correctly interpret the output that the LLM gives.
And so with that, let's return to see an example of an output
parser using LangChain. In this example, let's
take a look at how you can have an LLM output JSON, and use LangChain to parse that output. And the running example that I'll
use will be to extract information from a product review, and format that output in a JSON format. So here's an example of how
you would like the output to be formatted. Technically,
this is a Python dictionary, where whether or not
the product is a gift, maps to false,
the number of days it took to deliver was five,
and the price value was pretty affordable. So this is one example of a desired
output, here is an example of customer review, as well as a template to try to get to that JSON
output. So here's a customer review. It
says, this lead blower is pretty amazing. It
has four settings, candle blower, gender breeze, windy city, and
tornado. It arrived in two days,
just in time for my wife's anniversary present. I
think my wife liked it so much she was speechless. So
far, I've been the only one using it, and so
on. And here's a review template. For the following
text, extract the following information. Specify, was this a gift?
So in this case, it would be yes, because this is a gift. And also, delivery days.
How long did it take to deliver? It looks like in this case,
it arrived in two days. And what's the price value? You
know, slightly more expensive than the lead blowers, and so on. So,
the review template asks the LLM to take as input a customer review and extract these three fields and then
format the output as JSON with the following keys. All right. So here's
how you can wrap this in LangChain. Let's
import the chat prompt template. We'd actually imported this already
earlier. So technically, this line
is redundant, but I'll just import it again and then
have the prompt templates created from the review template up on top. And so, here's the prompt template. And now, similar to our earlier
usage of a prompt template, let's create the messages to pass to the OpenAI, endpoint. Create the OpenAI endpoint,
call that endpoint, and then let's print out the response. I encourage you to pause
the video and run the code. And there it is. It says,
give us true, delivery day is 2, and the price value also looks pretty accurate. But note that if we check the type of the response,
this is actually a string. So it looks like JSON
and looks like it has key-value pairs, but it's actually
not a dictionary. This is just one long string. So what I'd really like to do
is go to the response content and get
the value from the gift key which should be true, but
I run this, this should generate an error because, well,
this is actually a string. This is not a Python dictionary. So,
let's see how we will use LangChain's parser
in order to do this. I'm going to import response schema and
structured output parser from LangChain. And I'm going to tell it what
I wanted to parse by specifying these response schemas. So
the gif schema is named gif, and here's the description. Was the
item purchased as a gift for someone else? Answer true or yes,
false if not or unknown, and so on. So, have a gift schema,
delivery date schema, price value schema, and then let's
put all three of them into a list as follows. Now that I've specified the schema for
these LangChain can actually give you the prompt itself by having the output parser tell you
what instructions it wants you to send to the LLM.
So if I were to print format instructions. She has a pretty precise set
of instructions for the LLM that will cause it to generate an
output that the output parser can process. So here's the new review template, and the review
template includes the format instructions that LangChain generated. And so we can create a prompt from the review template too, and then create the messages that will pass to the OpenAI endpoint. If you want, you can take a
look at the actual prompt, which gives the instructions to extract the fields gift, delivery days,
price value, here's the text, and then here are the formatting
instructions. Finally, if we call the OpenAI endpoint, let's
take a look at what response we got. It is now this, and now if we use
the output parser that we created earlier, you can then parse
this into an output dictionary, which if I print, looks like this. And notice that this is of type dictionary, not a string, which is why I can now extract the value
associated with the key gift and get true, or the value associated with delivery days and get two, or you can also extract the
value associated with price value. So this is a nifty way to
take your LLM output and parse it into a Python dictionary, to make the output easier
to use in downstream processing. I encourage you to pause
the video and run the code. And so, that's it for models, prompts,
and parsers. With these tools, hopefully you'll be
able to reuse your own prompt templates easily,
share prompt templates with others that you're
collaborating with, even use LangChain's built-in prompt templates,
which as you just saw, can often be
coupled with an output parser, so that the input prompt to output in a specific format
and then the parser, parses that output to store the
data in a Python dictionary or some other data
structure that makes it easy for downstream processing.
I hope you find this useful in many of your applications. And with that, let's
go into the next video where we'll see how LangChain can help you
build better chatbots, or have an LLM have more effective chats
by better managing what it remembers
from the conversation you've had so far.

---

## Lesson 3: Memory

When you interact with these models,
naturally they don't remember what you say
before or any of the previous conversation, which
is an issue when you're building some applications like
Chatbot and you want to have a conversation with
them. And so, in this section we'll
cover memory, which is basically how do you remember previous parts of
the conversation and feed that into the language model so that they
can have this conversational flow as you're interacting
with them. So, LangChain offers multiple
sophisticated options of managing these memories. Let's
jump in and take a look. So, let me start off by importing my OpenAI API key, and then let me import
a few tools that I'll need. Let's use as the motivating
example for memory, using LangChain to manage a chat
or a chatbot conversation. So, to do that, I'm
going to set the LLM as a chat interface of OpenAI with temperature equals 0, and I'm going to use the memory as a
ConversationBufferMemory, and you'll
see later what this means. And I'm
going to build a conversation chain. Again, later in this short course, Harrison
will dive much more deeply into what exactly
is a chain in LangChain. So, don't worry too much about the details of
the syntax for now, but this builds an LLM. And if I start to have a conversation,
conversation.predict, give the input, Hi, my name is Andrew. Let's see what it says. Hello, Andrew, it's
nice to meet you. Right? And so on. And then, let's say I ask it, what is 1 plus 1? 1 plus 1 is 2, and then ask it again, you know, what's
my name? Your name is Andrew,
as you mentioned earlier. Hmm, there's a little bit of
trace of sarcasm there, not sure. And so if you want,
you can change this verbose variable to true, to see what LangChain is actually doing. When you run predict,
Hi my name is Andrew, this is the prompt
that LangChain is generating. It says, the following is a
friendly conversation between a human and an AI. AI is talkative,
and so on. So this is a prompt that LangChain has generated to have the system have
a hopeful and friendly conversation, and it has to save the conversation,
and here's the response. And when you execute this on the second and third parts of the
conversations, it keeps the prompt as follows.
And notice that by the time I'm uttering, what is my name? This
is the third turn, that's my third input. It has stored the current conversation as follows. Hi, my name is Andrew,
what is 1 plus 1, and so on. And so this memory
or this history of the conversation gets longer
and longer. In fact, up on top, I have used the memory
variable to store the memory. So if I were to print memory.buffer, it has stored the conversation so far. You can also print this out, memory.loadMemoryVariables.
The curly braces here is
actually an empty dictionary. There's some more advanced features that
you can use with a more sophisticated input, but we
won't talk about them in this short course. So don't worry
about why there's an empty curly braces here. But this is what LangChain has
remembered in the memory of the conversation so far. It's
just everything that the AI or that the human has said. I encourage you to pause
the video and run the code. So, the way that
LangChain is storing the conversation is with this ConversationBufferMemory. If I were to use the
ConversationBufferMemory to specify a couple of inputs and outputs,
this is how you add new things to the memory
if you wish to do so explicitly. Memory.saveContext says, hi, what's up? I know this is
not the most exciting conversation, but I wanted to have a short example. And with that,
this what the status of the memory is. And once again,
let me actually show the memory variables. Now,
if you want to add additional data to the memory, you can keep
on saving additional context. So, conversation goes on, not much,
just hanging, cool. And if you print out the memory,
you know, there's now more stuff in it. So when you use
a large language model for a chat conversation,
the large language model itself is actually stateless.
The language model itself does not remember the conversation you've
had so far. And each transaction, each call to the API
endpoint is independent. And chatbots appear to have memory only because there's usually rapid code that provides
the full conversation that's been had so far as context to the LLM. And so,
the memory can store explicitly the terms or the utterances so far.
Hi, my name is Andrew. Hello, it's just nice to meet you and so on. And this memory storage
is used as input or additional context to the LLM so that they can generate
an output as if it's just having the next conversational turn, knowing what's been said before. And as the conversation becomes long,
the amounts of memory needed becomes really,
really long and does the cost of sending a lot
of tokens to the LLM, which usually charges based
on the number of tokens it needs to process,
will also become more expensive. So LangChain provides several convenient kinds of memory to store
and accumulate the conversation. So far, we've been looking at
the ConversationBufferMemory. Let's
look at a different type of memory. I'm going to import the
conversation buffer window memory that only keeps
a window of memory. If I set memory to conversational buffer window
memory with k equals one, the variable k equals one specifies
that I wanted to remember just one conversational exchange.
That is one utterance from me and one utterance from chatbot. So, now if I were to have it save context,
hi, what's up, not much, just hanging. If I were to look at memory.load variables, it
only remembers the most recent utterance. Notice it's dropped. Hi, what's up?
It's just saying human says not much, just hanging,
and the AI says cool. So that's because k was equal to one. So this is a
nice feature because it lets you keep track
of just the most recent few conversational terms.
In practice, you probably won't use this with k equals one. You
use this with k set to a larger number. But still, this prevents the
memory from growing without limit as
the conversation goes longer. And so if I were to rerun the conversation that
we had just now, we'll say, hi, my name is Andrew. What is 1 plus 1? And now I ask it, what is my name? Because k equals 1,
it only remembers the last exchange versus what
is 1 plus 1? The answer is 1 plus 1 equals 2,
and it's forgotten this early exchange which is now, now says, sorry,
don't have access to that information. One thing I hope you
will do is pause the video, change this to true in
the code on the left, and rerun this conversation
with verbose equals true, and then you will
see the prompts actually used to generate this,
and hopefully you'll see that the memory, when you're
calling the LLM on what is my name, that the memory has
dropped this exchange where it learned what is my name,
which is why it now says it doesn't know what is my name. With the conversational token buffer memory, the memory will limit the number of tokens saved.
And because a lot of LLM pricing is based on tokens, this maps more directly to the cost of the LLM calls. So, if I were to say the
max token limit is equal to 50, and actually let me
inject a few comments. So let's say the conversation is, AI
is what? Amazing. Backpropagation is what? Beautiful.
Chatbot is what? Charming. I use ABC as the first letter of
all of these conversational terms. We can keep track of what was said
when. If I run this with a high token limit, it has almost the whole conversation. If I increase the token limit to 100, it now has the whole conversation,
sign of AI is what? If I decrease it, Then, you know, it chops off
the earlier parts of this conversation to retain the
number of tokens corresponding to the
most recent exchanges but subject to not exceeding the
token limit. And in case you're wondering why we needed
to specify an LLM, it's because different LLMs use
different ways of counting tokens, so this tells it to use the way of counting tokens that the
chatOpenAI LLM uses. I encourage you to pause
the video and run the code, and also try modifying the
prompt to see if you can get a different output. Finally, there's one last type of memory
I want to illustrate here, which is the conversation summary buffer memory. And the idea is, instead of limiting
the memory to a fixed number of tokens based on the most
recent utterances or a fixed number of conversational exchanges, let's use an LLM to write a summary
of the conversation so far, and let that be the memory. So here's an example where I'm going
to create a long string with someone's schedule, you
know, there's meeting at 8am with your product team, you need your PowerPoint
presentation, and so on and so on. So there's a long string saying what's
your schedule, you know, maybe ending with a noon
lunch at the Italian restaurant with a customer, bring
your laptop, show the latest LLM demo. And so, let me use a conversation summary buffer memory with a max token limit
of 400 in this case, pretty high token limit, and I'm going to insert in a few conversational terms in
which we start with hello, what's up, no one's just hanging, cool. And then what is on the schedule today,
and the response is, you know,
that long schedule. So this memory now has quite a lot of text in it.
In fact, let's take a look at the memory variables. It contains that entire piece of text, because 400 tokens was sufficient to store all this text. But now, if I were to reduce the max token limit,
say to 100 tokens, remember, this stores the
entire conversational history. If I reduce the number of tokens to 100, then, the conversation summary
buffer memory has actually used an LLM,
the OpenAI endpoint in this case, because that's
where we set the LLM to, to actually generate a summary of the conversation so far.
So the summary is, human-AI engage in small talk before
the start of the schedule, and informs human in the morning meeting,
blah, blah, blah, lunch meeting with customer
interested in AI and latest AI developments. And so, if we were to have a conversation, using this LLM, let me create a conversation chain, same as before. And let's say that we were to ask, you know, input what would be
a good demo to show. I said verbose equals true, so here's
the prompt. The LLM thinks the current conversation has had this discussion so far, because that's
the summary of the conversation. And just one note, if you're
familiar with the OpenAI chat API endpoint,
there is a specific system message. In this example, this is not using
the official OpenAI system message, it's just including it as part
of the prompt here, but it nonetheless works pretty well.
And given this prompt, you know, the LLM outputs
basic constituent AI developments, so it's just showcasing our
latest NLP capabilities. Okay, that's cool. Well, it's, you know, making
some suggestions to the cool demos, and makes you think if I
was meeting a customer, I would say, boy, if only there were open source
framework available to help me build cool NLP applications
using LLMs. Good things are launching. And the interesting thing is,
if you now look at what has happened to the memory, so, notice that here,
it has incorporated the most recent AI system output,
whereas my utterance asking it, what would be a good demo to show,
has been incorporated into the system message, you know,
the overall summary of the conversation so far.
With the conversation summary buffer memory,
what it tries to do is keep the explicit storage of the
messages up to the number of tokens we
have specified as a limit. So, you know, this part,
the explicit storage, we're trying to cap at 100 tokens, because
that's what we're asked for. And then anything beyond that, it will use CLM to generate a summary,
which is what is seen up here. And even though I've
illustrated these different memories using a chat as
a running example, these memories are useful
for other applications too, where you might keep on
getting new snippets of text, or keep on getting new information, such as if your
system repeatedly goes online to search for facts, but you want to
keep the total memory used to store this
growing list of facts as, you know, capped and not
growing arbitrarily long. I encourage you to pause
the video and run the code. In this video,
you saw a few types of memory including buffer memories
that limits based on number of conversation exchanges or tokens or a memory that can
summarize tokens above a certain limit. LangChain actually supports additional
memory types as well. One of the most
powerful is vector data memory, if you're familiar with word embeddings
and text embeddings, the vector database actually
stores such embeddings. If you don't know what that means, don't
worry about it. Harrison will explain it later. And it can then
retrieve the most relevant blocks of text using this type of a
vector database for its memory. And LangChain also
supports entity memories, which is applicable when
you wanted to remember details about specific people,
specific other entities, such as if you talk about a specific friend,
you can have LangChain remember facts about that friend,
which would be an entity in an explicit way.
When you're implementing applications using LangChain, you
can also use multiple types of memories such as using one of the types of
conversation memory that you saw in this video plus
additionally entity memory to recall individuals. So this way
you can remember maybe a summary of the conversation
plus an explicit way of storing important facts about
important people in the conversation. And of course, in addition to
using these memory types, it's also not uncommon
for developers to store the entire conversation in the
conventional database. Some sort of key value store or SQL database.
So you could refer back to the whole conversation
for auditing or for improving the system further. And so, that's memory types. I
hope you find this useful building your own applications. And now let's go on to the next
video to learn about the key building block of LangChain, namely
the chain.

---

## Lesson 4: Chains

In this lesson, Harrison will teach
the most important key building block of LangChain,
namely, the chain. The chain usually combines an LLM,
large language model, together with a prompt,
and with this building block you can also put a bunch of
these building blocks together to carry out a sequence
of operations on your text or on your other data. I'm excited to dive into it. Alright,
to start, we're going to load the environment variables as
we have before. And then we're
also going to load some data that we're going to use. So part
of the power of these chains is that you can
run them over many inputs at a time. Here we're going to
load a pandas DataFrame. A pandas DataFrame is
just a data structure that contains a bunch
of different elements of data. If you're not familiar with pandas, don't
worry about it. The main point here is that we're
loading some data that we can then use later on. And so if we
look inside this pandas DataFrame, we can see that there is a product
column and then a review column. And each of these
rows is a different data point that we
can start passing through our chains. So the first chain we're
going to cover is the LLM chain. And this is a simple
but really powerful chain that underpins a lot
of the chains that we'll go over in the future. And so, we're going to import
three different things. We're going to import the OpenAI model, so the
LLM. We're going to import the chat prompt template. And so this
is the prompt. And then we're going to import
the LLM chain. And so first, what we're
going to do is we're going to initialize the language
model that we want to use. So we're going to
initialize the chat OpenAI with a high
temperature so that we can get some fun descriptions. Now we're
going to initialize a prompt. And this prompt is going to take in a
variable called product. It's going to ask the LLM to generate what the
best name is to describe a company that makes that product. And then
finally, we're going to combine these two things into
a chain. And so,
this is what we call an LLM chain. And it's quite simple. It's just
the combination of the LLM and the prompt. But now
this chain will let us run through the prompt and into the
LLM in a sequential manner. And so if we have a product called queen-size-sheet-set, we
can run this through the chain by using chain.run. And what this will,
do is it will format the prompt under the hood,
and then it will pass the whole prompt into the LLM.
And so we can see that we get back the name of
this hypothetical company called Royal Bettings. And so here would be
a good time to pause. And you can input any product
descriptions that you would want. And you can see what the
chain will output as a result. So the LLM chain is
the most basic type of chain. And that's
going to be used a lot in the future. And so we can see how
this will be used in the next type of chain, which
will be sequential chains. And so sequential chains run
a sequence of chains one after another. So to start, you're going to import the
simple sequential chain. And this works well
when we have subchains that expect only one
input and return only one output. And so here we're
going to first create one chain, which uses an LLM and a prompt. And this prompt is going to take in the product and will
return the best name to describe that company.
So that will be the first chain. Then we're
going to create a second chain. In this second chain, we'll
take in the company name and then output a 20-word
description of that company. And so you can imagine
how these chains might want to be run one after another,
where the output of the first chain, the company name,
is then passed into the second chain. We can easily do this by
creating a simple sequential chain where we have the
two chains described there. And we'll
call this overall simple chain. Now, what you can do is run this chain
over any product description. And so if we use
it with the product above, the queen size sheet set,
we can run it over and we can see that
it first outputs royal betting. And then it passes
it into the second chain and it comes
up with this description of what that company could be about. The simple sequential chain
works well when there's only a single input and a single output. But what about when there are
multiple inputs or multiple outputs? And so we can do this by using
just the regular sequential chain. So let's import that. And then you're going
to create a bunch of chains that we're going to
use one after another. We're going to be using the data from
above, which has a review. And so the first chain, we're
going to take the review and translate it into
English. With the second chain, we're
going to create a summary of that review in one sentence. And this will use
the previously generated English review. The third chain is
going to detect what the language of the
review was in the first place. And so if you notice,
this is using the review variable that is
coming from the original review. And finally, the fourth chain will
take in multiple inputs. So this will take
in the summary variable, which we calculated with the second
chain, and the language variable,
which we calculated with the third chain. And it's going to ask for a follow-up response
to the summary in the specified language. One important thing to
note about all these subchains is that the input
keys and output keys need to be pretty precise. So here, we're taking in review. This
is a variable that will be passed in at the start. We can see that
we explicitly set the output key to English review.
This is then used in the next prompt, down below, where we take
in English review with that same variable name. And we set the output
key of that chain to summary, which we can see is
used in the final chain. The third prompt takes in review,
the original variable, and outputs language, which is again used in the final prompt. It's really important to get
these variable names lined up exactly right, because
there's so many different inputs and outputs going on. And if
you get any key errors, you should definitely check that they are lined up so. The simple sequential chain
takes in multiple chains, where each one has a
single input and a single output. To see a visual representation of this,
we can look at the slide, where it has one chain feeding into the other chain,
one after another. Here we can see a visual
description of the sequential chain. Comparing it to the above chain,
you can notice that any step in the chain can
take in multiple input variables. This is useful when you have
more complicated downstream chains that need to be a
composition of multiple previous chains. Now that we have all these chains,
we can easily combine them in the sequential chain. You'll
notice here that we'll pass in the four chains
we created into the chains variable. We'll create the
inputs variable with the one human input, which is the
review. And then we want to
return all the intermediate outputs. So the English review, the summary,
and then the follow-up message. Now,
we can run this over some of the data. So let's choose a review and pass it
in through the overall chain. We can see here
that the original review looks like it was in French. We can see the English review as a
translation. We can see a summary of that review and then
we can see a follow-up message in the original
language of French. You should pause the
video here and try putting in different inputs. So far we've covered the LLM chain and
then a sequential chain. But what if you want
to do something more complicated? A pretty common but
basic operation is to route an input to
a chain depending on what exactly that input is. A good way to imagine this is if
you have multiple sub chains, each of which specialized for
a particular type of input, you could have a
router chain which first decides which subchain to
pass it to and then passes it to that chain. For a concrete example, let's
look at where we are routing between different
types of chains depending on the subject that
seems to come in. So we have here different prompts. One
prompt is good for answering physics questions. The
second prompt is good for answering math questions, the
third for history, and then a fourth for computer science. Let's
define all these prompt templates. After we have these prompt templates,
we can then provide more information about them. We can give each one
a name and then a description. This description for
the physics one is good for answering questions about physics.
This information is going to be passed to the router chain,
so the router chain can decide when to use this subchain. Let's now import the other types
of chains that we need. Here we need a multi-prompt chain. This is a specific type of
chain that is used when routing between multiple different
prompt templates. As you can see, all the options we
have are prompt templates themselves. But this is just one type of thing
that you can route between. You can route between
any type of chain. The other classes that we'll
implement here are an LLM router chain. This uses a language
model itself to route between the different subchains.
This is where the description and the name
provided above will be used. We'll
also import a router output parser. This parses the LLM
output into a dictionary that can be used
downstream to determine which chain to use and what the input to
that chain should be. Now we can get around to using it.
First, let's import and define the language model that we will use. We now create the destination chains.
These are the chains that will be called
by the router chain. As you can see,
each destination chain itself is a language model chain,
an LLM chain. In addition to the destination chains,
we also need a default chain. This is the chain that's
called when the router can't decide which of the subchains to use. In the
example above, this might be called when the
input question has nothing to do with physics, math, history,
or computer science. Now we define the
template that is used by the LLM to route between the different chains. This has instructions of
the task to be done, as well as the specific formatting that the
output should be in. Let's put a few of
these pieces together to build the router chain. First, we create the full
router template by formatting it with the destinations
that we defined above. This template is flexible
to a bunch of different types of destinations. One thing you can do here is pause
and add different types of destinations. So up here, rather than just physics,
math, history, and computer science, you could add a different subject,
like English or Latin. Next, we create the prompt
template from this template, and then we create
the router chain by passing in the LLM
and the overall router prompt. Note that here we
have the router output parser. This is important as it will
help this chain decide which subchains
to route between. And finally, putting it all together,
we can create the overall chain.
This has a router chain, which is defined here.
It has destination chains, which we pass in here.
And then we also pass in the default chain.
We can now use this chain. So let's ask it some questions. If we ask it a question about physics,
we should hopefully see that it is routed
to the physics chain with the input,
what is blackbody radiation? And then that is passed
into the chain down below, and we can see that
the response is very detailed with lots of physics details. You should pause the
video here and try putting in different inputs.
You can try with all other types of special chains
that we have defined above. So, for example,
if we ask it a math question, we should see that it's
routed to the math chain and then passed into that. We can also see what
happens when we pass in a question that is not
related to any of the subchains. So here, we ask it a
question about biology and we can see the
chain that it chooses is none. This means that it
will be passed to the default chain which
itself is just a generic call to the language model.
The language model luckily knows a lot about biology so it can
help us out here. Now that we've covered these basic
building blocks types of chains we can start to
put them together to create really interesting applications. For
example, in the next section, we're going to cover how to
create a chain that can do question answering over your documents.

---

## Lesson 5: Question and Answer

One of the most common,
complex applications that people are building using an LLM
is a system that can answer questions on top of or about
a document. So, given a piece of text,
maybe extracted from a PDF file or from a webpage or from
some company's intranet internal document collection, can
you use an LLM to answer questions about the
content of those documents to help users gain a
deeper understanding and get access to the information that
they need? This is really powerful because it
starts to combine these language models
with data that they weren't originally trained on. So
it makes them much more flexible and adaptable
to your use case. It's also really exciting because we'll start to
move beyond language models, prompts, and output parsers and start introducing
some more of the key components of LangChain, such as embedding
models and vector stores. As Andrew mentioned,
this is one of the more popular chains that we've got, so
I hope you're excited. In fact,
embeddings and vector stores are some of the
most powerful modern techniques, so if you have not seen them yet,
they are very much worth learning about. So with that, let's dive in! Let's do it! So we're going
to start by importing the environment variables as
we always do. Now we're going to import some
things that will help us when building this chain. We're
going to import the retrieval QA chain. This will do retrieval over
some documents. We're going to import our favorite chat open
AI language model. We're going to import
a document loader. This is going to be used to load some proprietary data that
we're going to combine with the language model. In
this case it's going to be in a
CSV. So we're
going to import the CSV loader. Finally we're going
to import a vector store. There are many different types
of vector stores and we'll cover what exactly these are
later on but we're going to get started with the "DocArrayInMemorySearch" vector
store. This is
really nice because it's an in-memory vector store and
it doesn't require connecting to an external database of any
kind so it makes it really easy to get started. We're also going to import display and
markdown to common utilities for displaying
information in Jupyter notebooks. We've provided a CSV of
outdoor clothing that we're going to use to combine with
the language model. Here we're going to
initialize a loader, the CSV loader, with a path
to this file. We're next going to import an index, the
"VectorStoreIndexCreator". This will help us create a
vector store really easily. As we can see below,
there will only be a few lines of code to create this. To create it, we're
going to specify two things. First, we're going to specify the
vector store class. As mentioned before, we're
going to use this vector store, as it's a particularly easy one to
get started with. After it's been created, we're then
going to call "from_loaders", which takes in a list of document
loaders. We've only got one loader that
we really care about, so that's what we're passing in here. It's now been created and
we can start to ask questions about it. Below we'll cover what exactly happened
under the hood, so let's not worry about that for now. Here, we'll
start with a query. We'll then create a response using "index.query"
and pass in this query. Again, we'll cover what's going
on under the hood down below. For now, we'll
just wait for it to respond. After it finishes, we can now take a
look at what exactly was returned. We've gotten back a table
in markdown with names and descriptions for all
shirts with sun protection. We've also got a nice
little summary that the language model has provided us. So we've gone over how to do question
answering over your documents, but what exactly is going
on underneath the hood? First, let's think about the general idea. We want
to use language models and combine it with a lot
of our documents. But there's a key issue. Language models can only
inspect a few thousand words at a time. So if we have really large documents,
how can we get the language model to
answer questions about everything that's in there? This is where embeddings and
vector stores come into play. First, let's talk about embeddings. Embeddings create
numerical representations for pieces of text. This numerical representation
captures the semantic meaning of the piece of text
that it's been run over. Pieces of text with similar content
will have similar vectors. This lets us compare pieces
of text in the vector space. In the example below,
we can see that we have three sentences. The first two are about pets,
while the third is about a car. If we look at the
representation in the numeric space, we can see that when we compare the
two vectors on the pieces of text corresponding
to the sentences about pets, they're very similar. While if we compare it to
the one that talks about a car, they're not similar at all. This will let us easily
figure out which pieces of text are like each other,
which will be very useful as we think about which pieces of
text we want to include when passing to the language model to
answer a question. The next component that we're
going to cover is the vector database. A vector database is a way
to store these vector representations that
we created in the previous step. The way that we
create this vector database is we populate it
with chunks of text coming from incoming documents. When we get a big incoming document,
we're first going to break it up into smaller chunks. This helps create pieces
of text that are smaller than the original document,
which is useful because we may not be able to pass the
whole document to the language model. So we want to
create these small chunks so we can only
pass the most relevant ones to the language model. We then create an embedding
for each of these chunks, and then we store those in a vector
database. That's what happens when we create the index. Now that we've got this index, we
can use it during runtime to find the
pieces of text most relevant to an incoming query. When a query comes in,
we first create an embedding for that query. We then compare it
to all the vectors in the vector database,
and we pick the n most similar. These are then returned,
and we can pass those in the prompt to the language model to get back a
final answer. So above, we created this chain and
only a few lines of code. That's
great for getting started quickly. But let's now do it a bit more step-by-step and
understand what exactly is going on under the hood. The first step
is similar to above. We're
going to create a document loader, loading from that CSV with all the
descriptions of the products that we want to do
question answering over. We can then load
documents from this document loader. If we look at the individual documents,
we can see that each document corresponds to one of
the products in the CSV. Previously,
we talked about creating chunks. Because these documents
are already so small, we actually don't
need to do any chunking here. And so we can create embeddings
directly. To create embeddings, we're
going to use OpenAI's embedding class. We can import it and initialize it here. If we want to
see what these embeddings do, we can actually take a look at what
happens when we embed a particular piece of text. Let's use the "embed_query" method on
the embeddings object to create an embeddings for a
particular piece of text. In this case, the sentence, "Hi, my name
is Harrison." If we take a look at this embedding,
we can see that there are over a thousand different elements. Each of these elements
is a different numerical value. Combined, this creates the
overall numerical representation for this piece of text. We want to create
embeddings for all the pieces of text that
we just loaddand then we also want to store them in a
vector store. We can do that by using the "from_documents"
method on the vector store. This method takes in
a list of documents, an embedding object, and then we'll
create an overall vector store. We can now use this vector store to
find pieces of text similar to an incoming query. So let's look at the query, "Please
suggest a shirt with sunblocking". If we use the similarity
search method on the vector store and pass in a query,
we will get back a list of documents. We can see that
it returns four documents, and if we look at the first one,
we can see that it is indeed a shirt about sunblocking. So, how do we use
this to do question answering over our own documents?
First, we need to create a retriever from this vector store.
A retriever is a generic interface that can
be underpinned by any method that takes in
a query and returns documents. Vector stores and embeddings are
one such method to do so, although there are
plenty of different methods, some less advanced,
some more advanced. Next, because we want to
do text generation and return a natural language response,
we're going to import a language model and we're going
to use ChatOpenAI. If we were doing this by hand,
what we would do is we would combine the documents
into a single piece of text. So we'd do something like this, where
we join all the page content in the
documents into a variable and then would pass
this variable or a variant on the question, like, "Please
list all your shirts with sun protection in
a table in markdown and summarize each one." into
the language model. And if we print out the response here,
we can see that we get back a table exactly as we asked for. All of those steps can be
encapsulated with the LangChain chain. So here we can
create a retrieval QA chain. This does retrieval and then does
question answering over the retrieved documents.
To create such a chain, we'll pass in a few different things. First,
we'll pass in the language model. This will be used for doing
the text generation at the end. Next, we'll pass in the chain type. We're
going to use "stuff". This is the simplest method as
it just stuffs all the documents into context
and makes one call to a language model. There are a few other
methods that you can use to do question answering that I'll
maybe touch on at the end, but we're not
going to look at in detail. Third, we're
going to pass in a retriever. The retriever we created
above is just an interface for fetching documents. This will be used to
fetch the documents and pass it to the language model. And then finally, we're
going to set "verbose=True". Now, we can create a
query and we can run the chain on this query. When we get the response,
we can again display it using the display and markdown utilities.
You can pause the video here and try it out
with a bunch of different queries. So that's how you do it in detail, but
remember that we can still do it pretty easily with
just the one line that we had up above. So, these two things equate
to the same result. And that's part of the interesting
stuff about LangChain. You can do it in one line, or
you can look at the individual things and
break it down into five more detailed ones. The five more detailed
ones let you set more specifics about what
exactly is going on, but the one-liner is easy to get started. So
up to you as to how you'd prefer to go forward. We can also customize the index when we're
creating it. And so if you remember, when
we created it by hand, we specified an embedding. And
we can specify an embedding here as well. And
so this will give us flexibility over how the
embeddings themselves are created. And we can also swap
out the vector store here for a different
type of vector store. So there's the same level of customization that
you did when you create it by hand that's also available
when you create the index here. We use the "stuff method"
in this notebook. The stuff method is
really nice because it's pretty simple. You just put all of
it into one prompt and send that to the language model and
get back one response. So it's
quite simple to understand what's going on. It's quite cheap
and it works pretty well. But that doesn't always work okay. So if you remember,
when we fetched the documents in the notebook,
we only got four documents back and they were relatively small. But what if you wanted to do the
same type of question answering over lots of
different types of chunks? Then there are a few
different methods that we can use. The first is "Map_reduce". This basically takes all the chunks,
passes them along with the question to a language model,
gets back a response, and then uses another language model
call to summarize all of the individual responses into
a final answer. This is really powerful
because it can operate over any number of documents. And it's also really powerful because
you can do the individual questions in parallel. But it does take a lot more calls.
And it does treat all the documents as independent,
which may not always be the most desired thing. "Refine",
which is another method, is again used to
loop over many documents. But it actually does it iteratively.
It builds upon the answer from the previous document. So this is really good for
combining information and building up an answer over time.
It will generally lead to longer answers. And it's also not as fast because
now the calls aren't independent. They depend on the result of
previous calls. This means that it
often takes a good while longer and takes
just as many calls as "Map_reduce", basically. "Map_rerank" is a pretty interesting and
a bit more experimental one where you do a
single call to the language model for each document. And you
also ask it to return a score. And then you select the highest score. This relies on the
language model to know what the score should be.
So you often have to tell it, "Hey, it should be a high score if it's
relevant to the document and really refine the instructions
there". Similar to "Map_reduce", all the
calls are independent. So you can batch them and it's relatively fast.
But again, you're making a bunch of language model calls.
So it will be a bit more expensive. The most common of
these methods is the "stuff method", which we used in
the notebook to combine it all into one document. The second most common is the "Map_reduce"
method, which takes these chunks and sends them to the language
model. These methods here, stuff, map_reduce,
refine, and rerank can also be used for lots of other
chains besides just question answering. For example,
a really common use case of the "Map_reduce" chain is for summarization, where
you have a really long document and you want
to recursively summarize pieces of information
in it. That's it for question
answering over documents. As you may have noticed, there's
a lot going on in the different chains that we have here.
And so in the next section, we'll cover ways to better understand
what exactly is going on inside all of
these chains.

---

## Lesson 6: Evaluation

When building a complex
application using an LLM, one of the important but sometimes
tricky steps is how do you evaluate how well
your application is doing? Is it meeting some accuracy criteria? And also, if you decide
to change your implementation, maybe swap in a different LLM,
or change the strategy of how you use a vector database or
something else to retrieve chunks, or change some other
parameters of your system, how do you know if you're
making it better or worse? In this video, Harrison
will dive into some frameworks on how to
think about evaluating a LLM-based application, as well
as some tools to help you do that. These applications are really
chains and sequences of a lot of different steps.
And so honestly, part of the first thing that you should
do is just understand what exactly is going
in and coming out of each step. And so some of the tools can really
just be thought of as visualizers or debuggers
in that vein. But it's often really useful to
get a more holistic picture on a lot of different data points
of how the model is doing. And one way to do that is
by looking at things by eye. But there's also this really cool
idea of using language models themselves and chains themselves
to evaluate other language models, and other
chains, and other applications. And we'll dive a
bunch into that as well. So, lots of cool topics,
and I find that with a lot of development shifting towards prompting-based
development, developing applications using LLMs, this
whole workflow evaluation process is being rethought. So, lots
of exciting concepts in this video. Let's dive in. Alright, so let's
get set up with evaluation. First, we need to have the chain
or the application that we're going to evaluate in the first place. And we're going to use the
document question answering chain from the previous lesson. So we're
going to import everything we need. We're going to load the same
data that we were using. We're going to create that
index with one line. And then we're going to create the
retrieval QA chain by specifying the language model, the
chain type, the retriever, and then the verbosity that we're going
to print out. So we've got this application, and
the first thing we need to do is we need to really
figure out what are some data points that
we want to evaluate it on. And so there's
a few different methods that we're going to cover for doing this. The first is the most simple,
which is basically we're going to come up with
data points that we think are good examples ourselves. And so to do that, we can just look
at some of the data and come up with example questions and
then example ground truth answers that we can
later use to evaluate. So if we look at
a few of the documents here, we can kind of get a sense of what's
going on inside them. It looks like the first one, there's this
pullover set, there's this in the second one, there's this jacket, it
has a bunch of details about all of them. And from these details,
we can create some example query and answer pairs. So the first one,
we can ask a simple, "Does the Cozy Comfort
Pullover Set have side pockets?". And we can see by
looking above that it does, in fact, have some side pockets in it. And then for the second one,
we can see that this jacket is from a certain collection,
the DownTek collection. And so we can ask the question,
"What collection is this jacket from?" And have the answer be,
"The DownTek collection". So here we've created two examples. But this doesn't
really scale that well. It takes a bit of time
to look through each example and figure out what's going
on. And so is there a way that we can automate it? And one of the
really cool ways that we think we can automate it is with
language models themselves. So we have a chain in
LangChain that can do exactly that. So we can import
the QA generation chain. And this will take
in documents and it will create a question
answer pair from each document. It'll do this using a
language model itself. So we need to create this
chain by passing in the Chat OpenAI language model. And then from there,
we can create a bunch of examples. And so we're going to use the
apply and parse method because this is applying
an output parser to the result because we
want to get back a dictionary that has
the query and answer pair, not just a single string. And so now, if we look at
what exactly is returned here, we can see a query,
and we can see an answer, and let's check the document that this is
a question and answer for, and we can see that it's asking
what the weight of this is, we can see that it's taking the
weight from here, and look at that! We just generated
a bunch of question-answer pairs. We didn't have to write it
all ourselves. Saves us a bunch of time, and we can do more
exciting things. And so now, let's go ahead and add these examples into the examples
that we already created. So, we got these examples now,
but how exactly do we evaluate what's going on? The first thing we want
to do is just run an example through the chain,
and take a look at the output it produces. So here we pass in a query,
and we get back an answer. But, this is a little
bit limiting in terms of what we can see that's
actually happening inside the chain. What is the actual prompt that's
going into the language model? What are the documents that it retrieves?
If this were a more complex chain with multiple
steps in it, what are the intermediate results? It's oftentimes not enough to
just look at the final answer to understand what is or could
be going wrong in the chain. And to help with that, we have a fun
little util in LangChain called "langchain.debug". And so if we set "langchain.debug =
True", and we now rerun the same example as above. We can see that
it starts printing out a lot more information. And so if we look at what exactly it's
printing out, we can see that it's diving down first into the
retrieval QA chain. And then it's going down into a
stuff documents chain. And so as mentioned, we're using
the stuff method. And now it's entering the LLM chain, where
we have a few different inputs. So we can see the original
question is right there. And now we're
passing in this context. And we can see that this context is created
from a bunch of the different documents that we've retrieved. And so when doing question answering,
oftentimes when a wrong result is returned, it's not necessarily the language
model itself that's messing up. It's actually the
retrieval step that's messing up. And so taking a
really close look at what exactly the question is,
and what exactly the context is, can help debug what's going wrong. We can then step
down one more level and see exactly what
is entering the language model, Chat OpenAI itself. And so here we can
see the full prompt that's passed in. So we've got
a system message. We've got the description of
the prompt that's used. And so this is the prompt that the question answering
chain is using under the hood, which we
actually haven't even looked at until now. And so we can
see the prompt printing out, "Use the following pieces of
context to answer the user's question. If you don't know
the answer, just say that you don't know, don't try to make
up an answer." And then we see a bunch of the context as
inserted before, and then we see a human question, which is the question
that we asked it. We can also see a lot more information
about the actual return type. So rather than just
a string, we get back a bunch of information like
the "token_usage", so the "prompt_tokens", the "completion_tokens", "total_tokens", and the "model_name". And this can be really useful
to track the tokens that you're using in your chains or calls to language
models over time and keep track of the
total number of tokens, which corresponds very closely to
the total cost. And because this is
a relatively simple chain, we can now see that the final response,
"The Cozy Comfort Pullover Set, Stripe does have side pockets.",
is getting bubbled up through the chains and
getting returned to the user. So we've just walked through how to
look at and debug what's going on with a single input
to this chain. But what about all
the examples we created? How are we going to evaluate those? Similarly to when creating them,
one way to do it would be manually. We could run the chain over all the
examples, then look at the outputs, and try to figure out what's
going on, whether it's correct, incorrect, partially correct. Similar to
creating the examples, that starts to get a little bit
tedious over time. And so let's
go back to our favorite solution. Can we ask a language model to do it? First,
we need to create predictions for all the examples. Before
doing that, I'm actually going to turn off
the debug mode in order to just not print everything out onto
the screen. And then I'm going to create
predictions for all the different examples. And
so I think we had seven examples total, and
so we're going to loop through this chain seven times, getting a
prediction for each one. Now that we've got these examples, we
can think about evaluating them. So we're going to import the QA, question
answering, eval chain. We are going to create this
chain with a language model, because again, we're going to be using a
language model to help do the evaluation. And then we're
going to call evaluate on this chain. We're going to pass in examples
and predictions, and we're going to get back a bunch of
graded outputs. And so, in order to see what exactly is going on
for each example, we're going to loop through them. We're
going to print out the question, and again, this
was generated by a language model. We're
going to print out the real answer, and again, this was also generated by
a language model when it had the whole document in front of it, and
so it could generate a ground truth answer. We're going to print out
the predicted answer, and this is generated by a
language model when it's doing the QA chain, when it's doing the
retrieval with the embeddings and the vector databases, passing that into
a language model, and then trying to guess the predicted
answer. And then we're
also going to print out the grade, and again, this
is also generated by a language model when it's asking
the eval chain to grade what's going on and whether it's correct or incorrect. And so, when we loop through all
these examples and print them out, we can see those in detail for each
example. And looks like here
it got everything correct. This is a relatively simple retrieval problem,
so that is reassuring. So let's look at the first example. The
question here is, "Does the Cozy Comfort Pullover
Set have side pockets?". The real answer, and
we created this, is "Yes". The predicted answer,
which the language model produced was, "The Cozy Comfort Pullover Set,
Stripe does have side pockets". And so we can understand
that this is a correct answer. And actually the language
model does as well, and it grades it correct. But let's think about why we actually
need to use the language model in the first place. These two strings
are actually nothing alike. They're very different. One's really
short, one's really long. I don't even think, yes doesn't appear anywhere in this
string. So if we were to try to do some string
matching, or exact matching, or even some regexes here,
it wouldn't know what to do. They're not the same thing. And that
shows off the importance of using the language model to do
evaluation here. You've got these answers, which are arbitrary strings.
There's no single one truth string that is the
best possible answer. There's many different variants. And
as long as they have the same semantic meaning,
they should be graded as being similar. And that's what
a language model helps with, as opposed to just
doing exact matching. This difficulty in
comparing strings is what makes evaluation
of language models so hard in the first place. We're
using them for these really open-ended tasks, where they're asked to
generate text. This hasn't really been done
before, as models until recently weren't really good enough to
do this. And so a lot of the evaluation metrics that
did exist up to this point just aren't
good enough. And we're having to invent new ones, and
invent new heuristics for doing so. And the most interesting and most popular
of those heuristics at the moment is actually using a language model
to do the evaluation. This finishes the evaluation lesson, but one
last thing I want to show you is the LangChain Evaluation Platform. This
is a way to do everything that we just did
in the notebook, but persisted and show it in a
UI. And so let's check it out. Here, we can see that we have a session.
We called it, deeplearningai. And we can see here that we've
actually persisted all the runs that we ran
in the notebook. And so this is a good
way to track the inputs and outputs at a high level. But it's also a really good
way to see what exactly is going on underneath. So
this is the same information that was printed
out in the notebook when we turned on
debug mode. But it's just visualized in a UI in a
little bit of a nicer way. And so we can see the inputs to
the chain and the outputs to the chain at each step.
And then we can click further and further
down into the chain and see more and
more information about what is actually getting passed in.
And so if we go all the way down to the bottom,
we can now see what's getting passed exactly to
the chat model. We've got the system message here. We've got the human question here. We've
got the response from the chat model here. And we've got some
output metadata. One other thing that we've added here is
the ability to add these examples to a data set. So if you remember,
when creating those data sets of examples at the
start, we created them partially by hand, partially with a language
model. Here, we can add it to a data set
by clicking on this little button. And we now have the
input query and the output results. And so we can create a data set.
We can call it deep learning. And then we can start
adding examples to this data set. And so again, getting back to
the original thing that we tackled at the beginning of the lesson,
we need to create these data sets so that we can do
evaluation. This is a really good way to have
this just running in the background. And then add to the example
data sets over time and start building up these examples that you
can start using for evaluation and have this flywheel
of evaluation start turning.

---

## Lesson 7: Agents

Sometimes people think of
a large language model as a knowledge store, as if it's
learned to memorize a lot of information, maybe
off the internet, so when you ask it a question, it
can answer the question. But I think a even more useful way
to think of a large language model is
sometimes as a reasoning engine, in which you can give it chunks of
text or other sources of information. And then the large language model,
LLM, will maybe use this background knowledge that's
learned off the internet, but to use the new
information you give it to help you answer
questions or reason through content or decide even
what to do next. And that's what LangChain's Agents framework
helps you to do. Agents are probably my
favorite part of LangChain. I think they're
also one of the most powerful parts, but they're also
one of the newer parts. So we're seeing a lot of stuff emerge
here that's really new to everyone in the field. And so this should
be a very exciting lesson as we dive into what
agents are, how to create and how to use agents, how to equip them
with different types of tools, like search engines that
come built into LangChain, and then also how
to create your own tools, so that you can
let agents interact with any data stores, any APIs, any
functions that you might want them to. So this is exciting, cutting-edge
stuff, but already with emerging, important
use cases. So with that, let's dive in! So to get started with Agents, we're
going to start as we always do, by importing the correct
environment variables. We're also going to need to
install a few packages here. So we're going to use the "duckduckgo-search" engine
and "wikipedia". So we're going to want
to pip install those. I've already installed those in my environment, so I'm not going
to run this line. But if you guys have not,
you should uncomment that line, run it, and then you're good
to go. We're then going to import
some methods and classes that we need from LangChain. So
we're going to import some methods to load tools. And these are things that we're
going to connect the language model to. We're going
to load a method to initialize the agent. We're going to
load the Chat OpenAI wrapper, and we're going to load
"AgentType". So "AgentType"
will be used to specify what type of agent we want to use.
There are a bunch of different types of agents in LangChain. We're
not going to go over all of them right now. We'll just
choose one and run with that. We're then going to initialize the language model
that we're going to use. Again, we're using this as the
reasoning engine that we're using to drive the agent. We'll then load the tools that we're going
to use. So we're going to load DuckDuckGo
search and Wikipedia. And these are built-in LangChain
tools. Finally, we're going to initialize the agent. We pass it the tools,
the language model, and agent type. And so here we're using "CHAT_ZERO_SHOT_REACT_DESCRIPTION". Not going to go over in
too much detail what this means. The important things to note are chat.
This is optimized to work with chat models. And then react. React is a
prompting strategy that elicits better thoughts
from a language model. We're also going to set "handle_parsing_errors=True". If you remember from the first lesson,
we chatted a bunch about output parsers and
how those can be used to take the LLM output, which is a string,
and parse it into a specific format that
we can use downstream. That's extremely important here. When
we take the output of the LLM, which is text, and parse it into
the specific action and the specific action input that
the language model should take. Let's now use this agent. Let's ask
it a question about a recent event that the model, when it
was trained, didn't know. So let's ask it about
the 2022 World Cup. The models here were trained
on data up to around 2021. So it shouldn't
know the answer to this question. And so it should realize that
it needs to use a tool to look up this
recent piece of information. So we can see here that the agent
realizes that it needs to use DuckDuckGo search,
and then looks up the 2022 World Cup winner. And so it gets back a bunch of
information. We can then see that the agent thinks
that the 2022 World Cup has not happened yet. So this is a good example of why
agents are still pretty exploratory. You can see that there's
a bunch of information here about the 2022 World Cup, but
it doesn't quite realize all that has happened. And so
it needs to look up more things and get more information. And so
then based on that information, it can respond with the correct
answer that "Argentina won the 2022 World Cup". Let's then ask it a
question where it should recognize that it needs
to use Wikipedia. So Wikipedia, it has a lot
of information about specific people and specific entities
from a long time ago. It doesn't need to be current information. So let's ask it about Tom M. Mitchell,
an American computer scientist. And
what book did he write? We can see here that
it recognizes that it should use Wikipedia to
look up the answer. So it searches for Tom M. Mitchell
Wikipedia. And then does another follow-up
search just to make sure that it's got the right answer. So it
searches for "Tom M. Mitchell Machine Learning" and gets
back more information. And then based on that, it's
able to finally answer with "Tom M. Mitchell wrote the textbook, 'Machine
Learning'". You should pause the
video here and try putting in different inputs. So far, we've used tools that come
defined in LangChain already, but a big power of agents is that you
can connect it to your own sources of information, your
own APIs, your own data. So here we're going to go over
how you can create a custom tool so
that you can connect it to whatever you want. Let's make a tool that's going
to tell us what the current data is. First, we're
going to import this tool decorator. This can be applied
to any function and it turns it into
a tool that LangChain can use. Next, we're
going to write a function called "time", which takes in any text string. We're
not really going to use that. And it's going to return today's date by calling
date time. In addition to the name of the function,
we're also going to write a really detailed doc string. That's because this is what
the agent will use to know when it
should call this tool and how it should call this tool. For example, here we say that,
"The input should always be an empty string.". That's
because we don't use it. If we have more
stringent requirements on what the input should be, for example,
if we have a function that should always
take in a search query or a SQL statement, you'll want to make sure
to mention that here. We're now going to create another agent. This time
we're adding the time tool to the list
of existing tools. And finally, let's
call the agent and ask it what the date today is. It recognizes that it needs
to use the time tool, which it specifies here. It has the action input as an empty
string. This is great. This is what we told it to do. And then it returns with an observation.
And then finally, the language model
takes that observation and responds to the user, "Today's
date is 2023-05-21". You should pause the
video here and try putting in different inputs.
This wraps up the lesson on agents. This is one of the newer
and more exciting and more experimental
pieces of LangChain. So I hope you enjoy using it.
Hopefully it showed you how you can use a language model as
a reasoning engine to take different
actions and connect to other functions and data sources.

---

## Lesson 8: Conclusion

In this short course,
you saw a range of applications, including processing customer reviews,
and building an application to answer
questions over documents, and even using an LLM
to decide when to make a call to an external tool,
like web search, to answer complex questions. If a week or two ago,
someone had asked you, how much work would it be to build
all of these applications? I think a lot of people would have
thought, "Boy, this sounds like weeks, you know,
maybe even longer of work.". But you saw in this short course,
how with just a pretty reasonable number of lines of code,
you can use LangChain to build all of
these applications pretty efficiently. As I hope you take these ideas,
maybe even take some code snippets that you
saw in the Jupyter Notebooks and use them
in your own applications. And these ideas are
really just the start. There's a lot of other
applications that you can use language models for. These
models are so powerful because they're applicable
to such a wide range of tasks, whether it be answering questions
about CSVs, querying SQL databases, interacting with
APIs. There's a lot of different
examples of using chains and the combinations of
prompts and output parsers and then more chains
to do all these things in LangChain. And
most of that is due to the LangChain community. So
I want to also give a really big thank out
to everyone in the community who's contributed, whether it
be improvements in the documentation, making it easier for others to
get started, or new types of chains opening up a whole new
world of possibilities. And so, with that,
if you have not yet already done so, I hope you go to your laptop or
your desktop and run pip install LangChain and
then go use this tool to go build some amazing applications.
