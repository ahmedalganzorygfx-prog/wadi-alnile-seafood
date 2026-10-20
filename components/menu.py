import streamlit as st
from database.database import get_connection

CATEGORIES = [
    "الكل",
    "الأسماك",
    "الجمبري",
    "السي فود",
    "الأرز",
    "السلطات",
    "الشوربة",
    "المشروبات",
    "الحلويات",
]


def load_products():
    connection = get_connection()
    products = connection.execute(
        """
        SELECT
            products.id,
            products.name,
            products.description,
            products.price,
            products.image,
            products.available,
            categories.name AS category
        FROM products
        LEFT JOIN categories
            ON products.category_id = categories.id
        WHERE products.available = 1
        ORDER BY products.id DESC
        """
    ).fetchall()
    return products


def render_menu():
    st.markdown('<div id="menu"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align:center; margin:50px 0 25px; direction:rtl;">
            <h2 style="color:#07566a; font-size:36px; font-weight:900;">🍽️ منيو أسماك وادي النيل</h2>
            <p style="color:#68777d; font-size:16px;">اختر التصنيف أو ابحث عن أكلتك البحرية المفضلة</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # تهيئة التصنيف الحالي في session_state إذا لم يكن موجوداً
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "الكل"

    # شريط البحث العلوي
    col_search, _ = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 ابحث عن وجبة...", placeholder="اكتب اسم الوجبة...")

    st.markdown("<br>", unsafe_allow_html=True)

    # عرض التصنيفات كأزرار أفقية متجاورة
    cols = st.columns(len(CATEGORIES))
    for idx, category in enumerate(CATEGORIES):
        with cols[idx]:
            # تمييز الزر النشط بلون مختلف
            is_active = st.session_state.selected_category == category
            btn_type = "primary" if is_active else "secondary"
            if st.button(category, key=f"cat_btn_{idx}", use_container_width=True, type=btn_type):
                st.session_state.selected_category = category
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # جلب المنتجات وتصفيتها
    products = load_products()
    filtered_products = []
    for p in products:
        match_cat = (st.session_state.selected_category == "الكل") or (p["category"] == st.session_state.selected_category)
        match_search = (not search_query) or (search_query.lower() in p["name"].lower())
        if match_cat and match_search:
            filtered_products.append(p)

    if not filtered_products:
        st.warning("⚠️ عذراً، لا توجد وجبات تطابق اختيارك حالياً.")
        return

    # عرض المنتجات في شبكة (Grid)
    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols_row = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(filtered_products):
                prod = filtered_products[idx]
                with cols_row[j]:
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="
                                background: linear-gradient(180deg, #ffffff 0%, #f8fbfb 100%);
                                border: 1px solid rgba(7, 86, 106, 0.1);
                                border-radius: 24px;
                                padding: 22px;
                                margin-bottom: 20px;
                                box-shadow: 0 10px 30px rgba(7, 86, 106, 0.05);
                                text-align: right;
                                direction: rtl;
                            ">
                                <div style="font-size: 21px; font-weight: 900; color: #07566a; margin-bottom: 8px;">
                                    {prod['name']}
                                </div>
                                <div style="font-size: 14px; color: #68777d; margin-bottom: 18px; min-height: 42px; line-height: 1.6;">
                                    {prod['description'] or 'وجبة بحرية طازجة ومميزة مُجهزة بأعلى معايير الجودة'}
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div style="font-size: 19px; font-weight: 900; color: #0d9488;">
                                        {prod['price']} جنيه
                                    </div>
                                    <div style="font-size: 12px; background: #e6f4f1; color: #0d9488; padding: 4px 10px; border-radius: 20px; font-weight: bold;">
                                        طازج يومياً
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button(f"🛒 أضف للسلة", key=f"add_{prod['id']}"):
                            cart = st.session_state.get("cart", [])
                            found = False
                            for item in cart:
                                if item["id"] == prod["id"]:
                                    item["quantity"] += 1
                                    found = True
                                    break
                            if not found:
                                cart.append(
                                    {
                                        "id": prod["id"],
                                        "name": prod["name"],
                                        "price": prod["price"],
                                        "quantity": 1,
                                    }
                                )
                            st.session_state.cart = cart
                            st.success(f"تمت إضافة '{prod['name']}' إلى السلة بنجاح!")
                            st.rerun()
