import os
from contextlib import contextmanager

import psycopg
import streamlit as st
from psycopg.rows import dict_row


def get_database_url():
    """قراءة عنوان قاعدة البيانات من Streamlit Secrets أو متغيرات البيئة."""
    try:
        url = st.secrets.get("DATABASE_URL", "")
    except Exception:
        url = ""

    if not url:
        url = os.environ.get("DATABASE_URL", "")

    if not url:
        raise RuntimeError(
            "لم يتم ضبط DATABASE_URL. أضف عنوان اتصال Supabase "
            "في إعدادات Secrets."
        )

    return url


@contextmanager
def get_connection():
    """فتح اتصال وإغلاقه تلقائيًا."""
    conn = psycopg.connect(
        get_database_url(),
        row_factory=dict_row,
        connect_timeout=15,
    )
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """إنشاء الجداول المطلوبة وتهيئة بيانات البداية."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'أسماك',
                description TEXT NOT NULL DEFAULT '',
                price NUMERIC(12, 2) NOT NULL DEFAULT 0,
                image_url TEXT NOT NULL DEFAULT '',
                available BOOLEAN NOT NULL DEFAULT TRUE,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id BIGSERIAL PRIMARY KEY,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                notes TEXT NOT NULL DEFAULT '',
                branch_name TEXT NOT NULL DEFAULT '',
                subtotal NUMERIC(12, 2) NOT NULL DEFAULT 0,
                delivery_fee NUMERIC(12, 2) NOT NULL DEFAULT 0,
                total NUMERIC(12, 2) NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'جديد',
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                id BIGSERIAL PRIMARY KEY,
                order_id BIGINT NOT NULL
                    REFERENCES orders(id) ON DELETE CASCADE,
                product_id BIGINT,
                product_name TEXT NOT NULL,
                unit_price NUMERIC(12, 2) NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                line_total NUMERIC(12, 2) NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL DEFAULT ''
            )
        """)

        defaults = {
            "restaurant_name": "مطاعم أسماك وادي النيل",
            "restaurant_subtitle": "أشهى المأكولات البحرية الطازجة",
            "restaurant_phone": "",
            "whatsapp_number": "",
            "restaurant_address": "",
            "delivery_fee": "25",
            "free_delivery_minimum": "0",
            "currency": "جنيه",
            "announcement": "أهلاً بكم في مطاعم أسماك وادي النيل",
        }

        for key, value in defaults.items():
            conn.execute(
                """
                INSERT INTO settings (key, value)
                VALUES (%s, %s)
                ON CONFLICT (key) DO NOTHING
                """,
                (key, value),
            )

        count = conn.execute(
            "SELECT COUNT(*) AS total FROM products"
        ).fetchone()["total"]

        if count == 0:
            products = [
                (
                    "سمك بلطي مشوي",
                    "أسماك",
                    "سمك طازج مشوي بتتبيلة مميزة",
                    180,
                    "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2",
                ),
                (
                    "سمك دنيس",
                    "أسماك",
                    "دنيس طازج محضر حسب الطلب",
                    320,
                    "https://images.unsplash.com/photo-1510130387422-82bed34b37e9",
                ),
                (
                    "جمبري مقلي",
                    "جمبري",
                    "جمبري مقرمش يقدم ساخنًا",
                    280,
                    "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47",
                ),
                (
                    "سبيط مقلي",
                    "مأكولات بحرية",
                    "سبيط مقلي بتتبيلة المطعم",
                    240,
                    "https://images.unsplash.com/photo-1559737558-2f5a35f4523b",
                ),
                (
                    "أرز صيادية",
                    "إضافات",
                    "أرز صيادية بالتوابل",
                    45,
                    "https://images.unsplash.com/photo-1516684732162-798a0062be99",
                ),
                (
                    "سلطة خضراء",
                    "إضافات",
                    "سلطة طازجة يوميًا",
                    30,
                    "https://images.unsplash.com/photo-1512621776951-a57141f2eefd",
                ),
            ]

            for product in products:
                conn.execute(
                    """
                    INSERT INTO products
                        (name, category, description, price, image_url)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    product,
                )


def get_setting(key, default=""):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT value FROM settings WHERE key = %s",
            (key,),
        ).fetchone()

    return row["value"] if row else default


def get_settings():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT key, value FROM settings ORDER BY key"
        ).fetchall()

    return {row["key"]: row["value"] for row in rows}


def save_settings(values):
    with get_connection() as conn:
        for key, value in values.items():
            conn.execute(
                """
                INSERT INTO settings (key, value)
                VALUES (%s, %s)
                ON CONFLICT (key)
                DO UPDATE SET value = EXCLUDED.value
                """,
                (key, str(value)),
            )


def get_products(available_only=False):
    sql = "SELECT * FROM products"
    if available_only:
        sql += " WHERE available = TRUE"
    sql += " ORDER BY category, name"

    with get_connection() as conn:
        return conn.execute(sql).fetchall()


def get_product(product_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM products WHERE id = %s",
            (product_id,),
        ).fetchone()


def save_product(
    product_id,
    name,
    category,
    description,
    price,
    image_url,
    available,
):
    if product_id:
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE products
                SET name = %s,
                    category = %s,
                    description = %s,
                    price = %s,
                    image_url = %s,
                    available = %s
                WHERE id = %s
                """,
                (
                    name,
                    category,
                    description,
                    price,
                    image_url,
                    available,
                    product_id,
                ),
            )
    else:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO products
                    (name, category, description, price,
                     image_url, available)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    name,
                    category,
                    description,
                    price,
                    image_url,
                    available,
                ),
            )


def delete_product(product_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM products WHERE id = %s",
            (product_id,),
        )


def create_order(
    customer_name,
    phone,
    address,
    notes,
    branch_name,
    cart_items,
    delivery_fee,
):
    """حفظ الطلب وجميع أصنافه داخل معاملة واحدة."""
    with get_connection() as conn:
        subtotal = sum(
            float(item["price"]) * int(item["quantity"])
            for item in cart_items
        )
        total = subtotal + float(delivery_fee)

        order = conn.execute(
            """
            INSERT INTO orders (
                customer_name, phone, address, notes, branch_name,
                subtotal, delivery_fee, total, status
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (
                customer_name,
                phone,
                address,
                notes,
                branch_name,
                subtotal,
                delivery_fee,
                total,
                "جديد",
            ),
        ).fetchone()

        order_id = order["id"]

        for item in cart_items:
            conn.execute(
                """
                INSERT INTO order_items (
                    order_id, product_id, product_name,
                    unit_price, quantity, line_total
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    order_id,
                    item["id"],
                    item["name"],
                    item["price"],
                    item["quantity"],
                    float(item["price"]) * int(item["quantity"]),
                ),
            )

    return order_id, subtotal, total


def get_orders(limit=500):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT *
            FROM orders
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,),
        ).fetchall()


def get_order_items(order_id):
    with get_connection() as conn:
        return conn.execute(
            """
            SELECT *
            FROM order_items
            WHERE order_id = %s
            ORDER BY id
            """,
            (order_id,),
        ).fetchall()


def update_order_status(order_id, status):
    allowed_statuses = [
        "جديد",
        "قيد التجهيز",
        "خرج للتوصيل",
        "مكتمل",
        "ملغي",
    ]

    if status not in allowed_statuses:
        raise ValueError("حالة الطلب غير صالحة.")

    with get_connection() as conn:
        conn.execute(
            "UPDATE orders SET status = %s WHERE id = %s",
            (status, order_id),
        )
