# -*- coding: utf-8 -*-
"""موقع مطاعم أسماك وادي النيل - تطبيق Streamlit مستقل."""
from pathlib import Path
from urllib.parse import quote
import sqlite3
import streamlit as st

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
DB_PATH = BASE_DIR / "wadi_nile.db"
HOTLINE = "01103949998"
WHATSAPP = "201103949998"

st.set_page_config(page_title="أسماك وادي النيل | المنيو والطلبات", page_icon="🐟", layout="wide", initial_sidebar_state="collapsed")

CATEGORIES = ["الكل", "المقبلات الساخنة", "المقبلات الباردة", "شوربات", "أرز وادي النيل الخاص", "فخارات", "أطباق وادي النيل الخاصة", "وجبات فردية", "الساندوتشات", "باستا", "وجبة الأطفال", "مشروبات"]
SEED_PRODUCTS = [
    (1,"بطاطس ودجز","المقبلات الساخنة",35,"بطاطس مقرمشة متبلة بالأعشاب.","assets/dish_01.png"),
    (2,"أصابع موزاريلا","المقبلات الساخنة",45,"أصابع جبن ذهبية ومقرمشة.","assets/dish_02.png"),
    (3,"سمبوسة سي فود","المقبلات الساخنة",55,"رقائق مقرمشة بحشوة المأكولات البحرية.","assets/dish_03.png"),
    (4,"سلطة طحينة","المقبلات الباردة",20,"طحينة طازجة بالليمون والثوم.","assets/dish_04.png"),
    (5,"سلطة خضراء","المقبلات الباردة",25,"خضروات طازجة يومياً.","assets/dish_05.png"),
    (6,"شوربة سي فود بالكريمة","شوربات",85,"جمبري وسبيط وقطع سمك بمرق كريمي غني.","assets/dish_06.png"),
    (7,"شوربة سمك صافي","شوربات",60,"شوربة سمك مصرية بالتوابل والكزبرة.","assets/dish_07.png"),
    (8,"أرز وادي النيل بالجمبري","أرز وادي النيل الخاص",95,"أرز صيادية مع جمبري متبل.","assets/dish_08.png"),
    (9,"أرز صيادية سي فود","أرز وادي النيل الخاص",90,"أرز صيادية وقطع متنوعة من السي فود.","assets/dish_09.png"),
    (10,"طاجن سي فود بالكريمة","فخارات",155,"مأكولات بحرية بصوص أبيض وجبن موزاريلا.","assets/dish_10.png"),
    (11,"طاجن جمبري بالصلصة","فخارات",145,"جمبري بصلصة الطماطم والثوم في الفرن.","assets/dish_11.png"),
    (12,"ميكس جريل بحري","أطباق وادي النيل الخاصة",260,"فيليه وجمبري وسبيط مع أرز وسلطة.","assets/dish_12.png"),
    (13,"الصينية الملكية العائلية","أطباق وادي النيل الخاصة",650,"تشكيلة بحرية عائلية؛ السعر استرشادي قابل للتعديل.","assets/dish_13.png"),
    (14,"وجبة فيليه سمك","وجبات فردية",150,"فيليه مقرمش مع أرز وسلطة وطحينة.","assets/dish_14.png"),
    (15,"ساندويتش جمبري مقرمش","الساندوتشات",85,"جمبري مقرمش مع صوص خاص وخبز طازج.","assets/dish_15.png"),
    (16,"ساندويتش فياجرا وادي النيل","الساندوتشات",120,"خلطة سي فود مميزة داخل ساندويتش طازج.","assets/dish_16.png"),
    (17,"باستا سي فود","باستا",165,"باستا بقطع السي فود وصوص كريمي.","assets/dish_17.png"),
    (18,"وجبة الأطفال","وجبة الأطفال",95,"وجبة صغيرة مناسبة للأطفال.","assets/dish_18.png"),
    (19,"ليمون بالنعناع","مشروبات",35,"ليمون طازج بالنعناع.","assets/dish_19.png"),
    (20,"مشروب غازي","مشروبات",25,"مشروب غازي بارد.","assets/dish_20.png"),
]


def db_connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db_connect() as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL,
            price REAL NOT NULL DEFAULT 0, description TEXT DEFAULT '', image TEXT DEFAULT '', active INTEGER DEFAULT 1)""")
        conn.execute("""CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT DEFAULT (datetime('now','localtime')),
            customer_name TEXT, phone TEXT, address TEXT, branch TEXT, items TEXT, total REAL, status TEXT DEFAULT 'جديد')""")
        conn.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            conn.executemany("INSERT INTO products(id,name,category,price,description,image,active) VALUES(?,?,?,?,?,?,1)", SEED_PRODUCTS)
        if not conn.execute("SELECT value FROM settings WHERE key='admin_password'").fetchone():
            conn.execute("INSERT OR IGNORE INTO settings(key,value) VALUES('admin_password','wadi2026')")
        conn.commit()


def get_products(active_only=True):
    with db_connect() as conn:
        sql = "SELECT * FROM products" + (" WHERE active=1" if active_only else "") + " ORDER BY id"
        return [dict(x) for x in conn.execute(sql).fetchall()]


def money(value):
    return f"{float(value):,.2f} ج.م"


def image_path(value):
    p = Path(str(value or ""))
    if not p.is_absolute():
        p = BASE_DIR / p
    return p if p.exists() else ASSETS_DIR / "dish_default.png"


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    html, body, [class*="css"], .stApp {font-family:'Cairo',sans-serif;}
    .stApp {background:#f8fafc; direction:rtl;}
    [data-testid="stHeader"] {background:rgba(248,250,252,.95);}
    .block-container {padding-top:1rem; padding-bottom:2.5rem; max-width:1450px;}
    [data-testid="stSidebar"] {direction:rtl;}
    .topline {background:#0f172a;color:#cffafe;padding:9px 18px;border-radius:12px;margin-bottom:12px;font-size:13px;}
    .brandbox {background:linear-gradient(115deg,#0f172a,#1e3a8a 62%,#0e7490);color:white;border-radius:22px;padding:26px 28px;margin:8px 0 20px;box-shadow:0 14px 32px #0f172a20;}
    .brandbox h1 {font-size:clamp(25px,3vw,40px);font-weight:900;margin:0 0 8px;color:white;}
    .brandbox p {color:#cffafe;margin:0;font-size:15px;}
    .section-title {color:#0f172a;font-weight:900;font-size:23px;margin:8px 0 15px;}
    .product-card {background:#fff;border:1px solid #e2e8f0;border-radius:17px;padding:12px;box-shadow:0 5px 18px #0f172a0a;height:100%;}
    .product-name {font-weight:800;color:#0f172a;font-size:16px;min-height:48px;}
    .product-desc {font-size:12px;color:#64748b;min-height:38px;line-height:1.7;}
    .product-price {font-weight:900;color:#075985;font-size:18px;padding-top:5px;}
    .small-note {font-size:12px;color:#64748b;}
    div.stButton > button {border-radius:11px;font-family:'Cairo',sans-serif;font-weight:800;}
    div[data-testid="stHorizontalBlock"] {gap: .8rem;}
    [data-testid="stImage"] img {border-radius:13px;object-fit:cover;}
    .footer {background:#020617;color:#cbd5e1;text-align:center;padding:20px;border-radius:18px;margin-top:30px;}
    </style>
    """, unsafe_allow_html=True)


def add_to_cart(product):
    cart = st.session_state.setdefault("cart", {})
    key = str(product["id"])
    if key in cart:
        cart[key]["qty"] += 1
    else:
        cart[key] = {"id": product["id"], "name": product["name"], "price": float(product["price"]), "qty": 1}


def cart_total():
    return sum(x["price"] * x["qty"] for x in st.session_state.get("cart", {}).values())


def save_order(name, phone, address, branch):
    cart = st.session_state.get("cart", {})
    items_text = " | ".join(f"{x['name']} × {x['qty']}" for x in cart.values())
    with db_connect() as conn:
        conn.execute("INSERT INTO orders(customer_name,phone,address,branch,items,total,status) VALUES(?,?,?,?,?,?,?)",
                     (name, phone, address, branch, items_text, cart_total(), "جديد"))
        conn.commit()


def render_cart():
    st.markdown("### 🛒 سلة الطلبات")
    cart = st.session_state.setdefault("cart", {})
    if not cart:
        st.info("السلة فارغة حالياً. اختر وجباتك من المنيو.")
    else:
        for key in list(cart.keys()):
            item = cart[key]
            a, b, c = st.columns([5, 2, 2])
            with a:
                st.write(f"**{item['name']}**")
                st.caption(money(item['price']))
            with b:
                st.write(f"الكمية: {item['qty']}")
            with c:
                if st.button("➖", key=f"minus_{key}"):
                    item['qty'] -= 1
                    if item['qty'] <= 0: del cart[key]
                    st.rerun()
                if st.button("➕", key=f"plus_{key}"):
                    item['qty'] += 1
                    st.rerun()
        st.divider()
        st.markdown(f"### الإجمالي: :blue[{money(cart_total())}]")
        with st.form("checkout_form", clear_on_submit=False):
            name = st.text_input("اسم العميل *")
            phone = st.text_input("رقم الهاتف *", max_chars=15)
            address = st.text_area("عنوان التوصيل بالتفصيل *", height=75)
            branch = st.selectbox("الفرع", ["فرع المهندسين", "فرع التجمع الخامس", "فرع السادس من أكتوبر"])
            submit = st.form_submit_button("تجهيز الطلب عبر واتساب", type="primary", use_container_width=True)
            if submit:
                if not name.strip() or not phone.strip() or not address.strip():
                    st.error("يرجى استكمال الاسم ورقم الهاتف والعنوان.")
                else:
                    save_order(name.strip(), phone.strip(), address.strip(), branch)
                    lines = ["🛒 طلب جديد من موقع أسماك وادي النيل", "", f"الاسم: {name}", f"الهاتف: {phone}", f"العنوان: {address}", f"الفرع: {branch}", "", "الأصناف:"]
                    for item in cart.values():
                        lines.append(f"- {item['name']} × {item['qty']} = {money(item['price'] * item['qty'])}")
                    lines += ["", f"الإجمالي: {money(cart_total())}"]
                    url = f"https://wa.me/{WHATSAPP}?text={quote(chr(10).join(lines))}"
                    st.success("تم حفظ الطلب في قاعدة البيانات. اضغط الرابط لفتح واتساب وإرسال الطلب.")
                    st.link_button("فتح واتساب لإرسال الطلب", url, use_container_width=True)
                    st.session_state["cart"] = {}


def admin_panel():
    st.markdown('<div class="section-title">⚙️ لوحة إدارة الموقع</div>', unsafe_allow_html=True)
    with db_connect() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key='admin_password'").fetchone()
        correct = row[0] if row else "wadi2026"
    if not st.session_state.get("admin_ok"):
        with st.form("admin_login"):
            pwd = st.text_input("كلمة مرور الإدارة", type="password")
            if st.form_submit_button("دخول لوحة الإدارة", use_container_width=True):
                if pwd == correct:
                    st.session_state["admin_ok"] = True
                    st.rerun()
                else:
                    st.error("كلمة المرور غير صحيحة.")
        st.caption("كلمة المرور الافتراضية لأول تشغيل: wadi2026 — غيّرها من إعدادات الإدارة.")
        return
    tab1, tab2, tab3 = st.tabs(["إدارة المنتجات", "الطلبات", "الإعدادات"])
    with tab1:
        products = get_products(active_only=False)
        for p in products:
            with st.expander(f"{p['name']} — {money(p['price'])}"):
                with st.form(f"edit_{p['id']}"):
                    name = st.text_input("اسم المنتج", p['name'])
                    category = st.selectbox("القسم", CATEGORIES[1:], index=(CATEGORIES[1:].index(p['category']) if p['category'] in CATEGORIES[1:] else 0))
                    price = st.number_input("السعر بالجنيه", min_value=0.0, value=float(p['price']), step=5.0)
                    desc = st.text_area("الوصف", p['description'] or "")
                    img = st.text_input("مسار الصورة (محلي أو رابط https)", p['image'] or "assets/dish_default.png")
                    active = st.checkbox("إظهار المنتج في المنيو", value=bool(p['active']))
                    if st.form_submit_button("حفظ التعديلات"):
                        with db_connect() as conn:
                            conn.execute("UPDATE products SET name=?,category=?,price=?,description=?,image=?,active=? WHERE id=?", (name,category,price,desc,img,int(active),p['id']))
                            conn.commit()
                        st.success("تم حفظ المنتج.")
                        st.rerun()
        st.markdown("#### إضافة منتج جديد")
        with st.form("new_product"):
            new_name = st.text_input("اسم المنتج الجديد")
            new_cat = st.selectbox("قسم المنتج الجديد", CATEGORIES[1:], key="newcat")
            new_price = st.number_input("السعر", min_value=0.0, value=50.0, step=5.0, key="newprice")
            new_desc = st.text_area("الوصف", key="newdesc")
            new_img = st.text_input("مسار الصورة", "assets/dish_default.png", key="newimg")
            if st.form_submit_button("إضافة المنتج"):
                if not new_name.strip(): st.error("اكتب اسم المنتج أولاً.")
                else:
                    with db_connect() as conn:
                        conn.execute("INSERT INTO products(name,category,price,description,image,active) VALUES(?,?,?,?,?,1)", (new_name.strip(),new_cat,new_price,new_desc,new_img))
                        conn.commit()
                    st.success("تمت إضافة المنتج.")
                    st.rerun()
    with tab2:
        with db_connect() as conn:
            orders = [dict(x) for x in conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()]
        if not orders: st.info("لا توجد طلبات حتى الآن.")
        for o in orders:
            with st.expander(f"طلب #{o['id']} | {o['customer_name']} | {money(o['total'])} | {o['status']}"):
                st.write(f"**التاريخ:** {o['created_at']}  ")
                st.write(f"**الهاتف:** {o['phone']}  ")
                st.write(f"**العنوان:** {o['address']}  ")
                st.write(f"**الفرع:** {o['branch']}  ")
                st.write(f"**الأصناف:** {o['items']}  ")
                status = st.selectbox("حالة الطلب", ["جديد", "قيد التجهيز", "خرج للتوصيل", "تم التسليم", "ملغي"], index=["جديد", "قيد التجهيز", "خرج للتوصيل", "تم التسليم", "ملغي"].index(o['status']) if o['status'] in ["جديد", "قيد التجهيز", "خرج للتوصيل", "تم التسليم", "ملغي"] else 0, key=f"status_{o['id']}")
                if st.button("تحديث الحالة", key=f"save_status_{o['id']}"):
                    with db_connect() as conn:
                        conn.execute("UPDATE orders SET status=? WHERE id=?", (status,o['id']))
                        conn.commit()
                    st.success("تم تحديث الحالة.")
                    st.rerun()
    with tab3:
        st.write("تغيير كلمة مرور لوحة الإدارة")
        with st.form("change_pwd"):
            old = st.text_input("كلمة المرور الحالية", type="password")
            new = st.text_input("كلمة المرور الجديدة", type="password")
            confirm = st.text_input("تأكيد كلمة المرور الجديدة", type="password")
            if st.form_submit_button("تغيير كلمة المرور"):
                if old != correct: st.error("كلمة المرور الحالية غير صحيحة.")
                elif len(new) < 8: st.error("اجعل كلمة المرور 8 أحرف على الأقل.")
                elif new != confirm: st.error("تأكيد كلمة المرور غير مطابق.")
                else:
                    with db_connect() as conn:
                        conn.execute("UPDATE settings SET value=? WHERE key='admin_password'", (new,))
                        conn.commit()
                    st.success("تم تغيير كلمة المرور.")
                    st.session_state["admin_ok"] = False
                    st.rerun()
        if st.button("تسجيل الخروج من الإدارة"):
            st.session_state["admin_ok"] = False
            st.rerun()


init_db()
inject_css()
st.markdown(f'<div class="topline">📞 الخط الساخن: <b style="color:#fbbf24">{HOTLINE}</b> <span style="float:left">توصيل الطلبات عبر واتساب 🚚</span></div>', unsafe_allow_html=True)
st.markdown('''<div class="brandbox"><h1>🐟 أسماك وادي النيل</h1><p>أطزج مأكولات بحرية في مصر.. من البحر لمائدتك مباشرة 🦐</p><p style="margin-top:9px">صواني ملكية • طواجن فخار • أطباق سي فود • مذاق مصري أصيل</p></div>''', unsafe_allow_html=True)

page = st.radio("التنقل", ["المنيو والطلبات", "فروعنا", "عن وادي النيل", "لوحة الإدارة"], horizontal=True, label_visibility="collapsed")
if page == "المنيو والطلبات":
    products = get_products()
    search = st.text_input("🔎 ابحث عن منتج أو وجبة...", placeholder="مثال: جمبري، شوربة، طاجن", key="search_products")
    selected_category = st.radio("الأقسام", CATEGORIES, horizontal=True, label_visibility="collapsed", key="selected_category")
    filtered = [p for p in products if (selected_category == "الكل" or p['category'] == selected_category) and (search.strip().casefold() in (p['name'] + " " + (p['description'] or "") + " " + p['category']).casefold())]
    st.markdown(f'<div class="section-title">🍽️ {selected_category if selected_category != "الكل" else "قائمة الطعام"} <span style="font-size:13px;color:#64748b;font-weight:600">({len(filtered)} منتج)</span></div>', unsafe_allow_html=True)
    left, right = st.columns([2.15, 1], gap="large")
    with left:
        if not filtered: st.warning("لا توجد منتجات مطابقة للبحث.")
        else:
            cols = st.columns(3, gap="medium")
            for idx, p in enumerate(filtered):
                with cols[idx % 3]:
                    st.markdown('<div class="product-card">', unsafe_allow_html=True)
                    st.image(str(image_path(p['image'])), use_container_width=True)
                    st.markdown(f'<div class="product-name">{p["name"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-desc">{p["description"] or "وجبة شهية من مطاعم أسماك وادي النيل."}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="product-price">{money(p["price"])}</div>', unsafe_allow_html=True)
                    if st.button("➕ إضافة للسلة", key=f"add_{p['id']}", use_container_width=True, type="primary"):
                        add_to_cart(p)
                        st.toast(f"تمت إضافة {p['name']} إلى السلة")
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
    with right:
        with st.container(border=True): render_cart()
elif page == "فروعنا":
    st.markdown('<div class="section-title">📍 فروع مطاعم أسماك وادي النيل</div>', unsafe_allow_html=True)
    branches = [("فرع المهندسين","82 شارع وادي النيل، الجيزة."),("فرع التجمع الخامس","الحي الثالث، بجوار مول عنابة، القاهرة الجديدة."),("فرع السادس من أكتوبر","محور 26 يوليو، بجوار محطة بنزين شيل أوت.")]
    cols = st.columns(3)
    for i,(name,address) in enumerate(branches):
        with cols[i]:
            st.markdown(f"### {name}")
            st.write(address)
            st.caption(f"للطلب والاستفسار: {HOTLINE}")
            st.link_button("اتصال بالخط الساخن", f"tel:{HOTLINE}", use_container_width=True)
    st.info("يرجى تأكيد العنوان ومواعيد العمل وأرقام الفروع من إدارة المطعم قبل نشر الموقع رسمياً.")
elif page == "عن وادي النيل":
    st.markdown('<div class="section-title">🌊 حكايتنا في وادي النيل</div>', unsafe_allow_html=True)
    st.write("نقدم تجربة مأكولات بحرية تجمع بين الطابع المصري الأصيل والتقديم العصري. تشمل القائمة الأسماك والجمبري والسي فود والطواجن والأرز والوجبات الفردية.")
    st.write("نحرص على أن تكون تفاصيل الأصناف والأسعار واضحة للعميل، ويمكن لفريق الإدارة تحديث المنيو من لوحة الإدارة.")
    st.warning("الأسعار والأوصاف والعناوين المدرجة في النسخة التجريبية بيانات مبدئية ويجب مراجعتها واعتمادها من المطعم قبل الاستخدام التجاري.")
else:
    admin_panel()

st.markdown(f'<div class="footer"><b style="color:white">مطاعم أسماك وادي النيل © 2026 — جميع الحقوق محفوظة</b><br>الخط الساخن: <span style="color:#22d3ee;font-weight:800">{HOTLINE}</span><br><span style="font-size:12px">تصميم تجريبي قابل للتخصيص</span></div>', unsafe_allow_html=True)
