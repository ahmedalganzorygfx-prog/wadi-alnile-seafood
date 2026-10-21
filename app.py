import sqlite3
import streamlit as st

# إعدادات الصفحة والتصميم العام (متوافق مع الهوية: الأزرق البترولي والذهبي والأبيض)
st.set_page_config(
    page_title="مطاعم أسماك وادي النيل",
    page_icon="🦐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* تنسيقات عامة للهوية البصرية */
    .main {
        background-color: #F8F9FA;
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        background-color: #004D61;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #C5A059;
        color: white;
    }
    .css-1544g2n {
        direction: rtl;
    }
    h1, h2, h3 {
        color: #004D61;
    }
    .price-tag {
        color: #C5A059;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .hotline-banner {
        background: linear-gradient(135deg, #004D61, #002B36);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# إعداد قاعدة البيانات SQLite محلياً
def init_db():
    conn = sqlite3.connect("wadi_alnile.db", check_same_thread=False)
    cursor = conn.cursor()
    # جدول الأصناف
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
    # جدول الطلبات
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

    # إدخال بيانات تجريبية أولية في حال كانت الجدول فارغة
    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] == 0:
        sample_items = [
            (
                "طاجن سبيد بصل وإسكندراني",
                "طواجن",
                180.0,
                "طاجن سبيط طازج بالخلطة الإسكندراني المميزة",
                "https://images.unsplash.com/photo-1544025162-d76694265947?w=500",
            ),
            (
                "جمبري مشوي عالبوتجاز",
                "جمبري",
                250.0,
                "جمبري جامبو طازج مشوي بالخلطة الخاصة",
                "https://images.unsplash.com/photo-1565680314427-a5abbbc49926?w=500",
            ),
            (
                "سمك دينيس مشوي زيت وليمون",
                "أسماك طازجة",
                220.0,
                "سمك دينيس بحري طازج مشوي على الفحم أو بالفرن",
                "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500",
            ),
            (
                "شوربة سي فود كريمة",
                "شوربات",
                120.0,
                "تشكيلة بحرية غنية بالجمبري والكاليماري والأسماك مع الكريمة",
                "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500",
            ),
            (
                "أرز صيادية بالجمبري",
                "مقبلات وأرز",
                65.0,
                "أرز بني بالبصل المحمر وقطع الجمبري الطازجة",
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

# شريط التنقل العلوي ورقم الخط الساخن
st.markdown(
    """
    <div class="hotline-banner">
        <h2>🌊 مطاعم أسماك وادي النيل 🌊</h2>
        <p style="font-size: 1.2rem; margin: 0;">الخط الساخن للطلب والتوصيل: <strong>19974</strong></p>
    </div>
""",
    unsafe_allow_html=True,
)

# القائمة الجانبية للتنقل
menu_selection = st.sidebar.selectbox(
    "القائمة الرئيسية",
    [
        "🏠 الرئيسية وقائمة الطعام",
        "🛒 سلة المشتريات وإتمام الطلب",
        "🔐 لوحة التحكم الإدارية",
        "📍 الفروع وتواصل معنا",
    ],
)

# تهيئة سلة المشتريات في جلسة المستخدم
if "cart" not in st.session_state:
    st.session_state.cart = []

# 1. الواجهة الرئيسية وقائمة الطعام
if menu_selection == "🏠 الرئيسية وقائمة الطعام":
    st.subheader("أبرز أصناف المأكولات البحرية الطازجة")

    # جلب التصنيفات المتاحة
    cursor.execute("SELECT DISTINCT category FROM items WHERE available = 1")
    categories = [row[0] for row in cursor.fetchall()]
    categories.insert(0, "الكل")

    selected_category = st.selectbox("اختر القسم:", categories)
    search_query = st.text_input("🔍 بحث عن صنف معين:", "")

    # تصفية الأصناف حسب القسم والبحث
    query = "SELECT id, name, category, price, description, image_url FROM items WHERE available = 1"
    params = []
    if selected_category != "الكل":
        query += " AND category = ?"
        params.append(selected_category)
    if search_query:
        query += " AND name LIKE ?"
        params.append(f"%{search_query}%")

    cursor.execute(query, params)
    items = cursor.fetchall()

    if not items:
        st.info("لا توجد أصناف متاحة حالياً تطابق بحثك.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(items):
            item_id, name, category, price, description, image_url = item
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div style="border: 1px solid #E0E0E0; border-radius: 10px; padding: 15px; margin-bottom: 20px; background-color: white; text-align: right;">
                        <img src="{image_url}" style="width: 100%; height: 160px; object-fit: cover; border-radius: 8px;">
                        <h4 style="margin-top: 10px; color: #004D61;">{name}</h4>
                        <p style="color: #666; font-size: 0.9rem; min-height: 40px;">{description}</p>
                        <p class="price-tag">{price} جنيه مصري</p>
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
                )
                if st.button(f"أضف للسلة 🛒", key=f"add_{item_id}"):
                    # التحقق إذا كان الصنف موجود مسبقاً في السلة وتحديث كميته
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

# 2. سلة المشتريات وإتمام الطلب
elif menu_selection == "🛒 سلة المشتريات وإتمام الطلب":
    st.subheader("🛒 سلة المشتريات")

    if not st.session_state.cart:
        st.warning(
            "سلة المشتريات فارغة حالياً. تفضل بزيارة قائمة الطعام لإضافة أطباقك المفضلة!"
        )
    else:
        total_amount = 0
        updated_cart = []

        for idx, cart_item in enumerate(st.session_state.cart):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(f"**{cart_item['name']}**")
            with col2:
                st.write(f"السعر: {cart_item['price']} ج.م")
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

        st.markdown(f"### إجمالي الفاتورة: <span style='color: #C5A059;'>{total_amount:.2f} جنيه مصري</span>", unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("بيانات التوصيل وإتمام الطلب")

        with st.form("checkout_form"):
            customer_name = st.text_input("الاسم الكريم:")
            phone = st.text_input("رقم الهاتف:")
            address = st.text_area("عنوان التوصيل بالتفصيل:")
            submit_order = st.form_submit_button("تأكيد وإرسال الطلب 🚀")

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

                    st.success("🎉 تم استلام طلبك بنجاح! جاري تجهيزه من مطاعم وادي النيل.")
                    st.info(f"رقم الخط الساخن للتأكيد الفوري: 19974")
                    # تفريغ السلة بعد إتمام الطلب
                    st.session_state.cart = []

# 3. لوحة التحكم الإدارية
elif menu_selection == "🔐 لوحة التحكم الإدارية":
    st.subheader("🔐 لوحة التحكم الإدارية")

    admin_password = st.text_input("أدخل كلمة مرور الإدارة:", type="password")
    if admin_password == "change-me-now":
        st.success("تم تسجيل الدخول بنجاح للصلاحيات الإدارية.")

        admin_tab1, admin_tab2 = st.tabs(["إدارة الأصناف والقائمة", "متابعة الطلبات الواردة"])

        with admin_tab1:
            st.markdown("### إضافة صنف جديد للقائمة")
            with st.form("add_item_form"):
                new_name = st.text_input("اسم الصنف:")
                new_cat = st.selectbox(
                    "القسم:", ["طواجن", "جمبري", "أسماك طازجة", "شوربات", "مقبلات وأرز"]
                )
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
                            (new_name, new_cat, new_price, new_desc, new_img),
                        )
                        conn.commit()
                        st.success(f"تمت إضافة الصنف '{new_name}' بنجاح!")
                    else:
                        st.error("الرجاء إدخال اسم الصنف على الأقل.")

            st.markdown("---")
            st.markdown("### الأصناف الحالية في القائمة")
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
            st.markdown("### الطلبات الواردة")
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

                        new_status = st.selectbox(
                            "تحديث حالة الطلب:",
                            ["جديد", "قيد التجهيز", "خرج للتوصيل", "مكتمل"],
                            key=f"status_{o_id}",
                        )
                        if st.button("حفظ التحديث", key=f"save_status_{o_id}"):
                            cursor.execute(
                                "UPDATE orders SET status = ? WHERE id = ?",
                                (new_status, o_id),
                            )
                            conn.commit()
                            st.success("تم تحديث حالة الطلب بنجاح!")
                            st.rerun()

    elif admin_password != "":
        st.error("كلمة المرور غير صحيحة.")
    else:
        st.info("الرجاء إدخال كلمة مرور الإدارة للوصول إلى لوحة التحكم.")

# 4. قسم الفروع وتواصل معنا
elif menu_selection == "📍 الفروع وتواصل معنا":
    st.subheader("📍 فروع مطاعم أسماك وادي النيل")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            ### فرع الجيزة الرئيسي
            - **العنوان:** شارع الهرم الرئيسي - الجيزة
            - **الهواتف:** 01000000000 / 0233333333
            - **الخط الساخن:** 19974
            - **مواعيد العمل:** من الساعة 11:00 صباحاً حتى 2:00 صباحاً
        """
        )
    with col2:
        st.markdown(
            """
            ### فرع القاهرة
            - **العنوان:** مدينة نصر - شارع مكرم عبيد
            - **الهواتف:** 01111111111 / 0222222222
            - **الخط الساخن:** 19974
            - **مواعيد العمل:** من الساعة 11:00 صباحاً حتى 2:00 صباحاً
        """
        )

    st.markdown("---")
    st.markdown("© 2026 مطاعم أسماك وادي النيل. جميع الحقوق محفوظة.")
