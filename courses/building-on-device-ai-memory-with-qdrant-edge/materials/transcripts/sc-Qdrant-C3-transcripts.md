# Transcripts: Building On-Device AI Memory with Qdrant Edge
Source: videos/sc-Qdrant-C3-L1-v2.mp4 to sc-Qdrant-C3-L5-v2.mp4 (24:20 in total)
Instructor: Dylan Couzon

All five verified lesson transcripts in one file, concatenated in lesson order from
`sc-Qdrant-C3-L1-transcript.md` to `sc-Qdrant-C3-L5-transcript.md`. Each lesson keeps its own
title, source and instructor lines; only the lesson title is demoted from `#` to `##` so this file
has a single top-level heading. The text is otherwise unchanged; see `README.md` for how the
transcripts were produced and `corrections.md` for every edit.

---

## Lesson 1: Why Devices Need Memory
Source: videos/sc-Qdrant-C3-L1-v2.mp4 (4:36)
Instructor: Dylan Couzon

In this lesson, you'll learn how devices turn text and images into searchable memories. Let's dive in. I interact with these robots through my phone. And here I can ask it, where did you last see my watch? And here you can see that my watch was last seen yesterday in my hotel room. And there's no specific training, there's no LLM running on this device. We basically teach an object once, and then it saves every new sightings of this object. To do this, this robot is using our open-source vector search engine, Qdrant Edge. So how did we do that? You know, starting with the simplest version of a memory, text.

I can take a note, "I had ramen for lunch." An embedding model turns the text into a vector. A vector is a list of numbers that represents the meaning of text. A vector search engine then creates a navigable graph to allow search through those vectors to happen extremely fast, sometimes in less than a millisecond. A question goes through the same embedding model. For example, "What did I eat for lunch?" Then that vector search engine returns the approximate nearest neighbor to this query. The closer the vectors, the higher the similarity score.

Returning the closest vectors is called retrieval. This is the core pattern you will use in this course. That same idea also works with photos. For this, we use the model called CLIP. CLIP has one encoder for images, another one for text. It creates a similar embedding whether you show it an image of a cat or describe a cat. That means we can search images using words. And the same idea lets this robot recognize what it sees by comparing with what it knows.

If the similarity score is above a certain threshold, we have a match. And to do this, we need no LLM, no retraining, or no custom vision pipeline. You might ask, why would we want to keep memory on the device? And first of all, because it can work without an internet connection. This robot is not connected to any network. It only has direct Wi-Fi to my phone.

So this can be useful in many use cases when, for example, you cannot afford or you cannot wait for a network round trip. Recall can be a lot faster and a lot more reliable when on the device. Also, it allows for your private memories to stay private without any cloud storage or API required. Cloud storage can still be useful when, you know, some memories needs to be shared. And local devices can also have some limitations like less compute and less storage. This is why Qdrant Edge has the capability to sync with a cloud server whenever you need more compute or more storage space.

But for today, we will only be working locally. You can always use cloud and local retrieval combined together if your use case requires it. Now, let's face this robot towards me. All right. So here you can see that it says Dylan's coffee mug. It doesn't say any coffee mug. It knows that it is mine because it is a view that I taught it.

And every time it sees that coffee mug, it will create a new sighting saying where and when it was seen. So I can ask it again, where did you last see Dylan's coffee mug? You can see like the latest memories here. And here, you know, I have two cat plushies that are currently being unrecognized. And because I have not taught it yet, I haven't told it what this is. So here I can say, you know, this is my cat Luna.

This is Luna. And the robots will take a few images, a few representations of that plushie. And every time it sees it, it takes a new image that it turns into vectors. So here I can confirm that memory. And the more it sees Luna, the better it will get at recognizing it. So we can see the score went up to like 97.

And so this is how we create all the memories. We created, stored, and recalled memories without using any LLM. What changed was only some vectors. Next, we'll open the robots and see how it was built.

---

## Lesson 2: Building the Device
Source: videos/sc-Qdrant-C3-L2-v2.mp4 (2:32)
Instructor: Dylan Couzon

In this lesson, you'll see how the AI assistant device's hardware, models, and local memory work together. You'll follow the path from a camera image or spoken name to a memory the AI assistant device can find by sight or meaning. Alright, let's get to it. We saw the robot recall my watch. We told it Luna. Now, let's look at how it was built. The camera, the computer, the storage, and the interface. Everything runs inside the application on the device, including the embedding models and vector search.

There is no separate vector database server, and the memory is stored in a folder on the device. The complete build is open source, with all the code, hardware details, enclosure 3D print files, and setup instructions. Let's take a look at the repo now. This specific robot uses an NVIDIA Jetson Orin with 8 gigabytes of memory. Other parts include an SSD drive, a USB camera, and a 3D printed enclosure. But please note that you do not need any specific hardware for this course.

You can run the application on a Raspberry Pi 5 or your personal computer. In the very last lesson, we will run this code project on a local computer as well. Let's briefly take a look at how the case was designed. The robot includes no microphone, speaker, or screen. I am connected to it with my phone through direct Wi-Fi, and the phone is the interface. The processing stays on the robot.

So here, you can see that you have all the multiple representations of all the memories that we have on the robot. And you can see that I can rename, forget them, or drop a specific view. The phone keeps the physical build compact, but you could add the microphone, speaker, or screen to the robot instead. The memory architecture would stay the same, as all the processing is already done on the robot. Then, how do we go from a camera frame to a memory? Our goal today is to create memory, not this exact robot.

This robot is just one complete example. But you can think about smart glasses, security system, home assistant, or in-the-field device. They all require different cameras, sensors, and interfaces, but it is the same memory loop underneath. Here, you just need to decide what your device should remember, and then design it however you wish. In the next lesson, we will build the core memory loop, which is the brain of the robot.

---

## Lesson 3: Store, Find, and Forget Memories
Source: videos/sc-Qdrant-C3-L3-v2.mp4 (6:38)
Instructor: Dylan Couzon

What does it take to give an application a memory? In this lesson, you'll build one from scratch and test how it stores, finds, filters, and forgets text and images. Alright, let's go! We start by importing our helper functions and Qdrant Edge. Then we create a shard. So the shard is just the directory where your memory store will live. We'll also call this a collection. So here it is named mem_shard. Then we configure Qdrant Edge. We say which types of vectors do we want. And here we want a text and an image vector. And then we configure the parameters for those vectors. So here the size for the text is 768 embeddings. And this means that the embedding model creates 768 dimensions for the text. And then for the images, we create 512. Then for the distance metrics, we use cosine to compare the vectors to the questions for both text and images. And then we just create the shard.

Then to verify that our shard is working, we're going to try to ask a question. So the question right now is a good place to eat or drink nearby. But you could change that question to anything else. We're then going to embed that question with the same embedding model that we're using to embed our text memories. And then we're going to query the shard. So you can see that we're requesting for the nearest vectors to our questions and we're doing a limit of 3. And right now nothing returned because we haven't stored any memories yet into our collection. So to create those memories, we're going to import a JSON file that contains text notes as memories, but also a payload on those memories. So metadata like category and price that gives us additional information about those memories.

Then what we need to do is to embed those memories one by one. And once this is done, this is what a vector looks like. So you can see that it is just an array of numbers that represents the meaning behind the text. Then the only thing that is left to do is to upload those memories into Qdrant. So we use what we call points to store the memory with all the vectors, but also any metadata that is associated with that memory. So we have the ID, we have the source type, which is where the memory came from. We have a category label, the location, the exact timestamp, the text version of the notes and the price when it is applicable.

Then we can ask our question again, a good place to eat or drink nearby. We emit that query and then we ask our memory store again. And here we can see our top three matches. The first one, a great little coffee place on 5th with outdoor seating and fast Wi-Fi. And our best score is 0.58. But then what happens when I want to query memories from a specific category or a specific price?

What we're doing here, we're creating field indexes to enable us filtering on specific fields. So here we enable filtering on category and price. Now we want to ask the same question again, a good place to eat or drink nearby. But we have some filters that are applied. We want the category to match food and the price to be lower than $15. Now you can see that all the results match our food category filter and also match our price condition.

And the best match is a great little coffee place on 5th with outdoor seating and fast Wi-Fi with a score of 0.587. Our robot doesn't only process text. It also process images and live video. Now let's add images to our memories. We're importing a bunch of different images, all representing different objects. We started with 20 text memories.

And now we stored an additional 165 photos as memory into our memory store for a total of 185 memories. Since we're using CLIP, an embedding model that matches text and images, we can ask it a red bicycle, embed that query, and then search. And here we have a red bicycle retrieved.

The last thing we may want to do is to forget memories. So here we're just taking the first memory that we've learned. Great little coffee place on 5th with outdoor seating and fast Wi-Fi. And we're forgetting it by calling delete_points. And here you can see the before and after of our question, a good place to eat or drink nearby. Where in the before, we're still retrieving great little coffee place on 5th.

Now that this memory was deleted, our first result is Found a quiet cafe with good Wi-Fi to work from near the park, which was our second result before deletion. Let's also take a look at the latency. This plot was generated on my own Mac using the code that is in this notebook. Different machines will generate different latency numbers, but the trend should still be similar. You can see here that the x-axis is logarithmic. So the last value is 250 times greater than the first one.

So you can see that the latency has gone up about 50 times, while the numbers of memories has gone up 250 times. Vector databases are optimized to handle hundreds of thousands or even millions of memories, but forgetting and cleaning up your data is still valuable. In this lesson, you created your first memory store. You stored text notes and images, and you learned to search, add filters, and learned about the latency implications. In the next lesson, you would put all of that together and start building a voice assistant that can search through your day.

---

## Lesson 4: Your On-Device Assistant
Source: videos/sc-Qdrant-C3-L4-v2.mp4 (4:58)
Instructor: Dylan Couzon

Your day is scattered across photos, voice notes, and text. In this lesson, you'll bring them into one on-device memory. Search it with typed or spoken questions and add a new memory you can recall immediately. Let's have some fun. First, let's import our helper functions and load our memories. Here, you can see that we have 42 different memories, 17 photos, 20 text memories, and 5 voice memories. First, let's look at our image memories. Today, you can see that at 7:20 we went to the gym, then we had some pastries, coffee, looks like we went to work, we had ramen for lunch, we went to do some shopping, we went to the park, seems like we visited downtown, and then we went home around 5:30 p.m. Now, let's take a look at our notes. So you can see that our notes seem to be matching our image memories. We went to the gym this morning, we renewed our membership, we went to a bakery, then we found a coffee place, we parked our bike near the station when we went to work, and then we had some notes about work. Some of these notes were added as text, and some others were added as voice notes.

So now, let's look into how those voice notes were created. Here, we have a note audio file. "Note to self, the ramen downtown was incredible. $14 and worth it. Sat right by the window." We used a Whisper local model to create that transcript. What we are storing is this transcript, not the audio itself. Now, as we've done before, we will create our memory store, then embed each memory with the source type as metadata, if it was text or voice. And lastly, we will be storing our memory photos. Now, you're ready to recall your day. We're creating a helper function called recall that will allow you to search through your photos, voice notes, and text notes.

And here, we're going to be asking the question, what was the ramen place downtown? We're calling that recall function. And here, you can see that we're using a minimum text score of 0.6 and a minimum photo score of 0.23. We're using different scores or thresholds because we're using different models. You will learn about those thresholds in more details. As you can see, we have retrieved multiple voice notes and multiple text notes for our search. But every result that falls below the threshold we have set gets ignored. So this is why those results are grayed out here.

In our top results, you can see that today, at 12:30, I created a text note that says, "Try the new ramen place downtown, everyone raves about the Tonkotsu." Then, at 1:12 p.m., apparently, I went to a place called Ramen-ya, and it looks like I tried the Tonkotsu ramen. Then, after lunch, I created a voice note that said, "Note to self, the ramen downtown was incredible." Then, since we're transcribing the audio into text, the search works exactly the same as a text search. And we ask, hey, where did I park the bike? And we can see a note from this morning, "Park the bike near the station, second rack from the entrance." And it looks like we also took a picture before going into work this morning.

Looking at the results that did not meet our threshold, you can see here that we're mentioning the park. And so this is why there's a weak match with parking the bike, and this could be the reason why these notes showed up at the top, but still below our threshold. Now, let's test out our assistant. Here, we're adding a note that says, "Left the spare key with the neighbor in apartment 4B." But you could also be adding a voice note or an image here. Now, let's ask the assistant a question related to the memory we just created.

So here, I'm going to ask it, where did I leave the spare key? But you can ask it any kind of question you want that is related to the memory you just created. And here, our best match with the highest similarity score is the note that we wrote earlier, "Left the spare key with the neighbor in apartment 4B," which is exactly the memory we were looking for. In this lesson, you created your first assistant that can recall different types of memories. In the next lesson, you will teach your assistant to recognize concepts it has never seen before. Alright, see you there!

---

## Lesson 5: Teaching Your Assistant to See
Source: videos/sc-Qdrant-C3-L5-v2.mp4 (5:36)
Instructor: Dylan Couzon

What if your assistant could learn to recognize something new? In this lesson, you'll teach the assistant device an object from a few photos, test it on a view it hasn't seen, and combine meaning with recency to surface the right memories, all offline. Let's go! As in the previous lessons, we will start by importing our helper functions, Qdrant Edge, and create a new memory store. Then, we will create two more reusable functions. The first one, add_memory, that adds a memory into our memory bank.

And the second one, teach, which just adds multiple memories at once. Then, let's seed a few objects into our memory store. Alright, and here we have a few sample memories. A bicycle, chess pieces, and a camera. We're gonna be using those two images on the left side to teach, and the third one on the right side to test. If you want to teach your own object, you can use the photo uploader here.

In the first one, you need to upload two images to teach with, and in the second one, you need to upload one image to test with. The first two images will be replacing these two on the left side, and the last image will be replacing this image on the right side. Uploading your own images is fully optional. If you don't upload any images, the rubber ducks will be used as the default. Now, let's show our test image to the AI assistant to see what happens. And here, you can see that we showed it the image of a duck, but since we have never taught it a duck, the closest match that we have so far is a bicycle, which is not a duck.

Now, let's teach our AI assistant those two images. We're entering the subject name, "rubber duck", for the metadata, and then we're teaching the photos. And here, you can see that we taught those two views of the rubber duck. Now, let's try to recognize our test image again and see what happens. And here, you can clearly see that the closest memory to the photo that we showed was another rubber duck, with a similarity score of 0.88. Now, retrieval will always return the highest similarity, no matter how low.

To find the right balance for the threshold, I have run an experiment with a large set of images that includes 220 non-matches and 6 matches, and here is the result. As you can see, the lowest scoring match is at 0.86, and the highest non-match is at 0.74. So 0.8 is the right middle for the threshold in my use case. Depending on the significance of false positives and false negatives, for your use case, you can select a threshold that fits your use case the best. So now, let's build our assistant end-to-end. Let's create a new memory store.

And now, let's store a few memories from our day. A few notes and photos. Then, we're going to add the memory that we just created. So here are rubber ducks with an additional note: "Rubber duck for the bath from the toy shop on Elm Street." And we can see here that our assistant now has a total of 145 memories.

To make this AI assistant even better, we might want to prioritize certain types of memories, like the most recent ones. Because here, when we ask the question, "what is my gym locker code?", you can see that the memory from August 30th scored higher than the memory from September 14th. And ideally, we would want the most recent memory with the most recent code to score the highest. To address this problem, you can add a soft forgetting. So here, we're creating a half-life of seven days in seconds.

And then we're adding a freshness weight. It tells how important it is that the memories should be recent. Now, running that same query with the freshness applied, you can see that the most recent memory is the one that scores the highest by a huge margin. Now that we have all the components for your AI assistant, let's ask it a few questions. What did I get at the toy shop? Show me the bakery.

Where did I have brunch? And what did the bike chain cost? That first question, "what did I get at the toy shop?", is the rubber duck memory that we created. If you use your own memory and your own photos, you might have a different result here. And then "show me the bakery", "where did I have brunch?", and "what did the bike chain cost?" all seem to fit previous memory well. Here we can see that it remembered a new bakery on the corner. There's an amazing morning cronut. And we have a picture of that cronut.

Brunch at the cafe with pancakes and coffee for $14. And we see here I had brunch with family and the bike chain. And we can see that we bought it for $32. And we also have found like a picture of our bike attached. And all of this was done through pure retrieval without any LLM involved. In this lesson, you put everything together and taught your assistant a new memory.

If you apply the same concepts to a video frame by frame, this is how the robot that we've showcased today works. The robot is based on the same assistant code that we've built here. It just runs on a loop frame by frame. In the next lesson, we will run the full AI assistant loop on the personal machine.
