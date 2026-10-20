import sqlite3
from pathlib import Path


# =========================================================
# مسار قاعدة البيانات
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DB_PATH = BASE_DIR / "restaurant.db"


# =========================================================
# الاتصال بقاعدة البيانات
# =========================================================

def get_connection():

    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# =========================================================
# إنشاء قاعدة البيانات
# =========================================================

def init_database():

    connection = get_connection()

    cursor = connection.cursor()


    # =====================================================
    # USERS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            phone TEXT UNIQUE,

            email TEXT,

            password_hash TEXT,

            created_at
                TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


    # =====================================================
    # CATEGORIES
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL UNIQUE,

            description TEXT
        )
        """
    )


    # =====================================================
    # PRODUCTS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category_id INTEGER,

            name TEXT NOT NULL,

            description TEXT,

            price REAL DEFAULT 0,

            image TEXT,

            available INTEGER DEFAULT 1,

            created_at
                TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(category_id)
                REFERENCES categories(id)
        )
        """
    )


    # =====================================================
    # BRANCHES
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS branches (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            address TEXT,

            phone TEXT,

            latitude REAL,

            longitude REAL,

            opening_time TEXT,

            closing_time TEXT,

            active INTEGER DEFAULT 1
        )
        """
    )


    # =====================================================
    # ORDERS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            branch_id INTEGER,

            total REAL DEFAULT 0,

            status TEXT DEFAULT 'جديد',

            order_type TEXT,

            address TEXT,

            notes TEXT,

            created_at
                TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
                REFERENCES users(id),

            FOREIGN KEY(branch_id)
                REFERENCES branches(id)
        )
        """
    )


    # =====================================================
    # ORDER ITEMS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            order_id INTEGER,

            product_id INTEGER,

            quantity INTEGER DEFAULT 1,

            price REAL DEFAULT 0,

            FOREIGN KEY(order_id)
                REFERENCES orders(id),

            FOREIGN KEY(product_id)
                REFERENCES products(id)
        )
        """
    )


    # =====================================================
    # REVIEWS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            branch_id INTEGER,

            rating INTEGER,

            comment TEXT,

            created_at
                TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


    # =====================================================
    # COMPLAINTS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS complaints (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            branch_id INTEGER,

            subject TEXT,

            message TEXT,

            status TEXT
                DEFAULT 'قيد المراجعة',

            created_at
                TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


    # =====================================================
    # COUPONS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS coupons (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            code TEXT NOT NULL UNIQUE,

            discount_type TEXT DEFAULT 'percentage',

            discount_value REAL DEFAULT 0,

            active INTEGER DEFAULT 1,

            expires_at TEXT
        )
        """
    )


    # =====================================================
    # FAVORITES
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            product_id INTEGER,

            created_at
                TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(user_id, product_id)
        )
        """
    )


    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            title TEXT,

            message TEXT,

            is_read INTEGER DEFAULT 0,

            created_at
                TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


    # =====================================================
    # التصنيفات الأساسية
    # =====================================================

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
            INSERT OR IGNORE INTO categories
            (name)

            VALUES (?)
            """,
            (category,)
        )


    connection.commit()

    connection.close()


    # =====================================================
    # البيانات التجريبية
    # =====================================================

    seed_products()
    seed_branches()


# =========================================================
# المنتجات التجريبية
# =========================================================

def seed_products():

    connection = get_connection()

    cursor = connection.cursor()


    products = [

        (
            "الأسماك",
            "دنيس مشوي",
            "سمك دنيس طازج مشوي بتتبيلة خاصة",
            280
        ),

        (
            "الأسماك",
            "قاروص مشوي",
            "قاروص طازج مشوي على الطريقة المصرية",
            320
        ),

        (
            "الجمبري",
            "جمبري مشوي",
            "جمبري طازج مشوي بتتبيلة وادي النيل",
            350
        ),

        (
            "الجمبري",
            "جمبري مقلي",
            "جمبري مقرمش بتتبيلة خاصة",
            320
        ),

        (
            "السي فود",
            "سي فود ميكس",
            "تشكيلة منوعة من المأكولات البحرية",
            420
        ),

        (
            "الأرز",
            "أرز صيادية",
            "أرز صيادية مصري مميز",
            70
        ),

        (
            "السلطات",
            "سلطة خضراء",
            "تشكيلة خضروات طازجة",
            50
        ),

        (
            "الشوربة",
            "شوربة سي فود",
            "شوربة مميزة بالمأكولات البحرية",
            100
        ),

        (
            "المشروبات",
            "بيبسي",
            "مشروب غازي",
            30
        ),

        (
            "المشروبات",
            "مياه معدنية",
            "مياه معدنية",
            15
        ),

    ]


    for category_name, name, description, price in products:

        category = cursor.execute(
            """
            SELECT id
            FROM categories
            WHERE name = ?
            """,
            (category_name,)
        ).fetchone()


        if not category:
            continue


        exists = cursor.execute(
            """
            SELECT id
            FROM products
            WHERE name = ?
            """,
            (name,)
        ).fetchone()


        if not exists:

            cursor.execute(
                """
                INSERT INTO products
                (
                    category_id,
                    name,
                    description,
                    price,
                    available
                )

                VALUES (?, ?, ?, ?, 1)
                """,
                (
                    category["id"],
                    name,
                    description,
                    price,
                )
            )


    connection.commit()

    connection.close()


# =========================================================
# الفروع التجريبية
# =========================================================

def seed_branches():

    connection = get_connection()

    cursor = connection.cursor()


    branches = [

        (
            "فرع وادي النيل",
            "القاهرة",
            "19974"
        ),

        (
            "فرع الجيزة",
            "الجيزة",
            "19974"
        ),

        (
            "فرع أكتوبر",
            "مدينة 6 أكتوبر",
            "19974"
        ),

    ]


    for name, address, phone in branches:

        exists = cursor.execute(
            """
            SELECT id

            FROM branches

            WHERE name = ?
            """,
            (name,)
        ).fetchone()


        if not exists:

            cursor.execute(
                """
                INSERT INTO branches
                (
                    name,
                    address,
                    phone,
                    active
                )

                VALUES (?, ?, ?, 1)
                """,
                (
                    name,
                    address,
                    phone,
                )
            )


    connection.commit()

    connection.close()
