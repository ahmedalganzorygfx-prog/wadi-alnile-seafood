
# -*- coding: utf-8 -*-
"""
موقع مطاعم أسماك وادي النيل
Python + Streamlit + SQLite

التشغيل:
    pip install -r requirements.txt
    streamlit run app.py
"""

import os
import json
import sqlite3
from datetime import datetime
from urllib.parse import quote

import streamlit as st


# =========================================================
# 1. إعدادات الموقع
# =========================================================

st.set_page_config(
    page_title="أسماك وادي النيل | طلبات أونلاين",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "wadi_nile.db")

HOTLINE = "01103949998"
WHATSAPP_NUMBER = "201103949998"

CATEGORIES = [
    "المقبلات الساخنة",
    "شوربات",
    "ارز وادي النيل الخاص",
    "اطباق وادي النيل الخاصة",
    "فخارات",
    "الساندوتشات",
    "مشروبات",
]

BRANCHES = {
    "فرع المهندسين": "82 شارع وادي النيل، الجيزة.",
    "فرع التجمع الخامس": "الحي الثالث، بجوار مول عنابة، القاهرة الجديدة.",
    "فرع السادس من أكتوبر": "محور 26 يوليو، بجوار محطة بنزين شيل أوت.",
}

SEED_PRODUCTS = [
    (1, "بطاطا ودجز", "المقبلات الساخنة", 35,
     "شرائح بطاطس مقرمشة ومتبلة بالأعشاب الطبيعية.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Potato+Wedges", 1),

    (2, "أصابع الموزاريلا", "المقبلات الساخنة", 45,
     "أصابع جبن موزاريلا غنية ومقرمشة.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Mozzarella", 1),

    (3, "سمبوسة سي فود", "المقبلات الساخنة", 40,
     "رقائق هشة محشوة بخلطة السي فود والبهارات الخاصة.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Samosa", 1),

    (4, "كبة مقلية", "المقبلات الساخنة", 45,
     "قشرة برغل مقرمشة محشوة باللحم المفروم والبهارات.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Kibbeh", 1),

    (5, "شوربة سي فود مخلية ملكية", "شوربات", 65,
     "تشكيلة من الجمبري والسبيط والصدف بمرق الكريمة.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Soup", 1),

    (6, "شوربة صافي صريح", "شوربات", 45,
     "مرق السمك الصافي المبهر بالتوابل المصرية والكزبرة.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Fish+Soup", 1),

    (7, "أرز وادي النيل بالجمبري المدفون",
     "ارز وادي النيل الخاص", 65,
     "أرز صيادية مصري مبهر ومغطى بالجمبري.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Shrimp+Rice", 1),

    (8, "أرز صيادية سي فود", "ارز وادي النيل الخاص", 50,
     "أرز صيادية بالبصل المكرمل وقطع الفيليه.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Sayadeya+Rice", 1),

    (9, "وجبة ميكس جريل بحري فاخرة",
     "اطباق وادي النيل الخاصة", 210,
     "فيليه سمك مشوي وجمبري وسبيط مع الأرز والسلطات.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Mix+Grill", 1),

    (10, "صينية وادي النيل الملكية الكبرى",
     "اطباق وادي النيل الخاصة", 450,
     "تشكيلة عائلية من السمك والجمبري والسبيط والكابوريا والأرز.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Royal+Seafood+Tray", 1),

    (11, "طاجن سي فود صوص أبيض وكريمة", "فخارات", 130,
     "سي فود مطهو بالكريمة والجبن في الفرن الفخاري.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Casserole", 1),

    (12, "طاجن جمبري بالصلصة الحمراء", "فخارات", 120,
     "جمبري بصلصة الطماطم والثوم والبصل في الفرن الفخاري.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Shrimp+Casserole", 1),

    (13, "ساندويتش جمبري مقرمش", "الساندوتشات", 55,
     "جمبري مقلي مع صوص الطحينة في خبز طازج.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Crispy+Shrimp+Sandwich", 1),

    (14, "ساندويتش فياجرا وادي النيل", "الساندوتشات", 85,
     "خلطة من السي فود والجمبري والسبيط والبطارخ.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Sandwich", 1),

    (15, "عصير ليمون نعناع طازج", "مشروبات", 25,
     "عصير ليمون طبيعي منعش مع أوراق النعناع.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Lemon+Mint", 1),

    (16, "مشروبات غازية", "مشروبات", 15,
     "اختيارك من المشروبات الغازية الباردة.",
     "https://placehold.co/600x400/f1f5f9/1e293b?text=Soft+Drinks", 1),
]


# =========================================================
# 2. قاعدة البيانات
# =========================================================

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT DEFAULT '',
                image_url TEXT DEFAULT '',
                active INTEGER DEFAULT 1
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                branch TEXT NOT NULL,
                items_json TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT DEFAULT 'جديد'
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM products"
        ).fetchone()[0]

        if count == 0:
            conn.executemany(
                """
                INSERT INTO products
                (id, name, category, price, description, image_url, active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                SEED_PRODUCTS,
            )

        conn.commit()


def get_products(include_inactive=False):
    with get_conn() as conn:
        if include_inactive:
            sql = "SELECT * FROM products ORDER BY category, name"
        else:
            sql = (
                "SELECT * FROM products WHERE active=1 "
                "ORDER BY category, name"
            )

        return [
            dict(row)
            for row in conn.execute(sql).fetchall()
        ]


def money(value):
    return f"{float(value):,.2f} ج.م"


def get_admin_password():
    """قراءة كلمة المرور من Streamlit Secrets أو متغير البيئة."""
    try:
        password = st.secrets.get("ADMIN_PASSWORD", "")
    except Exception:
        password = ""

    if not password:
        password = os.environ.get("WADI_ADMIN_PASSWORD", "")

    # للتشغيل المحلي فقط. يجب ضبط كلمة مرور آمنة قبل النشر.
    if not password:
        password = "admin123"

    return str(password)


# =========================================================
# 3. تنسيقات CSS
# =========================================================

def inject_css():
    st.markdown("""
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap'
    );

    html, body, [class*="css"],
    [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
    }

    .stApp {
        background: #f8fafc;
        direction: rtl;
    }

    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
    }

    .topbar {
        background: #172554;
        color: #cffafe;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 14px;
        font-size: 14px;
        text-align: center;
    }

    .brand {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 18px 22px;
        box-shadow: 0 4px 16px #0f172a0c;
        margin-bottom: 16px;
    }

    .brand h1 {
        color: #1e3a8a;
        font-size: 30px;
        font-weight: 900;
        margin: 0;
    }

    .brand p {
        color: #64748b;
        margin: 0;
        font-size: 14px;
    }

    .hero {
        background: linear-gradient(
            100deg, #172554, #1e3a8a, #164e63
        );
        color: white;
        text-align: center;
        padding: 32px 14px;
        border-radius: 20px;
        margin: 12px 0 22px;
    }

    .hero h2 {
        font-size: 30px;
        font-weight: 900;
        margin: 0 0 8px;
    }

    .hero p {
        color: #a5f3fc;
        margin: 0;
    }

    .price-pill {
        display: inline-block;
        background: #172554;
        color: #fde68a;
        padding: 5px 10px;
        border-radius: 8px;
        font-weight: 900;
        margin-top: 8px;
    }

    .product-name {
        font-weight: 900;
        color: #1e3a8a;
        font-size: 18px;
        margin: 8px 0 2px;
    }

    .product-desc {
        color: #64748b;
        font-size: 13px;
        min-height: 42px;
        margin-bottom: 8px;
    }

    .section-title {
        font-weight: 900;
        color: #1e3a8a;
        font-size: 22px;
        margin: 12px 0;
        text-align: right;
    }

    div.stButton > button {
        border-radius: 11px;
        font-family: 'Cairo', sans-serif;
        font-weight: 800;
    }

    div.stButton > button[kind="primary"] {
        background: #172554;
        border-color: #172554;
        color: #fde68a;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 12px;
        border-radius: 14px;
    }

    footer {
        visibility: hidden;
    }

    @media (max-width: 768px) {
        .brand h1 {
            font-size: 24px;
        }

        .hero h2 {
            font-size: 23px;
        }
    }
    </style>
    """, unsafe_allow_html=True)


# =========================================================
# 4. تسجيل الطلبات
# =========================================================

def save_order(name, phone, address, branch, cart, total):
    items = []

    for product, quantity in cart.values():
        items.append({
            "id": product["id"],
            "name": product["name"],
            "price": float(product["price"]),
            "qty": int(quantity),
            "subtotal": float(product["price"]) * int(quantity),
        })

    with get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO orders (
                created_at, customer_name, phone, address,
                branch, items_json, total
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            phone,
            address,
            branch,
            json.dumps(items, ensure_ascii=False),
            float(total),
        ))

        conn.commit()
        return cursor.lastrowid, items


# =========================================================
# 5. لوحة الإدارة
# =========================================================

def admin_page():
    st.markdown(
        '<div class="section-title">⚙️ لوحة إدارة الموقع</div>',
        unsafe_allow_html=True,
    )

    password = st.text_input(
        "كلمة مرور الإدارة",
        type="password",
        key="admin_password",
    )

    if password != get_admin_password():
        st.info("أدخل كلمة مرور الإدارة لفتح لوحة التحكم.")
        st.caption(
            "للتشغيل المحلي الأولي فقط، كلمة المرور الافتراضية "
            "هي admin123. غيّرها قبل نشر الموقع."
        )
        return

    tab_products, tab_orders, tab_settings = st.tabs([
        "إدارة المنتجات",
        "الطلبات",
        "إعدادات الإدارة",
    ])

    # إدارة المنتجات
    with tab_products:
        products = get_products(include_inactive=True)

        if products:
            st.dataframe(
                [
                    {
                        "رقم": p["id"],
                        "اسم المنتج": p["name"],
                        "القسم": p["category"],
                        "السعر": p["price"],
                        "متاح": "نعم" if p["active"] else "لا",
                    }
                    for p in products
                ],
                use_container_width=True,
                hide_index=True,
            )

            selected_id = st.selectbox(
                "اختر منتجًا للتعديل",
                [p["id"] for p in products],
                format_func=lambda product_id: next(
                    f'{p["name"]} (#{p["id"]})'
                    for p in products
                    if p["id"] == product_id
                ),
            )

            product = next(
                p for p in products if p["id"] == selected_id
            )

            with st.form("edit_product_form"):
                name = st.text_input(
                    "اسم المنتج",
                    value=product["name"],
                )

                category = st.selectbox(
                    "القسم",
                    CATEGORIES,
                    index=(
                        CATEGORIES.index(product["category"])
                        if product["category"] in CATEGORIES
                        else 0
                    ),
                )

                price = st.number_input(
                    "السعر بالجنيه",
                    min_value=0.0,
                    value=float(product["price"]),
                    step=5.0,
                )

                description = st.text_area(
                    "الوصف",
                    value=product["description"],
                )

                image_url = st.text_input(
                    "رابط الصورة",
                    value=product["image_url"],
                )

                active = st.checkbox(
                    "المنتج متاح للبيع",
                    value=bool(product["active"]),
                )

                submitted = st.form_submit_button(
                    "حفظ التعديلات",
                    use_container_width=True,
                )

                if submitted:
                    if not name.strip():
                        st.error("اكتب اسم المنتج.")
                    else:
                        with get_conn() as conn:
                            conn.execute("""
                                UPDATE products
                                SET name=?, category=?, price=?,
                                    description=?, image_url=?, active=?
                                WHERE id=?
                            """, (
                                name.strip(),
                                category,
                                price,
                                description.strip(),
                                image_url.strip(),
                                int(active),
                                selected_id,
                            ))
                            conn.commit()

                        st.success("تم حفظ تعديلات المنتج.")
                        st.rerun()
        else:
            st.info("لا توجد منتجات مسجلة.")

    # متابعة الطلبات
    with tab_orders:
        with get_conn() as conn:
            orders = [
                dict(row)
                for row in conn.execute(
                    "SELECT * FROM orders ORDER BY id DESC LIMIT 500"
                ).fetchall()
            ]

        if not orders:
            st.info("لا توجد طلبات مسجلة حتى الآن.")
        else:
            st.dataframe(
                [
                    {
                        "رقم الطلب": order["id"],
                        "التاريخ": order["created_at"],
                        "العميل": order["customer_name"],
                        "الهاتف": order["phone"],
                        "الفرع": order["branch"],
                        "الإجمالي": order["total"],
                        "الحالة": order["status"],
                    }
                    for order in orders
                ],
                use_container_width=True,
                hide_index=True,
            )

            order_id = st.selectbox(
                "اختر طلبًا لعرض التفاصيل",
                [order["id"] for order in orders],
            )

            chosen = next(
                order for order in orders if order["id"] == order_id
            )

            st.write(f'**اسم العميل:** {chosen["customer_name"]}')
            st.write(f'**الهاتف:** {chosen["phone"]}')
            st.write(f'**العنوان:** {chosen["address"]}')
            st.write(f'**الفرع:** {chosen["branch"]}')

            st.markdown("#### الأصناف المطلوبة")
            st.json(json.loads(chosen["items_json"]))

            statuses = [
                "جديد",
                "جارٍ التجهيز",
                "خرج للتوصيل",
                "تم التسليم",
                "ملغي",
            ]

            current_status = (
                chosen["status"]
                if chosen["status"] in statuses
                else "جديد"
            )

            status = st.selectbox(
                "تحديث حالة الطلب",
                statuses,
                index=statuses.index(current_status),
            )

            if st.button("حفظ حالة الطلب"):
                with get_conn() as conn:
                    conn.execute(
                        "UPDATE orders SET status=? WHERE id=?",
                        (status, order_id),
                    )
                    conn.commit()

                st.success("تم تحديث حالة الطلب.")
                st.rerun()

    # إعدادات الإدارة وإضافة المنتجات
    with tab_settings:
        st.write(
            "يمكن تغيير كلمة المرور باستخدام Streamlit Secrets "
            "أو متغير البيئة WADI_ADMIN_PASSWORD."
        )

        st.warning(
            "لا تستخدم كلمة المرور الافتراضية عند نشر الموقع."
        )

        st.markdown("#### إضافة منتج جديد")

        with st.form("add_product_form"):
            new_name = st.text_input("اسم المنتج الجديد")

            new_category = st.selectbox(
                "القسم",
                CATEGORIES,
                key="new_category",
            )

            new_price = st.number_input(
                "السعر بالجنيه",
                min_value=0.0,
                step=5.0,
                key="new_price",
            )

            new_description = st.text_area(
                "وصف المنتج",
                key="new_description",
            )

            new_image = st.text_input(
                "رابط الصورة",
                value="https://placehold.co/600x400/f1f5f9/1e293b?text=New+Product",
                key="new_image",
            )

            add_product = st.form_submit_button(
                "إضافة المنتج",
                use_container_width=True,
            )

            if add_product:
                if not new_name.strip():
                    st.error("اكتب اسم المنتج.")
                else:
                    with get_conn() as conn:
                        next_id = conn.execute(
                            "SELECT COALESCE(MAX(id), 0) + 1 FROM products"
                        ).fetchone()[0]

                        conn.execute("""
                            INSERT INTO products (
                                id, name, category, price,
                                description, image_url, active
                            )
                            VALUES (?, ?, ?, ?, ?, ?, 1)
                        """, (
                            next_id,
                            new_name.strip(),
                            new_category,
                            new_price,
                            new_description.strip(),
                            new_image.strip(),
                        ))

                        conn.commit()

                    st.success("تمت إضافة المنتج بنجاح.")
                    st.rerun()


# =========================================================
# 6. سلة المشتريات
# =========================================================

def render_cart():
    st.markdown("## 🛒 سلة طلباتك")

    cart = st.session_state.cart

    if not cart:
        st.caption("السلة فارغة حاليًا.")
    else:
        for product_id in list(cart.keys()):
            product, quantity = cart[product_id]

            st.markdown(f"**{product['name']}**")

            col_minus, col_qty, col_plus, col_remove = st.columns(
                [1, 1, 1, 1]
            )

            if col_minus.button(
                "−",
                key=f"minus_{product_id}",
                use_container_width=True,
            ):
                if quantity <= 1:
                    del st.session_state.cart[product_id]
                else:
                    st.session_state.cart[product_id] = (
                        product,
                        quantity - 1,
                    )
                st.rerun()

            col_qty.write(f"× {quantity}")

            if col_plus.button(
                "+",
                key=f"plus_{product_id}",
                use_container_width=True,
            ):
                st.session_state.cart[product_id] = (
                    product,
                    quantity + 1,
                )
                st.rerun()

            if col_remove.button(
                "✖",
                key=f"remove_{product_id}",
                use_container_width=True,
            ):
                del st.session_state.cart[product_id]
                st.rerun()

            st.caption(money(product["price"] * quantity))
            st.divider()

    total = sum(
        float(product["price"]) * quantity
        for product, quantity in cart.values()
    )

    st.markdown(f"### الإجمالي: {money(total)}")

    with st.form("checkout_form"):
        customer_name = st.text_input("الاسم الكريم")
        customer_phone = st.text_input("رقم الهاتف")
        customer_address = st.text_area(
            "عنوان التوصيل بالتفصيل",
            height=80,
        )

        branch = st.selectbox(
            "فرع الاستلام / التوصيل",
            list(BRANCHES.keys()),
        )

        submitted = st.form_submit_button(
            "تأكيد الطلب عبر واتساب",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            if not cart:
                st.error("أضف صنفًا واحدًا على الأقل إلى السلة.")

            elif (
                not customer_name.strip()
                or not customer_phone.strip()
                or not customer_address.strip()
            ):
                st.error("يرجى استكمال الاسم ورقم الهاتف والعنوان.")

            else:
                order_id, items = save_order(
                    customer_name.strip(),
                    customer_phone.strip(),
                    customer_address.strip(),
                    branch,
                    cart,
                    total,
                )

                lines = [
                    "طلب جديد من موقع أسماك وادي النيل",
                    f"رقم الطلب: {order_id}",
                    f"الاسم: {customer_name.strip()}",
                    f"الهاتف: {customer_phone.strip()}",
                    f"العنوان: {customer_address.strip()}",
                    f"الفرع: {branch}",
                    "",
                    "الأصناف المطلوبة:",
                ]

                for item in items:
                    lines.append(
                        f"- {item['name']} × {item['qty']} "
                        f"= {item['subtotal']:.2f} ج.م"
                    )

                lines.append(
                    f"الإجمالي الكلي: {total:.2f} ج.م"
                )

                whatsapp_url = (
                    f"https://wa.me/{WHATSAPP_NUMBER}"
                    f"?text={quote(chr(10).join(lines))}"
                )

                # حفظ الطلب وإظهار رابط واتساب قبل إعادة التشغيل.
                st.session_state.cart = {}

                st.success(
                    f"تم تسجيل الطلب رقم {order_id} في قاعدة البيانات."
                )

                st.markdown(
                    "اضغط الزر التالي لفتح واتساب وإرسال تفاصيل الطلب."
                )

                st.link_button(
                    "📲 فتح واتساب وإرسال الطلب",
                    whatsapp_url,
                    use_container_width=True,
                )


# =========================================================
# 7. عرض المنتجات والبحث والأقسام
# =========================================================

def render_products():
    search = st.text_input(
        "🔎 ابحث عن منتج أو وجبة...",
        placeholder="اكتب اسم الوجبة أو جزءًا منه",
    )

    category_options = ["الكل"] + CATEGORIES
    category_cols = st.columns(4)

    for index, category in enumerate(category_options):
        with category_cols[index % 4]:
            if st.button(
                category,
                key=f"category_{index}",
                type=(
                    "primary"
                    if st.session_state.category == category
                    else "secondary"
                ),
                use_container_width=True,
            ):
                st.session_state.category = category
                st.rerun()

    products = get_products()

    if search.strip():
        query = search.strip().casefold()

        products = [
            product for product in products
            if query in product["name"].casefold()
            or query in product["description"].casefold()
            or query in product["category"].casefold()
        ]
    elif st.session_state.category != "الكل":
        products = [
            product for product in products
            if product["category"] == st.session_state.category
        ]

    title = (
        st.session_state.category
        if st.session_state.category != "الكل"
        else "كل المنتجات"
    )

    st.markdown(
        f'<div class="section-title">{title} '
        f'<span style="font-size:13px;color:#64748b">'
        f'({len(products)} منتج)</span></div>',
        unsafe_allow_html=True,
    )

    if not products:
        st.info("لم يتم العثور على منتجات مطابقة للبحث.")
        return

    columns_per_row = 3

    for start in range(0, len(products), columns_per_row):
        columns = st.columns(columns_per_row, gap="medium")

        for column, product in zip(
            columns,
            products[start:start + columns_per_row],
        ):
            with column:
                with st.container(border=True):
                    if product["image_url"]:
                        st.image(
                            product["image_url"],
                            use_container_width=True,
                        )

                    st.markdown(
                        f'<div class="price-pill">'
                        f'{money(product["price"])}</div>'
                        f'<div class="product-name">'
                        f'{product["name"]}</div>'
                        f'<div class="product-desc">'
                        f'{product["description"]}</div>',
                        unsafe_allow_html=True,
                    )

                    if st.button(
                        "➕ إضافة إلى السلة",
                        key=f"add_{product['id']}",
                        use_container_width=True,
                    ):
                        product_id = str(product["id"])

                        if product_id in st.session_state.cart:
                            old_product, quantity = (
                                st.session_state.cart[product_id]
                            )

                            st.session_state.cart[product_id] = (
                                old_product,
                                quantity + 1,
                            )
                        else:
                            st.session_state.cart[product_id] = (
                                product,
                                1,
                            )

                        st.toast(
                            f"تمت إضافة {product['name']} إلى السلة"
                        )
                        st.rerun()


# =========================================================
# 8. الفروع والتذييل
# =========================================================

def render_branches():
    st.markdown("---")

    st.markdown(
        '<div class="section-title" style="text-align:center">'
        '📍 فروع سلسلة مطاعم وادي النيل</div>',
        unsafe_allow_html=True,
    )

    columns = st.columns(3)

    for column, (name, address) in zip(columns, BRANCHES.items()):
        with column:
            st.markdown(f"""
            <div style="
                background:#172554;
                color:white;
                border:1px solid #1e40af;
                padding:20px;
                border-radius:16px;
                min-height:130px;
                margin-bottom:12px;
            ">
                <div style="
                    font-weight:900;
                    color:#a5f3fc;
                    font-size:18px;
                ">{name}</div>
                <div style="
                    color:#cbd5e1;
                    margin-top:8px;
                ">{address}</div>
            </div>
            """, unsafe_allow_html=True)


def render_footer():
    st.markdown(f"""
    <div style="
        background:#020617;
        color:#cbd5e1;
        text-align:center;
        padding:18px;
        border-radius:12px;
        margin-top:24px;
    ">
        مطاعم أسماك وادي النيل © 2026 جميع الحقوق محفوظة
        <br>
        الخط الساخن:
        <b style="color:#67e8f9">{HOTLINE}</b>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# 9. تشغيل الموقع
# =========================================================

def main():
    init_db()
    inject_css()

    if "cart" not in st.session_state:
        st.session_state.cart = {}

    if "category" not in st.session_state:
        st.session_state.category = "الكل"

    # الشريط العلوي
    st.markdown(f"""
    <div class="topbar">
        📞 الخط الساخن الموحد:
        <b style="color:#fbbf24">{HOTLINE}</b>
        | خدمة الطلبات والتوصيل طوال أيام الأسبوع
    </div>
    """, unsafe_allow_html=True)

    # شعار واسم المطعم
    st.markdown("""
    <div class="brand">
        <div style="
            display:flex;
            align-items:center;
            justify-content:center;
            gap:14px;
            flex-wrap:wrap;
            text-align:center;
        ">
            <div style="font-size:46px">🐟</div>
            <div>
                <h1>أسماك وادي النيل</h1>
                <p>سلسلة مطاعم المأكولات البحرية</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # الواجهة الرئيسية
    st.markdown("""
    <div class="hero">
        <h2>أشهى المأكولات البحرية في مصر 🦐</h2>
        <p>
            صواني مميزة، طواجن فخار،
            وألذ الساندوتشات والشوربات البحرية
        </p>
    </div>
    """, unsafe_allow_html=True)

    # السلة في القائمة الجانبية
    with st.sidebar:
        render_cart()

    # المنتجات والبحث
    render_products()

    # الفروع
    render_branches()

    # لوحة الإدارة
    with st.expander("⚙️ إدارة الموقع"):
        admin_page()

    # التذييل
    render_footer()


if __name__ == "__main__":
    main()
