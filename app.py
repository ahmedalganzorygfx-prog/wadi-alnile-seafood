import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st

# =========================================================
# إعدادات عامة
# =========================================================
st.set_page_config(
    page_title="مطاعم أسماك وادي النيل | طعم البحر بطعم مصري أصيل",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DB_PATH = Path(__file__).with_name("wadi_alnile.db")
HOTLINE = "19974"
NAVY = "#07566A"
DARK = "#063B49"
GOLD = "#FFB703"
CREAM = "#FFFDF4"

# صور تجريبية من Unsplash؛ يمكن استبدالها بصور المطعم الفعلية.
DEFAULT_PRODUCTS = [
    ("سمك بلطي مشوي", "الأسماك", 180.0, "سمك طازج مشوي على الفحم", "https://images.unsplash.com/photo-1510130387422-82bed34b37e9?auto=format&fit=crop&w=900&q=85", 1),
    ("سمك دنيس مشوي", "الأسماك", 320.0, "دنيس مشوي بتتبيلة المطعم", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=85", 1),
    ("جمبري مقلي", "الجمبري", 290.0, "جمبري مقرمش يقدم ساخنًا", "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=85", 1),
    ("طاجن جمبري", "الجمبري", 340.0, "طاجن جمبري بصلصة خاصة", "https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?auto=format&fit=crop&w=900&q=85", 1),
    ("شوربة سي فود", "الشوربة", 120.0, "شوربة مأكولات بحرية غنية بالنكهة", "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=900&q=85", 1),
    ("أرز صيادية", "الأرز", 55.0, "أرز صيادية بالتوابل الشرقية", "https://images.unsplash.com/photo-1516684732162-798a0062be99?auto=format&fit=crop&w=900&q=85", 1),
    ("سلطة خضراء", "السلطات", 35.0, "خضروات طازجة يوميًا", "https://images.unsplash.com/photo-1512621776951-a57141f2eegde?auto=format&fit=crop&w=900&q=85", 1),
    ("وجبة عائلية بحرية", "العروض", 750.0, "تشكيلة مختارة للمشاركة", "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=900&q=85", 1),
]
CATEGORIES = ["الكل", "الأسماك", "الجمبري", "المشويات", "الشوربة", "الأرز", "السلطات", "العروض"]


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL DEFAULT 0,
                description TEXT DEFAULT '',
                image_url TEXT DEFAULT '',
                active INTEGER NOT NULL DEFAULT 1
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                notes TEXT DEFAULT '',
                items_json TEXT NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'جديد',
                created_at TEXT NOT NULL
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            conn.executemany(
                """INSERT INTO products
                   (name, category, price, description, image_url, active)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                DEFAULT_PRODUCTS,
            )


def load_products():
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM products WHERE active=1 ORDER BY category, name"
        ).fetchall()


def money(value):
    return f"{value:,.0f} ج.م"


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');
        html, body, [class*="css"], [data-testid="stAppViewContainer"] {
            font-family: 'Cairo', sans-serif !important;
            direction: rtl;
        }
        .stApp { background: #ffffff; }
        [data-testid="stHeader"] { background: rgba(255,255,255,0); }
        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none; }
        .block-container { max-width: 1440px; padding-top: 1rem; padding-bottom: 2rem; }
        .topbar {
            background: linear-gradient(110deg, #063B49, #07566A);
            color: white; border-radius: 0 0 18px 18px;
            padding: 13px 24px; display:flex; justify-content:space-between;
            align-items:center; gap:12px; box-shadow: 0 7px 22px #063b491c;
            font-size: 14px; font-weight:700;
        }
        .topbar .gold { color:#FFCA28; }
        .brand { text-align:center; padding:34px 12px 20px; }
        .brand h1 { color:#07566A; font-size:clamp(30px,4vw,50px); font-weight:900; margin:0; }
        .brand p { color:#D99A00; font-size:18px; font-weight:700; margin-top:8px; }
        .hero {
            border-radius:24px; padding:42px 34px; margin:12px 0 28px;
            background:linear-gradient(90deg, rgba(3,42,54,.92), rgba(3,42,54,.56)),
            url('https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=1800&q=90') center/cover;
            color:white; min-height:285px; display:flex; flex-direction:column;
            justify-content:center; box-shadow:0 14px 35px #063b4920;
        }
        .hero h2 {font-size:clamp(27px,3.6vw,44px);font-weight:900;margin:0 0 12px;}
        .hero p {font-size:17px;max-width:650px;line-height:1.9;margin:0 0 20px;}
        .section-title {color:#063B49;font-size:27px;font-weight:900;margin:18px 0 6px;}
        .section-subtitle {color:#687780;margin-bottom:18px;font-size:14px;}
        .product-card {
            border:1px solid #e8eef0; border-radius:18px; overflow:hidden;
            background:#fff; margin-bottom:18px; box-shadow:0 7px 24px #073b4910;
            transition:transform .2s ease,box-shadow .2s ease;
        }
        .product-card:hover {transform:translateY(-3px);box-shadow:0 12px 28px #073b4920;}
        .product-card img {width:100%;height:170px;object-fit:cover;display:block;}
        .product-info {padding:14px;}
        .product-name {font-weight:900;color:#063B49;font-size:17px;margin-bottom:5px;}
        .product-desc {color:#6d7b80;font-size:12px;min-height:42px;line-height:1.7;}
        .product-price {color:#B78300;font-weight:900;font-size:18px;margin:10px 0;}
        .feature {
            background:#f5fafb;border:1px solid #e3eff1;border-radius:16px;
            padding:20px;text-align:center;height:100%;
        }
        .feature .icon {font-size:30px;}
        .feature h4 {color:#07566A;margin:8px 0;font-size:17px;}
        .feature p {color:#687780;font-size:13px;margin:0;line-height:1.8;}
        .footer {
            margin-top:38px;padding:28px;border-radius:20px;
            background:#063B49;color:white;text-align:center;line-height:2;
        }
        div.stButton > button {
            border-radius:11px;border:0;background:#07566A;color:#fff;
            font-weight:800;min-height:42px;transition:.2s;
        }
        div.stButton > button:hover {background:#063B49;color:#fff;border:0;}
        div[data-testid="stFormSubmitButton"] button {
            background:#07566A;color:white;border-radius:10px;font-weight:800;
        }
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
            border-radius:10px;
        }
        @media(max-width:700px) {
            .block-container {padding-left:12px;padding-right:12px;}
            .topbar {padding:12px;font-size:12px;}
            .hero {padding:28px 20px;min-height:260px;}
            .product-card img {height:145px;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    st.markdown(
        f"""
        <div class="topbar">
            <div>📞 الخط الساخن: <span class="gold">{HOTLINE}</span></div>
            <div>🐟 <span class="gold">مطاعم أسماك وادي النيل</span></div>
        </div>
        <div class="brand">
            <h1>🐟 مطاعم أسماك وادي النيل</h1>
            <p>طعم البحر .. بطعم مصري أصيل</p>
        </div>
        <div class="hero">
            <h2>أشهى المأكولات البحرية على مائدتك</h2>
            <p>اختار وجبتك المفضلة من قائمة أسماك وادي النيل، وأرسل طلبك بسهولة. طعم أصيل وتجربة طلب أبسط.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_features():
    st.markdown('<div class="section-title">لماذا تختار وادي النيل؟</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">نهتم بالتفاصيل من اختيار المكونات حتى وصول طلبك.</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    features = [
        ("🐟", "اختيارات متنوعة", "أسماك ومأكولات بحرية تناسب مختلف الأذواق."),
        ("🔥", "تحضير طازج", "تجهيز الوجبات عند الطلب قدر الإمكان."),
        ("🛵", "طلب سهل", "أرسل بيانات طلبك من الموقع في خطوات بسيطة."),
        ("☎️", "تواصل مباشر", f"يمكنك الاتصال بالخط الساخن {HOTLINE}."),
    ]
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f'<div class="feature"><div class="icon">{icon}</div><h4>{title}</h4><p>{desc}</p></div>',
                unsafe_allow_html=True,
            )


def render_menu():
    st.markdown('<div class="section-title">قائمة الطعام</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">تصفح الأصناف واختر ما يناسبك ثم أضفه إلى سلة المشتريات.</div>', unsafe_allow_html=True)
    products = load_products()
    if not products:
        st.info("لا توجد أصناف متاحة حاليًا.")
        return

    selected_category = st.radio(
        "الأقسام",
        CATEGORIES,
        horizontal=True,
        label_visibility="collapsed",
        key="category_filter",
    )
    search = st.text_input("🔎 ابحث عن وجبتك", placeholder="اكتب اسم الصنف...", key="product_search")
    filtered = [
        p for p in products
        if (selected_category == "الكل" or p["category"] == selected_category)
        and (search.strip() in p["name"] or search.strip() == "")
    ]
    if not filtered:
        st.warning("لا توجد أصناف مطابقة لبحثك.")
        return

    cart = st.session_state.setdefault("cart", {})
    cols_per_row = 4
    for start in range(0, len(filtered), cols_per_row):
        row = st.columns(cols_per_row)
        for col, product in zip(row, filtered[start:start + cols_per_row]):
            with col:
                image_url = product["image_url"] or "https://images.unsplash.com/photo-1510130387422-82bed34b37e9?auto=format&fit=crop&w=900&q=85"
                st.markdown(
                    f"""
                    <div class="product-card">
                        <img src="{image_url}" alt="{product['name']}">
                        <div class="product-info">
                            <div class="product-name">{product['name']}</div>
                            <div class="product-desc">{product['description'] or 'اختيار لذيذ من قائمة وادي النيل.'}</div>
                            <div class="product-price">{money(product['price'])}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                qty_col, add_col = st.columns([1, 1.5])
                with qty_col:
                    qty = st.number_input(
                        "الكمية", min_value=1, max_value=20, value=1,
                        key=f"qty_{product['id']}", label_visibility="collapsed"
                    )
                with add_col:
                    if st.button("أضف للسلة ＋", key=f"add_{product['id']}", use_container_width=True):
                        pid = product["id"]
                        if pid in cart:
                            cart[pid]["quantity"] += int(qty)
                        else:
                            cart[pid] = {
                                "id": pid, "name": product["name"],
                                "price": float(product["price"]),
                                "quantity": int(qty),
                            }
                        st.session_state["cart"] = cart
                        st.toast(f"تمت إضافة {product['name']} إلى السلة")
                        st.rerun()


def render_cart_and_checkout():
    st.markdown('<div class="section-title">🛒 سلة المشتريات وإتمام الطلب</div>', unsafe_allow_html=True)
    cart = st.session_state.setdefault("cart", {})
    if not cart:
        st.info("سلتك فارغة حاليًا. أضف الأصناف التي ترغب بها من قائمة الطعام.")
        return

    total = 0.0
    for pid in list(cart.keys()):
        item = cart[pid]
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        with c1:
            st.write(f"**{item['name']}**")
        with c2:
            st.write(money(item["price"]))
        with c3:
            new_qty = st.number_input(
                "الكمية", min_value=1, max_value=20, value=int(item["quantity"]),
                key=f"cart_qty_{pid}", label_visibility="collapsed"
            )
            item["quantity"] = int(new_qty)
        with c4:
            if st.button("حذف", key=f"remove_{pid}"):
                del cart[pid]
                st.rerun()
        total += item["price"] * item["quantity"]

    st.markdown(f"### إجمالي الطلب: <span style='color:{NAVY}'>{money(total)}</span>", unsafe_allow_html=True)
    st.divider()
    st.markdown("#### بيانات العميل")
    with st.form("checkout_form", clear_on_submit=False):
        name = st.text_input("الاسم بالكامل *")
        phone = st.text_input("رقم الهاتف *", placeholder="01xxxxxxxxx")
        address = st.text_area("عنوان التوصيل بالتفصيل *")
        notes = st.text_area("ملاحظات إضافية (اختياري)")
        submitted = st.form_submit_button("تأكيد إرسال الطلب", use_container_width=True)
        if submitted:
            digits = "".join(ch for ch in phone if ch.isdigit())
            if not name.strip() or not address.strip() or len(digits) < 10:
                st.error("يرجى إدخال الاسم ورقم هاتف صحيح وعنوان التوصيل.")
            else:
                import json
                items = [
                    {"name": v["name"], "price": v["price"], "quantity": v["quantity"]}
                    for v in cart.values()
                ]
                with get_conn() as conn:
                    cur = conn.execute(
                        """INSERT INTO orders
                        (customer_name, phone, address, notes, items_json, total, status, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                        (name.strip(), phone.strip(), address.strip(), notes.strip(),
                         json.dumps(items, ensure_ascii=False), total, "جديد",
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    )
                    order_id = cur.lastrowid
                st.session_state["cart"] = {}
                st.success(f"تم تسجيل طلبك بنجاح. رقم الطلب: {order_id}")
                st.info(f"للاستفسار عن الطلب اتصل بالخط الساخن {HOTLINE}.")
                st.rerun()


def render_admin():
    with st.expander("🔐 لوحة إدارة الموقع", expanded=False):
        st.warning("لحماية بيانات العملاء، لا تترك لوحة الإدارة متاحة للعامة في النشر الفعلي. عيّن كلمة مرور قوية من إعدادات التطبيق.")
        password = st.text_input("كلمة مرور الإدارة", type="password", key="admin_password")
        admin_password = st.secrets.get("ADMIN_PASSWORD", "change-me-now")
        if password != admin_password:
            st.caption("أدخل كلمة مرور الإدارة لعرض أدوات الإدارة. كلمة المرور الافتراضية للتطوير هي change-me-now ويجب تغييرها قبل النشر.")
            return

        tab_products, tab_orders = st.tabs(["إدارة الأصناف", "الطلبات"])
        with tab_products:
            st.markdown("##### إضافة صنف جديد")
            with st.form("new_product_form"):
                name = st.text_input("اسم الصنف")
                category = st.selectbox("القسم", CATEGORIES[1:])
                price = st.number_input("السعر بالجنيه", min_value=0.0, step=5.0)
                description = st.text_input("وصف مختصر")
                image_url = st.text_input("رابط الصورة (اختياري)")
                add = st.form_submit_button("إضافة الصنف")
                if add:
                    if not name.strip() or price <= 0:
                        st.error("أدخل اسم الصنف وسعرًا أكبر من صفر.")
                    else:
                        with get_conn() as conn:
                            conn.execute(
                                """INSERT INTO products(name, category, price, description, image_url, active)
                                   VALUES (?, ?, ?, ?, ?, 1)""",
                                (name.strip(), category, price, description.strip(), image_url.strip()),
                            )
                        st.success("تمت إضافة الصنف.")
                        st.rerun()

            products = load_products()
            if products:
                options = {f"{p['name']} — {money(p['price'])}": p["id"] for p in products}
                selected_label = st.selectbox("اختر صنفًا لإيقاف عرضه", list(options.keys()))
                if st.button("إخفاء الصنف المحدد"):
                    with get_conn() as conn:
                        conn.execute("UPDATE products SET active=0 WHERE id=?", (options[selected_label],))
                    st.success("تم إخفاء الصنف من قائمة الطعام.")
                    st.rerun()

        with tab_orders:
            import pandas as pd
            with get_conn() as conn:
                orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
            if not orders:
                st.info("لا توجد طلبات مسجلة حتى الآن.")
            else:
                df = pd.DataFrame([dict(o) for o in orders])
                st.dataframe(df.drop(columns=["items_json"]), use_container_width=True, hide_index=True)
                order_ids = [o["id"] for o in orders]
                order_id = st.selectbox("رقم الطلب لتحديث حالته", order_ids)
                status = st.selectbox("الحالة الجديدة", ["جديد", "قيد التجهيز", "خرج للتوصيل", "مكتمل", "ملغي"])
                if st.button("حفظ حالة الطلب"):
                    with get_conn() as conn:
                        conn.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
                    st.success("تم تحديث حالة الطلب.")
                    st.rerun()


def render_footer():
    st.markdown(
        f"""
        <div class="footer">
            <h3 style="margin:0;color:#FFCA28;">مطاعم أسماك وادي النيل 🐟</h3>
            <div>طعم البحر .. بطعم مصري أصيل</div>
            <div>الخط الساخن: <strong style="color:#FFCA28;">{HOTLINE}</strong></div>
            <div style="font-size:12px;color:#d6e6e9;">جميع الحقوق محفوظة © {datetime.now().year} مطاعم أسماك وادي النيل</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# تشغيل الموقع
# =========================================================
init_db()
inject_css()
render_header()

# روابط انتقال سريعة
nav1, nav2, nav3 = st.columns(3)
with nav1:
    if st.button("🍽️ قائمة الطعام", use_container_width=True):
        st.session_state["jump_menu"] = True
with nav2:
    if st.button("🛒 سلة المشتريات", use_container_width=True):
        st.session_state["jump_cart"] = True
with nav3:
    st.link_button("☎️ اتصل بنا", f"tel:{HOTLINE}", use_container_width=True)

render_features()
st.divider()
render_menu()
st.divider()
render_cart_and_checkout()
st.divider()
render_admin()
render_footer()
