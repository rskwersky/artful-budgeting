import re

def clean_merchant(name: str) -> str:
    name = name.lower()
    name = re.sub(r"\d+", "", name)
    name = re.sub(r"s\s#", "", name)
    name = re.sub(r"#", "", name)
    
    for city in ["san francisco", "berkeley", "ca", "oakland"]:
        name = name.replace(city, "")
    
    for n in ["pos", "transaction", "counter", "purchase", "terminal", "card"]:
        name = name.replace(n, "")

    return name.strip()

def load_statement(csv_file):
    df = pd.read_csv(csv_file)
    df["merchant_clean"] = df["merchant"].apply(clean_merchant)
    return df