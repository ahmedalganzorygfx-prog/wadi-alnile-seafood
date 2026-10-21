import sqlite3
import urllib.parse
import streamlit as st

# إعدادات الصفحة والتصميم العام (إخفاء القائمة الجانبية تماماً)
st.set_page_config(
    page_title="مطاعم أسماك وادي النيل",
    page_icon="🦐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# تصميم CSS متقدم وعصري بالكامل (RTL، تباين عالي، خطوط ظاهرة، وتوحيد البطاقات)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');

    /* إخفاء القائمة الجانبية الافتراضية بالكامل */
    [data-testid="stSidebar"] {
        display: none;
    }

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #F4F6F9 !important;
        color: #111827 !important;
    }

    /* رأس الصفحة الاحترافي الفاخر */
    .hero-banner {
        background: linear-gradient(135deg, #06283D 0%, #1363DF 100%);
        color: #FFFFFF;
        padding: 40px 20px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(6, 40, 61, 0.25);
        border-bottom: 5px solid #FFD700;
    }
    .hero-banner h1 {
        color: #FFFFFF !important;
        font-weight: 900;
        font-size: 2.8rem !important;
        margin-bottom: 10px;
    }
    .hero-banner p {
        color: #E2E8F0 !important;
        font-size: 1.3rem !important;
        font-weight: 700;
    }

    /* تنسيق أزرار Streamlit العامة لتكون واضحة وفخمة */
    .stButton>button {
        background-color: #06283D !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 2px solid #06283D !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        width: 100% !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #FFD700 !important;
        color: #06283D !important;
        border-color: #FFD700 !important;
        transform: translateY(-2px);
    }

    /* تصميم البطاقات بمقاس موحد وثابت تماماً */
    .menu-card {
        background-color: #FFFFFF;
        border: 2px solid #E2E8F0;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        height: 490px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 6px 15px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
    }
    .menu-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(6, 40, 61, 0.15);
        border-color: #1363DF;
    }
    .menu-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    .menu-title {
        color: #06283D !important;
        font-weight: 900 !important;
        font-size: 1.35rem !important;
        margin-bottom: 8px;
    }
    .menu-desc {
        color: #4A5568 !important;
        font-size: 1.05rem !important;
        line-height: 1.5;
        height: 50px;
        overflow: hidden;
        margin-bottom: 12px;
        font-weight: 600;
    }
    .price-tag {
        color: #B7791F !important;
        font-weight: 900 !important;
        font-size: 1.45rem !important;
        background-color: #FEFCBF;
        padding: 8px 15px;
        border-radius: 8px;
        display: inline-block;
        text-align: center;
        width: 100%;
        border: 1px solid #ECC94B;
    }

    h2, h3 {
        color: #06283D !important;
        font-weight: 900 !important;
    }
    label {
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        color: #2D3748 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# إعداد قاعدة البيانات SQLite محلياً
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
            (
                "طاجن سبيط بصل وإسكندراني",
                "طواجن",
                180.0,
                "طاجن سبيط طازج بالخلطة الإسكندراني المميزة والبهارات الأصلية",
                "https://images.unsplash.com/photo-1544025162-d76694265947?w=500",
            ),
            (
                "جمبري مشوي عالبوتجاز",
                "جمبري",
                250.0,
                "جمبري جامبو طازج مشوي بالخلطة الخاصة والليمون والثوم الفاخر",
                "https://images.unsplash.com/photo-1565680314427-a5abbbc49926?w=500",
            ),
            (
                "سمك دينيس مشوي زيت وليمون",
                "أسماك طازجة",
                220.0,
                "سمك دينيس بحري طازج مشوي على الفحم أو بالفرن بالزيت والليمون",
                "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500",
            ),
            (
                "شوربة سي فود كريمة",
                "شوربات",
                120.0,
                "تشكيلة بحرية غنية بالجمبري والكاليماري والأسماك مع الكريمة الغنية",
                "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500",
            ),
            (
                "أرز صيادية بالجمبري",
                "مقبلات وأرز",
                65.0,
                "أرز بني بالبصل المحمر وقطع الجمبري الطازجة والتوابل الشرقية",
                "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500",
            ),
        ]
        cursor.executemany(
            "INSERT INTO items (name, category, price, description, image_url) VALUES (?, ?, ?, ?, ?)",
            sample_items,
        )
        conn.commit()

    return conn


conn = init_db()
cursor = conn.cursor()

# رأس الموقع العصري الفاخر
st.markdown(
    """
    <div class="hero-banner">
        <h1>🌊 مطاعم أسماك وادي النيل 🌊</h1>
        <p>الخط الساخن للطلب والتوصيل السريع: <strong>19974</strong></p>
    </div>
""",
    unsafe_allow_html=True,
)

# تهيئة الذاكرة للتنقل عبر الأزرار
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 الرئيسية وقائمة الطعام"

if "cart" not in st.session_state:
    st.session_state.cart = []

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "الكل"

# أزرار التنقل الرئيسية داخل الصفحة (بديل القائمة الجانبية)
nav_cols = st.columns(4)
with nav_cols[0]:
    if st.button("🏠 قائمة الطعام"):
        st.session_state.current_page = "🏠 الرئيسية وقائمة الطعام"
        st.rerun()
with nav_cols[1]:
    cart_count = sum([item["qty"] for item in st.session_state.cart])
    if st.button(f"🛒 سلة المشتريات ({cart_count})"):
        st.session_state.current_page = "🛒 سلة المشتريات وإتمام الطلب"
        st.rerun()
with nav_cols[2]:
    if st.button("🔐 لوحة التحكم"):
        st.session_state.current_page = "🔐 لوحة التحكم الإدارية"
        st.rerun()
with nav_cols[3]:
    if st.button("📍 الفروع وتواصل معنا"):
        st.session_state.current_page = "📍 الفروع وتواصل معنا"
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# 1. الواجهة الرئيسية وقائمة الطعام
if st.session_state.current_page == "🏠 الرئيسية وقائمة الطعام":
    st.markdown("<h2 style='border-right: 6px solid #FFD700; padding-right: 12px; margin-bottom: 20px;'>قائمة المأكولات البحرية الطازجة</h2>", unsafe_allow_html=True)

    cursor.execute("SELECT DISTINCT category FROM items WHERE available = 1")
    categories = [row[0] for row in cursor.fetchall()]
    categories.insert(0, "الكل")

    st.markdown("<p style='font-size: 1.2rem; font-weight: 800; margin-bottom: 10px;'>اختر القسم:</p>", unsafe_allow_html=True)
    cat_cols = st.columns(len(categories))
    for idx, cat in enumerate(categories):
        with cat_cols[idx]:
            if st.button(cat, key=f"cat_btn_{idx}"):
                st.session_state.selected_category = cat
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    search_query = st.text_input("🔍 بحث عن صنف معين:", "")

    query = "SELECT id, name, category, price, description, image_url FROM items WHERE available = 1"
    params = []
    if st.session_state.selected_category != "الكل":
        query += " AND category = ?"
        params.append(st.session_state.selected_category)
    if search_query:
        query += " AND name LIKE ?"
        params.append(f"%{search_query}%")

    cursor.execute(query, params)
    items = cursor.fetchall()

    if not items:
        st.info("لا توجد أصناف متاحة حالياً تطابق بحثك أو اختيارك.")
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
                            <div class="price-tag">{price} جنيه مصري</div>
                        </div>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                qty = st.number_input(
                    f"الكمية لـ {name}",
                    min_value=1,
                    max_value=20,
                    value=1,
                    key=f"qty_{item_id}",
                    label_visibility="collapsed",
                )
                if st.button(f"أضف للسلة 🛒 ({name})", key=f"add_{item_id}"):
                    found = False
                    for cart_item in st.session_state.cart:
                        if cart_item["id"] == item_id:
                            cart_item["qty"] += qty
                            found = True
                            break
                    if not found:
                        st.session_state.cart.append(
                            {
                                "id": item_id,
                                "name": name,
                                "price": price,
                                "qty": qty,
                            }
                        )
                    st.success(f"تمت إضافة {name} إلى السلة بنجاح!")
                    st.rerun()

# 2. سلة المشتريات وإتمام الطلب
elif st.session_state.current_page == "🛒 سلة المشتريات وإتمام الطلب":
    st.markdown("<h2 style='border-right: 6px solid #FFD700; padding-right: 12px; margin-bottom: 20px;'>سلة المشتريات ومراجعة الطلب</h2>", unsafe_allow_html=True)

    if not st.session_state.cart:
        st.warning("سلة المشتريات فارغة حالياً. انتقل إلى قائمة الطعام لاختيار أطباقك المفضلة!")
    else:
        total_amount = 0
        updated_cart = []

        for idx, cart_item in enumerate(st.session_state.cart):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.markdown(f"<span style='font-size: 1.2rem; font-weight: 800;'>{cart_item['name']}</span>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<span style='font-size: 1.1rem; font-weight: 700;'>السعر: {cart_item['price']} ج.م</span>", unsafe_allow_html=True)
            with col3:
                new_qty = st.number_input(
                    "الكمية",
                    min_value=1,
                    value=cart_item["qty"],
                    key=f"cart_qty_{idx}",
                )
                cart_item["qty"] = new_qty
            with col4:
                if st.button("حذف", key=f"del_{idx}"):
                    continue

            total_amount += cart_item["price"] * cart_item["qty"]
            updated_cart.append(cart_item)

        st.session_state.cart = updated_cart

        st.markdown(f"<h3 style='margin-top: 20px;'>إجمالي الفاتورة: <span style='color: #B7791F;'>{total_amount:.2f} جنيه مصري</span></h3>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("<h3>بيانات التوصيل وإتمام الطلب</h3>", unsafe_allow_html=True)

        with st.form("checkout_form"):
            customer_name = st.text_input("الاسم الكريم:")
            phone = st.text_input("رقم الهاتف:")
            address = st.text_area("عنوان التوصيل بالتفصيل:")
            submit_order = st.form_submit_button("تأكيد وحفظ الطلب 🚀")

            if submit_order:
                if not customer_name or not phone or not address:
                    st.error("الرجاء استكمال جميع بيانات التوصيل (الاسم، الهاتف، العنوان).")
                else:
                    items_summary = ", ".join(
                        [f"{i['name']} (x{i['qty']})" for i in st.session_state.cart]
                    )
                    
                    cursor.execute(
                        "INSERT INTO orders (customer_name, phone, address, items_summary, total_price) VALUES (?, ?, ?, ?, ?)",
                        (customer_name, phone, address, items_summary, total_amount),
                    )
                    conn.commit()

                    st.success("🎉 تم حفظ طلبك بنجاح في نظام المطعم!")
                    
                    whatsapp_number = "201000000000" 
                    
                    msg_text = f"🚨 *طلب جديد من موقع وادي النيل*\n\n" \
                               f"👤 *الاسم:* {customer_name}\n" \
                               f"📱 *الهاتف:* {phone}\n" \
                               f"📍 *العنوان:* {address}\n\n" \
                               f"🍽️ *الأصناف المطلوبة:*\n{items_summary}\n\n" \
                               f"💰 *الإجمالي الكلي:* {total_amount:.2f} ج.م"
                    
                    encoded_msg = urllib.parse.quote(msg_text)
                    whatsapp_url = f"https://wa.me/{whatsapp_number}?text={encoded_msg}"
                    
                    st.markdown(
                        f"""
                        <div style="text-align: center; margin-top: 25px;">
                            <a href="{whatsapp_url}" target="_blank" style="background-color: #25D366; color: white; padding: 15px 30px; border-radius: 10px; text-decoration: none; font-weight: 800; font-size: 1.3rem; display: inline-block; box-shadow: 0 4px 12px rgba(37,211,102,0.4);">
                                💬 إرسال تفاصيل الطلب عبر واتساب للمطعم
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    st.session_state.cart = []

# 3. لوحة التحكم الإدارية
elif st.session_state.current_page == "🔐 لوحة التحكم الإدارية":
    st.markdown("<h2 style='border-right: 6px solid #FFD700; padding-right: 12px; margin-bottom: 20px;'>لوحة التحكم الإدارية</h2>", unsafe_allow_html=True)

    admin_password = st.text_input("أدخل كلمة مرور الإدارة:", type="password")
    if admin_password == "change-me-now":
        st.success("تم تسجيل الدخول بنجاح للصلاحيات الإدارية.")

        admin_tab1, admin_tab2 = st.tabs(["إدارة الأصناف والقائمة", "متابعة الطلبات الواردة"])

        with admin_tab1:
            st.markdown("<h3>إضافة صنف جديد للقائمة</h3>", unsafe_allow_html=True)
            with st.form("add_item_form"):
                new_name = st.text_input("اسم الصنف:")
                
                st.markdown("اختر القسم:")
                cat_options = ["طواجن", "جمبري", "أسماك طازجة", "شوربات", "مقبلات وأرز"]
                selected_new_cat = st.radio("القسم:", cat_options, horizontal=True, label_visibility="collapsed")
                
                new_price = st.number_input("السعر (بالجنيه المصري):", min_value=0.0, value=100.0)
                new_desc = st.text_area("وصف مختصر:")
                new_img = st.text_input(
                    "رابط الصورة (URL):",
                    value="https://images.unsplash.com/photo-1544025162-d76694265947?w=500",
                )
                submitted_item = st.form_submit_button("حفظ وإضافة الصنف")

                if submitted_item:
                    if new_name:
                        cursor.execute(
                            "INSERT INTO items (name, category, price, description, image_url) VALUES (?, ?, ?, ?, ?)",
                            (new_name, selected_new_cat, new_price, new_desc, new_img),
                        )
                        conn.commit()
                        st.success(f"تمت إضافة الصنف '{new_name}' بنجاح!")
                        st.rerun()
                    else:
                        st.error("الرجاء إدخال اسم الصنف على الأقل.")

            st.markdown("---")
            st.markdown("<h3>الأصناف الحالية في القائمة</h3>", unsafe_allow_html=True)
            cursor.execute("SELECT id, name, category, price, available FROM items")
            all_items = cursor.fetchall()
            for it in all_items:
                it_id, it_name, it_cat, it_price, it_avail = it
                c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
                c1.write(f"**{it_name}** ({it_cat})")
                c2.write(f"{it_price} ج.م")
                c3.write("متاح" if it_avail == 1 else "غير متاح")
                if c4.button("حذف", key=f"del_item_{it_id}"):
                    cursor.execute("DELETE FROM items WHERE id = ?", (it_id,))
                    conn.commit()
                    st.rerun()

        with admin_tab2:
            st.markdown("<h3>الطلبات الواردة</h3>", unsafe_allow_html=True)
            cursor.execute(
                "SELECT id, customer_name, phone, address, items_summary, total_price, status, created_at FROM orders ORDER BY id DESC"
            )
            orders = cursor.fetchall()

            if not orders:
                st.info("لا توجد طلبات مسجلة حتى الآن.")
            else:
                for ord_item in orders:
                    (
                        o_id,
                        o_name,
                        o_phone,
                        o_addr,
                        o_summary,
                        o_total,
                        o_status,
                        o_time,
                    ) = ord_item
                    with st.expander(
                        f"طلب #{o_id} - العميل: {o_name} ({o_time})"
                    ):
                        st.write(f"📱 **رقم الهاتف:** {o_phone}")
                        st.write(f"📍 **العنوان:** {o_addr}")
                        st.write(f"🍽️ **الأصناف:** {o_summary}")
                        st.write(f"💰 **الإجمالي:** {o_total} ج.م")
                        st.write(f"📌 **حالة الطلب الحالية:** {o_status}")

                        st.markdown("تحديث حالة الطلب:")
                        status_cols = st.columns(4)
                        statuses = ["جديد", "قيد التجهيز", "خرج للتوصيل", "مكتمل"]
                        for s_idx, st_val in enumerate(statuses):
                            with status_cols[s_idx]:
                                if st.button(st_val, key=f"status_btn_{o_id}_{s_idx}"):
                                    cursor.execute(
                                        "UPDATE orders SET status = ? WHERE id = ?",
                                        (st_val, o_id),
                                    )
                                    conn.commit()
                                    st.success(f"تم تحديث حالة الطلب إلى: {st_val}")
                                    st.rerun()

    elif admin_password != "":
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة مرور الإدارة للوصول إلى لوحة التحكم.")

# 4. قسم الفروع وتواصل معنا
elif st.session_state.current_page == "📍 الفروع وتواصل معنا":
    st.markdown("<h2 style='border-right: 6px solid #FFD700; padding-right: 12px; margin-bottom: 20px;'>فروع مطاعم أسماك وادي النيل</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div style="background: white; padding: 25px; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <h3 style="color: #06283D; margin-bottom: 15px;">فرع الجيزة الرئيسي</h3>
                <p><strong>العنوان:</strong> شارع الهرم الرئيسي - الجيزة</p>
                <p><strong>الهواتف:</strong> 01000000000 / 0233333333</p>
                <p><strong>الخط الساخن:</strong> 19974</p>
                <p><strong>مواعيد العمل:</strong> من 11:00 صباحاً حتى 2:00 صباحاً</p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div style="background: white; padding: 25px; border-radius: 14px; border: 1px solid #E2E8F0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
                <h3 style="color: #06283D; margin-bottom: 15px;">فرع القاهرة</h3>
                <p><strong>العنوان:</strong> مدينة نصر - شارع مكرم عبيد</p>
                <p><strong>الهواتف:</strong> 01111111111 / 0222222222</p>
                <p><strong>الخط الساخن:</strong> 19974</p>
                <p><strong>مواعيد العمل:</strong> من 11:00 صباحاً حتى 2:00 صباحاً</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #4A5568; font-weight: 700; font-size: 1.1rem;'>© 2026 مطاعم أسماك وادي النيل. جميع الحقوق محفوظة.</p>", unsafe_allow_html=True)
