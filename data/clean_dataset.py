import pandas as pd
import ast
import re
import os

INPUT_PATH = os.path.join("data", "products.csv")
OUTPUT_PATH = os.path.join("data", "products_clean.csv")

def extract_first_image(images_str):
    if pd.isna(images_str):
        return None
    try:
        images_list = ast.literal_eval(images_str)
        if isinstance(images_list, list) and len(images_list) > 0:
            return images_list[0]
    except:
        pass
    return None

def extract_category(breadcrumbs):
    if pd.isna(breadcrumbs):
        return "General"
    parts = str(breadcrumbs).split("›")
    if len(parts) >= 2:
        return parts[1].strip()
    return parts[0].strip()

def clean_rating(rating_stars):
    if pd.isna(rating_stars):
        return 0.0
    match = re.search(r"[\d.]+", str(rating_stars))
    if match:
        return float(match.group())
    return 0.0

def clean_price(price_value):
    if pd.isna(price_value):
        return 0.0
    try:
        return float(price_value)
    except:
        return 0.0

df = pd.read_csv(INPUT_PATH)
print(f"Loaded {len(df)} rows")

clean_df = pd.DataFrame()
clean_df["title"] = df["title"]
clean_df["category"] = df["breadcrumbs"].apply(extract_category)
clean_df["brand"] = df["brand_name"].fillna("Unknown Brand")
clean_df["price"] = df["price_value"].apply(clean_price)
clean_df["rating"] = df["rating_stars"].apply(clean_rating)
clean_df["review_summary"] = df["customer_review_summary"].fillna("No reviews yet")
clean_df["availability"] = df["availability"].fillna("Unknown")
clean_df["image_url"] = df["all_images"].apply(extract_first_image)
clean_df["product_link"] = df["product_url"]

# Drop rows with no title or price
clean_df = clean_df.dropna(subset=["title"])
clean_df = clean_df[clean_df["price"] > 0]

clean_df.to_csv(OUTPUT_PATH, index=False)
print(f"Saved {len(clean_df)} cleaned products to {OUTPUT_PATH}")
print(f"\nCategories found: {clean_df['category'].unique().tolist()}")
print(f"\nSample row:")
print(clean_df.iloc[0])