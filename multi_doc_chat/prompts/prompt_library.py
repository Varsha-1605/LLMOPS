from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

contextualize_question_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "Given a conversation history and the most recent user query, rewrite the query as a standalone question "
        "that makes sense without relying on the previous context. Do not provide an answer—only reformulate the "
        "question if necessary; otherwise, return it unchanged."
    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt for answering based on context
context_qa_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a helpful AI assistant.\n"
        "Use the retrieved context below when it is relevant:\n"
        "{context}\n\n"
        "If the context does not contain the answer, rely on your general reasoning ability.\n"
        "Do NOT say 'I don't know' unless the question is truly unanswerable."

    )),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Central dictionary to register prompts
PROMPT_REGISTRY = {
    "contextualize_question": contextualize_question_prompt,
    "context_qa": context_qa_prompt,
}

