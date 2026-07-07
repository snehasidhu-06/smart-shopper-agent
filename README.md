# Smart E-Commerce Personal Shopper and Recommendation Agent

## Overview

A GenAI-powered shopping assistant that helps users find products through natural language conversations. Instead of searching with keywords, users can describe what they want, and the assistant recommends suitable products using AI.

---

## Features

* Chat-based shopping assistant
* Understands natural language queries
* Detects shopping requests and casual conversations
* Recommends relevant products using AI
* Displays product images, prices, ratings, and Buy Now links
* Separate frontend and backend architecture

---

## Tech Stack

* **Frontend:** Streamlit
* **Backend:** FastAPI
* **LLM:** Groq (Llama 3.1 8B Instant)
* **Framework:** LangChain
* **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
* **Vector Database:** FAISS
* **Database:** SQLite
* **Data Processing:** Pandas

---

## How It Works

1. The user enters a message in the Streamlit interface.
2. The message is sent to the FastAPI backend.
3. The AI detects whether the user wants to shop or is simply chatting.
4. For shopping requests, similar products are retrieved using FAISS.
5. The LLM generates personalized recommendations.
6. Product details are displayed to the user.

---

## Dataset

The project uses a cleaned Amazon product dataset with approximately **700 products**, including:

* Product title
* Brand
* Category
* Price
* Rating
* Product image
* Product link

---

## How to Run

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add:

   ```
   GROQ_API_KEY=your_api_key
   ```
5. Set up the database:

   ```
   python database/db_setup.py
   ```
6. Generate embeddings:

   ```
   python embeddings/generate_embeddings.py
   ```
7. Start the backend:

   ```
   uvicorn backend.main:app --reload
   ```
8. Start the frontend:

   ```
   streamlit run frontend/app.py
   ```

---

## Future Improvements

* Real-time product APIs
* Conversation memory
* Price filtering
* User login and recommendation history
* Docker deployment

---

## Project Type

Summer Training Project – GenAI-based Product Recommendation System
