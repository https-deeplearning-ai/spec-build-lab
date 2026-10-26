# Pattern card: LangChain for LLM Application Development

*Confirmed by the owner, 2026-10-23. Drafted by a clean-room generator (guide v2.4) from the materials. Two changes were suggested by Claude (the orchestrator) and accepted by the owner: item 1 lost "split when too big" (splitting is a learner choice); the proposed item 4 (say "I don't know" when the pieces lack the answer) moved off the card into a rule of the recommended build. Lesson numbers follow the transcript headers.*

*Reconfirmed by the owner, 2026-10-24: all three items kept unchanged; every quote checked against the materials and found. No changes.*

*Reconfirmed by the owner, 2026-10-26: all three items kept unchanged. One change, suggested by Claude (the orchestrator) and accepted by the owner: conversation memory and other lessons' parts moved out of the "Not on the card" line, which reads as "options", into their own line "Background notes, not offered". No "Offered from other lessons" section (none).*

*Reconfirmed by the owner again, 2026-10-26, before the v2.5 regeneration: no changes.*

**The one kind of program:** a program that answers a person's plain-language questions about their own collection of documents, using the few pieces of the collection most similar in meaning to the question.

## What every build keeps

1. **The documents are indexed by meaning before any question.** Each piece of text gets a numeric representation of its meaning, stored next to its original text, so pieces with similar meaning can be found later.
   - L5: "Embeddings create numerical representations for pieces of text. This numerical representation captures the semantic meaning of the piece of text ... Pieces of text with similar content will have similar vectors."
   - L5: "We then create an embedding for each of these chunks, and then we store those in a vector database. That's what happens when we create the index."

2. **For each question, only the few stored pieces most similar in meaning are retrieved, not the whole collection.**
   - L5: "When a query comes in, we first create an embedding for that query. We then compare it to all the vectors in the vector database, and we pick the n most similar."
   - L5: "Language models can only inspect a few thousand words at a time."

3. **A language model writes the answer from the question plus the retrieved pieces, so the answer rests on the person's documents.**
   - L5: "These are then returned, and we can pass those in the prompt to the language model to get back a final answer."
   - L5: "This is really powerful because it starts to combine these language models with data that they weren't originally trained on."

## Not on the card (rules of the recommended build, options, settings, or notes)
- **Saying "I don't know" when the retrieved pieces lack the answer** is a rule of the recommended build. Its source is the L6 chain prompt: "If you don't know the answer, just say that you don't know, don't try to make up an answer."
- Evaluation, debug tracing, how the pieces are combined (stuff, map_reduce, refine, map_rerank), splitting, the store and embedding choices, temperature, and the product-catalog example.
- **Background notes, not offered:** conversation memory and other lessons' parts.
