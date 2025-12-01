import json
from collections import defaultdict

# Load vectorizer + ML model (saved earlier)
import joblib
model = joblib.load("model/spend_model.pkl")
vectorizer = model.named_steps["tfidf"]

# Load merchant memory
MEMORY_FILE = "model/memory.json"

try:
    with open(MEMORY_FILE, "r") as f:
        merchant_memory = json.load(f)
except:
    merchant_memory = {}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(merchant_memory, f, indent=2)

# Your rule-based classifier
def guess_category(merchant: str):
    if any(w in merchant for w in ["coffee", "cafe", "latte", "roaster", "espresso"]):
        return "coffee"
    if any(w in merchant for w in ["market", "trader", "whole", "produce", "grocery"]):
        return "groceries"
    if any(w in merchant for w in ["lyft", "uber", "wheels", "clipper"]):
        return "transport"
    if any(w in merchant for w in ["classpass", "yoga", "corepower"]):
        return "fitness"
    if any(w in merchant for w in ["spotify", "patreon"]):
        return "subscriptions"
    if any(w in merchant for w in ["salon", "beauty", "scent", "sephora", "nail"]):
        return "selfcare"
    return "other"

# Hybrid classifier
def hybrid_classify(merchant: str):
    m = merchant.lower()

    # 1. memory check
    if m in merchant_memory:
        return merchant_memory[m]

    # 2. rule-based
    rule = guess_category(m)
    if rule != "other":
        merchant_memory[m] = rule
        save_memory()
        return rule

    # 3. ML model
    ml_cat = model.predict([m])[0]
    merchant_memory[m] = ml_cat
    save_memory()
    return ml_cat
