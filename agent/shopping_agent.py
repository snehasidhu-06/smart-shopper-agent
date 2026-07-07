import os
import sys
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Allow importing from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recommender.search_engine import search_products

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)


def detect_intent(user_message: str) -> str:
    """
    Classify whether the user wants to shop or is just chatting.
    """
    intent_prompt = f"""
Classify this message as either "shopping" or "chat".

Rules:
- shopping = user wants to buy something, asks for product recommendations,
  mentions a product, budget, brand, or shopping need.
- chat = greetings, casual conversation, questions about the assistant,
  or anything unrelated to shopping.

Message:
"{user_message}"

Reply with ONLY one word:
shopping
or
chat
"""
    try:
        response = llm.invoke(intent_prompt)
        intent = response.content.strip().lower()

        if intent == "shopping":
            return "shopping"
        elif intent == "chat":
            return "chat"
        else:
            return "chat"

    except Exception as e:
        print("Intent Detection Error:", e)
        return "chat"


def shopping_agent(user_message: str):
    """
    Main shopping assistant.
    Returns a tuple: (response_text, results_list)
    """

    intent = detect_intent(user_message)

    # -------------------------
    # Casual conversation
    # -------------------------
    if intent == "chat":
        chat_prompt = f"""
You are a friendly e-commerce shopping assistant.

The user said:
"{user_message}"

Respond naturally and warmly.
Keep your answer short.

If appropriate, mention that you can help them find products whenever they need.
"""
        try:
            response = llm.invoke(chat_prompt)
            return response.content, []
        except Exception as e:
            return f"Sorry, I couldn't process your message.\nError: {e}", []

    # -------------------------
    # Shopping flow
    # -------------------------
    results = search_products(user_message, top_k=3)

    if not results:
        return (
            "Sorry, I couldn't find any products matching your request. "
            "Try using different keywords or being more specific."
        ), []

    product_lines = []
    for i, product in enumerate(results, start=1):
        product_lines.append(
            f"{i}. {product['title']} | "
            f"Category: {product['category']} | "
            f"Brand: {product['brand']} | "
            f"Price: ${product['price']} | "
            f"Rating: {product['rating']}"
        )

    product_list_text = "\n".join(product_lines)

    prompt = f"""
You are a helpful e-commerce shopping assistant.

Customer request:
"{user_message}"

These are the products available:

{product_list_text}

Instructions:
Format your response EXACTLY like this structure for each product (2-3 products only):

1. [Product name, short version, max 8 words]
   Highlight: [one short reason, max 10 words]
   Price: $[price]
   Rating: [rating] stars

Rules:
- Use this exact line-by-line format, do not merge into paragraphs.
- No extra commentary, no introduction sentence, no conclusion sentence.
- No trade-off paragraph at the end.
- If none are a good match, just say: "No close matches found for this request."
- Do not mention any product that is not in the list above.
"""

    try:
        response = llm.invoke(prompt)
        return response.content, results
    except Exception as e:
        return f"Sorry, something went wrong while generating recommendations.\nError: {e}", []


# -------------------------
# Testing
# -------------------------
if __name__ == "__main__":
    test_messages = [
        "hi",
        "how are you",
        "I need a casual polo shirt for men",
        "recommend workout clothes for women",
        "gift for a baby"
    ]

    for msg in test_messages:
        print("\n" + "=" * 60)
        print(f"User: {msg}")
        print("-" * 60)
        text, results = shopping_agent(msg)
        print(text)
        print(f"\n[Returned {len(results)} product results]")