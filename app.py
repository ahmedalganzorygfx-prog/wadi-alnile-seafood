import os
from urllib.parse import quote

import pandas as pd
import streamlit as st

from database import (
    init_db,
    get_setting,
    get_settings,
    save_settings,
    get_products,
    get_product,
    save_product,
    delete_product,
    create_order,
    get_orders,
    get_order_items,
    update_order_status,
)


# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="مطاعم أسماك وادي النيل",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# تنسيق الواجهة العربية RTL
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    .stApp {
        direction: rtl;
        text-align: right;
        background: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
        background: #102a43;
    }

    [data-testid="stSidebar"] * {
        color: #ffffff;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        text-align: right;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 36px 30px;
        border-radius: 22px;
        background: linear-gradient(125deg, #082f49, #075985, #0e7490);
        color: #ffffff;
        text-align: center;
        margin-bottom: 26px;
        box-shadow: 0 12px 35px rgba(8, 47, 73, 0.16);
    }

    .hero h1 {
        color: #ffffff;
        font-size: clamp(27px, 4vw, 44px);
        font-weight: 900;
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #e0f2fe;
        font-size: 17px;
        margin: 0;
    }

    .section-title {
        color: #102a43;
        font-size: 25px;
        font-weight: 900;
        margin: 18px 0;
    }

    .product-card {
        background: #ffffff;
        border: 1px solid #e5eaf1;
        border-radius: 18px;
        padding: 16px;
        min-height: 155px;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.045);
        margin-bottom: 10px;
    }

    .product-card h3 {
        color: #102a43;
        font-size: 19px;
        font-weight: 800;
        margin: 4px 0 8px 0;
    }

    .product-card p {
        color: #64748b;
        font-size: 13px;
        min-height: 35px;
        margin-bottom: 10px;
    }

    .price {
        color: #087f5b;
        font-weight: 900;
        font-size: 20px;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
    }

    .muted {
        color: #64748b;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 10px;
        font-weight: 800;
        min-height: 42px;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px;
    }

    div[data-testid="stDataFrame"] {
        direction: rtl;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 0.8rem;
        }
        .hero {
            padding: 24px 14px;
            border-radius: 16px;
        }
        .hero p {
            font-size: 14px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# التهيئة العامة
# =========================================================

try:
    init_db()
except Exception as exc:
    st.error(
        "تعذر الاتصال بقاعدة البيانات. راجع إعداد DATABASE_URL "
        "في Streamlit Secrets."
    )
    with st.expander("تفاصيل الخطأ"):
        st.code(str(exc))
    st.stop()


def money(value):
    """تنسيق السعر."""
    try:
        amount = float(value or 0)
    except (ValueError, TypeError):
        amount = 0
    currency = get_setting("currency", "جنيه")
    return f"{amount:,.2f} {currency}"


def get_admin_password():
    """كلمة مرور لوحة الإدارة من Secrets أو البيئة."""
    try:
        password = st.secrets.get("ADMIN_PASSWORD", "")
    except Exception:
        password = ""

    return password or os.environ.get("ADMIN_PASSWORD", "")


def normalize_whatsapp(number):
    """إزالة الرموز غير الرقمية من رقم واتساب."""
    return "".join(char for char in str(number) if char.isdigit())


def hero():
    restaurant = get_setting(
        "restaurant_name",
        "مطاعم أسماك وادي النيل",
    )
    subtitle = get_setting(
        "restaurant_subtitle",
        "أشهى المأكولات البحرية الطازجة",
    )
    announcement = get_setting("announcement", "")

    st.markdown(
        f"""
        <div class="hero">
            <div style="font-size:42px; margin-bottom:8px">🐟</div>
            <h1>{restaurant}</h1>
            <p>{subtitle}</p>
            <div style="
                margin-top:18px;
                font-size:14px;
                color:#ffffff;
                opacity:.9;
            ">{announcement}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def admin_logged_in():
    return bool(st.session_state.get("admin_logged_in", False))


# =========================================================
# القائمة الجانبية
# =========================================================

with st.sidebar:
    st.markdown(
        """
        <div style="text-align:center;padding:16px 4px 22px">
            <div style="font-size:48px">🐟</div>
            <div style="font-size:21px;font-weight:900">
                وادي النيل
            </div>
            <div style="font-size:12px;color:#cbd5e1">
                مطاعم الأسماك والمأكولات البحرية
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page_options = [
        "الرئيسية وقائمة الطعام",
        "سلة المشتريات",
        "تواصل معنا",
        "لوحة الإدارة",
    ]

    page = st.radio(
        "القائمة الرئيسية",
        page_options,
        label_visibility="collapsed",
    )

    st.divider()

    st.caption("طازج من البحر إلى مائدتك 🌊")


# =========================================================
# الرئيسية وقائمة الطعام
# =========================================================

if page == "الرئيسية وقائمة الطعام":
    hero()

    categories_products = get_products(available_only=True)

    if not categories_products:
        st.info("لا توجد أصناف متاحة حاليًا.")
    else:
        categories = sorted(
            {
                product["category"]
                for product in categories_products
                if product["category"]
            }
        )

        chosen_category = st.selectbox(
            "اختر القسم",
            ["كل الأصناف"] + categories,
        )

        search = st.text_input(
            "🔎 ابحث عن وجبتك",
            placeholder="اكتب اسم السمك أو الصنف...",
        )

        filtered = categories_products

        if chosen_category != "كل الأصناف":
            filtered = [
                p for p in filtered
                if p["category"] == chosen_category
            ]

        if search.strip():
            term = search.strip().casefold()
            filtered = [
                p for p in filtered
                if term in p["name"].casefold()
                or term in p["description"].casefold()
            ]

        st.markdown(
            '<div class="section-title">🍽️ قائمة الطعام</div>',
            unsafe_allow_html=True,
        )

        if not filtered:
            st.warning("لم نعثر على أصناف مطابقة للبحث.")
        else:
            cols_per_row = 3

            for start in range(0, len(filtered), cols_per_row):
                row_products = filtered[start:start + cols_per_row]
                cols = st.columns(cols_per_row)

                for col, product in zip(cols, row_products):
                    with col:
                        with st.container(border=True):
                            image_url = product["image_url"]

                            if image_url:
                                st.image(
                                    image_url,
                                    use_container_width=True,
                                )
                            else:
                                st.markdown(
                                    "<div style='text-align:center;"
                                    "font-size:60px'>🐟</div>",
                                    unsafe_allow_html=True,
                                )

                            st.markdown(
                                f"### {product['name']}"
                            )
                            st.caption(product["category"])
                            st.write(product["description"])
                            st.markdown(
                                f"<div class='price'>{money(product['price'])}</div>",
                                unsafe_allow_html=True,
                            )

                            quantity = st.number_input(
                                "الكمية",
                                min_value=1,
                                max_value=50,
                                value=1,
                                step=1,
                                key=f"qty_{product['id']}",
                            )

                            if st.button(
                                "➕ أضف إلى السلة",
                                key=f"add_{product['id']}",
                                use_container_width=True,
                            ):
                                cart = st.session_state.setdefault(
                                    "cart", {}
                                )
                                pid = int(product["id"])

                                if pid in cart:
                                    cart[pid]["quantity"] += int(quantity)
                                else:
                                    cart[pid] = {
                                        "id": pid,
                                        "name": product["name"],
                                        "price": float(product["price"]),
                                        "quantity": int(quantity),
                                    }

                                st.success(
                                    f"تمت إضافة {product['name']} إلى السلة."
                                )


# =========================================================
# سلة المشتريات وإتمام الطلب
# =========================================================

elif page == "سلة المشتريات":
    hero()
    st.markdown(
        '<div class="section-title">🛒 سلة المشتريات</div>',
        unsafe_allow_html=True,
    )

    cart = st.session_state.setdefault("cart", {})

    if not cart:
        st.info("سلة المشتريات فارغة. أضف بعض الأصناف أولًا.")
    else:
        for pid in list(cart.keys()):
            item = cart[pid]

            with st.container(border=True):
                col1, col2, col3, col4 = st.columns(
                    [3, 1.3, 1.5, 1]
                )

                with col1:
                    st.markdown(f"**{item['name']}**")

                with col2:
                    st.write(money(item["price"]))

                with col3:
                    new_qty = st.number_input(
                        "الكمية",
                        min_value=1,
                        max_value=50,
                        value=int(item["quantity"]),
                        key=f"cart_qty_{pid}",
                    )
                    cart[pid]["quantity"] = int(new_qty)

                with col4:
                    if st.button(
                        "حذف",
                        key=f"remove_{pid}",
                    ):
                        del cart[pid]
                        st.rerun()

        subtotal = sum(
            item["price"] * item["quantity"]
            for item in cart.values()
        )

        delivery_fee = float(
            get_setting("delivery_fee", "25") or 0
        )
        free_minimum = float(
            get_setting("free_delivery_minimum", "0") or 0
        )

        if free_minimum > 0 and subtotal >= free_minimum:
            delivery_fee = 0

        total = subtotal + delivery_fee

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric("قيمة الأصناف", money(subtotal))
        col2.metric("التوصيل", money(delivery_fee))
        col3.metric("الإجمالي", money(total))

        st.markdown("### 📝 بيانات التوصيل")

        with st.form("checkout_form"):
            customer_name = st.text_input(
                "الاسم بالكامل *",
                placeholder="اسم العميل",
            )
            phone = st.text_input(
                "رقم الهاتف *",
                placeholder="01xxxxxxxxx",
            )
            address = st.text_area(
                "عنوان التوصيل بالتفصيل *",
                placeholder="المحافظة، المنطقة، الشارع، رقم العقار",
            )
            branch_name = st.text_input(
                "الفرع المطلوب",
                value="الفرع الرئيسي",
            )
            notes = st.text_area(
                "ملاحظات الطلب",
                placeholder="تعليمات إضافية أو طريقة التسوية المفضلة",
            )

            submitted = st.form_submit_button(
                "تأكيد الطلب",
                use_container_width=True,
                type="primary",
            )

        if submitted:
            if not customer_name.strip():
                st.error("يرجى كتابة اسم العميل.")
            elif not phone.strip():
                st.error("يرجى كتابة رقم الهاتف.")
            elif not address.strip():
                st.error("يرجى كتابة عنوان التوصيل.")
            else:
                try:
                    cart_items = list(cart.values())

                    order_id, saved_subtotal, saved_total = create_order(
                        customer_name=customer_name.strip(),
                        phone=phone.strip(),
                        address=address.strip(),
                        notes=notes.strip(),
                        branch_name=branch_name.strip(),
                        cart_items=cart_items,
                        delivery_fee=delivery_fee,
                    )

                    restaurant_phone = normalize_whatsapp(
                        get_setting("whatsapp_number", "")
                    )

                    message_lines = [
                        f"طلب جديد رقم {order_id}",
                        get_setting(
                            "restaurant_name",
                            "مطاعم أسماك وادي النيل",
                        ),
                        "",
                        f"العميل: {customer_name}",
                        f"الهاتف: {phone}",
                        f"العنوان: {address}",
                        f"الفرع: {branch_name}",
                        "",
                        "تفاصيل الطلب:",
                    ]

                    for item in cart_items:
                        line_total = (
                            float(item["price"])
                            * int(item["quantity"])
                        )
                        message_lines.append(
                            f"- {item['name']} × {item['quantity']}"
                            f" = {line_total:,.2f}"
                        )

                    message_lines.extend(
                        [
                            "",
                            f"قيمة الأصناف: {saved_subtotal:,.2f}",
                            f"التوصيل: {delivery_fee:,.2f}",
                            f"الإجمالي: {saved_total:,.2f}",
                            f"ملاحظات: {notes or 'لا يوجد'}",
                        ]
                    )

                    message = "\n".join(message_lines)

                    st.session_state["last_order_id"] = order_id
                    st.session_state["last_order_message"] = message
                    st.session_state["cart"] = {}

                    st.success(
                        f"تم حفظ طلبك بنجاح. رقم الطلب: {order_id}"
                    )

                    if restaurant_phone:
                        whatsapp_url = (
                            "https://wa.me/"
                            + restaurant_phone
                            + "?text="
                            + quote(message)
                        )

                        st.link_button(
                            "📲 إرسال تفاصيل الطلب عبر واتساب",
                            whatsapp_url,
                            use_container_width=True,
                        )
                    else:
                        st.warning(
                            "تم حفظ الطلب في قاعدة البيانات، "
                            "لكن رقم واتساب المطعم لم يُضبط بعد."
                        )

                except Exception as exc:
                    st.error("تعذر حفظ الطلب. حاول مرة أخرى.")
                    with st.expander("تفاصيل الخطأ"):
                        st.code(str(exc))


# =========================================================
# التواصل ومعلومات المطعم
# =========================================================

elif page == "تواصل معنا":
    hero()

    settings = get_settings()

    st.markdown(
        '<div class="section-title">📍 تواصل معنا</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="info-card">
            <h3>📌 عنوان المطعم</h3>
            <p>{settings.get('restaurant_address', '') or 'سيتم إضافة العنوان قريبًا'}</p>
            <h3>☎️ الهاتف</h3>
            <p>{settings.get('restaurant_phone', '') or 'سيتم إضافة رقم الهاتف قريبًا'}</p>
            <h3>🕒 خدمة العملاء</h3>
            <p>تواصل معنا للاستفسار عن الأصناف والطلبات.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    whatsapp = normalize_whatsapp(
        settings.get("whatsapp_number", "")
    )

    if whatsapp:
        st.link_button(
            "تواصل عبر واتساب",
            f"https://wa.me/{whatsapp}",
            use_container_width=True,
        )


# =========================================================
# لوحة الإدارة
# =========================================================

elif page == "لوحة الإدارة":
    st.markdown(
        '<div class="section-title">🔐 لوحة إدارة المطعم</div>',
        unsafe_allow_html=True,
    )

    if not admin_logged_in():
        st.info("يرجى تسجيل الدخول للوصول إلى لوحة الإدارة.")

        with st.form("admin_login"):
            password = st.text_input(
                "كلمة مرور الإدارة",
                type="password",
            )
            login = st.form_submit_button(
                "تسجيل الدخول",
                use_container_width=True,
            )

        if login:
            configured_password = get_admin_password()

            if not configured_password:
                st.error(
                    "لم يتم ضبط ADMIN_PASSWORD في إعدادات Secrets."
                )
            elif password == configured_password:
                st.session_state["admin_logged_in"] = True
                st.rerun()
            else:
                st.error("كلمة المرور غير صحيحة.")

        st.stop()

    if st.button("تسجيل الخروج"):
        st.session_state["admin_logged_in"] = False
        st.rerun()

    tab_products, tab_orders, tab_settings = st.tabs(
        ["إدارة الأصناف", "إدارة الطلبات", "إعدادات المطعم"]
    )

    # -----------------------------------------------------
    # إدارة الأصناف
    # -----------------------------------------------------

    with tab_products:
        st.subheader("إضافة صنف أو تعديل صنف موجود")

        all_products = get_products(available_only=False)

        product_options = {
            "إضافة صنف جديد": None
        }

        for product in all_products:
            product_options[
                f"{product['id']} - {product['name']}"
            ] = product["id"]

        selected_product_label = st.selectbox(
            "اختر الصنف",
            list(product_options.keys()),
        )

        selected_product_id = product_options[
            selected_product_label
        ]

        selected_product = (
            get_product(selected_product_id)
            if selected_product_id
            else None
        )

        with st.form("product_form"):
            name = st.text_input(
                "اسم الصنف",
                value=(
                    selected_product["name"]
                    if selected_product else ""
                ),
            )

            category = st.text_input(
                "القسم",
                value=(
                    selected_product["category"]
                    if selected_product else "أسماك"
                ),
            )

            description = st.text_area(
                "وصف الصنف",
                value=(
                    selected_product["description"]
                    if selected_product else ""
                ),
            )

            price = st.number_input(
                "السعر بالجنيه",
                min_value=0.0,
                step=5.0,
                value=(
                    float(selected_product["price"])
                    if selected_product else 0.0
                ),
            )

            image_url = st.text_input(
                "رابط صورة الصنف",
                value=(
                    selected_product["image_url"]
                    if selected_product else ""
                ),
                help="أدخل رابط صورة مباشر يبدأ بـ https://",
            )

            available = st.checkbox(
                "الصنف متاح للبيع",
                value=(
                    bool(selected_product["available"])
                    if selected_product else True
                ),
            )

            save_button = st.form_submit_button(
                "حفظ الصنف",
                use_container_width=True,
                type="primary",
            )

        if save_button:
            if not name.strip():
                st.error("اسم الصنف مطلوب.")
            elif not category.strip():
                st.error("القسم مطلوب.")
            else:
                try:
                    save_product(
                        selected_product_id,
                        name.strip(),
                        category.strip(),
                        description.strip(),
                        price,
                        image_url.strip(),
                        available,
                    )
                    st.success("تم حفظ الصنف بنجاح.")
                    st.rerun()
                except Exception as exc:
                    st.error("تعذر حفظ الصنف.")
                    st.code(str(exc))

        st.divider()
        st.subheader("الأصناف المسجلة")

        if all_products:
            product_df = pd.DataFrame(
                [
                    {
                        "رقم الصنف": p["id"],
                        "اسم الصنف": p["name"],
                        "القسم": p["category"],
                        "السعر": float(p["price"]),
                        "متاح": "نعم" if p["available"] else "لا",
                    }
                    for p in all_products
                ]
            )
            st.dataframe(
                product_df,
                use_container_width=True,
                hide_index=True,
            )

            delete_options = {
                f"{p['id']} - {p['name']}": p["id"]
                for p in all_products
            }

            delete_label = st.selectbox(
                "اختر صنفًا لحذفه",
                list(delete_options.keys()),
                key="delete_product_select",
            )

            if st.button("🗑️ حذف الصنف المحدد"):
                delete_product(delete_options[delete_label])
                st.success("تم حذف الصنف.")
                st.rerun()
        else:
            st.info("لا توجد أصناف مسجلة.")

    # -----------------------------------------------------
    # إدارة الطلبات
    # -----------------------------------------------------

    with tab_orders:
        st.subheader("متابعة الطلبات")

        orders = get_orders(limit=500)

        if not orders:
            st.info("لا توجد طلبات مسجلة حتى الآن.")
        else:
            total_orders = len(orders)
            new_orders = sum(
                1 for order in orders
                if order["status"] == "جديد"
            )
            completed_orders = sum(
                1 for order in orders
                if order["status"] == "مكتمل"
            )
            revenue = sum(
                float(order["total"])
                for order in orders
                if order["status"] != "ملغي"
            )

            metric1, metric2, metric3, metric4 = st.columns(4)

            metric1.metric("إجمالي الطلبات", total_orders)
            metric2.metric("طلبات جديدة", new_orders)
            metric3.metric("طلبات مكتملة", completed_orders)
            metric4.metric("الإيرادات غير الملغاة", money(revenue))

            order_options = {
                (
                    f"#{order['id']} - "
                    f"{order['customer_name']} - "
                    f"{order['status']}"
                ): order["id"]
                for order in orders
            }

            selected_order_label = st.selectbox(
                "اختر طلبًا لعرض التفاصيل",
                list(order_options.keys()),
            )

            selected_order_id = order_options[
                selected_order_label
            ]

            selected_order = next(
                order for order in orders
                if order["id"] == selected_order_id
            )

            st.markdown(
                f"""
                <div class="info-card">
                    <h3>الطلب رقم #{selected_order['id']}</h3>
                    <p><b>العميل:</b> {selected_order['customer_name']}</p>
                    <p><b>الهاتف:</b> {selected_order['phone']}</p>
                    <p><b>العنوان:</b> {selected_order['address']}</p>
                    <p><b>الفرع:</b> {selected_order['branch_name']}</p>
                    <p><b>التاريخ:</b> {selected_order['created_at']}</p>
                    <p><b>قيمة الأصناف:</b> {money(selected_order['subtotal'])}</p>
                    <p><b>التوصيل:</b> {money(selected_order['delivery_fee'])}</p>
                    <p><b>الإجمالي:</b> {money(selected_order['total'])}</p>
                    <p><b>ملاحظات:</b> {selected_order['notes'] or 'لا يوجد'}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            items = get_order_items(selected_order_id)

            if items:
                items_df = pd.DataFrame(
                    [
                        {
                            "الصنف": item["product_name"],
                            "سعر الوحدة": float(item["unit_price"]),
                            "الكمية": item["quantity"],
                            "الإجمالي": float(item["line_total"]),
                        }
                        for item in items
                    ]
                )

                st.dataframe(
                    items_df,
                    use_container_width=True,
                    hide_index=True,
                )

            statuses = [
                "جديد",
                "قيد التجهيز",
                "خرج للتوصيل",
                "مكتمل",
                "ملغي",
            ]

            current_index = (
                statuses.index(selected_order["status"])
                if selected_order["status"] in statuses
                else 0
            )

            new_status = st.selectbox(
                "تحديث حالة الطلب",
                statuses,
                index=current_index,
            )

            if st.button("حفظ حالة الطلب"):
                update_order_status(
                    selected_order_id,
                    new_status,
                )
                st.success("تم تحديث حالة الطلب.")
                st.rerun()

            export_df = pd.DataFrame(
                [
                    {
                        "رقم الطلب": order["id"],
                        "العميل": order["customer_name"],
                        "الهاتف": order["phone"],
                        "العنوان": order["address"],
                        "الفرع": order["branch_name"],
                        "الإجمالي": float(order["total"]),
                        "الحالة": order["status"],
                        "التاريخ": str(order["created_at"]),
                    }
                    for order in orders
                ]
            )

            st.download_button(
                "📥 تصدير الطلبات إلى Excel-compatible CSV",
                data=export_df.to_csv(
                    index=False,
                    encoding="utf-8-sig",
                ).encode("utf-8-sig"),
                file_name="wadi_el_nile_orders.csv",
                mime="text/csv",
            )

    # -----------------------------------------------------
    # إعدادات المطعم
    # -----------------------------------------------------

    with tab_settings:
        st.subheader("بيانات المطعم والتوصيل")

        current_settings = get_settings()

        with st.form("restaurant_settings"):
            restaurant_name = st.text_input(
                "اسم المطعم",
                value=current_settings.get(
                    "restaurant_name",
                    "مطاعم أسماك وادي النيل",
                ),
            )

            restaurant_subtitle = st.text_input(
                "الوصف المختصر",
                value=current_settings.get(
                    "restaurant_subtitle",
                    "",
                ),
            )

            restaurant_phone = st.text_input(
                "رقم هاتف المطعم",
                value=current_settings.get(
                    "restaurant_phone",
                    "",
                ),
            )

            whatsapp_number = st.text_input(
                "رقم واتساب المطعم بصيغة دولية",
                value=current_settings.get(
                    "whatsapp_number",
                    "",
                ),
                help="مثال مصري: 2010XXXXXXXX. اكتب الأرقام فقط.",
            )

            restaurant_address = st.text_area(
                "عنوان المطعم",
                value=current_settings.get(
                    "restaurant_address",
                    "",
                ),
            )

            delivery_fee_value = st.number_input(
                "رسوم التوصيل بالجنيه",
                min_value=0.0,
                step=5.0,
                value=float(
                    current_settings.get("delivery_fee", "25") or 0
                ),
            )

            free_delivery_minimum_value = st.number_input(
                "الحد الأدنى للطلب للحصول على توصيل مجاني (0 لتعطيله)",
                min_value=0.0,
                step=50.0,
                value=float(
                    current_settings.get(
                        "free_delivery_minimum",
                        "0",
                    ) or 0
                ),
            )

            currency = st.text_input(
                "اسم العملة",
                value=current_settings.get("currency", "جنيه"),
            )

            announcement = st.text_input(
                "رسالة واجهة الموقع",
                value=current_settings.get("announcement", ""),
            )

            settings_submit = st.form_submit_button(
                "حفظ إعدادات المطعم",
                use_container_width=True,
                type="primary",
            )

        if settings_submit:
            save_settings(
                {
                    "restaurant_name": restaurant_name.strip(),
                    "restaurant_subtitle": restaurant_subtitle.strip(),
                    "restaurant_phone": restaurant_phone.strip(),
                    "whatsapp_number": whatsapp_number.strip(),
                    "restaurant_address": restaurant_address.strip(),
                    "delivery_fee": delivery_fee_value,
                    "free_delivery_minimum": free_delivery_minimum_value,
                    "currency": currency.strip() or "جنيه",
                    "announcement": announcement.strip(),
                }
            )

            st.success("تم حفظ إعدادات المطعم.")
            st.rerun()


# =========================================================
# تذييل الموقع
# =========================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748b;
        padding:12px;
        font-size:13px;
    ">
        🐟 مطاعم أسماك وادي النيل
        <br>
        طعم البحر الأصيل، وجودة تستحقها
    </div>
    """,
    unsafe_allow_html=True,
)
