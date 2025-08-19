from typing import Optional
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

def _df(engine: Engine, sql: str, params: dict | None = None) -> pd.DataFrame:
    with engine.connect() as con:
        return pd.read_sql(text(sql), con, params=params or {})

def q_providers_receivers_by_city(engine: Engine) -> pd.DataFrame:
    sql = """
    WITH cities AS (
      SELECT city FROM providers
      UNION
      SELECT city FROM receivers
    )
    SELECT c.city,
           (SELECT COUNT(*) FROM providers p WHERE p.city = c.city) AS providers,
           (SELECT COUNT(*) FROM receivers r WHERE r.city = c.city) AS receivers
    FROM cities c
    ORDER BY c.city;
    """
    return _df(engine, sql)

def q_top_provider_types_by_quantity(engine: Engine) -> pd.DataFrame:
    sql = """
    SELECT fl.provider_type, SUM(fl.quantity) AS total_quantity
    FROM food_listings fl
    GROUP BY fl.provider_type
    ORDER BY total_quantity DESC;
    """
    return _df(engine, sql)

def q_providers_contact_by_city(engine: Engine, city: Optional[str]) -> pd.DataFrame:
    sql = """
    SELECT name, type, address, city, contact
    FROM providers
    WHERE (:city IS NULL OR UPPER(city) LIKE UPPER(:city_like))
    ORDER BY name;
    """
    params = {"city": city, "city_like": f"%{city}%" if city else None}
    return _df(engine, sql, params)

def q_receivers_most_claims(engine: Engine, limit: int = 10) -> pd.DataFrame:
    sql = """
    SELECT r.name, r.city, COUNT(c.claim_id) AS claims
    FROM receivers r
    JOIN claims c ON c.receiver_id = r.receiver_id
    GROUP BY r.name, r.city
    ORDER BY claims DESC
    LIMIT :limit;
    """
    return _df(engine, sql, {"limit": limit})

def q_total_food_available(engine: Engine, city_filter: Optional[str] = None) -> pd.DataFrame:
    sql = """
    SELECT COALESCE(SUM(quantity),0) AS total_quantity
    FROM food_listings
    WHERE (:city IS NULL OR UPPER(location) LIKE UPPER(:city_like));
    """
    return _df(engine, sql, {"city": city_filter, "city_like": f"%{city_filter}%" if city_filter else None})

def q_top_cities_listings(engine: Engine, limit: int = 5) -> pd.DataFrame:
    sql = """
    SELECT location AS city, COUNT(*) AS listings
    FROM food_listings
    GROUP BY location
    ORDER BY listings DESC
    LIMIT :limit;
    """
    return _df(engine, sql, {"limit": limit})

def q_common_food_types(engine: Engine) -> pd.DataFrame:
    sql = """
    SELECT food_type, COUNT(*) AS count_listings, SUM(quantity) AS total_quantity
    FROM food_listings
    GROUP BY food_type
    ORDER BY total_quantity DESC, count_listings DESC;
    """
    return _df(engine, sql)

def q_claims_per_food_item(engine: Engine) -> pd.DataFrame:
    sql = """
    SELECT fl.food_id, fl.food_name, COUNT(c.claim_id) AS claims
    FROM food_listings fl
    LEFT JOIN claims c ON c.food_id = fl.food_id
    GROUP BY fl.food_id, fl.food_name
    ORDER BY claims DESC, fl.food_id ASC;
    """
    return _df(engine, sql)

def q_provider_highest_successful_claims(engine: Engine, limit: int = 10) -> pd.DataFrame:
    sql = """
    SELECT p.name AS provider_name, COUNT(c.claim_id) AS successful_claims
    FROM providers p
    JOIN food_listings fl ON fl.provider_id = p.provider_id
    JOIN claims c ON c.food_id = fl.food_id
    WHERE UPPER(c.status) = 'COMPLETED'
    GROUP BY p.name
    ORDER BY successful_claims DESC
    LIMIT :limit;
    """
    return _df(engine, sql, {"limit": limit})

def q_claims_status_percentages(engine: Engine) -> pd.DataFrame:
    sql = """
    WITH counts AS (
        SELECT status, COUNT(*) AS cnt
        FROM claims
        GROUP BY status
    ), total AS (
        SELECT SUM(cnt) AS total_cnt FROM counts
    )
    SELECT c.status,
           c.cnt,
           ROUND(100.0 * c.cnt / NULLIF(t.total_cnt,0), 2) AS percent
    FROM counts c CROSS JOIN total t
    ORDER BY percent DESC;
    """
    return _df(engine, sql)

def q_avg_quantity_per_receiver(engine: Engine) -> pd.DataFrame:
    sql = """
    SELECT r.name, AVG(fl.quantity) AS avg_quantity_claimed
    FROM receivers r
    JOIN claims c ON c.receiver_id = r.receiver_id
    JOIN food_listings fl ON fl.food_id = c.food_id
    GROUP BY r.name
    ORDER BY avg_quantity_claimed DESC;
    """
    return _df(engine, sql)

def q_most_claimed_meal_type(engine: Engine) -> pd.DataFrame:
    sql = """
    SELECT fl.meal_type, COUNT(c.claim_id) AS claims
    FROM food_listings fl
    JOIN claims c ON c.food_id = fl.food_id
    GROUP BY fl.meal_type
    ORDER BY claims DESC
    LIMIT 1;
    """
    return _df(engine, sql)

def q_total_quantity_by_provider(engine: Engine) -> pd.DataFrame:
    sql = """
    SELECT p.name AS provider_name, SUM(fl.quantity) AS total_quantity
    FROM providers p
    JOIN food_listings fl ON fl.provider_id = p.provider_id
    GROUP BY p.name
    ORDER BY total_quantity DESC;
    """
    return _df(engine, sql)