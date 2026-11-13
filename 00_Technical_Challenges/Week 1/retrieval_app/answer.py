"""Stage 5: turn retrieved chunks into an answer.

YOUR CODE GOES HERE. The prompt is yours to write — it is the cheapest thing
in the pipeline to change and often the most effective.
"""

from .index import Hit, client

CHAT_MODEL = "gpt-4.1-mini"

# SYSTEM_PROMPT = """You are a helpful assistant that answers questions based strictly on the provided context.

# Instructions:
# - Only answer questions using information from the provided context.
# - Each context passage is labelled like [chunk 3]. Cite the labels of the passages you used.
# - If the context doesn't contain relevant information, respond with
#   "I don't have information about that in my knowledge base."
# - Do not use external knowledge, and only answer when you are confident the context supports your response.
# - Keep responses concise.""" 

SYSTEM_PROMPT = """You are a helpful assistant that answers questions based strictly on the provided context.

Instructions:
- Only answer questions using information from the provided context.
- Each context passage is labelled like [chunk 3]. Cite those labels for every claim you make.
- If the context fully answers the question, answer it.
- If it only partly answers, state what the context covers (with citations), then say plainly what it does not cover.
- If it does not answer at all, respond with "I don't have information about that in my knowledge base."
- Never infer, generalise, or add facts that are not stated in the context, even if they seem reasonable.
- If the question assumes something ("like you said", a number, a claim), do not agree with it unless the context supports it.
- Keep responses concise."""

USER_TEMPLATE = """Context Information:
{context}

Number of relevant sources found: {context_count}
Relevance scores: {scores}

Question: {question}

Please provide your answer based solely on the context above."""

def build_messages(question: str, hits: list[Hit]) -> list[dict]:
    """Assemble the messages list sent to the chat model.

    Args:
        question: the user's question.
        hits: what search() returned. May be empty.

    Returns:
        A list of {"role": ..., "content": ...} dicts — a system message
        setting the rules, and a user message carrying the context and the
        question.

    Three things your prompt has to decide, and they are real decisions:
      1. How do you label each chunk in the context so the model can refer to
         it? (hit.chunk_id exists for this.)
      2. What should it do when the context does not contain the answer? Say
         so explicitly, or it will answer from the nearest chunk regardless.
      3. What happens when `hits` is empty? Write that branch deliberately.

    Hint: Session 2's RAG_SYSTEM_TEMPLATE is a good starting point, and a
    better one once you have read Step 3's failures and edited it.
    """
    if hits:
        context = "\n\n".join(f"[chunk {h.chunk_id}]: {h.text}" for h in hits)
        scores = ", ".join(f"chunk {h.chunk_id}: {h.score:.3f}" for h in hits)
    else:
        context = "(No passages were retrieved for this question.)"
        scores = "n/a"

    user = USER_TEMPLATE.format(
        context=context, context_count=len(hits), scores=scores, question=question
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user},
    ]


def answer(question: str, hits: list[Hit]) -> str:
    """Call the chat model and return its reply as a string.

    Hint: `client().chat.completions.create(model=CHAT_MODEL, messages=...)`,
    then dig out `.choices[0].message.content`. Look up what `temperature`
    does to your results when you run the same question twice.
    """
    response = client().chat.completions.create(
        model=CHAT_MODEL,
        messages=build_messages(question, hits),
        temperature=0,
    )
    return response.choices[0].message.content
