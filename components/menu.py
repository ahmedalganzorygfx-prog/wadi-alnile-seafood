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
            <p style="color:#68777d; font-size:16px;">اختر أكلتك البحرية المفضلة وأضفها للسلة بضغطة زر</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # شريط البحث والتصنيفات
    col_search, col_cat = st.columns([1, 2])
    with col_search:
        search_query = st.text_input("🔍 ابحث عن وجبة...", placeholder="اكتب اسم الوجبة...")

    with col_cat:
        selected_category = st.selectbox("📂 تصفية حسب التصنيف", CATEGORIES)

    products = load_products()

    # تصفية المنتجات
    filtered_products = []
    for p in products:
        match_cat = (selected_category == "الكل") or (p["category"] == selected_category)
        match_search = (not search_query) or (search_query.lower() in p["name"].lower())
        if match_cat and match_search:
            filtered_products.append(p)

    if not filtered_products:
        st.warning("⚠️ عذراً، لا توجد وجبات تطابق بحثك حالياً.")
        return

    # عرض المنتجات في شبكة (Grid)
    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(filtered_products):
                prod = filtered_products[idx]
                with cols[j]:
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="
                                background: white;
                                border: 1px solid rgba(0,0,0,0.08);
                                border-radius: 20px;
                                padding: 20px;
                                margin-bottom: 20px;
                                box-shadow: 0 8px 25px rgba(0,0,0,0.04);
                                text-align: right;
                                direction: rtl;
                            ">
                                <div style="font-size: 20px; font-weight: 900; color: #07566a; margin-bottom: 8px;">
                                    {prod['name']}
                                </div>
                                <div style="font-size: 13px; color: #68777d; margin-bottom: 15px; min-height: 40px;">
                                    {prod['description'] or 'وجبة بحرية طازجة ومميزة'}
                                </div>
                                <div style="font-size: 18px; font-weight: 800; color: #10b981; margin-bottom: 15px;">
                                    {prod['price']} جنيه
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
