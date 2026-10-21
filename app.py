import sqlite3
import urllib.parse
import streamlit as st

# إعدادات الصفحة والتصميم العام
st.set_page_config(
    page_title="موقع مطاعم أسماك وادي النيل | Wadi Al Nile Seafood",
    page_icon="🦐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# نظام الترجمة البسيط (عربي / English)
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

translations = {
    "ar": {
        "title": "🌊 مطاعم أسماك وادي النيل 🌊",
        "hotline": "الخط الساخن للطلب والتوصيل السريع: 19974",
        "nav_menu": "🏠 قائمة الطعام",
        "nav_cart": "🛒 سلة المشتريات",
        "nav_admin": "🔐 لوحة التحكم",
        "nav_branches": "📍 الفروع وتواصل معنا",
        "hero_title": "طزاجة البحر على أصولها في مطاعم وادي النيل",
        "hero_desc": "استمتع بألذ أطباق الأسماك الطازجة، الجمبري الجامبو، الطواجن الساخنة، والعروض العائلية المميزة",
        "offers_title": "🔥 عروض وادي النيل المميزة",
        "featured_title": "⭐ الأكثر طلباً",
        "menu_title": "🍽️ قائمة الطعام الكاملة",
        "all_cats": "الكل",
        "search": "🔍 بحث عن صنف معين...",
        "add_to_cart": "أضف للسلة 🛒",
        "price_label": "جنيه مصري",
        "cart_title": "سلة المشتريات ومراجعة الطلب",
        "cart_empty": "سلة المشتريات فارغة حالياً. انتقل إلى قائمة الطعام لاختيار أطباقك المفضلة!",
        "total": "إجمالي الفاتورة",
        "checkout_title": "بيانات التوصيل وإتمام الطلب",
        "name_label": "الاسم الكريم:",
        "phone_label": "رقم الهاتف:",
        "address_label": "عنوان التوصيل بالتفصيل:",
        "submit_order": "تأكيد وحفظ الطلب 🚀",
        "wa_btn": "💬 إرسال تفاصيل الطلب عبر واتساب للمطعم",
        "branches_title": "فروع مطاعم أسماك وادي النيل",
        "branch_giza": "فرع الجيزة الرئيسي",
        "branch_cairo": "فرع القاهرة",
        "footer": "© 2026 مطاعم أسماك وادي النيل - جميع الحقوق محفوظة | الخط الساخن: 19974"
    },
    "en": {
        "title": "🌊 Wadi Al Nile Seafood Restaurants 🌊",
        "hotline": "Hotline for Ordering & Fast Delivery: 19974",
        "nav_menu": "🏠 Menu",
        "nav_cart": "🛒 Cart",
        "nav_admin": "🔐 Admin Dashboard",
        "nav_branches": "📍 Branches & Contact",
        "hero_title": "Authentic Seafood Freshness at Wadi Al Nile",
        "hero_desc": "Enjoy the finest fresh fish, jumbo shrimp, hot clay pots, and special family offers",
        "offers_title": "🔥 Special Wadi Al Nile Offers",
        "featured_title": "⭐ Best Sellers",
        "menu_title": "🍽️ Full Menu",
        "all_cats": "All",
        "search": "🔍 Search for a dish...",
        "add_to_cart": "Add to Cart 🛒",
        "price_label": "EGP",
        "cart_title": "Shopping Cart & Order Review",
        "cart_empty": "Your cart is empty. Visit the menu to choose your favorite dishes!",
        "total": "Total Amount",
        "checkout_title": "Delivery Information & Checkout",
        "name_label": "Full Name:",
        "phone_label": "Phone Number:",
        "address_label": "Detailed Delivery Address:",
        "submit_order": "Confirm & Save Order 🚀",
        "wa_btn": "💬 Send Order Details via WhatsApp",
        "branches_title": "Wadi Al Nile Restaurant Branches",
        "branch_giza": "Giza Main Branch",
        "branch_cairo": "Cairo Branch",
        "footer": "© 2026 Wadi Al Nile Seafood - All Rights Reserved | Hotline: 19974"
    }
}

t = translations[st.session_state.lang]
rtl_ltr = "rtl" if st.session_state.lang == "ar" else "ltr"
text_align = "right" if st.session_state.lang == "ar" else "left"

# تصميم CSS فاخر وعصري مع دعم اللغتين والتباين العالي
st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

    [data-testid="stSidebar"] {{ display: none; }}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    html, body, [class*="css"] {{
        font-family: 'Cairo', sans-serif !important;
        direction: {rtl_ltr} !important;
        text-align: {text_align} !important;
        background-color: #F8F9FA !important;
        color: #1A202C !important;
    }}

    /* الهيدر الفاخر */
    .site-header {{
        background: linear-gradient(135deg, #0B2545 0%, #134074 100%);
        color: #FFFFFF;
        padding: 35px 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(11, 37, 69, 0.2);
        border-bottom: 5px solid #D4AF37;
    }}
    .site-header h1 {{
        color: #FFFFFF !important;
        font-weight: 900;
        font-size: 2.6rem !important;
        margin-bottom: 8px;
    }}
    .site-header p {{
        color: #E2E8F0 !important;
        font-size: 1.25rem !important;
        font-weight: 700;
        margin: 0;
    }}

    /* البانر الترويجي الفاخر للواجهة الرئيسية */
    .hero-banner {{
        background: linear-gradient(rgba(11, 37, 69, 0.85), rgba(19, 64, 116, 0.85)), url('https://images.unsplash.com/photo-1544025162-d76694265947?w=1200');
        background-size: cover;
        background-position: center;
        color: white;
        padding: 60px 30px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    }}
    .hero-banner h2 {{
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        margin-bottom: 15px;
    }}
    .hero-banner p {{
        color: #F7FAFC !important;
        font-size: 1.3rem !important;
        margin-bottom: 20px;
    }}

    .section-title {{
        color: #0B2545 !important;
        font-weight: 900 !important;
        font-size: 1.8rem !important;
        border-right: 6px solid #D4AF37;
        padding-right: 12px;
        margin-top: 30px;
        margin-bottom: 20px;
    }}

    .stButton>button {{
        background-color: #0B2545 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 2px solid #0B2545 !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        width: 100% !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }}
    .stButton>button:hover {{
        background-color: #D4AF37 !important;
        color: #0B2545 !important;
        border-color: #D4AF37 !important;
        transform: translateY(-2px);
    }}

    /* البطاقات الموحدة الفاخرة */
    .menu-card {{
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        height: 500px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 6px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }}
    .menu-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(11, 37, 69, 0.12);
        border-color: #D4AF37;
    }}
    .menu-img {{
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 15px;
    }}
    .menu-title {{
        color: #0B2545 !important;
        font-weight: 900 !important;
        font-size: 1.35rem !important;
        margin-bottom: 8px;
    }}
    .menu-desc {{
        color: #4A5568 !important;
        font-size: 1.05rem !important;
        line-height: 1.5;
        height: 50px;
        overflow: hidden;
        margin-bottom: 12px;
        font-weight: 600;
    }}
    .price-tag {{
        color: #B8860B !important;
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        background-color: #FDF8E2;
        padding: 8px 15px;
        border-radius: 8px;
        display: inline-block;
        text-align: center;
        width: 100%;
        border: 1px solid #D4AF37;
    }}

    .site-footer {{
        background-color: #0B2545;
        color: #FFFFFF;
        text-align: center;
        padding: 25px;
        border-radius: 14px;
        margin-top: 50px;
        border-top: 5px solid #D4AF37;
        font-weight: 700;
        font-size: 1.15rem;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# قاعدة البيانات التهيئة
def init_db():
    conn = sqlite3.connect("wadi_alnile.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_url TEXT,
            is_featured INTEGER DEFAULT 0,
            is_offer INTEGER DEFAULT 0,
            available INTEGER DEFAULT 1
        )
    """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            phone TEXT,
            address TEXT,
            items_summary TEXT,
            total_price REAL,
            status TEXT DEFAULT 'جديد',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        sample_items = [
            ("عرض العيلة الملكي (سنجاري + جمبري + أرز + شوربة)", "عروض ووجبات", 650.0, "وجبة عائلية متكاملة تشمل صينية سمك سنجاري، كيلو جمبري، أرز صيادية، وشوربة سي فود", "https://images.unsplash.com/photo-1565680314427-a5abbbc49926?w=500", 1, 1),
            ("طاجن سبيط بصل وإسكندراني", "طواجن", 180.0, "طاجن سبيط طازج بالخلطة الإسكندراني المميزة والبهارات الأصلية", "https://images.unsplash.com/photo-1544025162-d76694265947?w=500", 1, 0),
            ("جمبري مشوي عالبوتجاز", "جمبري", 250.0, "جمبري جامبو طازج مشوي بالخلطة الخاصة والليمون والثوم الفاخر", "https://images.unsplash.com/photo-1565680314427-a5abbbc49926?w=500", 1, 0),
            ("سمك دينيس مشوي زيت وليمون", "أسماك طازجة", 220.0, "سمك دينيس بحري طازج مشوي على الفحم أو بالفرن بالزيت والليمون", "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500", 0, 0),
            ("شوربة سي فود كريمة", "شوربات", 120.0, "تشكيلة بحرية غنية بالجمبري والكاليماري والأسماك مع الكريمة الغنية", "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500", 0, 0),
            ("أرز صيادية بالجمبري", "مقبلات وأرز", 65.0, "أرز بني بالبصل المحمر وقطع الجمبري الطازجة والتوابل الشرقية", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500", 0, 0),
        ]
        cursor.executemany("INSERT INTO items (name, category, price, description, image_url, is_featured, is_offer) VALUES (?, ?, ?, ?, ?, ?, ?)", sample_items)
        conn.commit()

    return conn

conn = init_db()
cursor = conn.cursor()

# شريط تبديل اللغة (Language Switcher) في أعلى الشاشة
lang_col1, lang_col2 = st.columns([10, 2])
with lang_col2:
    if st.session_state.lang == "ar":
        if st.button("🇬🇧 English"):
            st.session_state.lang = "en"
            st.rerun()
    else:
        if st.button("🇸🇦 العربية"):
            st.session_state.lang = "ar"
            st.rerun()

# الهيدر الفاخر
st.markdown(
    f"""
    <div class="site-header">
        <h1>{t["title"]}</h1>
        <p>{t["hotline"]}</p>
    </div>
""",
    unsafe_allow_html=True,
)

if "current_page" not in st.session_state:
    st.session_state.current_page = "menu"
if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected_category" not in st.session_state:
    st.session_state.selected_category = t["all_cats"]

# شريط التنقل العلوي
nav_cols = st.columns(4)
with nav_cols[0]:
    if st.button(t["nav_menu"]):
        st.session_state.current_page = "menu"
        st.rerun()
with nav_cols[1]:
    cart_count = sum([item["qty"] for item in st.session_state.cart])
    if st.button(f"{t['nav_cart']} ({cart_count})"):
        st.session_state.current_page = "cart"
        st.rerun()
with nav_cols[2]:
    if st.button(t["nav_admin"]):
        st.session_state.current_page = "admin"
        st.rerun()
with nav_cols[3]:
    if st.button(t["nav_branches"]):
        st.session_state.current_page = "branches"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 1. قائمة الطعام والواجهة الرئيسية
if st.session_state.current_page == "menu":
    st.markdown(
        f"""
        <div class="hero-banner">
            <h2>{t["hero_title"]}</h2>
            <p>{t["hero_desc"]}</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # العروض
    st.markdown(f'<div class="section-title">{t["offers_title"]}</div>', unsafe_allow_html=True)
    cursor.execute("SELECT id, name, category, price, description, image_url FROM items WHERE is_offer = 1 AND available = 1")
    offers = cursor.fetchall()
    
    if offers:
        offer_cols = st.columns(len(offers) if len(offers) <= 3 else 3)
        for idx, offer in enumerate(offers):
            item_id, name, category, price, description, image_url = offer
            with offer_cols[idx % len(offer_cols)]:
                st.markdown(
                    f"""
                    <div class="menu-card" style="border-color: #D4AF37;">
                        <div>
                            <img src="{image_url}" class="menu-img">
                            <div class="menu-title">{name}</div>
                            <div class="menu-desc">{description}</div>
                        </div>
                        <div>
                            <div class="price-tag">{price} {t["price_label"]}</div>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
                if st.button(t["add_to_cart"], key=f"offer_add_{item_id}"):
                    found = False
                    for cart_item in st.session_state.cart:
                        if cart_item["id"] == item_id:
                            cart_item["qty"] += 1
                            found = True
                            break
                    if not found:
                        st.session_state.cart.append({"id": item_id, "name": name, "price": price, "qty": 1})
                    st.success("تمت الإضافة للسلة بنجاح!")
                    st.rerun()

    # الأكثر طلباً
    st.markdown(f'<div class="section-title">{t["featured_title"]}</div>', unsafe_allow_html=True)
    cursor.execute("SELECT id, name, category, price, description, image_url FROM items WHERE is_featured = 1 AND available = 1")
    featured = cursor.fetchall()

    if featured:
        feat_cols = st.columns(3)
        for idx, feat in enumerate(featured):
            item_id, name, category, price, description, image_url = feat
            with feat_cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="menu-card">
                        <div>
                            <img src="{image_url}" class="menu-img">
                            <div class="menu-title">{name}</div>
                            <div class="menu-desc">{description}</div>
                        </div>
                        <div>
                            <div class="price-tag">{price} {t["price_label"]}</div>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
                if st.button(t["add_to_cart"], key=f"feat_add_{item_id}"):
                    found = False
                    for cart_item in st.session_state.cart:
                        if cart_item["id"] == item_id:
                            cart_item["qty"] += 1
                            found = True
                            break
                    if not found:
                        st.session_state.cart.append({"id": item_id, "name": name, "price": price, "qty": 1})
                    st.success("تمت الإضافة للسلة بنجاح!")
                    st.rerun()

    # القائمة الكاملة
    st.markdown(f'<div class="section-title">{t["menu_title"]}</div>', unsafe_allow_html=True)
    
    cursor.execute("SELECT DISTINCT category FROM items WHERE available = 1")
    categories = [row[0] for row in cursor.fetchall()]
    categories.insert(0, t["all_cats"])

    search_query = st.text_input(t["search"], "")

    query = "SELECT id, name, category, price, description, image_url FROM items WHERE available = 1"
    params = []
    if search_query:
        query += " AND name LIKE ?"
        params.append(f"%{search_query}%")

    cursor.execute(query, params)
    items = cursor.fetchall()

    if not items:
        st.info("لا توجد أصناف متاحة حالياً.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(items):
            item_id, name, category, price, description, image_url = item
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class="menu-card">
                        <div>
                            <img src="{image_url}" class="menu-img">
                            <div class="menu-title">{name}</div>
                            <div class="menu-desc">{description}</div>
                        </div>
                        <div>
                            <div class="price-tag">{price} {t["price_label"]}</div>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )
                if st.button(t["add_to_cart"], key=f"add_{item_id}"):
                    found = False
                    for cart_item in st.session_state.cart:
                        if cart_item["id"] == item_id:
                            cart_item["qty"] += 1
                            found = True
                            break
                    if not found:
                        st.session_state.cart.append({"id": item_id, "name": name, "price": price, "qty": 1})
                    st.success("تمت الإضافة للسلة بنجاح!")
                    st.rerun()

# 2. سلة المشتريات وإتمام الطلب
elif st.session_state.current_page == "cart":
    st.markdown(f'<div class="section-title">{t["cart_title"]}</div>', unsafe_allow_html=True)

    if not st.session_state.cart:
        st.warning(t["cart_empty"])
    else:
        total_amount = 0
        updated_cart = []

        for idx, cart_item in enumerate(st.session_state.cart):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"**{cart_item['name']}**")
            with col2:
                st.markdown(f"{cart_item['price']} {t['price_label']}")
            with col3:
                new_qty = st.number_input("الكمية", min_value=1, value=cart_item["qty"], key=f"cart_qty_{idx}")
                cart_item["qty"] = new_qty
            with col4:
                if st.button("حذف", key=f"del_{idx}"):
                    continue

            total_amount += cart_item["price"] * cart_item["qty"]
            updated_cart.append(cart_item)

        st.session_state.cart = updated_cart
        st.markdown(f"<h3>{t['total']}: <span style='color: #B8860B;'>{total_amount:.2f} {t['price_label']}</span></h3>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"<h3>{t['checkout_title']}</h3>", unsafe_allow_html=True)

        with st.form("checkout_form"):
            customer_name = st.text_input(t["name_label"])
            phone = st.text_input(t["phone_label"])
            address = st.text_area(t["address_label"])
            submit_order = st.form_submit_button(t["submit_order"])

            if submit_order:
                if not customer_name or not phone or not address:
                    st.error("الرجاء استكمال جميع بيانات التوصيل.")
                else:
                    items_summary = ", ".join([f"{i['name']} (x{i['qty']})" for i in st.session_state.cart])
                    cursor.execute("INSERT INTO orders (customer_name, phone, address, items_summary, total_price) VALUES (?, ?, ?, ?, ?)", (customer_name, phone, address, items_summary, total_amount))
                    conn.commit()

                    st.success("🎉 تم حفظ طلبك بنجاح!")
                    whatsapp_number = "201000000000"
                    msg_text = f"🚨 *New Order*\n👤 {customer_name}\n📱 {phone}\n📍 {address}\n\n🍽️ {items_summary}\n💰 Total: {total_amount} EGP"
                    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={urllib.parse.quote(msg_text)}"
                    
                    st.markdown(f'<div style="text-align: center; margin-top: 25px;"><a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 1.2rem; display: inline-block;">{t["wa_btn"]}</a></div>', unsafe_allow_html=True)
                    st.session_state.cart = []

# 3. لوحة التحكم
elif st.session_state.current_page == "admin":
    st.markdown('<div class="section-title">🔐 لوحة التحكم الإدارية</div>', unsafe_allow_html=True)
    admin_password = st.text_input("أدخل كلمة مرور الإدارة:", type="password")
    if admin_password == "change-me-now":
        st.success("تم تسجيل الدخول بنجاح.")
        tab1, tab2 = st.tabs(["إدارة القائمة", "الطلبات الواردة"])
        with tab1:
            with st.form("add_item"):
                name = st.text_input("اسم الصنف:")
                cat = st.selectbox("القسم:", ["عروض ووجبات", "طواجن", "جمبري", "أسماك طازجة", "شوربات"])
                price = st.number_input("السعر:", value=100.0)
                desc = st.text_area("الوصف:")
                img = st.text_input("رابط الصورة:", value="https://images.unsplash.com/photo-1544025162-d76694265947?w=500")
                if st.form_submit_button("حفظ الصنف"):
                    cursor.execute("INSERT INTO items (name, category, price, description, image_url) VALUES (?, ?, ?, ?, ?)", (name, cat, price, desc, img))
                    conn.commit()
                    st.success("تمت الإضافة بنجاح!")
                    st.rerun()
        with tab2:
            cursor.execute("SELECT id, customer_name, phone, address, items_summary, total_price, status FROM orders ORDER BY id DESC")
            for o in cursor.fetchall():
                st.write(f"طلب #{o[0]} - {o[1]} | الإجمالي: {o[5]} ج.م | الحالة: {o[6]}")

# 4. الفروع
elif st.session_state.current_page == "branches":
    st.markdown(f'<div class="section-title">{t["branches_title"]}</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="background: white; padding: 25px; border-radius: 14px; border: 1px solid #E2E8F0;"><h3>فرع الجيزة الرئيسي</h3><p>شارع الهرم - الخط الساخن: 19974</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="background: white; padding: 25px; border-radius: 14px; border: 1px solid #E2E8F0;"><h3>فرع القاهرة</h3><p>مدينة نصر - الخط الساخن: 19974</p></div>', unsafe_allow_html=True)

# الفوتر الثابت
st.markdown(f'<div class="site-footer">{t["footer"]}</div>', unsafe_allow_html=True)
