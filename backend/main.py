from fastapi import FastAPI
from pydantic import BaseModel
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.shopping_agent import shopping_agent

app = FastAPI(title="Smart Shopper Agent API")

class ChatRequest(BaseModel):
    message: str

class ProductResult(BaseModel):
    title: str
    category: str
    brand: str
    price: float
    rating: float
    availability: str
    image_url: str | None = None
    product_link: str | None = None

class ChatResponse(BaseModel):
    reply: str
    products: list[dict]

@app.get("/")
def root():
    return {"status": "Smart Shopper Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply_text, results = shopping_agent(request.message)

    # Convert results (pandas rows / dicts) to plain dicts safely
    products = []
    for product in results:
        products.append({
            "title": product.get("title", ""),
            "category": product.get("category", ""),
            "brand": product.get("brand", ""),
            "price": float(product.get("price", 0)),
            "rating": float(product.get("rating", 0)),
            "availability": product.get("availability", ""),
            "image_url": product.get("image_url"),
            "product_link": product.get("product_link"),
        })

    return ChatResponse(reply=reply_text, products=products)