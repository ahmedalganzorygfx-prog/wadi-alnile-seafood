import streamlit as st
from datetime import datetime
import sqlite3
import json
import os
from urllib.parse import quote

# =========================================================
# إعداد الصفحة
# =========================================================
st.set_page_config(
    page_title="المنصة الرقمية | أسماك وادي النيل",
    page_icon="🦐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

HOTLINE = "19974"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "wadi_alnile.db")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-this-password")
DELIVERY_FEE_DEFAULT = 25.0


def db_connect():
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    with db_connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            notes TEXT,
            items_json TEXT NOT NULL,
            subtotal REAL NOT NULL,
            delivery_fee REAL NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'جديد',
            created_at TEXT NOT NULL
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            phone TEXT,
            branch TEXT,
            rating INTEGER,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )""")
        conn.execute("""CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )""")
        conn.execute("INSERT OR IGNORE INTO settings(key, value) VALUES('delivery_fee', ?)", (str(DELIVERY_FEE_DEFAULT),))
        conn.execute("INSERT OR IGNORE INTO settings(key, value) VALUES('whatsapp_number', '')")


def get_setting(key, default=''):
    with db_connect() as conn:
        row = conn.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
    return row['value'] if row else default


def set_setting(key, value):
    with db_connect() as conn:
        conn.execute('INSERT INTO settings(key,value) VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value', (key, str(value)))


def save_order(order):
    with db_connect() as conn:
        cur = conn.execute("""INSERT INTO orders
            (customer_name, phone, address, notes, items_json, subtotal, delivery_fee, total, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (order['name'], order['phone'], order['address'], order['notes'],
             json.dumps(order['items'], ensure_ascii=False), order['subtotal'],
             order['delivery_fee'], order['total'], 'جديد', order['date']))
        return cur.lastrowid


init_database()

# =========================================================
# البيانات الأساسية
# =========================================================
BRANCHES = [
    {"name": "فرع المهندسين الرئيسي", "address": "82 ش وادي النيل، المهندسين، الجيزة", "phone": HOTLINE, "icon": "🏢"},
    {"name": "فرع محور 26 يوليو", "address": "محور 26 يوليو، داخل محطة بنزين شيل آوت، السادس من أكتوبر، الجيزة", "phone": HOTLINE, "icon": "📍"},
    {"name": "فرع الهرم", "address": "شارع الضغط العالي، المنطقة ط، داخل أهرام مول، بوابة 2، الدور الأرضي", "phone": HOTLINE, "icon": "🏪"},
    {"name": "فرع طريق الواحات", "address": "طريق الواحات، البوابة الرابعة، داخل محطة بنزين شيل آوت الهرم", "phone": HOTLINE, "icon": "🚗"},
    {"name": "فرع الساحل الشمالي", "address": "كم 81، داخل قرية قرطاج، طريق إسكندرية مطروح الصحراوي", "phone": HOTLINE, "icon": "🌊"},
]

MENU = {
    "🍤 المقبلات والشوربات": [
        {"name": "شوربة سي فود", "price": 95, "desc": "شوربة كريمية غنية بالمأكولات البحرية"},
        {"name": "جمبري بانيه", "price": 180, "desc": "جمبري مقرمش مع صوص خاص"},
        {"name": "كاليماري مقلي", "price": 165, "desc": "حلقات كاليماري مقرمشة"},
    ],
    "🐟 الأسماك الطازجة": [
        {"name": "سمك دنيس مشوي", "price": 260, "desc": "دنيس طازج مشوي على الطريقة المصرية"},
        {"name": "سمك قاروص مشوي", "price": 280, "desc": "قاروص طازج مع التتبيلة الخاصة"},
        {"name": "بلطي مشوي", "price": 150, "desc": "بلطي طازج مشوي مع السلطة والطحينة"},
    ],
    "🍲 الطواجن": [
        {"name": "طاجن سي فود", "price": 240, "desc": "تشكيلة مأكولات بحرية بصوص مميز"},
        {"name": "طاجن جمبري", "price": 260, "desc": "جمبري طازج مع الخضروات والصوص"},
        {"name": "طاجن سمك", "price": 220, "desc": "سمك طازج بطريقة الطاجن المصرية"},
    ],
    "🍱 الوجبات العائلية": [
        {"name": "وجبة العائلة البحرية", "price": 650, "desc": "تشكيلة متنوعة تكفي العائلة"},
        {"name": "وجبة وادي النيل", "price": 850, "desc": "اختيار مميز من أفضل المأكولات البحرية"},
    ],
    "🥪 الساندويتشات": [
        {"name": "ساندويتش جمبري", "price": 120, "desc": "جمبري مقرمش داخل خبز طازج"},
        {"name": "ساندويتش فيليه سمك", "price": 110, "desc": "فيليه سمك مقرمش مع الصوص الخاص"},
    ],
}

OFFERS = [
    {"title": "عرض العائلة", "desc": "وجبة بحرية متنوعة للعائلة بسعر مميز", "price": "599 جنيه", "icon": "👨‍👩‍👧‍👦"},
    {"title": "عرض الجمبري", "desc": "وجبة جمبري مميزة مع الأرز والسلطة", "price": "299 جنيه", "icon": "🍤"},
    {"title": "عرض وادي النيل", "desc": "اختيار منوع من أشهر أطباق المطعم", "price": "699 جنيه", "icon": "⭐"},
]

# =========================================================
# الحالة
# السلة داخل الجلسة، أما الطلبات والتقييمات فتحفظ في SQLite محليًا.
# =========================================================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "orders" not in st.session_state:
    st.session_state.orders = []

if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================================================
# تنسيقات CSS عامة فقط؛ محتوى الصفحات مبني بمكونات Streamlit الأصلية.
# =========================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');
    :root { --navy:#071f33; --deep:#0b3449; --ocean:#0b7185; --teal:#13a89e; --gold:#e5b65c; --ink:#183247; --muted:#6b7d89; --line:#dce7eb; }
    html, body, [class*="css"], [data-testid="stAppViewContainer"] { font-family:"Cairo",sans-serif !important; }
    .stApp { direction:rtl; color:var(--ink); background:radial-gradient(ellipse at 92% 0%,rgba(19,168,158,.12),transparent 25%),radial-gradient(ellipse at 4% 20%,rgba(229,182,92,.10),transparent 22%),linear-gradient(180deg,#f8fbfc 0%,#eef4f6 58%,#f8f7f2 100%); }
    [data-testid="stAppViewContainer"] *, [data-testid="stMarkdownContainer"] { direction:rtl; }
    [data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] h1,[data-testid="stMarkdownContainer"] h2,[data-testid="stMarkdownContainer"] h3,[data-testid="stCaptionContainer"],label { text-align:right; }
    .block-container { max-width:1380px; padding-top:1.1rem; padding-bottom:3rem; }
    [data-testid="stSidebar"] { display:none; }
    h1,h2,h3 { color:var(--navy) !important; font-weight:900 !important; letter-spacing:-.45px; }
    h1 { font-size:2.5rem !important; line-height:1.35 !important; } h2 { font-size:1.85rem !important; line-height:1.4 !important; margin-top:.35rem !important; } h3 { font-size:1.22rem !important; }
    p,li { line-height:1.9; } [data-testid="stCaptionContainer"] { color:var(--muted); font-size:.94rem; }
    [data-testid="stVerticalBlockBorderWrapper"] { background:rgba(255,255,255,.97); border:1px solid rgba(210,226,232,.95); border-radius:22px; box-shadow:0 12px 32px rgba(7,31,51,.065); padding:15px; transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease; }
    [data-testid="stVerticalBlockBorderWrapper"]:hover { border-color:#b8d9dd; box-shadow:0 17px 38px rgba(7,31,51,.10); transform:translateY(-2px); }
    [data-testid="stImage"] img { border-radius:17px; object-fit:cover; }
    .stButton > button,.stLinkButton > a { font-family:"Cairo",sans-serif !important; font-weight:800 !important; border-radius:13px !important; min-height:48px; border:1px solid #d3e1e6; transition:all .18s ease; background:#fff; color:var(--navy); }
    .stButton > button[kind="primary"] { background:linear-gradient(135deg,var(--navy),var(--ocean)) !important; color:white !important; border:0 !important; box-shadow:0 8px 18px rgba(11,113,133,.20); }
    .stButton > button:hover,.stLinkButton > a:hover { transform:translateY(-2px); border-color:var(--teal); box-shadow:0 9px 20px rgba(7,55,75,.13); }
    [data-testid="stAlert"] { border-radius:15px; border-width:1px; }
    [data-testid="stSelectbox"],[data-testid="stTextInput"],[data-testid="stTextArea"] { text-align:right; }
    [data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea { border-radius:12px; background:#fff; }
    [data-testid="stMetricValue"] { color:var(--navy); } hr { border-color:#d7e5eb; margin:1.6rem 0; } div[data-testid="stHorizontalBlock"] { gap:.9rem; }
    [data-testid="stVerticalBlockBorderWrapper"]:has(img) { overflow:hidden; }
    @media (max-width:900px) { .block-container { padding-left:1rem; padding-right:1rem; } h1 { font-size:1.85rem !important; } h2 { font-size:1.45rem !important; } [data-testid="stVerticalBlockBorderWrapper"] { padding:11px; border-radius:17px; } }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# الرأس الرئيسي — هوية بصرية للمطعم
# =========================================================
HERO_IMAGE = "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=1800&q=85"
with st.container(border=True):
    hero_left, hero_right = st.columns([1.08, 1.2], gap="large")
    with hero_left:
        st.caption("تجربة بحرية مختارة بعناية")
        st.markdown("# أسماك وادي النيل")
        st.markdown("### من خيرات البحر إلى مائدتك")
        st.write("مذاق مصري أصيل، مكونات طازجة، وأطباق تُحضّر لتستمتع بكل تفصيلة.")
        st.markdown(f"**☎ الخط الساخن: {HOTLINE}**")
        st.caption("✦ جودة يومية  ·  ✦ وصفات مميزة  ·  ✦ اختيارات تناسب العائلة")
        hero_btn1, hero_btn2 = st.columns(2)
        with hero_btn1:
            if st.button("🍽️ استكشف المنيو", key="hero_menu", type="primary", use_container_width=True):
                st.session_state.page = "menu"
                st.rerun()
        with hero_btn2:
            if st.button("🎁 اكتشف العروض", key="hero_offers", use_container_width=True):
                st.session_state.page = "offers"
                st.rerun()
    with hero_right:
        st.image(HERO_IMAGE, use_container_width=True, caption="اختيارات بحرية بطعم مميز")

st.write("")

# =========================================================
# المميزات
# =========================================================
features = [
    ("🐟", "أسماك طازجة", "اختيار يومي من أجود الأسماك والمأكولات البحرية"),
    ("👨‍🍳", "خبرة وجودة", "وصفات مميزة وطريقة إعداد تحافظ على جودة الطعم"),
    ("🚗", "خدمة متميزة", "نحرص على تقديم تجربة سهلة ومميزة لعملائنا"),
    ("⭐", "رضا العملاء", "رأي العميل هو أساس التطوير المستمر"),
]

feature_cols = st.columns(4)
for col, (icon, title, description) in zip(feature_cols, features):
    with col:
        with st.container(border=True):
            st.markdown(f"### {icon}")
            st.markdown(f"**{title}**")
            st.caption(description)

# =========================================================
# القائمة الرئيسية
# =========================================================
st.divider()
st.markdown("## 🌊 اكتشف تجربة وادي النيل")
st.caption("كل ما تحتاجه لاختيار وجبتك والتواصل معنا — في مكان واحد")

nav = [
    ("🍽️ المنيو", "menu"),
    (f"🛒 الطلبات ({len(st.session_state.cart)})", "orders"),
    ("🎁 العروض", "offers"),
    ("🤖 مساعد الوجبات", "smart"),
    ("📍 الفروع", "branches"),
    ("⭐ التقييمات", "reviews"),
    ("📝 الشكاوى والاقتراحات", "complaints"),
    ("🔐 إدارة المطعم", "admin"),
]

nav_cols = st.columns(4)
for i, (label, page) in enumerate(nav):
    with nav_cols[i % 4]:
        with st.container(border=True):
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.page = page
                st.rerun()

st.write("")

if st.button("🏠 العودة إلى الرئيسية", key="home_button", use_container_width=True):
    st.session_state.page = "home"
    st.rerun()

# =========================================================
# الرئيسية
# =========================================================
if st.session_state.page == "home":
    st.markdown("## نكهة البحر… بتفاصيل تستحق التجربة")
    st.caption("اكتشف أطباقنا المميزة، اختر ما تحب، واجعل وجبتك القادمة أقرب مما تتخيل.")

    featured = [
        ("سمك دنيس مشوي", "260 جنيه", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=85"),
        ("جمبري بانيه", "180 جنيه", "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=85"),
        ("طاجن سي فود", "240 جنيه", "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=900&q=85"),
    ]
    featured_cols = st.columns(3, gap="large")
    for i, (dish, price, image_url) in enumerate(featured):
        with featured_cols[i]:
            with st.container(border=True):
                st.image(image_url, use_container_width=True)
                st.caption("اختيار مميز من وادي النيل")
                st.markdown(f"### {dish}")
                st.markdown(f"**{price}**")
                if st.button("اكتشف في المنيو ←", key=f"featured_{i}", use_container_width=True):
                    st.session_state.page = "menu"
                    st.rerun()

    st.write("")
    promo_left, promo_right = st.columns([1.5, 1], gap="large")
    with promo_left:
        with st.container(border=True):
            st.markdown("### 🎁 عروض تجمع العائلة")
            st.write("وجبات مختارة وأسعار مميزة لتشاركوا لحظات لذيذة معًا.")
            if st.button("استعرض العروض", key="home_offers", type="primary", use_container_width=True):
                st.session_state.page = "offers"
                st.rerun()
    with promo_right:
        with st.container(border=True):
            st.markdown("### 📍 أقرب إليك")
            st.write("تعرّف على فروعنا واختر الفرع المناسب لك.")
            if st.button("عرض الفروع", key="home_branches", use_container_width=True):
                st.session_state.page = "branches"
                st.rerun()

# =========================================================
# المنيو
# =========================================================
elif st.session_state.page == "menu":
    st.markdown("## 🍽️ قائمة الطعام")
    st.caption("اختر من مجموعة متنوعة من أفضل المأكولات البحرية.")

    category = st.selectbox("اختر القسم", list(MENU.keys()), key="menu_category")

    FOOD_IMAGES = {
        "شوربة سي فود": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=900&q=80",
        "جمبري بانيه": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=80",
        "كاليماري مقلي": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?auto=format&fit=crop&w=900&q=80",
        "سمك دنيس مشوي": "https://images.unsplash.com/photo-1510130387422-82bed34b37e9?auto=format&fit=crop&w=900&q=80",
        "سمك قاروص مشوي": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80",
        "بلطي مشوي": "https://images.unsplash.com/photo-1510130387422-82bed34b37e9?auto=format&fit=crop&w=900&q=80",
        "طاجن سي فود": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=900&q=80",
        "طاجن جمبري": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=80",
        "طاجن سمك": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80",
        "وجبة العائلة البحرية": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=900&q=80",
        "وجبة وادي النيل": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80",
        "ساندويتش جمبري": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=80",
        "ساندويتش فيليه سمك": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80",
    }
    items = MENU[category]
    cols = st.columns(3)

    for idx, item in enumerate(items):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(FOOD_IMAGES.get(item["name"], HERO_IMAGE), use_container_width=True)
                st.markdown(f"### {item['name']}")
                st.write(item["desc"])
                st.markdown(f"### 🟡 {item['price']} جنيه")

                if st.button(
                    f"➕ إضافة {item['name']}",
                    key=f"add_{category}_{idx}",
                    use_container_width=True,
                ):
                    st.session_state.cart.append(item.copy())
                    st.success(f"تمت إضافة {item['name']} إلى الطلب.")

# =========================================================
# الطلبات
# =========================================================
elif st.session_state.page == "orders":
    st.markdown("## 🛒 الطلبات")
    st.caption("راجع طلبك وأرسل بيانات التواصل.")

    if not st.session_state.cart:
        st.info("🛒 السلة فارغة حاليًا. اذهب إلى المنيو لإضافة الوجبات.")
    else:
        subtotal = sum(item["price"] for item in st.session_state.cart)
        delivery_fee = float(get_setting("delivery_fee", DELIVERY_FEE_DEFAULT) or 0)
        total = subtotal + delivery_fee

        for i, item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{item['name']}**")
                    st.write(f"{item['price']} جنيه")
                with c2:
                    if st.button("❌ حذف", key=f"remove_{i}", use_container_width=True):
                        st.session_state.cart.pop(i)
                        st.rerun()

        st.info(f"قيمة الأصناف: {subtotal:.2f} جنيه | رسوم التوصيل: {delivery_fee:.2f} جنيه")
        st.success(f"💰 إجمالي الطلب شامل التوصيل: {total:.2f} جنيه")

        st.markdown("### 📋 بيانات العميل")
        name = st.text_input("الاسم", key="order_name")
        phone = st.text_input("رقم الهاتف", key="order_phone")
        address = st.text_area("العنوان", key="order_address")
        notes = st.text_area("ملاحظات إضافية", key="order_notes")

        if st.button("🚀 إرسال الطلب", use_container_width=True, type="primary"):
            if not name.strip() or not phone.strip() or not address.strip():
                st.warning("من فضلك أدخل الاسم ورقم الهاتف والعنوان.")
            else:
                order = {
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "address": address.strip(),
                    "notes": notes.strip(),
                    "items": st.session_state.cart.copy(),
                    "subtotal": subtotal,
                    "delivery_fee": delivery_fee,
                    "total": total,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                order_id = save_order(order)
                st.session_state.cart = []
                st.success(f"تم تسجيل طلبك بنجاح. رقم الطلب: {order_id}")
                whatsapp = ''.join(ch for ch in get_setting("whatsapp_number", "") if ch.isdigit())
                if whatsapp:
                    lines = [f"طلب جديد رقم {order_id}", f"الاسم: {order['name']}", f"الهاتف: {order['phone']}", f"العنوان: {order['address']}", "تفاصيل الطلب:"]
                    lines.extend([f"- {item['name']} × 1 = {item['price']} جنيه" for item in order['items']])
                    lines += [f"قيمة الأصناف: {subtotal:.2f} جنيه", f"التوصيل: {delivery_fee:.2f} جنيه", f"الإجمالي: {total:.2f} جنيه", f"ملاحظات: {order['notes'] or 'لا يوجد'}"]
                    st.link_button("📲 إرسال الطلب عبر واتساب", f"https://wa.me/{whatsapp}?text={quote(chr(10).join(lines))}", use_container_width=True)

# =========================================================
# لوحة الإدارة — الطلبات والإعدادات والتقييمات
# =========================================================
elif st.session_state.page == "admin":
    st.markdown("## 🔐 لوحة إدارة المطعم")
    if not st.session_state.get("admin_authenticated", False):
        with st.form("admin_login_form"):
            entered_password = st.text_input("كلمة مرور الإدارة", type="password")
            login_clicked = st.form_submit_button("تسجيل الدخول", type="primary", use_container_width=True)
        if login_clicked:
            if ADMIN_PASSWORD == "change-this-password":
                st.warning("غيّر ADMIN_PASSWORD في متغيرات البيئة قبل استخدام لوحة الإدارة فعليًا.")
            if entered_password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة.")
    else:
        if st.button("تسجيل الخروج"):
            st.session_state.admin_authenticated = False
            st.rerun()
        tab_orders, tab_settings, tab_feedback = st.tabs(["📦 الطلبات", "⚙️ الإعدادات", "💬 آراء العملاء"])
        with tab_orders:
            with db_connect() as conn:
                rows = conn.execute("SELECT * FROM orders ORDER BY id DESC LIMIT 500").fetchall()
            if not rows:
                st.info("لا توجد طلبات حتى الآن.")
            else:
                st.metric("إجمالي الطلبات", len(rows))
                for row in rows:
                    with st.container(border=True):
                        st.markdown(f"### الطلب #{row['id']} — {row['customer_name']}")
                        st.write(f"📞 {row['phone']} | 📍 {row['address']}")
                        st.write(f"التاريخ: {row['created_at']} | الإجمالي: {row['total']:.2f} جنيه")
                        st.write(f"ملاحظات: {row['notes'] or 'لا يوجد'}")
                        for item in json.loads(row['items_json']):
                            st.write(f"• {item['name']} — {item['price']} جنيه")
                        status_options = ["جديد", "قيد التجهيز", "خرج للتوصيل", "مكتمل", "ملغي"]
                        current_status = row['status'] if row['status'] in status_options else "جديد"
                        new_status = st.selectbox("حالة الطلب", status_options, index=status_options.index(current_status), key=f"status_{row['id']}")
                        if st.button("حفظ حالة الطلب", key=f"save_status_{row['id']}"):
                            with db_connect() as conn:
                                conn.execute("UPDATE orders SET status=? WHERE id=?", (new_status, row['id']))
                            st.success("تم تحديث الحالة.")
                            st.rerun()
                export = [{"رقم الطلب": r['id'], "العميل": r['customer_name'], "الهاتف": r['phone'], "العنوان": r['address'], "الإجمالي": r['total'], "الحالة": r['status'], "التاريخ": r['created_at']} for r in rows]
                import pandas as pd
                st.download_button("📥 تنزيل الطلبات CSV", pd.DataFrame(export).to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"), file_name="wadi_alnile_orders.csv", mime="text/csv")
        with tab_settings:
            current_fee = float(get_setting("delivery_fee", DELIVERY_FEE_DEFAULT) or 0)
            current_whatsapp = get_setting("whatsapp_number", "")
            with st.form("admin_settings_form"):
                fee = st.number_input("رسوم التوصيل (جنيه)", min_value=0.0, value=current_fee, step=5.0)
                whatsapp_number = st.text_input("رقم واتساب المطعم بصيغة دولية، مثال 2010XXXXXXXX", value=current_whatsapp)
                save_settings_clicked = st.form_submit_button("حفظ الإعدادات", type="primary")
            if save_settings_clicked:
                set_setting("delivery_fee", fee)
                set_setting("whatsapp_number", whatsapp_number.strip())
                st.success("تم حفظ الإعدادات.")
                st.rerun()
        with tab_feedback:
            with db_connect() as conn:
                feedback_rows = conn.execute("SELECT * FROM feedback ORDER BY id DESC LIMIT 500").fetchall()
            if feedback_rows:
                st.dataframe([dict(r) for r in feedback_rows], use_container_width=True, hide_index=True)
            else:
                st.info("لا توجد تقييمات أو رسائل مسجلة حتى الآن.")

# =========================================================
# العروض
# =========================================================
elif st.session_state.page == "offers":
    st.markdown("## 🎁 عروض وادي النيل")
    st.caption("اختر العرض المناسب لك واستمتع بتجربة مميزة.")

    cols = st.columns(3)
    for i, offer in enumerate(OFFERS):
        with cols[i]:
            with st.container(border=True):
                offer_images = [
                    "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?auto=format&fit=crop&w=900&q=80",
                    "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=900&q=80",
                ]
                st.image(offer_images[i], use_container_width=True)
                st.markdown(f"## {offer['icon']}")
                st.markdown(f"### {offer['title']}")
                st.write(offer["desc"])
                st.markdown(f"### 🟡 {offer['price']}")

                if st.button(
                    f"🛒 اطلب {offer['title']}",
                    key=f"offer_{i}",
                    use_container_width=True,
                ):
                    st.success(
                        f"تم اختيار {offer['title']}. "
                        f"للتأكيد اتصل بالخط الساخن {HOTLINE}."
                    )

# =========================================================
# مساعد الوجبات
# =========================================================
elif st.session_state.page == "smart":
    st.markdown("## 🤖 مساعد الوجبات الذكي")
    st.info("أخبرنا بما تفضله وسنقترح لك وجبة مناسبة.")

    preference = st.selectbox(
        "ما الذي تفضله؟",
        ["جمبري", "أسماك مشوية", "طواجن", "وجبة عائلية", "ساندويتش"],
    )

    appetite = st.selectbox(
        "حجم الوجبة",
        ["فرد واحد", "شخصان", "عائلة"],
    )

    if st.button("✨ اقترح لي وجبة", use_container_width=True, type="primary"):
        recommendations = {
            "جمبري": "🍤 ننصحك بوجبة جمبري مع الأرز والسلطة.",
            "أسماك مشوية": "🐟 ننصحك بالدّنيس أو القاروص المشوي.",
            "طواجن": "🍲 ننصحك بطاجن السي فود المميز.",
            "وجبة عائلية": "🍱 ننصحك بوجبة العائلة البحرية.",
            "ساندويتش": "🥪 ننصحك بساندويتش الجمبري.",
        }
        st.success(f"{recommendations[preference]} — الاختيار المناسب: {appetite}")

# =========================================================
# الفروع
# =========================================================
elif st.session_state.page == "branches":
    st.markdown("## 📍 فروع وادي النيل")
    st.caption("تعرف على فروعنا.")

    for start in range(0, len(BRANCHES), 2):
        cols = st.columns(2)
        for idx, branch in enumerate(BRANCHES[start:start + 2]):
            with cols[idx]:
                with st.container(border=True):
                    st.markdown(f"### {branch['icon']} {branch['name']}")
                    st.write(f"📍 {branch['address']}")
                    st.write(f"☎ {branch['phone']}")

                    st.link_button(
                        "📞 الاتصال بالفرع",
                        f"tel:{branch['phone']}",
                        use_container_width=True,
                    )

# =========================================================
# التقييمات
# =========================================================
elif st.session_state.page == "reviews":
    st.markdown("## ⭐ تقييمات وآراء العملاء")
    st.caption("شاركنا رأيك وساعدنا على التطوير.")

    reviews = [
        ("محمد أحمد", "تجربة ممتازة والطعام طازج جدًا والخدمة رائعة.", 5),
        ("سارة محمود", "من أفضل أماكن الأسماك التي جربتها.", 5),
        ("أحمد علي", "الطعم ممتاز والأسعار مناسبة.", 4),
    ]

    for name, review, stars in reviews:
        with st.container(border=True):
            st.markdown(f"**👤 {name}**")
            st.markdown("⭐" * stars)
            st.write(review)

    st.divider()
    st.markdown("### ✍️ أضف تقييمك")

    customer_name = st.text_input("الاسم", key="review_name")
    rating = st.select_slider(
        "التقييم",
        options=[1, 2, 3, 4, 5],
        value=5,
        format_func=lambda x: "⭐" * x,
    )
    review_text = st.text_area("رأيك في تجربتك", key="review_text")

    if st.button("⭐ إرسال التقييم", use_container_width=True):
        if not customer_name.strip() or not review_text.strip():
            st.warning("من فضلك أدخل الاسم والتقييم.")
        else:
            with db_connect() as conn:
                conn.execute("INSERT INTO feedback(kind, customer_name, rating, message, created_at) VALUES(?,?,?,?,?)", ("تقييم", customer_name.strip(), int(rating), review_text.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            st.success(f"شكرًا {customer_name} على تقييمك ⭐ — تقييمك {rating}/5")

# =========================================================
# الشكاوى والاقتراحات
# =========================================================
elif st.session_state.page == "complaints":
    st.markdown("## 📝 الشكاوى والاقتراحات")
    st.caption("رأيك يهمنا ويساعدنا على تقديم خدمة أفضل.")

    st.info(
        "💬 يمكنك إرسال شكوى أو اقتراح أو ملاحظة أو شكر وتقدير، "
        "وسيتم التعامل معها بعناية."
    )

    name = st.text_input("الاسم", key="complaint_name")
    phone = st.text_input("رقم الهاتف", key="complaint_phone")

    complaint_type = st.selectbox(
        "نوع الرسالة",
        ["شكوى", "اقتراح", "ملاحظة", "شكر وتقدير"],
    )

    branch = st.selectbox(
        "الفرع",
        ["اختر الفرع"] + [b["name"] for b in BRANCHES],
    )

    message = st.text_area("اكتب رسالتك", height=180, key="complaint_message")

    if st.button("📨 إرسال الرسالة", use_container_width=True, type="primary"):
        if not name.strip() or not phone.strip() or not message.strip():
            st.warning("من فضلك أكمل البيانات المطلوبة.")
        elif branch == "اختر الفرع":
            st.warning("من فضلك اختر الفرع.")
        else:
            with db_connect() as conn:
                conn.execute("INSERT INTO feedback(kind, customer_name, phone, branch, message, created_at) VALUES(?,?,?,?,?,?)", (complaint_type, name.strip(), phone.strip(), branch, message.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            st.success(f"تم حفظ {complaint_type} بنجاح. شكرًا لتواصلك معنا.")

# =========================================================
# الطلبات المسجلة في الجلسة
# =========================================================
with db_connect() as conn:
    recent_orders = conn.execute("SELECT id, customer_name, total, status, created_at FROM orders ORDER BY id DESC LIMIT 5").fetchall()
if recent_orders:
    with st.expander("📦 أحدث الطلبات المسجلة"):
        for order in recent_orders:
            st.write(f"الطلب #{order['id']} — {order['customer_name']} — {order['total']:.2f} جنيه — {order['status']} — {order['created_at']}")

# =========================================================
# الفوتر
# =========================================================
st.divider()
footer_left, footer_right = st.columns([2, 1])
with footer_left:
    st.markdown("### 🦐 سلسلة مطاعم أسماك وادي النيل")
    st.caption("طعم البحر… بطعم مصري أصيل | جودة نهتم بها في كل طبق")
with footer_right:
    st.markdown(f"### ☎ {HOTLINE}")
    st.caption("يسعدنا استقبال اتصالاتكم")
st.caption("© منصة وادي النيل الرقمية")