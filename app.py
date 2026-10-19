# -*- coding: utf-8 -*-
"""
موقع مطاعم أسماك وادي النيل - نسخة Python / Streamlit
التشغيل:
    pip install -r requirements.txt
    streamlit run app.py

ملاحظة: المنتجات والأسعار والصور الأولية تجريبية مأخوذة من نموذج HTML المرفق.
يمكن تعديلها من لوحة الإدارة داخل التطبيق.
"""
import streamlit as st
import sqlite3
import json
import os
from urllib.parse import quote
from datetime import datetime

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "wadi_nile.db")
HOTLINE = "01103949998"
WHATSAPP_NUMBER = "201103949998"

CATEGORIES = [
    "المقبلات الساخنة", "شوربات", "ارز وادي النيل الخاص",
    "اطباق وادي النيل الخاصة", "فخارات", "الساندوتشات", "مشروبات"
]
BRANCHES = {
    "فرع المهندسين": "82 شارع وادي النيل، الجيزة.",
    "فرع التجمع الخامس": "الحي الثالث، بجوار مول عنابة، القاهرة الجديدة.",
    "فرع السادس من أكتوبر": "محور 26 يوليو، بجوار محطة بنزين شيل أوت."
}
SEED_PRODUCTS = [
    (1, "بطاطا ودجز", "المقبلات الساخنة", 35, "شرائح بطاطس مقرمشة ومتبلة بالأعشاب الطبيعية.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Potato+Wedges", 1),
    (2, "أصابع الموزاريلا", "المقبلات الساخنة", 45, "أصابع جبن موزاريلا غنية ومقرمشة.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Mozzarella", 1),
    (3, "سمبوسة سي فود", "المقبلات الساخنة", 40, "رقائق هشة محشوة بخلطة السي فود والبهارات الخاصة.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Samosa", 1),
    (4, "كبة مقلية", "المقبلات الساخنة", 45, "قشرة برغل مقرمشة محشوة باللحم المفروم والبهارات.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Kibbeh", 1),
    (5, "شوربة سي فود مخلية ملكية", "شوربات", 65, "تشكيلة من الجمبري والسبيط والصدف بمرق الكريمة.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Soup", 1),
    (6, "شوربة صافي صريح", "شوربات", 45, "مرق السمك الصافي المبهر بالتوابل المصرية والكزبرة.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Fish+Soup", 1),
    (7, "أرز وادي النيل بالجمبري المدفون", "ارز وادي النيل الخاص", 65, "أرز صيادية مصري مبهر ومغطى بالجمبري.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Shrimp+Rice", 1),
    (8, "أرز صيادية سي فود", "ارز وادي النيل الخاص", 50, "أرز صيادية بالبصل المكرمل وقطع الفيليه.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Sayadeya+Rice", 1),
    (9, "وجبة ميكس جريل بحري فاخرة", "اطباق وادي النيل الخاصة", 210, "فيليه سمك مشوي وجمبري وسبيط مع الأرز والسلطات.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Mix+Grill", 1),
    (10, "صينية وادي النيل الملكية الكبرى", "اطباق وادي النيل الخاصة", 450, "تشكيلة عائلية من السمك والجمبري والسبيط والكابوريا والأرز.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Royal+Seafood+Tray", 1),
    (11, "طاجن سي فود صوص أبيض وكريمة", "فخارات", 130, "سي فود مطهو بالكريمة والجبن في الفرن الفخاري.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Casserole", 1),
    (12, "طاجن جمبري بالصلصة الحمراء", "فخارات", 120, "جمبري بصلصة الطماطم والثوم والبصل في الفرن الفخاري.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Shrimp+Casserole", 1),
    (13, "ساندويتش جمبري مقرمش", "الساندوتشات", 55, "جمبري مقلي مع صوص الطحينة في خبز طازج.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Crispy+Shrimp+Sandwich", 1),
    (14, "ساندويتش فياجرا وادي النيل", "الساندوتشات", 85, "خلطة من السي فود والجمبري والسبيط والبطارخ.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Seafood+Sandwich", 1),
    (15, "عصير ليمون نعناع طازج", "مشروبات", 25, "عصير ليمون طبيعي منعش مع أوراق النعناع.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Lemon+Mint", 1),
    (16, "مشروبات غازية", "مشروبات", 15, "اختيارك من المشروبات الغازية الباردة.", "https://placehold.co/600x400/f1f5f9/1e293b?text=Soft+Drinks", 1),
]

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL,
            price REAL NOT NULL, description TEXT DEFAULT '', image_url TEXT DEFAULT '',
            active INTEGER DEFAULT 1)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL,
            customer_name TEXT NOT NULL, phone TEXT NOT NULL, address TEXT NOT NULL,
            branch TEXT NOT NULL, items_json TEXT NOT NULL, total REAL NOT NULL,
            status TEXT DEFAULT 'جديد')""")
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", SEED_PRODUCTS)
        conn.commit()

def get_products(include_inactive=False):
    with get_conn() as conn:
        sql = "SELECT * FROM products" if include_inactive else "SELECT * FROM products WHERE active=1"
        return [dict(r) for r in conn.execute(sql + " ORDER BY category, name").fetchall()]

def money(value):
    return f"{value:,.2f} ج.م"

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Cairo', sans-serif;
    }
    .stApp { background: #f8fafc; direction: rtl; }
    [data-testid="stSidebar"] { direction: rtl; }
    .topbar {background:#172554;color:#cffafe;padding:9px 18px;border-radius:12px;margin-bottom:14px;font-size:14px}
    .brand {background:white;border:1px solid #e2e8f0;border-radius:18px;padding:18px 22px;box-shadow:0 4px 16px #0f172a0c;margin-bottom:16px}
    .brand h1 {color:#1e3a8a;font-size:28px;font-weight:900;margin:0}
    .brand p {color:#64748b;margin:0;font-size:13px}
    .hero {background:linear-gradient(100deg,#172554,#1e3a8a,#164e63);color:white;text-align:center;padding:30px 14px;border-radius:20px;margin:12px 0 20px}
    .hero h2 {font-size:30px;font-weight:900;margin:0 0 8px}
    .hero p {color:#a5f3fc;margin:0}
    .product-card {background:white;border:1px solid #e2e8f0;border-radius:17px;padding:12px;box-shadow:0 2px 8px #0f172a08;height:100%}
    .price-pill {display:inline-block;background:#172554;color:#fde68a;padding:5px 10px;border-radius:8px;font-weight:900}
    .product-name {font-weight:900;color:#1e3a8a;font-size:17px;margin:8px 0 2px}
    .product-desc {color:#64748b;font-size:12px;min-height:38px}
    .section-title {font-weight:900;color:#1e3a8a;font-size:22px}
    div.stButton > button {border-radius:11px;font-family:'Cairo',sans-serif;font-weight:800}
    div[data-testid="stMetric"] {background:white;border:1px solid #e2e8f0;padding:12px;border-radius:14px}
    footer {visibility:hidden}
    </style>
    """, unsafe_allow_html=True)

def save_order(name, phone, address, branch, cart, total):
    items = [{"id": p["id"], "name": p["name"], "price": p["price"], "qty": q,
              "subtotal": p["price"] * q} for p, q in cart.values()]
    with get_conn() as conn:
        cur = conn.execute("""INSERT INTO orders
        (created_at, customer_name, phone, address, branch, items_json, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, phone, address, branch,
         json.dumps(items, ensure_ascii=False), total))
        conn.commit()
        return cur.lastrowid, items

def admin_page():
    st.markdown('<div class="section-title">⚙️ لوحة إدارة الموقع</div>', unsafe_allow_html=True)
    password = st.text_input("كلمة مرور الإدارة", type="password", key="admin_password")
    if password != st.secrets.get("ADMIN_PASSWORD", os.environ.get("WADI_ADMIN_PASSWORD", "admin123")):
        st.info("أدخل كلمة مرور الإدارة. كلمة المرور الافتراضية عند التشغيل المحلي: admin123")
        return
    tab_products, tab_orders, tab_settings = st.tabs(["إدارة المنتجات", "الطلبات", "إضافة منتج"])
    with tab_products:
        products = get_products(include_inactive=True)
        if products:
            st.dataframe([{"رقم": p["id"], "اسم المنتج": p["name"], "القسم": p["category"],
                           "السعر": p["price"], "متاح": "نعم" if p["active"] else "لا"} for p in products],
                         use_container_width=True, hide_index=True)
            selected_id = st.selectbox("اختر منتجًا للتعديل", [p["id"] for p in products],
                                       format_func=lambda x: next(f'{p["name"]} (#{p["id"]})' for p in products if p["id"] == x))
            product = next(p for p in products if p["id"] == selected_id)
            with st.form("edit_product_form"):
                name = st.text_input("اسم المنتج", product["name"])
                category = st.selectbox("القسم", CATEGORIES, index=CATEGORIES.index(product["category"]) if product["category"] in CATEGORIES else 0)
                price = st.number_input("السعر بالجنيه", min_value=0.0, value=float(product["price"]), step=5.0)
                desc = st.text_area("الوصف", product["description"])
                img = st.text_input("رابط الصورة", product["image_url"])
                active = st.checkbox("المنتج متاح للبيع", value=bool(product["active"]))
                submitted = st.form_submit_button("حفظ التعديلات", use_container_width=True)
                if submitted:
                    with get_conn() as conn:
                        conn.execute("UPDATE products SET name=?, category=?, price=?, description=?, image_url=?, active=? WHERE id=?",
                                     (name.strip(), category, price, desc.strip(), img.strip(), int(active), selected_id))
                        conn.commit()
                    st.success("تم حفظ المنتج.")
                    st.rerun()
    with tab_orders:
        with get_conn() as conn:
            orders = [dict(r) for r in conn.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 500").fetchall()]
        if not orders:
            st.info("لا توجد طلبات مسجلة حتى الآن.")
        else:
            st.dataframe([{"رقم الطلب": o["id"], "التاريخ": o["created_at"], "العميل": o["customer_name"],
                           "الهاتف": o["phone"], "الفرع": o["branch"], "الإجمالي": o["total"], "الحالة": o["status"]} for o in orders],
                         use_container_width=True, hide_index=True)
            order_id = st.selectbox("تفاصيل الطلب", [o["id"] for o in orders])
            chosen = next(o for o in orders if o["id"] == order_id)
            st.write(f"**العنوان:** {chosen['address']}")
            st.json(json.loads(chosen["items_json"]))
            status = st.selectbox("تحديث حالة الطلب", ["جديد", "جارٍ التجهيز", "خرج للتوصيل", "تم التسليم", "ملغي"],
                                  index=["جديد", "جارٍ التجهيز", "خرج للتوصيل", "تم التسليم", "ملغي"].index(chosen["status"]) if chosen["status"] in ["جديد", "جارٍ التجهيز", "خرج للتوصيل", "تم التسليم", "ملغي"] else 0)
            if st.button("حفظ حالة الطلب"):
                with get_conn() as conn:
                    conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
                    conn.commit()
                st.success("تم تحديث الحالة.")
                st.rerun()
    with tab_settings:
        st.write("يمكن تغيير كلمة مرور الإدارة من متغير البيئة `WADI_ADMIN_PASSWORD` أو من إعدادات Streamlit Secrets باسم `ADMIN_PASSWORD`.")
        st.warning("غيّر كلمة المرور الافتراضية قبل نشر الموقع على الإنترنت.")
    with st.expander("إضافة منتج جديد"):
        with st.form("add_product_form"):
            new_name = st.text_input("اسم المنتج الجديد")
            new_cat = st.selectbox("القسم الجديد", CATEGORIES, key="new_cat")
            new_price = st.number_input("السعر", min_value=0.0, step=5.0, key="new_price")
            new_desc = st.text_area("وصف المنتج", key="new_desc")
            new_img = st.text_input("رابط صورة المنتج", "https://placehold.co/600x400/f1f5f9/1e293b?text=New+Product", key="new_img")
            add = st.form_submit_button("إضافة المنتج", use_container_width=True)
            if add:
                if not new_name.strip():
                    st.error("اكتب اسم المنتج.")
                else:
                    with get_conn() as conn:
                        next_id = conn.execute("SELECT COALESCE(MAX(id),0)+1 FROM products").fetchone()[0]
                        conn.execute("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, 1)",
                                     (next_id, new_name.strip(), new_cat, new_price, new_desc.strip(), new_img.strip()))
                        conn.commit()
                    st.success("تمت إضافة المنتج.")
                    st.rerun()

def main():
    st.set_page_config(page_title="أسماك وادي النيل | طلبات أونلاين", page_icon="🐟", layout="wide", initial_sidebar_state="collapsed")
    init_db()
    inject_css()
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "category" not in st.session_state:
        st.session_state.category = "الكل"

    st.markdown(f'<div class="topbar">📞 الخط الساخن الموحد: <b style="color:#fbbf24">{HOTLINE}</b>　 |　 خدمة الطلبات والتوصيل طوال أيام الأسبوع</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="brand">
      <div style="display:flex;align-items:center;gap:14px">
        <div style="font-size:42px">🐟</div>
        <div><h1>أسماك وادي النيل</h1><p>سلسلة مطاعم المأكولات البحرية</p></div>
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="hero">
      <h2>أشهى المأكولات البحرية في مصر 🦐</h2>
      <p>صواني مميزة، طواجن فخار، وألذ الساندوتشات والشوربات البحرية</p>
    </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("## 🛒 سلة طلباتك")
        cart = st.session_state.cart
        if not cart:
            st.caption("السلة فارغة حاليًا.")
        else:
            for pid in list(cart.keys()):
                item, qty = cart[pid]
                c1, c2, c3 = st.columns([4, 1, 1])
                c1.write(item["name"])
                c2.write(f"x{qty}")
                if c3.button("✖", key=f"remove_{pid}"):
                    del st.session_state.cart[pid]
                    st.rerun()
                q1, q2, q3 = st.columns([1, 1, 1])
                if q1.button("−", key=f"minus_{pid}"):
                    if qty <= 1: del st.session_state.cart[pid]
                    else: st.session_state.cart[pid] = (item, qty - 1)
                    st.rerun()
                q2.caption(money(item["price"] * qty))
                if q3.button("+", key=f"plus_{pid}"):
                    st.session_state.cart[pid] = (item, qty + 1)
                    st.rerun()
        total = sum(p["price"] * q for p, q in cart.values())
        st.divider()
        st.markdown(f"### الإجمالي: {money(total)}")
        with st.form("checkout_form"):
            customer_name = st.text_input("الاسم الكريم")
            customer_phone = st.text_input("رقم الهاتف")
            customer_address = st.text_area("عنوان التوصيل بالتفصيل", height=80)
            branch = st.selectbox("فرع الاستلام / التوصيل", list(BRANCHES.keys()))
            submit = st.form_submit_button("تأكيد الطلب عبر واتساب", use_container_width=True, type="primary")
            if submit:
                if not cart:
                    st.error("أضف صنفًا واحدًا على الأقل إلى السلة.")
                elif not customer_name.strip() or not customer_phone.strip() or not customer_address.strip():
                    st.error("يرجى استكمال الاسم ورقم الهاتف والعنوان.")
                else:
                    order_id, items = save_order(customer_name.strip(), customer_phone.strip(), customer_address.strip(), branch, cart, total)
                    lines = [
                        "🛒 *طلب جديد من موقع أسماك وادي النيل*",
                        f"رقم الطلب: {order_id}",
                        f"الاسم: {customer_name.strip()}",
                        f"الهاتف: {customer_phone.strip()}",
                        f"العنوان: {customer_address.strip()}",
                        f"الفرع: {branch}", "", "*الأصناف المطلوبة:*"
                    ]
                    for it in items:
                        lines.append(f"- {it['name']} × {it['qty']} = {it['subtotal']:.2f} ج.م")
                    lines.append(f"\n*الإجمالي الكلي: {total:.2f} ج.م*")
                    wa_url = f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(chr(10).join(lines))}"
                    st.session_state.cart = {}
                    st.success(f"تم تسجيل الطلب رقم {order_id}. افتح واتساب لإرسال التفاصيل.")
                    st.link_button("فتح واتساب وإرسال الطلب", wa_url, use_container_width=True)
                    st.rerun()

    search = st.text_input("🔎 ابحث عن منتج أو وجبة...", placeholder="اكتب اسم الوجبة أو جزءًا منه")
    category_cols = st.columns(len(CATEGORIES) + 1)
    category_options = ["الكل"] + CATEGORIES
    for i, cat in enumerate(category_options):
        with category_cols[i]:
            if st.button(cat, key=f"cat_{i}", type="primary" if st.session_state.category == cat else "secondary", use_container_width=True):
                st.session_state.category = cat
                st.rerun()

    products = get_products()
    if search.strip():
        products = [p for p in products if search.strip().casefold() in p["name"].casefold() or search.strip().casefold() in p["description"].casefold()]
    elif st.session_state.category != "الكل":
        products = [p for p in products if p["category"] == st.session_state.category]
    st.markdown(f'<div class="section-title">{st.session_state.category if st.session_state.category != "الكل" else "كل المنتجات"} <span style="font-size:13px;color:#64748b;font-weight:600">({len(products)} منتج)</span></div>', unsafe_allow_html=True)
    if not products:
        st.info("لم يتم العثور على منتجات مطابقة للبحث.")
    else:
        cols_per_row = 3
        for start in range(0, len(products), cols_per_row):
            cols = st.columns(cols_per_row, gap="medium")
            for col, product in zip(cols, products[start:start + cols_per_row]):
                with col:
                    with st.container(border=True):
                        if product["image_url"]:
                            st.image(product["image_url"], use_container_width=True)
                        st.markdown(f'<div class="price-pill">{money(float(product["price"]))}</div><div class="product-name">{product["name"]}</div><div class="product-desc">{product["description"]}</div>', unsafe_allow_html=True)
                        if st.button("➕ إضافة إلى السلة", key=f"add_{product['id']}", use_container_width=True):
                            pid = str(product["id"])
                            if pid in st.session_state.cart:
                                old_product, qty = st.session_state.cart[pid]
                                st.session_state.cart[pid] = (old_product, qty + 1)
                            else:
                                st.session_state.cart[pid] = (product, 1)
                            st.toast(f"تمت إضافة {product['name']} إلى السلة")
                            st.rerun()

    st.markdown("---")
    st.markdown('<div class="section-title" style="text-align:center">📍 فروع سلسلة مطاعم وادي النيل</div>', unsafe_allow_html=True)
    branch_cols = st.columns(3)
    for col, (name, address) in zip(branch_cols, BRANCHES.items()):
        with col:
            st.markdown(f"""
            <div style="background:#172554;color:white;border:1px solid #1e40af;padding:20px;border-radius:16px;min-height:130px">
              <div style="font-weight:900;color:#a5f3fc;font-size:18px">{name}</div>
              <div style="color:#cbd5e1;margin-top:8px">{address}</div>
            </div>
            """, unsafe_allow_html=True)
    with st.expander("إدارة الموقع"):
        admin_page()
    st.markdown(f'<div style="background:#020617;color:#cbd5e1;text-align:center;padding:18px;border-radius:12px;margin-top:24px">مطاعم أسماك وادي النيل © 2026 جميع الحقوق محفوظة<br>الخط الساخن: <b style="color:#67e8f9">{HOTLINE}</b></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
