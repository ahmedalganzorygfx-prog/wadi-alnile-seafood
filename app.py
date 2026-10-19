# -*- coding: utf-8 -*-
"""موقع مطاعم أسماك وادي النيل - واجهة HTML الأصلية مع خادم Python/Flask."""
from datetime import datetime
from pathlib import Path
import json
import sqlite3
from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "wadi_nile.db"
app = Flask(__name__, template_folder="templates", static_folder="static")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            branch TEXT NOT NULL,
            items_json TEXT NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'جديد'
        )""")
        conn.commit()


@app.get("/")
def home():
    # The original HTML layout is served directly to preserve its design and interactions.
    return render_template("index.html")


@app.post("/api/orders")
def create_order():
    data = request.get_json(silent=True) or {}
    required = ["customer_name", "phone", "address", "branch", "items", "total"]
    if any(data.get(key) in (None, "", []) for key in required):
        return jsonify({"ok": False, "message": "بيانات الطلب غير مكتملة"}), 400
    try:
        total = float(data["total"])
        items = data["items"]
        if not isinstance(items, list) or not items:
            raise ValueError("empty items")
        with get_db() as conn:
            cur = conn.execute(
                """INSERT INTO orders
                (created_at, customer_name, phone, address, branch, items_json, total, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (datetime.now().isoformat(timespec="seconds"),
                 str(data["customer_name"]).strip(), str(data["phone"]).strip(),
                 str(data["address"]).strip(), str(data["branch"]).strip(),
                 json.dumps(items, ensure_ascii=False), total, "جديد")
            )
            order_id = cur.lastrowid
            conn.commit()
        return jsonify({"ok": True, "order_id": order_id})
    except (TypeError, ValueError, sqlite3.Error):
        return jsonify({"ok": False, "message": "تعذر حفظ الطلب"}), 400


@app.get("/health")
def health():
    return jsonify({"ok": True})


init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
