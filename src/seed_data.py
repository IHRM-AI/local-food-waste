import os
import sys
import traceback
import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import text
from dotenv import load_dotenv
from src.db import get_engine
from src.models import Base

load_dotenv()

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_csv(name: str) -> pd.DataFrame:
    path = os.path.join(DATA_DIR, name)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing data file: {path}")
    df = pd.read_csv(path)
    print(f"Loaded {name}: {len(df):,} rows")
    return df

def create_schema(engine: Engine):
    print("Creating database schema (if not exists)...")
    Base.metadata.create_all(engine)
    print("Schema ready.")

def seed(engine: Engine):
    print("Dropping existing tables (if any) in correct order...")
    with engine.begin() as con:
        con.execute(text("DROP TABLE IF EXISTS claims"))
        con.execute(text("DROP TABLE IF EXISTS food_listings"))
        con.execute(text("DROP TABLE IF EXISTS receivers"))
        con.execute(text("DROP TABLE IF EXISTS providers"))

    create_schema(engine)

    print("Reading CSVs from:", DATA_DIR)
    providers = load_csv("providers_data.csv")
    receivers = load_csv("receivers_data.csv")
    listings = load_csv("food_listings_data.csv")
    claims = load_csv("claims_data.csv")

    # Normalize headers
    providers.columns = [c.strip() for c in providers.columns]
    receivers.columns = [c.strip() for c in receivers.columns]
    listings.columns = [c.strip() for c in listings.columns]
    claims.columns = [c.strip() for c in claims.columns]

    # Parse dates safely
    if "Expiry_Date" in listings.columns:
        listings["Expiry_Date"] = pd.to_datetime(listings["Expiry_Date"], errors="coerce").dt.date
    if "Timestamp" in claims.columns:
        claims["Timestamp"] = pd.to_datetime(claims["Timestamp"], errors="coerce")

    # Validate required columns
    for df, required, name in [
        (providers, {"Provider_ID", "Name", "Type", "City"}, "providers"),
        (receivers, {"Receiver_ID", "Name", "Type", "City"}, "receivers"),
        (listings, {"Food_ID", "Food_Name", "Quantity", "Expiry_Date", "Provider_ID", "Provider_Type", "Location", "Food_Type", "Meal_Type"}, "food_listings"),
        (claims, {"Claim_ID", "Food_ID", "Receiver_ID", "Status", "Timestamp"}, "claims"),
    ]:
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{name} is missing required columns: {sorted(missing)}")

    print("Writing to database...")
    providers.to_sql("providers", con=engine, if_exists="append", index=False)
    receivers.to_sql("receivers", con=engine, if_exists="append", index=False)
    listings.to_sql("food_listings", con=engine, if_exists="append", index=False)
    claims.to_sql("claims", con=engine, if_exists="append", index=False)

    # Show final counts
    with engine.connect() as con:
        for t in ["providers", "receivers", "food_listings", "claims"]:
            cnt = con.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar_one()
            print(f"Table {t}: {cnt:,} rows")

def main():
    try:
        engine = get_engine()
        print("Seeding database at:", engine.url)
        seed(engine)
        print("Done.")
    except Exception as e:
        print("ERROR while seeding:", e, file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
