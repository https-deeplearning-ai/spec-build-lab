# Multi AI Agent Systems with crewAI — Transcripts

---

## Lesson 1: Introduction

Welcome to Multi AI agent systems
with CrewAI, built in partnership with CrewAI and taught by
its founder and CEO, João Moura. I think AI agent workflows will be a key
driver of AI progress in the near term. Multi agent workflows
let you break down the complex tasks into subtasks
that can be executed by agents, each of which plays
a particular defined role. For example,
if your goal is get a research report written, the roles might be researcher,
writer, and fact checker. Or if you want to get a website built,
perhaps the roles could be a web designer,
software engineer and testing engineer. I've really enjoyed using crewAI myself,
and I'm delighted that its creator João, is teaching this course. João had created crewAI when he needed a tool
to build better agents, to help him write LinkedIn posts,
and he has a lot of experience designing workflows
to collections of agents. Execute. Thanks, Andrew. Really, I'm excited to work with
you and your team and this is and has the potential to enable engineers
to build great things. In this course,
you learn the major building blocks for agentic systems
with an emphasis on multi-agent systems. Building blocks
you learn include: role-playing, tool use, memory, guardrails, and collaboration. And you use these components
to build a collection of agents, to customize a resume, to job description,
and to perform financial analysis, and also to perform event planning. As part
of assembling your agentic workflow, you also define
how these agents cooperate, which ones are able to delegate
to other agents to perform certain tasks like research,
and whether certain agents should execute their tasks in parallel or in series,
or in a hierarchical fashion, with a manager agent
delegating to a number of worker agents. João will go through these concepts
using the crewAI Open Source library. Yes, this course will help engineers
trying to understand how to build AI agentic applications
and how they differ from regular applications that
we have been building up to this point. After watching this,
you will be equipped with everything you need to build multi-agent systems
and reap all the benefits from it. I like to think of good multi-agent
systems designs like being a manager. You are now promoted
into this manager of agents and get to identify the goals
and the various roles that will work together
to achieve those goals, and also define clear expectations
for what success looks like. It's a very interesting mental shift
from regular engineering. Yes, indeed, many people
have worked to create this course. I'd like to thank the whole CrewAI
team and from DeepLearning.AI, Eddy Shyu,
also contributed to this course. The first lesson will give you
an overview of AI agents, and also an overview
of the rest of the course. So make sure to stick around. So let's go on to the next video
and dive into the key building blocks of AI agents.

---

## Lesson 2: Overview

First of all, congratulations
on signing up for this course. This is going to be great. I'm so excited to dive into this with you. We are going to learn everything
there is to know about agents. And in this first lesson we are going
to understand what makes them tick, how they work, and even look at some of the examples
that we're going to do together throughout the entire course. So let's dive in real quick. So in this course
we're going to talk about so many different things,
so many interesting concepts. I want to just highlight a few
so that you know what you're going to see. We're going to be talking about role playing. We're going to be talking about agents
that are able to focus, to use tools to cooperate with each other. We're going to really dive into
how guard rails are crucial to make agents work, and how memory
can make them so much better. We're going to talk about
how the different ways that agents can collaborate,
not only working sequentially and hierarchically,
but also asynchronously. There's so many different options. So make sure that you stick around
because we're going to build a lot of different crews
throughout the different lessons. A crew is a team of AI agents working together, each with their own defined roles. Don't worry if you don't know what this means. yet. That's what this course is about. We're going to start with an overview. We're going to build a simple research
and write crew. But we are going to go all the way
to build more complex ones. Building a customer support crew,
our customer outreach crew and event planning agent system
in a financial analysis agent system. And then to wrap up,
we're going to build our most complex crew yet, a crew that is going to be able to
tailor made your resume to any job posting out there, increasing your odds
of getting an interview. So make sure to stick around for that,
because honestly, things are only going to get more interest
from here out. So what we will build in this course. Let's look at this
full stack engineering job posting. So you can see there is a bunch
of interesting stuff in here. If you look close at the job
description, you're going to notice that they're basically looking
for a full stack developer. They want someone that nails
both front and back end. And there is a bunch of like
actual criteria in there. They want you to be able to write APIs
and to have experience with databases and all of that. So
this is what Noah's profile looks like. I'm not going to read over it,
but I just highlight some of this stuff. You can see that Noah is trying
to highlight how he's a good leader. So he mentioned how he has excelled
in leading teams both remote and in an office. He mentioned some data science
and machine learning, and he also mentions about deploying scalable AI solutions.
That is nothing to do with the actual position
that Noah wants to apply. But if you dig in there,
you're going to notice that Noah also has some of those skills. You can see that mentions there
that he knows Ruby, Python, JavaScript and that it has been a software engineer
for 18 years. So there are definitely enough things
in there that the kind of could explore and that make Noah qualify
for this position. So how do we make sure that we help know
where to highlight all that in his resume, so that he increases his odds of getting an actual interview for the position
that he does want to apply. Well, you can use agents to do it. In our case, by the end of this course,
you're going to be able to put together a multi-agency system that does that, we do that
by leveraging four different agents. that does that, we do that
by leveraging four different agents. It's going to have a tech job,
a researcher, a personal profile for engineer,
a resume strategist for engineers and engineering interviewer
preparer. Together,those four agents, we'll have a few tools
that they're going to be able to use from searching the internet
all the way to do rag over your resume, everything to kind of like help
in this case our friend Noah, but yourself as well, to make sure that you're
highlighting the right skills for the job. So this is what the new profile
looks like. Let's compare both for a second. So in the second one, you can see that it was highlighting
a lot of his leading experiences. But now in the second one, it's kind of
like doubling down on the other skills that he has that better
match the job that he's applying to. You can see that
we mentioned JavaScript, Python, Ruby. We also mentioned UI, UX. You mentioned how he knows HTML and CSS. It's everything in there. So it's still the same profile
and the same skill set. But framing a way that now
better allows them or in this case, it allows
Noah to get the interview that he desires. So we can also see these
throughout his experience. So stick around if you want to do this. Because by the end of it
you're going to be able to build not only this, but way more complex
groups of multi-agents. They're going to be able
to do a bunch of automation for you. All right.
So, what is agentic automation? If you think about
what automation used to be like before,
it was something completely different. In the past you would say, hey,
"I want to go from point A to point B."
And you can write code to automate that. And then what happens
is that as edge cases appear, you start to kind of make
that a little more complex. You start to add a lot of conditions
and it's analysis there. Where like, well, if X do C, if z do D,
and you can see how these things can become quite complex, especially as you start
adding more and more edge cases. So, in the old days,
whenever you're trying to do automation is what you end up with, is this very complex code base
with a lot of different conditions and edge cases,
and you just can never cover it all. The beauty of agentic automation
is that you don't need to drown the map. You can show the options. So it's fundamentally
a new way to write software. All right. So in regular applications
you have strong inputs. So you know exactly the data
that is gathered into your application. You understand
if that's a string if that's an integer, if that's a float you have a very clear
understanding of that. And then you also have a very clear understanding on
what is the mathematical operation that you might be doing with that
or any other aristics. So, you know, if you're multiplying those numbers together,
if you're interpolating their string, whatever is happening in there,
you have full control and understanding of what it is. And because of that, you also understand
what is the output. You know, if the outputs
are going to be another float or another integer or another string,
you can replicate it. And that's the beauty
of regular engineering. But with these new AI applications,
you have something else differently. You have a fuzzy input,
meaning that you don't know what the user is
input into your application. So you know that is a string
because we are talking about an LLM, but you don't know if it's a string that represents
tabular data, if it's a markdown, if it's a regular text,
or if it's a math operation. And then the transformations
are also fuzzy because they're LLMs. You don't know if the LLM will decide
to transform this into a list, or if it's to write
a full blown paragraph. And because of that, you don't know
exactly what the output will be because it can take different forms and shapes depending on the inputs
and under the transformation. But that's the beauty of that. There is a place in the word right now
where these fuzzy applications make way more sense than regular
existing software applications. So that's the main reason
why people like ChatGPT so much. If you think about ChatGPT, that's
an AI application with fuzzy inputs. You don't know what your user is
putting in the chat. It's also fuzzy transformations. You don't know why do they allow them
to do with that data? And it's also fuzzy outputs. You don't know
what will be the final output. What will be the final response
for that user input. And that's why people love it
because it's something they can relate to. If you think about the world as we have
today, the world is a fuzzy place. So this is the beauty about AI
applications is that it's a valuable tool that has its merits and places
where you want fuzzy applications in where you once chunk type
of applications in each one has its merits and its place, depending on the software
that you're trying to build. So let's look at some actual example here. Let's talk about data
collection and analysis. And if you have been working in engineering for a while
you're probably familiar with this. Your company probably has a website
that captures leads data through a form. And those leads eventually go into your sales team that are going
to try to make them into customers. So this is very usual
for most of the businesses out there. And the way that these two leads become
customers is by prioritizing them. And there's a bunch of ways
that companies used to do that. So you have your form
and you capture information about this company through that form,
and then goes through an automated process of classifying these leads
where you might look at some data points, like, hey, is this company
a big company has more than ten employees. Is this company located in the U.S. or is this company located somewhere else? And depending on the answers
for those questions, you might give a different score
for these companies or treat them differently
on your sales process. So this is regular data
analysis and data collection. But it turns out that
now that you can use multi-agent systems, you can go beyond that
and you can go within further. So let's try something different. Let's think how a crew of AI agents
could actually help us here and do something that's better than what
we have been doing through the past few years. Let's add a crew of AI agents on the lead
generation process. So what you can do now, instead of having
all those "ifs" analysis, analyzing like specific data points for the companies,
you could have this AI agents do research. Go out there
and do data collection. And this research can be searching Google, can search
online, can search on an internal database or internal data
set that you might have whatever you want. Any place where you can find
more information about these companies. Then you can also have this agents
drawn comparisons between these companies and companies that you already have
in your data set, companies that you're already talking to, companies
that it turns out to be great customers. And then you can also have this
AI agents do some scoring so they can actually score this company,
and making sure that this company has a score that you can
actually prioritize and decide to who you're going to be sending it to. And then the final point is
coming up with talking points. So not only doing the research,
the comparison and scoring, but also getting ahead
and making sure that, you know, what are the topics
that you should bring up when you go out
and reach out to this customer and what that conversation
should look like? And now you can take that
and send that to your sales team. And you have a way better data set
to work with than what we used to have before. So this is a great example
on how regular automation can actually become way better
by using agentic automation. All right. So we talked a lot about agents so far. We talking about a lot of different types
of automations. But in the end of the day what are agents. So let's talk about that
for a second and step back.

---

## Lesson 3: AI Agents

So you probably know our LLMs right. They come with all these different shapes
and sizes and forms. And there's a bunch of different vendors. You have Open AI, you have Hugging Face, you having a Ollama. You have a bunch of different options
to tap into this. And what those LLMs do is
predict the most likely next token. What happens is if you try to chat with some of these LLMs, you're going to quickly
realize that you're going to end up having like a regular prompting experience
similar to one you get with ChatGPT, where you kind of got
to give feedback to it to make sure that through the interactions between you and this LLM,
you get the results that you need. All right,
so let's use ChatGPT for a second to see how exactly does
that interaction works and why. It could be better if we use it agents. So in this case, let's ask ChatGPT
to help us create a marketing copy for crewAI, a platform, for building AI agents. So, in here you can see that as regular ChatGPT is going to start
to write it down. What should be this copy? But it turns out to be too long. I don't necessarily
want something this long. I want to make sure that it's smaller,
something that I maybe use on an Instagram post or whatever
it might be. So now I get the chance
to provide some feedback and say like, "hey, this is too long. Let's summarize it." So once that you say that,
you can see that it starts to get better. But the only reason why we can get
not only GPT but in LLM to get a better results is true
interaction, right? Is the interation between the user in the LLM
and the feedback that you provided it that allow it to kind of correct the wrongs
and get a better results. So what you quickly realize here
is that through the interactions you can get a better results,
but you quickly become a blocker. You got to be in there
kind of like answering this questions and interacting with it
in order to get good results. It's not a thing
you want to do other work. It's just like enhancing you. But AI agents actually can break up
that and allow you to do other work while allowing the LLM
to operate autonomously. And the reason why we can do that
is that because these LLMs were trained in so much text
and they understand text, they create a state
where they kind of have cognition. And by that,
I mean that they can reasonably react. They can choose between A
and B and left and right, because they can put words together
in a way that makes sense. So when you achieve that state,
if you can have the LLM to kind of insert
some questions, an agent is born. So the agent is born when you get these
LLM to basically into in their thinking process throughout it ask questions
and answer the questions itself to the point that it can move on
and get better by itself. So once that you get into that stage, it allows you to pass
a task into this agent. And throughout this thinking process, this agent can
then come up with a better answer. It's not the first answer
that it would have given you, but it can
then think through and optimize the answer up to the point that satisfies itself
and then spits it out. But there is one thing missing here,
a big component that makes this agent super powerful,
and that's the ability to use tools. Other frameworks
might call them SKUs or capabilities, but what they allow you to do is to your agent
to interact with the external world. It allows your agent to do more things that don't necessarily
would be able to do with itself. It could be calling an API,
it could be posting something, it could be gathering a data point,
whatever that might be. In these, this is a fully fledged agent. So let's talk real quick
about what our multi-agent systems. So multi-agent systems grow on top of the agent behavior
that we just described. Where instead of having just one
agent, you can now can have multiple of them. So whenever you task
an agent with something this agent can also task another agent
with another task. And in the end
you get one single final answer. But you might be wondering
what are the benefits of having that instead of having one single agent? Well, I do name a few, but we're going
to dig into that in further lessons. The first thing here is
that you can have each agent be customized to do one single thing and do it well.
You can have one agent, for example, being a researcher
and another agent being a writer. So that allows your agent,
that is a researcher to focus on doing one thing and making sure
that it finds all the sources that check all the sources that include
all the services and your writer just use that in order
to create the most amazing material ever. And the other good thing is that
because you have multiple agents, you can have them run from different LLMs.
So you can have your researcher running on Llama-3,
while your writers running on GPT-4. You can also have your own fine-tuned
version model powering some of those agents.
So you can see how a multi-agent systems can be so much more powerful
than single agents, because allows you to get
very focused agents that will be able to achieve
better results than if they're trying to do everything
themselves, while also tapping into this ability to use different models
from different sources. And we could keep going even one step
further, where you can actually say, "well, now I want to multiple multiple agents,"
but this is getting to meta. now I want to multiple multiple agents,"
but this is getting to meta. So I step back for a second
and let's first build our first multi-agent systems. For all the examples in this course, we're going to be using a super powerful
framework. It's called crewAI
and it's open source. It's simple and it's designed
for production use cases. It also offers a platform
to bring your agents into production. But all the concepts that we are going to discuss here
apply to all major frameworks out there. Before we jump into examples,
let's talk about what is crewAI? I want to take a solid moment to describe
why all of the options that we have out there. We are using crewAI on this course. crewAI is
a framework and a platform. And there's a few things that it offers
that makes it super easy and super meaningful for us. The first thing is, it breaks all these
concepts into very simple structures. So it makes super simple
for you to pick up on them. The second one is that it provides
a pattern to put these systems together, so you don't need to think about
how you're going to string all of this, because it already kind of offers
you an opinion on that. The third thing is that it provides many
tools and SKUs that are ready to be used, and we are going to use them
throughout the course. The fourth one is that it gives you
a module to build custom tools or agents. In some of our lessons, we're going to get
to build some of those custom tools, and you're going to see how helpful
that is. And also as a final touch point,
it also offers a platform for bringing these agents into production. So whatever you're building
throughout this course, you're going to be able to also deploy in production
through the crewAI platform if you choose. So All right. So let's start looking
at some of our initial building blocks. In this case, agents, tasks and crews. We're going to be diving into those
and building our first multi-agent system at the beginning of our next class. So if you like what you heard so far,
if you got excited about any of the examples that you mentioned,
I recommend to stick around, because things are only going
to get more interesting from here on. Though so much they're going
to be able to build with AI agents that I promise that are going
to be impressed by the end of this course. It's going to allow you to automate parts
of your life, automate parts of your job. And honestly, I like a lot of potential. So I hope you stick around
for our next lesson. Where we're going to actually build
our first multi-agent systems ourselves. And I'm going to guide you
through all the way. So thank you so much
and I'll see you in the next class.

---

## Lesson 4: Create agents to research and write an article

All right. So you learned a lot about agents already. You now understand a little more
about how they work, when they're made
for what makes them tick. Now let's get our hands on
and actually build our first multi-agent systems ourselves. For this one, we're going to be building
a crew that is able to do research and write an article for us. You're going to see how these agents work together,
and how you're able to create something that's super valuable, true multi-agent collaboration. So you stick around,
you're going to really like this one. Let's dive into it. All right. I'm super excited about this. We're going to be talking more about how
to actually build multiple agent systems. I honestly believe this is the future. It's going to be a key part
of how businesses are going to be built and how engineers can drive an immense
impact on your jobs and your career. We are going to start by looking at how
we can build our first multi-agent system, and we're going to try to do things
simple. I'm going to start by
just copying some code in here, making sure that we don't
get any warnings along the way. So we're going to start by importing
the three main things from crewAI. We're going to import
agent, task and crew. Those three classes
are the main important part from crewAI and how we are going to be building
those multi-agent systems. Now that we have imported them,
we got to choose what is going to be the LLM that is going to be the brain
for all of our agents. So in crewAI, you can choose your agents
to be run from different LLMs and by the food
they all run from GPT-4. But in this case, let's make sure
that they're running from GPT-3.5 turbo. And you can do that by setting environment
variable called open AI underscore model underscore name. And in there
you can add the name of the model. You're going to see down the road
that you can connect your agents to any LLMs out there
that are not necessarily Open AI. You can use local models. You can use any other major providers
out there. So for this,
let's make sure that we are using GPT-3.5. So let's start by creating our agents.
Agents are corner piece of how we're going
to build the multi-agent systems. So for this use case we're going to build
three different agents. We're going to have a planner,
a writer and an editor. These three agents together are going to help us come up
with amazing technical articles. So how do you create an agent? Well, it's pretty straightforward. You basically create an instance of the
agent class. When creating that instance, there are a few attributes
that you really care about, namely the role,
the go, and the backstory. So let's look into that. For our planner,
we want to make sure that we set a role that matches what we want it to do. So we're going to keep it simple and we're
going to say it's a content planner. You're going to notice that in the following of lessons
we might do more complex roles and goals. But for this one, let's keep things
simple. Now let's set up a goal for this agent. The goal for this planner
is basically plan engaging and factually accurate content
on a given topic. You notice here how we're interpolating
the variable topic within the goal. You can do that in the role. You can do that in the goal. And you can also do that in the backstory. And I'm going to show you
how that plays a role on actually running these agents down the road. So now let's set a back backstory
to this planner agent. So if you look at this,
you might be wondering, why are we going to the trouble of setting up the role
that go into backstory? One thing that you're going to learn
in future lessons is the fact that agents perform
better with role playing. In this case, you can see that the agent's
playing as a content planner. So as much context as we can set
in terms of like what kind of agent it is, the better. Because it's
going to conform to what we expect. So, now I'm going to set up
a couple other attributes, namely when that say that this agent
is not allowed to delegate work to another agent,
and also making sure that it's verbose. So we can see how this agent runs its
inner thoughts. Don't worry about those two attributes for now, we're going to get into them later. All right. So now that we have our planner here we can create this agent. And there we go.
We have our planner agent ready to go. Now let's move on and create our writer agent. That is going to be responsible
to actually write the content based on top of the research
that the planner did. So in here you can see that
we are doing a similar thing. This agent also has a role,
also has a goal and also has a backstory. And you can see interpellation
happening on multiple fronts. But all the interpellation that is happening is around
the same variable called topic. And we are going to see how that plays
a role in here by the end of it. So let's create our writer agent. Now let's create
our final agent for this crew. And this agent is an editor. The editor is basically responsible
to review the content, make sure that things are correctly
formatted. That's good. And it's ready to go. So let's go ahead and create
that editor agent as well. With that done,
we have three agents, but we have no tasks
and nothing to guide them. So let's now create a task
for each one of these agents. Create the task is as simple as creating
the agent. You need to create an instance of the task
class. So in here you can see that
you can just type task. In the task expect at least three attributes. The description,
the expected output, and the agent. So the description is actually
why do you expect the task to be. Why do you expect the agent to do so? In this case this is the planned task. So we expect our planner agent
to look at the latest trends and look at the key players
in making sure to create like a content or a research
that we can use to actually write it down. The other argument that we expect in here
is the expected output. And expected output here
differs from the description, because it kind of acts
as a forcing function to force you to think exactly
what you want to get out of the task when you want this agent
to produce as a final outcome. And here you can see that
we're being very descriptive about it. We are saying that we want
a comprehensive content plan with outline, audience analysis,
SEO keywords, and resources. And then the final thing that we need to do is actually assign
an agent to this task. So in this case, the agent that we're going to be assigning to
this is our planner agent. And with that we created our first task. Now let's move on and create or write
task. It's very similar
but again different different arguments a different description
and a different expected output. And here you can see that the expected output for the write task
is actually the actual blog post. And we want it to be writing as markdown,
having multiple sections in each section
having between 2 or 3 paragraphs. So with that, we are ready to go
because we have our two initial tasks. Now let's create our final task. This task is a little bit shorter
because it's the edit task. This task is where the actor comes in
and kind of proofreads the blog post. Make sure that the content is right,
making sure that we have the progress that we need
and that the thing is high quality. So we can also go ahead and create that task. So right now we have the agents
and we have the tasks. We just need one way
to mash those together. And that's
where the third element of crewAI comes in. And that is the crew. Crew basically puts together
agents and tasks so they can operate as a unit. So in here
you can see that we set three attributes. The first attribute
is a list of the agents. The second one is a list of the tasks. And then we have a verbose mode
that allows us to see how this crew is executing,
and look at some of its logs. One thing that I want to call out
is that by default, a crew operates sequentially, meaning that one task
is going to be executed after the next. Because of that, the order of the tasks. When you query the crew, it's important,
given that the output of one task is going to be sent
as part of the input for the next. So you really want to make sure
that you get that right. We're going to learn down the road
that that is not always the case. And you can have a way finer control on what order you want
those tasks to be executed. If you want tasks
to be executed in parallel, or if you want them to be executed
hierarchically, it's all up to you. For this initial use case, though,
this is going to work great. So how do we actually get
our multi-agent system run? One thing that I want to highlight here
is this verbose setting being set to two, depending
on how you're setting up or crew. You might want to be able
to see a certain level of granular logs. So in this case, you can set
your verbose node between 1 and 2. And that will define how much verbosity
you're going to see on your logs. If you're going to see all the logs
that are possible or just a subset of them in this case, because we really want to
see what is happening behind the scenes, we are going to set the highest number
possible in this case number two. So now we have our agents
and we have our tasks. So how do we get it run. How do we execute this multi-agent system. It's pretty straightforward. We use the crew
dot kickoff method. So you can do this
by basically calling kickoff So you can do this
by calling kickoff and then passing an input dictionary
into the kickoff method. In this input we have all the variables
that you interpolated throughout your tasks and agents. So this is where that topic thing
comes into play. So you remember how we interpolated this topic variable throughout or agents. when we first declare them up here. Well, now when we're kicking off our crew, we can actually send what is the word that we want to actually replace
in all those different places. So now let's kick off our crew
and see how that goes. So from the get-go, you can see that
the content planner starts off and it's starting its first task
that is prioritized the latest trend, keep players
and node worse news on artificial intelligence,
because that's the topic that we set. So we can see here
that, you know, already did that and gave us an outline of what
should be this article about what should be
the main topics that should include on it. So now we can see that our new agent kicks in, our content writer, and it uses the previous information,
the research that was made in order
to put together a markdown blog post. So you can see in here
how it's writing it all down for us. Now the editor comes in,
proofreads and reviews and makes sure that it aligns with our brain's voice
and that it looks great. And by the end of it, we should have
a full-fledged post. For doing that, I'm going to be
using this markdown helper. So once then you do that,
you can plot the markdown here and we can see what this article looks like. It's called "The Rise of Artificial Intelligence: A
Transformative Force in Today's World." And you can see that it has subtopics and each subtopics
has some nice content into it. All right. So now we have our agents
doing the work for us. And you can do it too. So I invite you to come in here and write the topic
that you want your agents to write about. And you can execute this code and see they
come alive and write this blog for you. So congratulations! This is your first multi-agent system
and works great. Now let's talk about other use cases. So throughout this course we are going
to use crewAI for all the examples. And you're going to probably find yourself
looking at our docs at some point. So let me go ahead
and tell you how the documentation that you find in crewAI
is actually written by a crew. So this is another great practical
use case that showcases how multi-agent systems can help you
with engineering work as well. Where we don't have anyone
on our team writing docs anymore, because now we have a multi-agent system
that does that for us. So I would definitely recommend you to think about all those different use cases that you could apply
those multi-agent systems into. Let's do a quick recap
about everything that we learned so far. Before we move on to the next lesson. So we now fully understand
what are agents. So we now understand
what are agents. They're LLMs
that can talk to itself. They have in your thought process. And they can receive
tasks and use tools in order to give way more complex answers
that they would be able to do otherwise. We also learned that you can have
multiple agents hooked up together, showed that one
agent can pass tasks to another agent. And by doing that, you can have specific
agents that are great in one single thing. Basically, we learn the three main pieces
and the corner pieces of crewAI. We learned about agents, tasks, and crews, and we now know how to put them together. But there are way more things
that we learned throughout this. First, we learned that agents
perform better when role-playing. Two you should focus on goals and expectations
whenever creating or tasks in your agents. You need to make sure
that you are setting up in a way they know what they're doing
and they know what is expected of them. Three one agent can do multiple tasks
if you want you. In our use case, we had one agent for
every task, but we could go beyond that. We also learned
that tasks and agents should be granular. You can see how we focus each
agent on one very specific thing. And we also knew that tasks
can be executed in different ways. We talked about
tasks being executed in parallel or sequentially or hierarchically. And we are going to dive
into all that in future lessons. And we also talked about how it's pretty easy to create
multi-agent systems with crewAI. So, thank you so much for sticking around
and learning more about multi-agent systems in this lesson. I'm looking forward to seeing you
in the next one, where we're going to dive even deeper
into how to build these agents, and making sure that we are taking
full advantage of them and their tools.

---

## Lesson 5: Key elements of AI agents

Let's talk about some of the concepts behind multi-agent. Because so far we're able to put together
a multi-agent system yourselves. But we want to make sure to understand
why make them great. So, what does make an agent great? Well, there is at least six elements
that make an agent, a great agent. The first one is role playing. The second one is focus. The third one is tools,
the fourth one is cooperation. The fifth one is guardrails,
and the sixth one is memory. A lot of that is what make good employees as well. You're probably good at a job
because you're able to focus, because you're able
to use the right tools, because you're able to cooperate
with others, because there are certain gaurdrails
and you should have good memory. So let's dig into each one of those
and talk about how this comes together
to help this agent be better. So let's start with role play. So the first thing is role play. Role playing can make a huge difference in the responses
that you're going to get from your agents. The ability for them to kind of like
just take the shape or form or function for something else
will have a direct impact on what kind of answers you're going to get
and kind of like what you're going for. So here's a quick example on how
that plays a role, even on a chat setting. But it plays an even bigger role
once that you're doing on an actually agentic system
where there is way more messages going on. But in here, I just asked ChatGPT
to give me an analysis on the Tesla stock. And then I ask the same ChatGPT
to give me analysis on the Tesla stock, but now I just said some context
for each to role play into. Saying that "you are a FINRA approved
financial analyst." So let's see the difference
between those two answers. The first answer you can see that
it basically mentions about many factors. It kind of talks
about financial performance. But the second one you can see
that is already digging straight into it, talking about Nasdaq,
talking about like the actual Tesla stock
and talking about EV manufacturing market. And you can see throughout the response, that I'm
going to spare you from seeing here how that played a role on the response overall. So this is just a tiny example. Not saying that it's better or worse,
but the role, the context that you set for your agent does have an impact
on how it's going to respond. So my call out here, is to be mindful
as you're creating these agents to make sure that you're
setting the appropriate roles, the appropriate goals
and their profit backstories, because there will play a role in the kind
of results that you're going to get. But let me step back for a second,
because I want to count out one thing. Realize how we use FINRA
in our context setting. We can't have just said that this Chat
is an actually financial analyst, and that's it. But by choosing the "FINRA" keyword,
we're helping the RAG LLM
to give a certain type of answer. So in here,
you can see how being careful and mindful about how you choose the role,
the go, and the backstory and the keywords that go into that,
allows you to get better results out of it. We actually have customers and users
using crewAI worldwide. They're applying similar concepts to get better results
out of their multiple agent systems. So, I would be mindful about
when you're setting the goals, the roles, and the backstory
to make sure to use keywords that will actually help you
and will get you better results. All right. So we talked about role play. Let's talk about focus. Focus. This is another big thing. And I'm not talking only about context
windows. We know nowadays that LLMs have longer
and longer context windows. And you can leverage that in order to produce amazing content
and to also import a lot of content. But the one thing that becomes clear
throughout many researches, is that if you mix things up too much,
doesn't matter if you're talking about too many tools, or if you're talking about
too much information or too much context,
your models can lose important information and also open up opportunities
for more hallucination. So another thing that makes agents
great is their ability to be focused. And when I say that,
I mean focused on the amount of the tools that they get to focus on,
the amount of content that they get sent in also focused on
what they're actually trying to achieve. You shouldn't
rely on one agent to do it all, but instead many agents
that work better together. We have seen this in the industry. People that are using crewAI out
there have way better results when they are using multiple agents,
compared to when you're using one single agent
throughout many different verticals. So all right, we know that agents work better when they're role-playing
and when they are focused. So what about tools? That's another common thing. People tend to try to give a lot of tools
for their agents. And that can get confusing. You can overload your agents
with too many tools, so they're going to have a hard time
to choose a tool. They may end up
not using a tool that they should, and you may end up having even bigger
problems if you're using smaller models, because then they're going
to get even more messy, not being able to distinguish
what is the tool, what is the context, what they're trying to achieve, because these smaller models
are also less capable in general. So, another rule of thumb that we tell for
everyone that is using crewAI out there is to choose the tools
that you're going to give your agents. You want to make sure that you're providing them with the key tools
to do the job that they need. The same way that you would do
if you're hiring someone or if you're getting someone
new on your team. All right. So we already know that agents
now are great at role-playing focus and using tools. Let's talk about cooperation,
because that also is another thing
that makes a huge difference for agents. Ability to cooperate
and to bounce ideas off each other makes a huge difference
on producing better outcomes. The same way that when you're talking
with ChatGPT, the process of having a conversation and giving it feedback
helps it to produce a better outcome. The ability for these agents, they're now
role-playing to talk to each other and simulate that same chat behavior
creates a better result. They can basically take feedback
from each other. They can delegate tasks to each other. And by doing that, produce
a better outcome. So, it doesn't matter if you're using crewAI
or any other framework out there, you want to make sure that your agents are set up to be able
to collaborate with each other. The next one is guardrails.
And guardrails is so important because remember that we're now
talking about AI applications. And we have talked about this in the past,
AI applications in applying fuzzy inputs, fuzzy
transformations, and fuzzy outputs. That means that you don't necessarily
get strongly typed results. But that's okay
because that's part of the application. That doesn't mean
that you want hallucination though, or that you want your agents
to get stuck on random loops, or using the same tools repeatedly,
or taking too long to give an answer. That was actually a problem
that we had early on on the first versions of crewAI,
where agents would be stuck trying to use the same two over and over again,
especially if they're using open sources models. But we fixed that,
throughout many iterations we implemented a series of guardrails
that prevents your agent from derailing and nudge
our agents to stay on track. And most of those are implemented
on the framework level. So make sure to check whatever framework
they're using. I can tell that crewAI has a bunch of them, but it's also something that you want
to consider when building custom tools, as we are going to discuss later
in this course. But these guardrails are going
to make sure to prevent hallucinations, and also make sure that you get a reliable and consistent results
throughout your multi-agent systems. All right. Now there's just one last thing
to talk about, memory. The memory can make a huge, immense difference on your agents. If anything, it can make more difference
than all the other things combined. Memory is the ability of your agent
to remember what it has done. And not only that, but you use data to
inform new decisions and new executions. The ability
to recollect what they did in the past, learn from it, and apply their knowledge
into future execution. Some frameworks will offer different types
of memory and different types of implementations for it. In the case of crewAI,
because we are using this, our agents will gather three types of memory for free,
out of the box: long term memory,
short term memory, and entity memory. Short term memory is a memory that
it leaves only during the crew execution. Every time that you run a crew and
you kick it off, it starts from the blank. These memories useful because as different
agents try to accomplish different tasks, they store different
things that they learn in this memory. And these memories are shared across
all the agents. Meaning that an agent number two
or an agent number three can tap into learnings
from agent number one shows a short term memory,
something that helps to share context during the crew execution
so that you get better outcomes. Now let's talk about long term memory. As the name suggests, long term
memory leaves even after the crew finishes, so that memory is stored
in a database locally. And that allows your agents
to learn from previous executions. So every time that your agent completes
a task, it self critiques itself to learn
what it should have done better, or what are the things that should be in there
that are not, and stores, that information so that it can tap back into that
when it's running once again and then use this knowledge to produce
better and more reliable outcomes. The entity memory plays
a role in here as well, as it's also short lived,
so it's only needed during the execution. It stores what are the subjects
that are being discussed. So if your agents trying to learn
something about a specific company,
it might store that company as an entity and its understanding of this company
in this database as well. So to gather entity short and long-term
memory plays a role on helping our agents
to get more reliable outcomes. If your agents didn't have a memory,
you would probably get is likely different results
every time that you run them. But because they do, you
not only get more reliable ones, but you also get increasingly better ones
because they learn from their mistakes.

---

## Lesson 6: Multi agent customer support automation

Okay. By now you're starting notice
you're seeing how these things are coming together, right? You can see how you can view these agents
and how they work and how can they be super helpful. So let's try to expand on that. Let's start to think about
what other use cases. What else can we build. In this lesson we're going to be using
a multi-agent system to help with customer support automation. So it's a different use case
but a very interesting one. Stick around I'm
sure that you're going to like this one. Let's dive into it. All right. Welcome to this lesson. I'm super excited about this one
because we're going to be talking about how to use multi-agents
for customer support automation. And that is such a big use case. If you think about customer support
it feels like a no-brainer to have AI agents, to help our customers,
to have just a better service in being able to tap into all of the docs,
knowledges, and help center
in order to provide very meaningful answers to these people
that are trying to use customer support. Let's try to do some code
and see how that works. Again I'm going to start
just doing some boilerplate code to make sure that warnings don't
get in the way. And I'm also going to import
the same components that we learned on the last lesson,
where we bring the agent, the task and the crew classes into this. For this example, we are going to be using
GPT-3.5 turbo once again. So let's go ahead and set that
environment variable. All right. So now let's dive into agents
and how we can make them great. How we can bring everything that we learn in the slides
into actually creating this agents. So we know that agents are impacted
by the role-playing, the focus, the cooperation, the tools,
the guardrails and the memories. All right. So for this use case, we are going to be
building a support multi-agent system. The goal is going to be to help supporting customers that might have wing queries about a product. supporting customers that might have inquiries about a product. So the first agent that we are going to
create is a support agent. So this support agent
should be straightforward. You can see here that the role is
a senior support representative. You can see how we use the key
word "senior" here again to imply that we expect answers that are a little bit more polished than what you would
mostly get out of the box. For the goal, we also mentioned that the goal
is to be super friendly and helpful. So there will also play a piece
on every stab on the process. And for the backstory,
we basically told this agent works at crewAI And for the backstory,
we basically told this agent works at crewAI and they are helping a specific customer. You can see the interpolation
happening here. Again,
trying to answer a specific question. But that agent alone
is not going to help us. We're going to need another agent as well. So this other agent is going to be
a support quality assurance agent. So let me copy that and paste it here. So this agent exists to help the support agent by fact
checking everything that it says and making sure that is the best response
possible for this customer. All right. So now we have both our support
agent in our support QA agent. So far we can see how we are doing very focused approach here.
Where we are prompting the agents to be very much
getting into the character of their role. You can also see how one agent
is not allowed to do any delegation, because we are setting
allow delegation to false, but we are not doing that for the support
quality assurance agent. That means that this agent
can delegate, work back to the original support agent
if it decides to. So this is an important trait
for your QA agents. Make sure that if they find something
that doesn't feel right, they don't necessarily
need to fix themselves, but they can actually delegated back
to another agent that might be better suited to do it, because either has like
the right set of tools or the right set of backstory,
goals and roles. So you might be wondering
when exactly an agent decides that's reasonable to delegate work
to another, or to ask question to another. And this is some of the differences
between regular engineering
and AI engineering. AI applications, again, they have fuzzy inputs, fuzzy transformations and fuzzy outputs, meaning that they don't necessarily
follow the same pattern all the time. So in this case,
we're relying on the brains, the LLMs, to make a conscious, reasonable call on
when to delegate and when not to delegate. All that goes back to the fact
that these models have a level of cognition,
because they understand the language. So depending on the customer inquiry,
they may understand that it's worth delegating
and to do more research. But if it's more simple inquiry
that demands a simpler answer. You might not want to delegate it back. So this is not something that you
necessarily will have full control off. But you don't really want to, right? That's the magic of AI apps. It's the ability for these apps to react on runtime, on how they're going to handle
with the information that they're being handled. So make sure to keep that in mind, that allowing an agent to delegate work
and ask questions don't necessarily imply
that it's going to do it every time, but that instead will give it the ption to do
so if it chooses to. So this is one way on how you can get
your agents to collaborate together in a great example, and how collaboration
helps with better quality responses. So this is a very common pattern
that we see throughout many users on crewAI. I usually having a final agent
that is kind of like a quality assurance
agent helps a lot and go a long way because they can do a final pass
on whatever you want to do: writing a blog post, entering a customer,
whatever it might be. So I do recommend you
considering adding a QA agent of sorts into whatever
multi-agent systems that you do, and that does tend to perform better
than regular, regular agents without it. So far, this is a great example of role
playing focus and cooperation. All right. So now let's move on and talk about tools,
guardrails and memory. For that, we're going to be using crewAI tools. So crewAI also has a tools package with a set of tools that you can use. They have simple ones, like the ones
that allow you to search the internet They have simple ones, like the ones
that allow you to search the internet to more complex ones
that allow you to do RAG over GitHub
if you want to, or websites. There is many that you can explore, but we're going to stick with
some of the simpler ones in here. We're going to use the server dev tool. We're going to use the scrape website too. And we're going to use the website
search tool. Server dev to basically integrates
with server. It's an external service
that allows you to search Google. Scrape website is a simple scraper
that allows your agent to access a given url and extract
the contents of that. And the website search tool,
is actually doing RAG over a website. If you don't know what a RAG means, it's
basically doing a semantic search
over the content of that website. So, in here you can see that
we are importing the crewAI tools package in then, these three
classes from it. And so let's go ahead and run that. So this is a great place where you can
also think about other tools. So we're not going to talk about
creating our custom tools right now. But this is a place
where you could bring like tools that load customer data
that tap into previous conversations or that load data from a CRM,
checking existing bugs, feature requests, or ongoing tickets,
all useful tools that would help these agents to provide
better answers to the customer inquiry. So you can see here on how
you should be thinking about what tools you should provide to your agents in order
for them to provide meaningful responses. All right. So for every crewAI tool, there is a few
different ways that you can use it. Let's say that we want to use the server dev tool. This is the only thing that we would need to do. Create an instance
of the server devtool, and we assign that into a variable
and we should be able to use that. We can also do the same thing
for the scrape website tool, where we create
an instance of that. And now we have that a tool. And we can assign that to an agent
or to a task. But another interesting feature of crewAI is
that you can also be more specific about how you want
these tools to be used. So let's say that in this case
I want of my agents to only search the crewAI docs. So I don't want it to be able
to scrape any website out there. But I wanted to scrape specifically,
one single page off our documentation. So I can actually do it when I instantiate
this scrape website too. I can set an optional argument
called website URL, and in that URL I can set a specific URL that I want this to to be able to scrape. So here is a great use case
where you can see that you use the same tool,
but one tool, would allow your agent to scrape any URL
that it becomes aware of, as long as the agent teams that are
scraping that URL would be beneficial. The second one allows your agent
only to scrape one certain URL,
and not every URL that it finds. So you can see how this can be very
versatile as you're building our agents. For now, let's focus only on our docs search tool
and see what our agents can do with that. All right. So now we already understand
how we can bring tools into this. So how do we assign those tools?
How do we give our agents those tools? There are basically two different ways
that you can give your agent tools. You can give them at the agent level
or you can give them at the task level. What that means is that if you give your
agent a tool that tool belongs to the agent, it can potentially use that
to for any task that it performs. But if you give it to the task,
that means that the agent will only use that tool
when performing that specific task. So an easier way to put this, is that task tools override the agent tools. So an agent
might have ten tools at his disposal. But when performing a given task,
if that task only says that it has three tools at his disposal, then
the agent will only use those three tools. So let's start by creating our first task. And the first task that we are going to do
is the inquiry resolution task. So in here, you can see that we are playing
even more with the interpolation. Where we are saying, "hey, this customer, just reached out
with a super, super important ask. Here is the inquiry. The person that works at this customer
is the one that reaches it out. Make sure to use everything that you know
to provide the best support possible. You must strive
to provide a complete answer." So you can see here how this looks like
more, regular prompting. But we are using that interpolation
in a lot of different ways. And then again,
we come with an expected output which very clear instructions and what we want
to get back from this agent. And we provide the tools in here. So the tools is just an argument
within the task. And it's an array that includes all
the tools that you want to be available when the agent performs this task. In this case,
it's only one tool, docs scrape tool. So let's go ahead and create this task. Now we're going to create our new task. That is going to be the task
that the key way agent will use in order to review the work
that the support agent did. So it's a similar task
that doesn't use interpolation but rechecks
what the agent viewed. You can see that in this case
this task has no tools at its disposal, meaning that the QA agent,
when performing this task, won't be able to look at our docs. It's purely assessing what is the actual
response by the support agent wrote. All right. So now we got our two tasks
that were created. That's great. So let's put our crew together.
Create our crew. And in this crew,
we're going to bring our two agents the support agent
and the support quality assurance agent. And also the two tasks
the Inquiry Resolution and Quality Assurance review task. And also, you notice
that we're using memory for this one. So using memory with crewAI
is super easy. You don't have to worry about it. You don't have to think about it too much. You can set this one
single attribute on your crew, and that enables
all those memories for you. The short term memory, the long term
memory and the entity memory. So you don't have to configure anything
other than set this one flag and everything works out of the box. So let's now focus on executing this crew so that we can actually get some results from it. In order to execute this crew,
we need to pass inputs to it. We need to basically override
all those interpolations We need to basically override
all those interpolations that we did in the tasks
and in the agents definitions. So in this case
we had three main interpolation variables. We had the customer
the person and the inquiry. Here, we are saying
that the customer is DeepLearning.AI. The person that is asking
the question is Andrew. In the inquiry is it needs help
setting up a crew and kicking it off. And you want to make sure that it's
using memory to set up that crew. Can the agents provide some guidance
and actually help Andrew with that? Let's see how our agents do in
trying to help Andrew. So from the get-go
you can see that our senior support representative
is kind of like kicking things off starting to look
into the issue that Andrew brought up. You can see here
the interpolation play its part where DeepLearning.AI, it's
kind of like popping up in the task. So we can see that the agent now decides
to read the website content, and it's actually looking into the documentation
that we provided it with. So with the access to that documentation,
it's learning everything about crewAI and how to create these agents, how to
create the crews and how to kick it off. And then it comes up with an answer. In this answer
you can see that it's super polite. It's says, "hey, Andrew. Hey, dear Andrew,
thank you for reaching out for assistance..." And then goes on into explaining
how to install both crewAI, crewAI tools, how to create agents,
and then how to create a crew with the memory and everything with it.
And you can see that once that this work is done,
we now have our next agent. The support QA specialist kicks off to make sure
that this is the best answer possible. So in here you can see that it didn't really like some of the responses. So we decided to delegate the work
back to the coworker asks this to review
and revise the response to ensure that it's comprehensive,
accurate, and friendly. So now, if we write being a little bit more friendly on the response,
you can see that it's more direct. It's basically saying like,
this is how you set our crew in, this is how you add memory. Because those were the specific topics
that Andrew originally asked for. So, you can see here
how the answer looks way better. And now we should be able
to get back to Andrew with that. You can see that the agent still
is not super fan of that. So we decided to ask question
to the coworker again to confirm if those are how the steps
to create a crew and to add memory. And if there's nothing
that is missing in there. So this agent kind of gives like more information around anything that might be helpful. And after that it puts together
a final answer. And the final answer
says: Hello DeepLearning.AI, Thank you for reaching out
for assistance in setting up a crew and adding memory. I have reviewed the response draft
and made some revisions to ensure clarity and completeness. Below are the steps
that you need to follow." And then goes on like with the steps to create the crew
and to add memory to that. So now this is something
that we could actually set up and send back to Andrew. Make sure that it has all the information
that it needs. And there we go. We created a new multi-agent system that is now capable of collaboration. So two agents are navigating
and asking questions to each other. They are using memory. So they remember what they are doing
as they are doing. And they are very much going
into their roles by using role-play. So you can see all those elements
that we talked about in those lines
being played at here at real time. So let's go back to our lives real quick.

---

## Lesson 7: Mental framework for agent creation

So I want to share a mental framework
with you for the agent creation. I think it's super helpful
because if you look at the agents that we put together right
now, it'll work at great. But what about when you decide to put together other agents
in other multi-agent systems? How do you make sure that you're creating
agents that are the best they could be? So I have a mental framework
that I like to share and I think will be super helpful to you. So the framework is
to think as a manager, honestly, there is a very high correlation
between being a good manager and being able to create
great multi-agent systems, because managers are conditioned
to think about what is the goal and what is the process. So whenever you are creating
multiple agents crews or your multiple agent systems,
I would say think about exactly what is the goal
that you are trying to accomplish, and then what is the process
that you're trying them to follow? If you think like that, you're going to
then start to think about what are the people
I would hire to get this job done? So that's the thing
you want to be asking yourself. If I had to hire people to do this,
what would it be the people that I would hire? So once that you get that answer,
you need to know what agency need to be. And more than that, you're going to know
exactly what should be their roles. What should be their backstories? What should be their goals? Because, you know, who would
you want to be working on these things? So let's talk about some examples. These are some examples
that are not necessarily the best. Like if you want to create, for example a use case related to HR,
you don't want necessarily you only a researcher,
you want an HR specialist. And that place across all the examples
that we're going to see throughout this course. So, better examples would be an HR research specialist,
instead of just a researcher or a senior copywriter,
instead of just a writer, or a FINRA approved analyst
instead of a financial analyst. So I would recommend you really think
about what are the keywords. What are the actual people
that you would hire to do this? And then once that you have those people in mind,
think about what would be their goals. What would be their roles?
What would be their backstories? Those are the agents that you want imbued
in in the community that uses for AI, we noticed that the people that get
the best results are the people that really think
about agents in that way. They think about what would be the people that they would
hire to do this job for them. All right, let's do a quick recap to see
everything that we learned this lesson. First thing we learned
that agents do a better job if they have a few things:
they are doing role-playing. They have focus. They have the appropriate tools. They're allowed to cooperate. They have some guardrails. They also can leverage memory. All right.
We also learned some other stuff. We've learned that agents are able to self
improve by using memory. We also learned that
crewAI prevents our agents to get into rabbit roles by making sure
to steer them in the right way. We also learned that the agents
we always attempt to get you an answer, and we also learn
that smaller tasks in focused agents, perform better than bigger tasks in agents
that have too much on their hands. Also,
focused use plays a huge role on that, and we are going
to be talking about tools next. So thank you so much for sticking around
for this lesson. Honestly, it has been incredible
to go over this with you. I hope you're having as much fun
as I am and stick around for the next one. It's going to be super fun. We're going to start talking about tools
and guess what? Tools is what unlocks
a lot of the fun use cases. So I'll see you in the next lesson.

---

## Lesson 8: Key elements of agent tools

All right. So what was that? We just built a super
interesting crew for support. But things can get even more interesting.
On this lesson, we are going to use tools
to build a customer outreach campaign. That's going to be super interesting because sales is a very common
use case for multi-agent systems. So let's look into that real quick. Welcome back to our new lesson. We are talking about tools. Tools are such an important part of crewAI and of any multiple-agent system out
there. Tools want to allow your agents
to communicate with the external world, to get out of their bubble,
of just chatting with themselves and actually perform actions
have an actual impact on your flows, on your systems, on your users,
and on your company. So it's a super key part
that makes agents great. So what makes a great tool? What makes a tool set itself
apart from another? Well, there is at least three things
that we found from the many users that use crewAI
that set tools apart from each other. The tools that are versatile, the tools, that are fault-tolerant,
and the tools that implement caching. We're going to talk
about each of those topics right now. So what it means for a tool
to be versatile. Well first thing: the tool needs to be able
to accept different kind of requests. The tool is the connection between the AI apps that have fuzzy inputs with the external world
that have strong typed inputs. So your tool needs to be versatile enough
so that it can handle the different things
that the LLM might throw at them. So crewAI supports converting
this arguments into the correct types, and they can handle the different nuances
coming out of your agent. But if you're building it to yourself,
you want to be sure that whatever the LLM sends your way,
you want to treat it properly. You want to convert it to the appropriate
type so that you can actually use it. So one big piece of making a great tool
is making sure that it's versatile. It can handle different types of inputs. The second thing: is being fault-tolerant. This is a thing that a lot of people
that were using AI agents early on realized that as your agent passes
information to your tools, things might break
and you going to get exceptions. If you get exceptions out of nowhere
and you don't treat them right, you stop your crew right there
because it stops the execution. And you don't want to do that. So you want to make sure that your tools
can fail gracefully. So in case something goes wrong
they can kind of self-heal crewAI actually implements
that by default for you. So even if an exception happens
when running a tool, instead of stopping the execution,
it sends that message back to the agent
so the agent can take action on that. Maybe it's the input. Maybe the agent should have sent
a different kind of input. Maybe the agent had missed on a required argument,
or maybe there was just another problem. But the important thing is that your tools
should be self-healing and should fail gracefully in a way
that doesn't stop your agent execution. This is something that we see
a lot out there. When you deploy these agents at scale,
especially in enterprise companies, you're going to have agents
dealing with all sorts of documents and all sorts of sources
for files and information. So you want to make sure that the tools
are able to handle all that and able to handle when seeing something
that they don't expect. We actually have seen this in
some of our biggest users, where you're analyzing
huge amounts of financial documents and sometimes the numbers
might not be the easiest ones to read, or the text might not be the easiest one
to parse. That aside, you want to make sure that your tools
kind of work around that a little bit. All right. So you have a tool that is versatile and
you have a tool that is fault-tolerant. That means that you got a lot of that job
done. What about caching? Caching is key to making these tools
worth it and usable in the real world. Whenever you have a tool,
most of the times, that you is using
to communicate it with the web. So it's going to call
different APIs. It's going to call different services. Sometimes it's going to be internal
services. Others are going to be external services. And whenever that call happens,
you want to make sure that you're being mindful
about taking the time to do the request and also not doing the request
unless necessary. So having a caching layer
that prevents unnecessary requests from happening is crucial
to make sure that you're building optimal crews. So you want to make sure that you have
not only cache but you have a smart cache. So in crewAI we offer cross-agent caching. What that means is that
if one agent tried to use a tool with a given set of arguments, and another agent try to use the same tool
with the same set of arguments, even if they're different agents, they're
going to actually use a cache layer. So the second time they try to use a tool,
they're not going to do that API call. That makes a lot of difference. That prevents unnecessary requests,
that prevents hitting rate limits, unnecessary consumptions,
and also saving the execution time. Making sure that you're crews
in your multiple agent systems run faster. So caching is super important
when you're building crews that you need to run at scale. What are some examples of tools? Well,
there's a bunch that we can talk about. There are the simple ones like
search the internet or scrape a website, tools that we actually have used ourselves
but goes beyond that. You also can connect to a database. You can call an API, you can send
notification and many, many more. So you can see here
how tools are such a cornerstone. And that is the case for all the frameworks out there,
including crewAI. Showing, crewAI tools are such an important piece that crew offers a bunch of them
out of the gate that you can use. So whenever you have
the time in the future when building your own tools, make sure
to check crewAI's documentation where you're going to find all the documentation
for all the existing tools in there. Also, another thing that's important
to highlight is that crewAI supports all LangChain tools,
so LangChain can also offer a huge set of existing tools
and you can use them right away. We share crews using crewAI. So just another thing to highlight. But enough of that. Let's jump into some code and see how
we can build some tools together.

---

## Lesson 9: Tools for a customer outreach campaign

All right. To get things started, let's
get some of the boilerplate code in here. And let's start build our crew. So, first thing that you want to do is make sure that you import
the agent task and the crew class again. Once that you import that, you're good
to go and ready to get started. All right. So now that you imported the agent,
the task, and the crew class, we can set up
the model that we're going to be using. So for
this one we're going to be using GPT-4. So you have been using
GPT-3.5 up to this point. But we are moving to four now because
we're going to be handling with more data. So you want to make sure that you have
that extra context window to handle all the information that we are
going to be sending to this agent. So let me just copy and paste in here. Another thing that you're going to notice
is that we are using serper API here. So serper is basically an API
that allows you to search Google. And you're going to be provided
with AI key that you can use. But you can also go into their website
and sign up and they offer free credits. But honestly, there's a lot of other like
search tools that we could use as well. We just choose to use serper
in this example. So let's go ahead and just execute that. All right. So now we're ready to dive into tools. We basically want to make sure
that we use some of the crewAI tools. And we also want to make sure that we create a simple custom
tool to show you how that looks. So let's
go ahead and start creating our agents. We are going to have two agents for this. The first one is going to be a sales
wrap agent, because we are going to be doing a sales
use case this time. The sales rep has one goal,
and that is identify high value leads
that match our ideal customer profile. People like to call that ICP in sales
is a big use case for multi-agent systems. So probably you're going to see
a lot of that around the internet as well. You can see that in the back story. We set some context around the fact
that the sales agent works at crewAI in some of the mission around it
and everything. You also going to notice that this agent is not allowed
to delegate any work or ask any questions. It's just supposed to do what it's told. We're also going to create a new agent. and that's going to be our lead sales
rep agent. So let's execute this
and then create a new one. So this leads sales rep agent. You're going to see
that it builds on top of our previous one. It has a different go. This go is kind of
the actual personalized content. And build a personalized communication
with this lead that we're going to be working on. So the idea of this crew
at the end of the day, it's given a lead,
find out a way to communicate with them that helps them
to get an interest on through crewAI. So let's see how that's going to play out. So let's first execute this agent. All right. So now we have those two agents created. Now it's time for us to look into
the tools that we are going to use. We are going to be using the crewAI
tools package again. So you can go ahead and type
that out and import those tools. You're going to see that we are using three
tools this time. We are using a directory read
tool we're using a file read tool, and we are using a serper
dev tool. So the directory read tool allows your agent
to read any directory that it wants. Or again
you can kind of like confine its options by seeing a specific directory
that you want wanted to run. Then the file read to the same thing. And the Serp tool we already talked about that
in another lesson. It allows you to search the internet. So let's go ahead and instantiate
those three tools. So you can create a directory read tool, the file read tool
and the search tool. And the one thing
that you're going to notice is that on the directory read tool,
we are specifying that we want it to be able to read
only this local instructions directory. So in this directory,
there are a series of instructions as markdown files on how to handle
companies from different sizes. So we're going to have big companies,
small companies and medium companies, instructions
on how to handle them. And we're letting our agents
being able to read these files by setting up these tools that allow them
to actually, look at that folder. So as you can see,
we now have three tools that we're using here: are directory read tool or file
read tool, indoor search tool. And you can see there are all similar but the directory read
tool is actually passing one attribute called
directory. This attributes forcing this tool
to only allow the agent to read this one single directory in this case is a local
directly called instructions. So this local directory
basically holds a set of instructions
on how to handle some of those customers. If it's a big customer or a small customer
or whatever it might be. Let's look at those files
real quick. So here you can see that
there are three files inside that directory, a file that has a set of instructions
to how to handle a small business,
and how to handle tech startups, and on how to handle, like,
more enterprise deals. And you can see here
there's like a specific template. There is key strategic points to address. There is there is introduction. So everything that our agent
might need in order to actually engage
with like a specific company. So now that we have our tools here,
we can create a custom tool
just to see what that would look like. So every framework out there
it's going to give you a pattern to create a custom crew, and crewAI is no different. It offers a couple different ways
that you can use to create a custom tool. So in this case,
the way that we are going to be using is by inheriting from a class inside
crewAI, we can import this class. It's called BaseTool. And now that we've imported it,
we can create our own class, that's going to be our tool,
that inherits from that. So in this case our class will be called
Sentiment analysis tool. So you can envision that at least you
would do some sort of sentiment analysis. But this could be anything. This could be an external API call
or whatever you want. But in this case we're just going to fake it a little bit
to make sure that we build a custom tool. And we learned how to do it. So one thing that every tool needs to have
inquiry crewAI is a name and a description. So in here we are setting the name of this
tool to sentiment analysis tool. And the description tells the agent
when it should use this tool. And what is its purpose. So in here we're saying that it analyzes
the sentiment of a text. And then in order to actually implement
the tool, all you got to do is create this run
function inside that class. So, as long as you have this underscore
run function in there, you can add any code that you want. So, in here is where you would call an API
or where you would take an action or send an email
or anything you wish your tool to do. In this case, we're keeping it very simple
because it's just an example and we are just
returning the word positive. So this is a sentiment analysis tool that always returns
that the sentiment is positive. So now that we create a stew
we can actually instantiated. So that we can use it. The same way
that we did with the tools of both we said, the directory,
the file, and the search tool. So you can go ahead and just do that. And now you have the sentiment
analysis tool and you can pass that to your agents
and tasks. So, now that we use our tools let's create
our tasks and assign them properly. Here we are going to be able to see
how we can focus in specific and clear goals on what we want to achieve
by using this tool. So the first task that we are going to
create is a lead profiling task. So the lead profiling task
basically conducts an analysis on a given lead in order to understand its sector, how big it is, information that might be useful for us to engage
with this potential customer. So, in here you can see that
we are providing it with a set of tools, are directly read tool our file
or read tool and our search tool. So with these tools, this agent
when performing this task are going to be able
to look at those instruction files that we saw before,
read them and then using the surfer API, search the internet
for more information about this lead. So let's go ahead and create this task. Now we're going to need a new task. This new task is going to help
with creating a personalized message
to outreach for this specific lead. So I can paste it in here. And you're going to see that
this task has a different set of tools. It doesn't need to read the directory any
longer, because by now it already knows it is a big or small company
and already has done some research on them. This task is focuses
specifically on doing a sentiment analysis and doing any further search
that might be necessary in order to make sure that we talk with this
customer in an appropriate manner. So you can go ahead and also create this. Okay. So now that we created the two tasks,
you can create your crew. The crew is pretty straightforward
the same way that we have been doing so far. We pass in the agents.
We pass in the tasks. You can set the verbose mode to two,
and you also set the memory so that this crew is using
the memory functionality and features. You don't necessarily need to
if you don't need, but I think it might be a good use case. So let's go ahead and run this. Now you can kick off this crew, and kicking it off
should be pretty straightforward. So in this case
we're passing a set of inputs. Remember that these inputs
are going to be interpolated in any place that we use them, both in the tasks
and in the agents. So these inputs are going to be used
into any place in the tasks
descriptions or the agents definitions. Anywhere where we try to interpolate these variables
we can now pass their values in here. So in this case we're simulating
that the lead name is Deep Learning and AI. In there, the industry is online learning platform. The key decision maker is Andrew. And he is the CEO of the company. And the basic milestone
that they have is a product launch. So we can go ahead now
and kickoff this crew. So everything starts with a first sales
representative. And it's going to start by conducting
this in-depth analysis of the DeepLearning.AI company and basically
trying to learn more about it. So you can see here that it started
by searching the internet, trying to understand
more about DeepLearning.AI. So in here you can see all this
search results that it got from Google. And if you scroll further
you're going to see that it by mistake decided to try to read one of the websites
as a file. And you know that we just talked about
how tools need to gracefully fail. This is a great example of this. This file content read tool is not meant to read a website,
but actually a file from your file system. So if you didn't plan for that,
you would throw an exception in your execution would stop. But crewAI automatically handles data
so that it fails gracefully. So you can see that despite of it
showing an exception, it tells the agent that it got this error. So the agent kind of like now understands
that it can directly access the external links
using the read files content. So it's it's learning
from the tool that it tried to use. So it then
go back into search the internet to try to find more information
about DeepLearning.AI. So if you're building your own thing,
or depending on your choices or framework, you might notice
that if your tool finds an exception, the decision there is let that exception actually blow up. And when that exception wblows up,
it stops the execution of your agent. So that means that hours
that it was completed so far is gone, and your agent execution stops,
so you can't move forward. That means that you would
then need to add an extra layer so that you can treat for that, either
kind of like kickoff your agent from the scratch
or do something else with that error. So for crew,
it was a conscious decision early on that we would prevent exceptions
from stopping execution. But you might find other frameworks
that choose it otherwise and choose to allow exceptions,
actually stop executions. And that is the commission's choices
that you can make. And if you're doing something
from scratch, because, again, you don't need to be using a framework,
you can be building these agents yourself. It's just going to be a lot of more coding. But it's something that you need
to be mindful of. How you want to handle exceptions
when using tools is a big thing as agents, So you can see that again, it finds a bunch of different research
and put together a DeepLearning.AI company profiles
with a background of 1 or 2 key personnel, recent business development
potential needs, engagement strategy, everything that we need to know
about the company. Now our next agent kicks in, the lead sales
representative. We're using the research
that your agent did before, it's going to try to come up with a good way
to engage with DeepLearning.AI. So in here you can see that again,
it's doing some research online. Keep in mind then this is where some of that caching strategy
that we talked about comes in. If this agent tries
to do the same research or the same search online that another agent did, it's gonna hit a caching layer. And instead of actually doing the search. So you're going to be saving
and rate limits and and the request in basically
is going to just work faster. And here you can see that it comes up
with an email where we can send to Andrew. The subject is: "Enhance DeepLearning.AI's Educational
Impact with crewAI's Advanced Analytics." And then it goes on explaining.
And you can see that even references The Batch. The Batch is actually a newsletter
from DeepLearning.AI. And we never told these agents
anything about it. They learn about it automatically
through the research that they made. So now we have an email
that we could engage. And we actually have a few other options here. So you can see that
it gives another option. Now a little bit more focus on
AI drive tools. And another one
talking more about a partnership. So you can choose what email you want to
use to actually engage with this company. This is such a great use case.
Throughout or interactions with the community
that has been building multi-agent systems independently of what framework
they are using, we realize that there is a few verticals they are very common,
and sales is a big one because a lot of the sales process
involves reporting, involves researching, involves engaging in all that are things that can now
be automated through agents. So it's going to be common for you going
out there and talking with other people. There are building agents to see that
they are doing things in this verticals. And this is honestly
a very interesting space in general.

---

## Lesson 10: Recap of tools

Okay, let's recap what we learned so far. We talked about
how tools are such a key part of agents, because they are what allow you to connect
your agents to the external world. So you're going to view tools
and use existing tools to call APIs to integrate with our internal systems,
to do some computational. It's a translation layer
that allows your agents to communicate with existing programs
that you might have. But in order for these tools to work properly,
you need to make sure they're versatile. You need to make sure they're fault tolerant and need to make sure
that they have a caching strategy. If you make sure that you're using
those three qualities on all the tools that you use, you
then have a system that is more reliable. So make sure to watch out for that
when you're choosing what tools are going to use
or building our own tools. Keep in mind again
that because are using crewAI, you can not only use the tools
that crewAI offers itself, but you can also use all the tools
that LangChain offers. So you have a huge range
of tools that you can start with. All right. We're going to wrap this lesson here. You're doing amazing. Keep at it. You're going to love our next lesson
because you're going to talk about even more interesting stuff
that is going to unlock more use cases. So I'll see you on your next lesson.

---

## Lesson 11: Key elements of well defined tasks

Okay, so we just built an amazing crew. By now, you're probably getting excited
and I am as well. But we can take a step further
in this lesson, we are going to build a multi-agent system
that's going to be able to help us plan an event. Think about a meetup
or a conference, whatever it might be. These agents are going to help us
to find a venue, do the planning, planning around the catering,
everything that comes with that. So let's jump into it
and see what that looks like. Welcome to our next lesson. And in this lesson
we're going to be talking about tasks. I'm super excited about this one. We talked about so many things already and this is another great topic for us
to dig into because at the end of the day, if you think about your agents,
they are performing tasks. So, tasks are a cornerstone
on multiple agent systems as well. So when you talk about tasks,
I want to bring back something
that we talked about a few lessons ago. The manager analogy. You might remember that we discussed
that this manager/mentor framework to create agents where you put yourself
in your manager's shoes and you think about what would be
the people that you would hire in order to do a series of tasks or the job
that you're trying to accomplish. And then you kind of use
that as a starting point to define what will be the roles, the goals,
and the backstory of your agents. So, you need to have
a very good understanding of what is the goal
that you're trying to accomplish. And you also need to have a very clear
understanding of the process
through how to achieve this goal. So with that in mind,
you're going to have a clear understanding of the people that it would hire
and those would be our agents. But now I want to build
on top of this analogy. I want to expand this mental model
to how you think about your tasks. Because whenever you hire
someone to do something, you also need to think about
how you're going to delegate work to them, especially
if it's more of a junior person. You want to make sure
that you're very explicit about why do you expect that they do
and what is the expected result. So I would say for you to build great agents, you should add data
to your mental model as well. So once that you think about
what are the people that you would hire to get the job done,
think about what processes and tasks I expect individuals on my team to do,
and you can use that to create the tasks. And whenever you're creating a task again,
you need to have at least two things top of mind. One: a clear description of what is the task. And two: set a clear and concise expectation. Again, to go back to your analogy,
let's think that you just hired a junior engineer
to work on your team, and your tasked with coaching this person. It's their first day on the job. You basically want to give them
a specific task to work on. You want to give them
a specific task to work on. You want to explain their task
very truthfully, and then you want to make sure that you say,
why do you expect them to do. So crewAI kind of forces you to think that way,
because crewAI makes sure that it's mandatory
for you to share at least two attributes on every task
that you create. The description and the expected outcome. And that is
used to build better internal prompts. But then also apply
to any other framework out there. You will get better results
if you go the extra mile on explaining what is a task
and what you expect your agent to do. Other than that,
there is a bunch of other things that you can set on the task. crewAI
offers a bunch of hyperparameters that you could use, like
setting a context, or setting a callback, or overriding the agent tools
with a specific task, force human input, kind of like making sure that before
the agent finishes the work, it stops and asks you how you feel about it
so you can give further instructions. Also, we can talk about execution. This tasks are synchronous
or outputting their results as pedantic objects or json object, or even outputting them as a file
or running these tasks in parallel. So you can see how there is a bunch of options
when you're talking about tasks in here. And you're going to need to take all that
into account depending on how complex
your multi-agent system is. crewAI offers all these options,
and you're going to find a bunch of them in other frameworks as well. Maybe not all of them,
and maybe in a different shapes and forms, but in the end of the day, it's
all about how you can set up your agents for success to perform
their tasks super efficiently. So with that in mind,
let's jump into code real quick,

---

## Lesson 12: Automate event planning

All right. So let's start by adding
the boiler plate code getting warnings out of the way. And now what you can do
is import your crew agent and tasks classes. So now that you have imported
your agent, crew, and task classes, we can shatter
environment variables. So in order to do it,
I'm going to copy this code here. Keep in mind that we are also going
to use serper in this example. So you're going to need to serp API key
that's going to be provided to you. But you can also find it
going on their website. And they do offer free credits. So now that we set up the keys
and the model that we're going to be using,
let's go ahead and import our tools. We're going to be using two tools
in this case the scrape website tool,
and the serper dev tool. So think about how those tools will
fit together. The Serp dev tool will allow you
to search the internet using Google and getting results back. And then the scrape website tool
will allow your agents to go into those websites that it finds and getting their contents, so that it can use
that during the execution. So you can see here
how planning out the tools goes a long way on
how your agents are going to behave. All right. So let's create your first agents now. Let's first create venue
coordinator. And that gives away
what we're building here. The example for this lesson is a crew that is able to organize an event
or a meetup for us. This first agent has one single
go, identify and book an appropriate venue. So giving an event circumstances
and requirements. It's going to search the internet
for venues that can support that and find these venues for us. Now we can create that agent. All right. So our next agent
is going to be a logistic manager agent. So this agent makes sure to think
through the logistics of the event. Now they have the first agent already
found a few options for the venue, it's going to think about
how will this work out in making sure that the venues
appropriate it for us to do whatever we're trying to do
with this conference or this meetup. So let's go ahead and create
this agent as well. Our third agent is kind of different, it's a marketing agent. It's supposed to work on top of the venue
and the logistics, in figuring out how can we market
this event, how we can market this meetup so that we can get as many people
as possible showing up today? So this agent are going to try
to be creative in thinking about the event that we're putting together in the venue
and the location, and bring all this together into something
that we can use for marketing. So let's go ahead and create
that agent as well. You can see here
how this can be a pretty interesting tool. We basically have a system
now that is not only finding things We have a system
now that is not only finding things about the event,
but thinking about logistics and also thinking
about marketing, everything in one go. And this would be extremely hard
to pull it off with conventional programing
if you're not building and AI application. So, now that we have this three agents,
we're going to do something else, something differently
that we haven't done yet. We are going to create a pydantic object that is going to hold our venue details. This is interesting because it's
going to show off a new feature for tasks that we haven't discussed yet. So in here you can see that
we are importing the pydantic Base model and we are creating a class
called venue Details that it inherits from the base model. And we're saying that this venue details
is going to have four different attributes: a name, address, a capacity,
and a booking status. The reason why we're creating this model
is so that our agents can work with it and populate this model,
create instances of this as they work. So this is a very interesting use case,
and how you can use agents to transfer the fuzzy outputs into actual strongly typed outputs
that you can use in your regular code. So before we start creating our tasks,
I want to spend a few seconds to talk about pydantic. Pydantic, It's a library
that has been getting a lot of attention. Allows you
to create models in work with strong
typed up variables in a very easy way. So you can see here that instead of
like what you would do with classic Python,
where you would declare a class and then you would need to declare a niche
method and in that method you would need to receive a bunch of arguments
and then set a bunch of variables. It gets away from all of that
and creates this syntactic sugar that allows you
to create models in a very simple way. So now it's not only a class that you're creating,
but you're creating a model or research that has attributes
without having to go through the hassle of creating a niche method
and setting them up individually. Pydantic is a huge library
and goes way beyond that. So if you're curious about it,
you can check it afterwards. But for the purpose of this lesson,
we're going to be using that in order to transform
some of the fuzzy outputs that we get from our agents into strongly
typed outputs that we can use in code. All right. So let's
get ahead and create our first task. So this task is pretty interesting. It's a task responsible
to find a venue for our event. So you can see that it expects
a few inputs in here. It expects an event city
and expects an event topic. And look at how you're using
a few different attributes that we haven't used before. So in here you can see that
we are seeing that we want to output a json in in order
to output this json, we're
passing or pydantic object. So, what is happening
behind the scenes, our agents are going to converge their
for the output into this very strong type of model,
and then convert that into json. And then we are outputting data results into a file,
a json file that we can actually use. So this is just to showcase some of this
attributes that you get on the task class that you don't use very often,
but are super powers in certain cases. People use this a lot
when you're trying to integrate agents into existing systems
without doing it through APIs. So instead of having an API that is going
to kick off your multi-agent system, if you want to have this agents
within your code, this would be a great way
to get an output out of them that you can already use
on like function or anything else. So now let's create our second task. Our second task is pretty interesting. It's a logistic task. This task is responsible for coordinating catering to equipment for the event. and you can see that in this, it's expecting a few different variables. looking for
what is the number of participants and what is the tentative date
for this event to happen. You can also see using
a few different attributes in here. So you can see that
we are using human input in here. This means that before this task
is completed, the agents are going to stop and ask us, the operator,
if we want to give an input. If we like the task result or If you wanted to change anything with it.
You can also see that we are doing a synchronous execution. So that means that this task
is going to be executed in parallel with any other tasks
that comes after that. So this is a very good use case
because if you think about it, this logistic task depends from the result
from the venue task, because the location is going to influence
how you're going to coordinate the catering,
the equipment and everything else. But as you're going to see in a second, it has nothing to do with our final task. So our final task is going to be or
marketing task. It's the task responsible
for creating the marketing campaign that will help us promote this event. So you can see in the description here
that again, we are talking about the event topic,
the expected participants. And we want to report
on all the marketing activities that we can use
in order to promote this event. And you can see that this task
is also allowed to execute in parallel. So what that means is that the first task, the task that selects the venue, it's
going to be executed by itself, alone. As all the other tasks that it have been
that we have seen so far. Then after that, the logistics tasks
and the marketing tasks are going to be executed in parallel. Because if you think about it,
one doesn't rely on the other. The output of the logistic task
doesn't necessarily matter for the marketing tasks to occur. So we can have them run in parallel
without too much trouble. And here we can see that we are outputting
the result of the marketing task into a file,
and in this case is a markdown file. And because in the expected output,
we are mentioning that we expect the result
to be formatted as markdown. Now this should work just fine. All right. With that, we created our three tasks. We are using a bunch of new attributes
for the tasks, and you can see how you can leverage
a lot of those for different use cases. In here we are kind of like forcing
ourselves to use some of these attributes, just as a way to showcase how useful
they might be in the real world. But you're probably already thinking about
all the use cases that you can support, thanks to some of these attributes
that crewAI brings into the table. So now that we have our tasks,
let's make sure that we create our crew. And creating a crew
is pretty straightforward. It's the same thing that we have done
so far. We have a set of agents,
a set of tasks. We set the verbose mode to true
and everything is ready and we can now kick it off. So let's keep in mind that there is
a bunch of variables that we use throughout the tasks in the agents
that needs to be interpolated. So let's start by setting those up. So this is the event that we are
organizing. It's a tech innovation conference
trying to gather tech innovators. It's going to happen in San Francisco. It has a date. We expect to have 500 people
and we have a $20,000 budget on it. We would love to have a conference hall
that we could use for this. So these are all the inputs
that this crew needs in order to do its research
and actually fulfill its tasks. So let's kick it off
and see how that goes. So from the get-go, you can see that
the venue coordinator kicks things off. And it starts by trying to find a venue
in San Francisco, because that's where we mentioned
that we want this conference to happen. that meets the criteria
for making a tech innovation conference. So in order to find out, you can see that
it decides to search the internet. So it searches for tech conference venues
in San Francisco. So it finds a bunch of results,
as you can see here. And then it decides to scrape
one of these results, among these results, it found tagvenue.com specifically mentioning
listing conference venues for rent. So, it decids that it's a good call
to kind of scrape that content. And here you can see the whole content
that was scraped from that website. It's quite large, but now it's ready
to give its final answer. The detail content from the tag venue
website helped it that you can understand
of what would be the options. So the selected venues have different
sizes and types and wants us to see
what is your feedback? If we agree that for a large conference
like this, it should go for the main hall at Trellis
or the second floor at Dogpatch Studios. I'm going to keep it simple,
and I'm going to say, "yeah, I like these Options." So, now that I gave it the input, it's
going to move on from that. And I'm going to keep executing the code. So if we look at what happens
after this, it's going to pass on to the next agent
that is now going to figure it out on how to come up with
not only the caterering, but also the marketing from this. So you can see the final answer in here. Nw that it took into account
what we said. And look, how cool is that? The output from our task
is now a valid json. It's not a text any longer. So you can see how our pydantic output
there is working its charm. We could use this to integrate
with anything else. We could save this into a database. We could save this into a file. There's just so many options here. The ability to convert like agents output into regular objects
that we know in programing, is super helpful,
and allows us to bridge the gap between AI applications
and regular applications. And you can see that
even though this is jason, this is being sent as jason
to our next agent, the logistics manager, to try to coordinate
gathering and equipment for that. So you can see that this agent now
kicks off together with new agents. So you can see there's two crew agent
executer running here, because we told that the last two tasks could be executed
in parallel asynchronously. So while we have one
agent kind of looking into the catering, the other one is looking into
how to promote this. And what would marketing
look like for a conference like this. So again,
they're both searching the internet and trying to come up
with everything that they need. All right, let's skip to the end
and see what we end up with. So now let's
look at some of the outputs of these agents. As they are wrapping up their work
and coming up with their final answer, we can actually look at some of the files
that got generated during the execution. First of all,
you might remember that we asked the venue details to be outputted
as json and written in thejson file. So this is the json file. This is the name of the place. This is the address, this is the capacity
and it seems to be available for rent. And now we can also look at what the marketing strategy could be
because it also got reading in here. So in here we can see that is a fully
fledged marketing campaign. Thinking about the digital marketing,
the content marketing, the partnership, the networking, the onsite,
the tools and even doing some budget allocation and how we could use our budget
to actually market this. So think about how amazing this is.
You basically created a multi-agent system that is capable of not only finding,
like a good venue and figuring out how to organize things
and bring the equipments and everything, but also capable of thinking
about a marketing strategy and planned it out for you
so that you can act on it. This is just the tip of the iceberg on what you can achieve with multiple
agent systems in a great use case example on how these agents
can be deployed outside in the world,
and not only in engineering.

---

## Lesson 13: Recap on tasks

So let's do a quick recap
on everything that we learned so far. So we learned that this mental framework for creating agents
is super helpful. Because it helps us to understand what are the agents
that are going to create. Also, what are the tasks
that we expect them to do? We also learn that
when we're thinking about these tasks, we should be very much thinking about
what are the clear descriptions and what is the clear expected output
that we want to get for each and every one of them. And we also got the chance to mess around
with a lot of those individual attributes that the tasks offer,
from parallel execution to output json to use pydantic
in a lot of different interesting stuff. You're going to get the chance
to play around with how those different arguments are as you build
the systems yourself in the future. But I hope this was a good way to showcase
how powerful these systems can be. So I really appreciate you sticking by
in this lesson and going through this. I think this is a turning point
where you kind of start to build really production case agents
where you understand how they work, and it's only going to get better
from here forward. So, congratulations for sticking
around and learning about this. I would say pause the video a little bit, go back into the Jupyter
notebook, change it a little bit. See what results you can get from it. It's going to be a lot of fun. And I'll see you in the next lesson.

---

## Lesson 14: Multi agent collaboration

Okay, in this lesson, we're going to dive
into agenetic collaboration. Multiple agent systems are great,
but they really shine when you can get the ability
for these agents to talk to each other. There's so many different ways
that you can get agents to collaborate when you're
trying to achieve certain goals. And you got to pick and choose
what are the right ways to assemble your team together. Again, think like a manager. You want to always to structure your team
the same way. So right now we're going to dig into that
and understanding how you can get these agents
to collaborate in so many different ways. Welcome to our new lesson. I'm so excited that you got to this point. We're going to be talking
about agenetic collaboration, and we're going to talk about
one specific sample that is so cool, and that's financial analysis. We have big companies. I'm talking about fortune 500 companies,
that are using CrewAI to do financial analysis. So this is a very common use case
where you're going to probably see out there
as you start to interact with more people that are doing multi-agent systems
in the real world. So let's dive into that. How multi-agents collaborate. We already saw this happenning The true like crews by seeing like one
agent passed the test to another. But there is just one way. There's so many other ways
that multi-agents can collaborate. So let's go back to when we started. We described the initial steps throughout
agent collaboration where you didn't have one agent finish a task
and then pass its output into the next. And we already know that we could do that
in parallel as well. And this is great for certain
kind of workflows, but similar to how you wouldn't
necessarily arrange the same team
the same way for all the tasks. That's also true for agents. So depending on what you're
trying to achieve, you might want to organize your agents
differently. You might still have the same agents. You might still have even the same tasks,
but you might want them to operate through a different process. Because of this, process
bring some consequences, for example. So for this process,
and specifically if you're talking about doing things sequentially,
you have some consequences. The most common is the fact
that the initial context moves slowly fade away as the tasks
get passed from one agent to another. And again, that's okay for some cases,
but not for all of them. So CrewAI
offers some flexibility around that. Similar to other framework but
in this case, it's very explicit about it. So let's talk about processes. All of our agents so far have been working
mainly in a sequential process. We did a experiment with parallel execution, but most of them are just performing
tasks sequentially. But there are other ways that you can
perform tasks using CrewAI. Another big one, is hierarchical.
And there's a lot of benefits for it. First is that you get a single point. You got a manager that always remembers
the initial goal, and that automatically delegates the work to the other members
and the other agents in this crew. And not only that, but also reviews
the result as these agents wrap their work, it can ask for further improvements
if necessary. And the cool thing is that you get
to create this agent manager yourself. So you can see here how different process gives you a completely different way
to perform the same actions if you really want to. And it's just a
one single line change that it would allow you to do that. But you don't need to stop there. You can also do some of what we did
with asynchronous execution. So independently of the process, CrewAI will also offer you the ability to execute
certain tasks in parallel. You have other tasks. Wait for them to be finished if necessary. So despite of the original schemas, crew
allows for agents to fully cooperate
and go off any predefined paths if necessary to fulfill the tasks at hand
so they can delegate to each other, ask questions to each other. You can have a manager
that reviews to work. You can have tasks
that happen in parallel. There's just so many options.
In terms of the collaboration itself, you can have agents ask questions, vaguely
talk to each other. We already talked a bit about this, but this happens independently
of the process that you choose. Meaning that even if you choose
to use hierarchical processes where you have one manager,
delegating work, that still means that the agents benefit can delegated work
between themselves. So that's still true and allows
for a more diverse outcome. So let's see some practical examples
of this. Let's jump
into our Jupyter notebook real quick.

---

## Lesson 15: Mutli agent collaboration for financial analysis

All right. So from the get-go
I'm going to add some of our boilerplate soon where I'm going to import all of the three classes that we care about: the agent,
the task and the crew. Now we're also going
to be using serper for this. So I'm going to make sure
that we are using GPT-4 turbo. And that we are also using our serper API key. You're going to be provided with one. You can also just get a one
from their website. They do offer free credits. So we're going to be using two tools here,
the search tool and the scrape two. So we already have used those tools
in other examples. So you're probably familiar with that. The search tool allows
allows your agents to search Google and the scrape
tool allows your agents to look into one where else they find and kind of extract all the content out of that. So now that we have our tool set up,
let's create our agents.
And we're going to use four agents here. We're going to have a data analyst agent responsible to analyze the market, trying to find
good opportunities for us to invest on. We also going to have our trading strategy
agent here, that is going to look at
those options and kind of like weigh in what are the movements
that we should do regarding any stocks. There we have the execution agent. This is the one that really thinks about
the timing, the price, the entry points. It's going to help us set up out there. And then the final one
is the risk management agent. This agent is basically making sure
that you understand the risks of buying stock
and balancing things out. So again this is not a recommendation
an investment in any shape or form. It's just one example of how you can use multiple agent systems
to also interact with financial problems. So we wrapped up creating more agents
and we are ready to create our tasks. This is not a financial recommendation
in any shape or form, but I have personally seen working
with companies, even fortune
500 companies that are actually doing risk analysis and financial analysis,
using crewAI to the book, to financial documents that are public
and private in order to understand how are those companies doing? So this is not a far at what
people are actually building out there. With that
said, let's start creating our tasks. Our first task is the data analysis. Basically monitoring the market,
trying to find good angles, good stocks that we could use. The second one is the strategy. It's once that it knows
what is your tolerance to the risk and what is stock selection, it can decide on
how to move those stocks. The third one is the execution task. That's
the one that is going to make the calls around the price,
the entry points, the right timing. And then,
the final task, is the risk assessment task. that wrap things up
and make sure that it's taking into account the risk
before making any recommendations. So now that we have created all our agents
and tasks, we are ready to put our crew together. But you're going to notice
a few different things in this script. First thing, you're going to notice
that we're importing a new class called process. This process class,
allows you to basically set a different way for agents to work together. You can see how we are using here
when we're creating a crew by setting this crew to operate it
hierarchically. By doing that,
we're going to have one manager and it's going to delegate the work
to the agents to perform their tasks. So this agent, is going to be a manager that crewAI
will create automatically for you. So in future versions of crew, you're going to be able
to set your manager yourself, and you're going to be able to pass this
agent as the manager agent. Meanwhile, you can set one as the LLM
that this agent will use. And crewAI, I will create this
agents for you internally. So you don't have to worry
about any of that. So here you can already see
some of the differences between using the regular sequential processes
and now the hierarchical process. So let's create our crew. And now that we have our crew ready
we can work on what inputs we're going to be sending to it. So if you look through our agents and tasks declarations,
you're going to find a few variables, namely the stock selection,
the initial capital, our risk tolerance and our trading strategy
and also using packets. So we can set all that from the get
go to make sure we can use it when we're kicking off. And I would say feel free
to kind of like stop the video off after this and play around
with some of those numbers. Bring your stocks,
the stocks that you care about. Play around with the initial capital. Play around with the risk tolerance. Make sure that you can really see
how these agents behave differently, given the different inputs
that you can send to it. All right. We are ready to kick off this screw. In order to do that, we basically call the kickoff
method and pass or find the initial trading inputs to it. So let's do that. From the get-go, you can see that the crew manager
kicks things off. So this is crewAI and their manager. It creates this manager
automatically for you. And it's going to use this manager
to delegate the work around. So you can see that it starts by
delegating the work to the data analyst. So that this agent can do some work around
finding information about Apple Inc. And from that point on, it's going to keep delegating work
to all the different agents up to the point that it completes
all the tasks and gives us a report on what we want to accomplish. What are the moves that we should do. What are the right values
to get into the stock or whatnot. So let's tag along this execution. You can see that
the data analyst decides to do a web search
for the current stock price in volume. And when doing that,
it finds a bunch of results. Among these results, each finds the Yahoo finance links
and decides to dig into that. It reads the website code dig
by using our other two in order to get all the information
from the Yahoo website. From that point on, it now knows,
what is the Apple inc actual value
in the closed value from April 24th. It also understands
everything about the stock that it was able to extract from that
a Yahoo finance. Now that information goes back to our crew manager, that will decide what to do next. In this case, it's delegating
work to our trading strategy developer. And you can see how it's passing
some of the information that it learned about the Apple stock price
increase in the after hours, everything that the previous agents
learned, is now being sent to this new agent. And all of that is being coordinated
by this crew manager that is autonomously delegating your work. So you can see that our agents
now actually Google for trading strategy Insights
trying to kind of learn a little bit more
about how Apple is doing. And then he decides
to look into a specific website itself in order to extract information from that. So you can see throughout the execution
how this pattern repeats, where like the agents who learned
through research and digging into these websites
informations about the stock and the company
and sending that back to the manager, and the manager kind of decides
where to go from there. So next up to the point that he completes
all the tasks that we want to complete. So let's dig along
and see what the final result actually is. So you can see through this execution
how a lot of delegation is happening. The crew manager keeps learning
throughout this delegation in that getting even further. So now it's delegating works to data
analyst, asking to provide analysis on the recent market
trends and price movements. So you can see that throughout our lessons
we have been building more complex crews. We started with four simple crew
to write an article, and now we're building fully fledged crew
that are able to do stock research, risk analysis and look into websites
and extract information delegate work
and do work in parallel. There is a lot going on there,
and this is honestly super exciting because it opened up
so many opportunities. So I would definitely say
play around with this. Make sure to play with
some of the attributes, change some of the crew, change
some of the agents and tasks. Make sure that you build something that you find value
and give it a try and share it online. People are super excited
to see what people are building with crewAI in multiple agents nowadays. All right,
so our crew finished in the task output is the comprehensive risk analysis report
for Apple Trading Strategies. So you can see that
it kind of like started with an overview and mentioned that you should utilize
a technique called 20 day and 200 day SMA. So you can see that raw the execution. Well we we kind of like skip
that because it's a long running crew. But throughout the execution it learned
about all those different market trends and ways to kind of like assess the risk
and decide what is the best entry point. But it mentions things like RSI or MACD in order to identify potential
to buy in the market. It also mentioned, like for you
to establish top wins and stop loss
as a way to also do risk management, identify some risks, mentioning what you should be watching for,
it also mentioned operation challenges
and also mentioned market volatility pact. So how can that impact your
your decision in there. The conclusion is that you have
a good strategy to basically invest in Apple. However, you should be careful
about how you deploy it. So you can see in here that the end result
just kind of like more from the view. There is a lot of work during the execution
that we could dig into. And it did offer some recommendations
on how we should try to think about entering these, these stocks,
specifically how it should analyze it. What I would invite you to do now is pause
the video and play around with this agent. These are very complex crew. It has a lot of moving
pieces, it's using a hierarchical process. So to play around with some of that,
maybe make it sequential, see what changes, maybe remove
some of this tasks or maybe change some of this task to is likely to see
what you can get out of it. But this is a very interesting use case
on how you can use crews to do thorough analysis on stocks and links and texts and methods. It's very interesting
what you put out together. All right. So let's go back
real quick. So by now you have acquired a complete understanding of how multi-agent system works
in all of their components. This is more of a simplistic
representation of crewAI specifically, but this is very similar to what
you find on other frameworks out there. You have crews, you have agents, you have do's, you have processes,
you have tasks. And the end goal is to produce
a good outcome out of that. So you probably learn
all the moving pieces. And should you ready to start building
more complex crews to gather. So, on our next lesson,
we're going to put together a more complex crew
that you can actually start using today, and that can help
you find your next job opportunity. So I hope to see you there. And so congratulations on all progress so far. Make sure to try things out. You set up
jump straight in the next lesson. Make sure that you play with the
Jupyter Notebook, and I'll see you in a second.

---

## Lesson 16: Build a crew to tailor job applications

All right. So you just learned a lot about agents. We talked
about all the different features. But this lesson is super important,
because this lesson it's we're going full circle. We're basically going back into lesson one
and talking about that use case that we showed
where we're going to help you build this agent that will help you apply for jobs. These agents are going to be able
to look at the job postings, understanding its requirements, and then cross that over
with your current resume and your skills and make sure that we tailor
your resume to apply for jobs. It's a very interesting use case,
and we're going to get the chance to apply everything that we learned so far. So let's look into that. So in this lesson ,we're going to be
building a super interesting crew. We are going full circle to the crew
that we mentioned in the first lesson. We are going to be building a crew that will help us to increase our odds
of getting an interview by tailor making, our resume me for a specific job
application. I'm so excited about this, honestly. By now, you're already understand
that this is the future of work and engineering, and I truly believe
that AI agents are a key part of the future businesses
and how you, as an engineer, can drive an immense impact on your job
and your career. So, let's talk about this crew,
what is the process and what is the goal? We talked about these in other lessons,
so let's dive right into that. So what is the goal? The goal is to maximize your chances
of getting an interview for a given job posting
and the process throughout we are able to achieve
that is one, learning the job requirements. Then two: crossing those requirements with
your specific skill set and experiences. And then we reshape your resume
to highlight your relevant areas. And then we rewrite that resume
with the appropriate language. And then as a bonus, we can also have this crew sell some
talking points for an initial interview, something that you can read before
jumping into the call, and that will help you understand
how you can better highlight your skills in a way that makes you look good
for that job position. So let's jump right into the code. All right. So let's get the boilerplate code
out of the way, making sure that we don't get any warnings
and that import or trimming classes the agent, the task, and the crew class. Now, we have those three classes
right for us. Let's make sure that we also add
or environment variables so that we send our models
we're going to be working with. In this case we are using GPT- 4 turbo. And you're going to notice
that we are using serper dev again. You're going to be provided with a key or you're going to be able to create
an account and get a key from there. All right. Now let's focus on the tools
that we are going to be using. And there is a set of different tools
that we're going to be using for this one. All of those tools are coming from
the crewAI package tools. And you can see there are four of them. There is the file read tool, there's the scrape website tool, there is the MDX search tool,
and there is the Serp dev tool. 61
00:03:17,430 --&gt; 00:03:20,333
Let's go over
each one of them. The search tool, we already know about that,
allows us to search the internet. The scrape tool, we also have used
it, allow us to scrape a website content.
The read resume tool, is using the file read tool, and making sure that it only allows
the agent to read one specific file. In this case is a fake resume That is written as a markdown, and I'm
going to show you that file in a second. And then the final tool:
is the MDX search tool. This allows us to perform RAG over
our fake resume. So, we can do semantic search over anything that is in or resume. So let's create those tools
and get those files. All right. So let's start
by looking at this fake resume file so that we can see what we are
working with. This is what the fake resume file
looks. And all of this is made up, so in this case, we have our buddy
Noah Williams. And you can see in here Noah's profile, his work history, everything that he have been up
to throughout his career. You can see that it has an MBA. It knows a lot about leadership
and it has like been calling out his leadership achievements
throughout his entire resume. You can see that it defines himself
as a software engineer leader, and talks about how he excelled in leading both
remote and in-office engineering teams. So, you can see that this is more of a profile for someone
that is applying to a manager role. Which is okay. But if you look further,
you're going to realize that Noah Williams is also a very good engineer. He has experience with Ruby, Python,
JavaScript, TypeScript, elixir. And you're going to find that
he hid them in his work history. There's a lot of amazing gems
of technical work that he has built throughout his career, but
is not being highlighted in the right way. Again, depending on what job
he might be applying. All right, let's go back to our code. So now that we have
our tools, let's start creating our agents. And for this crew, we're going to create
four different agents. The first one
is going to be a researcher agent. So let me copy this. And just paste it in here. So this agent is a tech job researcher. Its goal is to make sure
that doing analysis on the job posting, it's basically trying to understand what are the needs
behind that job posting, what are their what is the company
trying to achieve with their job posting? What is the kind of person
that they're trying to hire? So this is what these agents
are going to be responsible for. Now let's create our second agent. Our second agent is a profiler. So this profiler basically does a research
on the job applicants and tries to understand
some of the crossover. So, looking at the resume and the job posting, what are the things
that stand out in there that makes this person actually
look like a good match for this job opening. So this agent is
going to be very important in this crew, because it's going to be the one that's going to highlight
the things that we want to really pop up. So now let's go for a third agent. Our third agent
is a resume strategist. It's the one that's is going to actually updated
resume. It's going to learn about the job postings and learn about the skills
that the person has that has found
around the intersection. So it's going to write that down. You can see that among our three agents, all of them have access to a few different
dev tools. The resume strategist one is going
to be able to scrape the internet, search the internet, read the resume
and do a semantic search over the resume. So it's a very capable agent. On top of that, we need one final agent. We want one agent to help us
to prepare for the coming interview. So this is the engineering interview
preparer. This agent is going to,
once that things wrap up, make sure to put together questions and answers
and talking points that you want to come prepared to when going to this interview,
assuming we get it. It's a great way for us to make sure
that we're feeling confident and that we know that we can highlight
our skills in a way that makes sure that the employer understands that we are
a good fit for that job opening. So now that we have created our four
agents, we are ready to create our tasks and we are going to use four different
tasks. One task for every agent. And you can already see
some of the interpolation going on here. You can see that
we expect a job posting URL. The second task is the profiling task is the task that is actually responsible
to cross some information about you that you're trying to apply to this job
and the actual job position. So you can see that in here, there are other variables that are being
interpolated, like a GitHub URL and even like, a personal note on some of the things that you have been
doing as a professional. So that is also something
that we are going to leverage in here. Now for the third task,
we are going to do a resume strategy task. This task
is going to be the one responsible for actually updating the resume. And you can see in here that we are
outputting a file out of this task. So we're going to have a new file at the end of this crew
that is going to be your tailored resume. So we are going to start
from your actual resume. And we're going to have a new one that is
now optimized for that job posting. So we can go ahead and create that task. And now or final task
is the one that is going to help you prepare for the interview. It's going to put together
the talking points, your relevant to the job posting
so that you feel ready for that. And you're going to notice that this task
is also writing its results into a file. In this case,
the interview materials markdown file. And then you're going to be able to look into that later
once that this crew finishes up. Okay. We created all of our tasks. Now it's time for us to put this crew
together. So let's start by creating our crew and bringing all the agents
and all the tasks within it. Now that we have this crew, before we kick it off,
we need to make sure that we covered all the inputs and all the interpolations
that we expected through all of it. So in this case, that's quite a few. Let me paste them here. So you can see that
we expect a job posting URL, a GitHub URL, and a person right up
where you can explain a little bit about yourself with a few words
and the things that you think that make you suitable
for this job posting. All right. So now that we have our inputs ready
before we kick this crew off, let's go back to the tasks
just so that we fully understand what is happening with this crew. This is going to be
a very interesting exercise for us. So let's look at our tasks. If you look at the research
task, you're going to notice that it's allowing us to execute
that task in parallel. What it means that we're going to have one
agent working on that at the same time that we're going to have another agent
working on the next task, the profile task. Because you can see that also has the sync execution set to true. So you can see that in this case
we're going to have one agent doing research
and the job posting at the same time that we're going to have another agent
doing a research on your profile. So this is great because we are saving on time
by making this our crew execute faster because those two tasks
can be executed in parallel. But then for our third task,
the resume strategy task, we want to make sure that it's
using the output from both tasks that happened beforehand, so that these tasks can get their results
to off the resume research, but also from the job
application research. And you can see that
we do this here on this context argument, where we basically say
that the context for this task, it's actually those two tasks
that were executed above. So even if the profile tasks finish
executing earlier in the research task is still going on,
the resume strategy task is going to wait until both of those tasks
finishes before it can actually move on and use those context in order to come up
with a new strategy for your resume. All right. So now that we understand what is going
on, well, let's go ahead and kick off our crew. So, in here you can see
that two tasks are initiated in parallel. Our tech job researcher is just started doing its work.
And the personal profiler for engineer has also started doing its work. So both are doing their work in parallel
as expected. Let's see how they're doing. So you can see that one of them is doing
the compilation on the profiles for Noah. It's basically
trying to check GitHub contributions looking at the website
to kind of like do some scraping on that. And you can see that's going to try to get as much information
from that URL as possible. You can also see that our other agent
is actually scraping the job posting and trying to learn
as much as it can about what is the actual posting
and the actual needs for that job. So let's dig along and see how that goes. All right, so you can see here now
that one of the agents finished up its work. It now understands all the necessary skills
for this job posting and understands the qualifications
that this person must have, the experiences that are expected
and also the characteristics of what would be a good match
for this position. So now that we understand
all that we can see for other agent already
finished its research as well. All right. We can see that our other agent
also finished the research on Noah. And now it knows everything about Noah. It knows its SKUs, what it has been up to, what are the languages
that it's most proficient about. And one of the things
that Noah's interested in. So, now we can have our resume the strategy agent, kind of bring
those two set of information together to write you
a tailor-made resume for this job posting. So let's see how that goes. So in here we can see that our agent starts
by reading the original resume. So he understands everything
that's in there. And it's going to use
that as a starting point. You can see that it now rewrote the resume
to highlight the main things That are going to make Noah look like the best match possible
for this job posting. And by the end of this, you can see that
now, the engineering interview prepare is kind of during the questions
and some of the talking points that you're going to be able to use
to prepare yourself for the interview if you get it. All right. So this should be most of our crew
execution. Let's look at what
the actual end files are. So let's look at what the tailor-made
the resume looks like. So you can see if we put it side to side with the fake resume, that it changes
things is likely. Before no one was highlighting
how he was an amazing software engineering leader. But now he's highlighting
how he's a full stack developer that has a lot of experience
with software engineering. You can see that he was mentioning so much like this Skus, Ruby, and Python,
but it was kind of like buried in there. But in here, it's being very clear
that he's proficient in multiple programing languages
and talking about all of them. You can see that before, Noah didn't mention some of his knowledge
in databases, but now it does. It mentions
that it knows MySQL and MongoDB. And if we dive into Noah's work history, we can see how it now
it's more trimmed down to the things that actually matter
for this position. Highlighting Noah's Sku's they're better
matching, the better match the job posting and that makes sure that increase his odds
of actually getting in the interview. And we're going to see these changes
throughout the entire resume. Just making sure that it highlights
the things that makes Noah look great. Now let's check the interview materials,
the things that you're going to use to prepare
in case you do get the interview. This is so good. You can see in here
that it simulates and questions and talks about how you can prep to them,
and even give you some talking points that would allow you to showcase
your experience with specific frameworks or specific languages
or database management, how things that are deemed relevant
for that job posting. So with this, you should be able to go
into this interview feeling confident and prepared to answer any questions
that might be thrown your way. Now let's go back towards slides
real quick so that we can recap, shall we? Just put together an amazing crew. And the reason why I like this crew
so much, is because it's so practical. It helps you directly
if you are trying to apply for a job. This is something
that you could actually use today and that would increase your odds
of actually getting interviews. So you should be feeling
very proud of yourself for learning everything that you learned
so far throughout all of these lessons. And I'm looking forward
to see what you're going to be able to keep building with this. Now that you learned so much
about multiple agent systems. All right, let's wrap this lesson here. And I see you in the next one.

---

## Lesson 17: Next steps with AI agent systems

So what a trip it has been. It has been a pleasure
to have you all the way to disperse. You learned a lot about multi AI
agent systems. By now, you are able to put these agent systems
together yourself. So let's look at what are the next steps? Where do you go from here?
What else can you learn? What are good resources out there? So let's get into it. All right. So you came this far. You'll learn a lot
about multiple agent systems. You will learn about
how to use them together. And we use create an entire course
to build all these examples. So by now, you might be wondering,
how doI do more? Where do I go from here? Well, let me show you
a few resources that you can tap into. So, you can actually go at crewAI.com
to learn more about crewAI. And you're going to find
a bunch of interesting resources in here, A few ones that people would really like
is the documentation, and you can do that
by clicking on this link over here. And that will take you to the crewAI
docs, where you can get very specific around the core concepts,
the specific attributes, and even have access to some
how-to guides. But you can go beyond that. You can also chat with our docs. If you click in here,
you're going to get access to a custom GPT called crewAI Assistant that will help you
to put your crews together. This assistant knows everything
there is to know about crewAI, so you can ask about the agents,
the tasks, the processes, and even ask it
to write some of the code for you. So this is going to be a great resource
for you to iterate on it faster. And just make sure that you can build
their crews super fast. Alright, and that, in case you're wondering about how you can use
crewAI in a production setting, Don't be afraid to check crewAI+. It's
our enterprise solution for companies that are trying to deploy the systems
in a production setting. Right now
we are working with early beta customers, so we are kind of like hand-picking who
we want to work with. But hey, we are very eager
to hear all the use-cases. So if you believe
you have a great use-case and you would like to deploy that in a production setting,
click on Apply Now and reach out to us and we're going to be eager to onboard
you into our platform. In our platform, I'm going to show you some of the things
that you're going to get access to. So if you get access to crewAI+,
you're going to be able to transform your crews
into APIs in a matter of minutes without having
to change anything in your code. So you're going to be able to push it
to GitHub, select your repository add any environment variables
that you want, like specific models
that you are using or your Serp API key, whatever it might be. And after that,
you're going to get an API that you can now use. This API, it's
going to be hosted in a private VPC. It's going to use SSL. It's going to have auto-scaling. Everything that makes it ready
for production use-case. And this is just the tip of the iceberg. You can kind of see here
in the other menus, all the other features that you can get
access through in crewAI+. So if you believe that you're ready
to bring your crews into production and deploy them at a larger scale,
this is a great place to go. If you're looking for other resources
where you can learn more about crew AI, I would definitely recommend
you check YouTube. We have a huge community that have been putting out a lot of videos on crewAI. So you're going to find crewAI videos for days where you can learn about specific
use-cases. You can learn about how to build
more complex settings, how to integrate it with grok, mixtral,
and many other use-cases. So don't be afraid
of really going in there, searching YouTube and learning more about how to build
crewAI in production. It's definitely a great resource
if you're trying to learn more. Another thing is, if you are wondering
about a lot of those concepts that we discussed on agents role playing
and communicating and collaborating, there's a bunch of papers out there
that highlights the benefits of doing that versus regular prompting, engineering
or all the other techniques. One paper that I recommend
is the paper behind chatdev You can definitely dig into that
and see how agents that are able to talk to themselves,
are able to tackle way more complex problems
in a way better manner. So I would definitely recommend this paper in case
you want to dig into that a little bit. Don't be afraid
to join our Discord community as well. On our website you're going to find a link
right in the top called Join Our Discord. By clicking on that,
you're going to access thousands of people that are talking about crewAI
and how to build with them. So among everything that I just showed
you, you should be good to go and start your really putting
your skills to the tasks and build multiple agent systems
for production today. Another great resource
is the actual framework. You can go into GitHub
and see all the code that powers crewAI. So feel free to go in there. Check the issues, the pull requests and contribute
if you feel like it. There's so many good resources in here,
and so many people that are eager to help you. So make sure to check out the code, and If you find a bug, please let us know
and feel free to contribute to it. Thank you so much!

---

## Lesson 18: Conclusion

Wow! What a trip that was. We just Learned a lot. You by now know everything there is to know about how to input multiple agent systems. You're ready to get these crews and go out there and build actual production systems they're gonna be useful for yourself and for the businesses that you're working with. So I wanna first of all commend you for coming this far, and say that you should be go out there and actually put these skews into use. A lot of what you learn in this course is how businesses are gonna be built in the future. So make sure to give it a try to hold in these skus and to put them into use. If you always have a question or anything, feel free to reach out I'm always one message away. So congratulations, and I'll catch you online. Have a good one
