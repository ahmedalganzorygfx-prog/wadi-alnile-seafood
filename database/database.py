import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "restaurant.db"


def get_connection():
    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_connection()
    cursor = connection.cursor()

    # المستخدمون
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE,
            email TEXT,
            password_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # التصنيفات
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
        """
    )

    # المنتجات
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            image TEXT,
            available INTEGER DEFAULT 1,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
        """
    )

    # الفروع
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS branches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            address TEXT,
            phone TEXT
        )
        """
    )

    # جدول الطلبات
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            order_type TEXT NOT NULL,
            branch_name TEXT,
            address TEXT,
            notes TEXT,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'قيد المراجعة',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # جدول تفاصيل الطلب
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id)
        )
        """
    )

    connection.commit()

    # تعبئة التصنيفات الأساسية
    categories = [
        "الأسماك",
        "الجمبري",
        "السي فود",
        "الأرز",
        "السلطات",
        "الشوربة",
        "المشروبات",
        "الحلويات",
    ]

    for category in categories:
        cursor.execute(
            """
            INSERT OR IGNORE INTO categories (name)
            VALUES (?)
            """,
            (category,)
        )
    connection.commit()

    # تعبئة الفروع التجريبية
    branches = [
        ("فرع الدقي", "شارع مصدق، الجيزة", "01000000001"),
        ("فرع الهرم", "استوديو الأهرام، الجيزة", "01000000002"),
        ("فرع مدينة نصر", "شارع مكرم عبيد، القاهرة", "01000000003"),
    ]
    for b_name, b_addr, b_phone in branches:
        cursor.execute(
            """
            INSERT OR IGNORE INTO branches (name, address, phone)
            VALUES (?, ?, ?)
            """,
            (b_name, b_addr, b_phone)
        )
    connection.commit()

    # تعبئة منتجات تجريبية إذا كان الجدول فارغاً
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        seed_products()


def seed_products():
    connection = get_connection()
    cursor = connection.cursor()

    products = [
        ("الأسماك", "دنيس مشوي", "سمك دنيس طازج مشوي بتتبيلة خاصة", 280),
        ("الأسماك", "قاروص مشوي", "قاروص طازج مشوي على الطريقة المصرية", 320),
        ("الجمبري", "جمبري مشوي", "جمبري طازج مشوي بتتبيلة وادي النيل", 350),
        ("الجمبري", "جمبري مقلي", "جمبري مقرمش بتتبيلة خاصة", 320),
        ("السي فود", "سي فود ميكس", "تشكيلة منوعة من المأكولات البحرية", 420),
        ("الأرز", "أرز صيادية", "أرز بالبصل وبهارات الأسماك الخاصة", 50),
        ("السلطات", "سلطة بلدي", "سلطة خضار طازجة بالليمون والكمون", 35),
        ("الشوربة", "شوربة سي فود", "شوربة كريمة بالمأكولات البحرية الطازجة", 120),
    ]

    for cat_name, p_name, desc, price in products:
        cursor.execute("SELECT id FROM categories WHERE name = ?", (cat_name,))
        cat_row = cursor.fetchone()
        if cat_row:
            cat_id = cat_row["id"]
            cursor.execute(
                """
                INSERT INTO products (category_id, name, description, price, available)
                VALUES (?, ?, ?, ?, 1)
                """,
                (cat_id, p_name, desc, price)
            )

    connection.commit()
