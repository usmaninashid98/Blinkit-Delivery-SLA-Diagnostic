
import sqlite3
import random
from datetime import date, datetime, timedelta

rng = random.Random(1010)

conn = sqlite3.connect("blinkit_sla.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS dark_stores;
DROP TABLE IF EXISTS hour_bands;
DROP TABLE IF EXISTS orders;

CREATE TABLE dark_stores (
    store_id INTEGER PRIMARY KEY,
    store_name TEXT NOT NULL,
    city TEXT NOT NULL,
    cluster TEXT NOT NULL
);
CREATE TABLE hour_bands (
    hour_text TEXT PRIMARY KEY,
    band TEXT NOT NULL
);
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    store_id INTEGER NOT NULL,
    order_ts TEXT NOT NULL,
    order_date TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL,
    delivery_minutes INTEGER,
    within_sla INTEGER,
    FOREIGN KEY (store_id) REFERENCES dark_stores(store_id)
);
""")

stores = [
    (1, "Andheri West 1", "Mumbai", "Andheri"),
    (2, "Andheri East 2", "Mumbai", "Andheri"),
    (3, "Powai Lake 1", "Mumbai", "Powai"),
    (4, "Powai Hiranandani 2", "Mumbai", "Powai"),
    (5, "Thane Ghodbunder 1", "Mumbai", "Thane"),
    (6, "Thane Naupada 2", "Mumbai", "Thane"),
    (7, "Koramangala 5th Block", "Bengaluru", "Koramangala"),
    (8, "Koramangala 8th Block", "Bengaluru", "Koramangala"),
    (9, "Whitefield Main", "Bengaluru", "Whitefield"),
    (10, "Whitefield ITPL", "Bengaluru", "Whitefield"),
    (11, "Indiranagar 100ft", "Bengaluru", "Indiranagar"),
    (12, "Indiranagar CMH", "Bengaluru", "Indiranagar"),
    (13, "Powai Annex (not yet live)", "Mumbai", "Powai"),
]
cur.executemany("INSERT INTO dark_stores VALUES (?,?,?,?)", stores)

band_of_hour = {}
for h in range(6, 11):
    band_of_hour[h] = "Morning"
for h in range(11, 15):
    band_of_hour[h] = "Lunch"
for h in range(15, 19):
    band_of_hour[h] = "Afternoon"
for h in range(19, 23):
    band_of_hour[h] = "Evening"

cur.executemany(
    "INSERT INTO hour_bands VALUES (?,?)",
    [(f"{h:02d}", band_of_hour[h]) for h in sorted(band_of_hour)]
)

categories = [
    "Dairy & Bread",
    "Fruits & Vegetables",
    "Snacks & Beverages",
    "Personal Care",
    "Household"
]
cat_weights = [0.30, 0.22, 0.24, 0.12, 0.12]
hours = sorted(band_of_hour)

hour_weights = [
    0.04, 0.05, 0.05, 0.04, 0.04,
    0.07, 0.07, 0.06, 0.06,
    0.05, 0.05, 0.05, 0.05,
    0.08, 0.09, 0.09, 0.06
]

live_stores = [s for s in stores if s[0] != 13]
cluster_of = {s[0]: s[3] for s in stores}

start = date(2026, 10, 5)
TOTAL_ORDERS = 6000
BAND_BASE = {
    "Morning": -0.3,
    "Lunch": 0.6,
    "Afternoon": 0.0,
    "Evening": 0.8
}

orders = []

for oid in range(1, TOTAL_ORDERS + 1):
    store = rng.choice(live_stores)
    sid, cluster = store[0], store[3]
    day = rng.randint(0, 27)
    hour = rng.choices(hours, weights=hour_weights, k=1)[0]
    minute = rng.randint(0, 59)

    d = start + timedelta(days=day)
    ts = datetime(
        d.year, d.month, d.day,
        hour, minute, rng.randint(0, 59)
    )

    category = rng.choices(categories, weights=cat_weights, k=1)[0]
    band = band_of_hour[hour]

    if rng.random() < 0.06:
        orders.append((
            oid, sid,
            ts.strftime("%Y-%m-%d %H:%M:%S"),
            d.isoformat(),
            category, "Cancelled", None, None
        ))
        continue

    ramp = day / 27.0
    raw = rng.gauss(8.3, 1.7) + BAND_BASE[band]

    if category == "Fruits & Vegetables":
        raw += 1.5

    if cluster == "Andheri" and band == "Evening":
        if rng.random() < 0.15 + 0.45 * ramp:
            raw += 6.5

    if cluster == "Whitefield" and band == "Lunch":
        raw += 1.0 + 1.5 * ramp

    if cluster == "Koramangala" and band == "Evening":
        if rng.random() < 0.10 + 0.30 * ramp:
            raw += 5.0

    minutes = max(3, int(round(raw)))

    if minutes == 11 and rng.random() < 0.35:
        minutes = 10

    within = 1 if minutes <= 10 else 0

    orders.append((
        oid, sid,
        ts.strftime("%Y-%m-%d %H:%M:%S"),
        d.isoformat(),
        category, "Delivered", minutes, within
    ))

cur.executemany(
    "INSERT INTO orders VALUES (?,?,?,?,?,?,?,?)",
    orders
)

conn.commit()
conn.close()

print("blinkit_sla.db created.")
