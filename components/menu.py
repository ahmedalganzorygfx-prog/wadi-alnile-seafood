import streamlit as st
import os
from database.database import get_connection

CATEGORIES = [
    "الحلويات",
    "المشروبات",
    "الشوربة",
    "السلطات",
    "الأرز",
    "السي فود",
    "الجمبري",
    "الأسماك",
    "الكل",
]

CATEGORY_IMAGES = {
    "الأسماك": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80",
    "الجمبري": "https://images.unsplash.com/photo-1565680314210-5ab350e965cc?auto=format&fit=crop&w=600&q=80",
    "السي فود": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80",
    "الأرز": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
    "السلطات": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80",
    "الشوربة": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",
    "المشروبات": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=600&q=80",
    "الحلويات": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=600&q=80",
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80"

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
        <style>
        div[data-baseweb="input"], input {
            direction: rtl !important;
            text-align: right !important;
            background-color: #0b2538 !important;
            color: #ffffff !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
        }
        .stTextInput > label {
            direction: rtl !important;
            text-align: right !important;
            display: block;
            color: #94a3b8 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "الكل"

    col_left, col_search, col_right = st.columns([1, 2, 1])
    with col_search:
        search_query = st.text_input("🔍 ابحث عن وجبة...", placeholder="اكتب اسم الوجبة...")

    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(len(CATEGORIES))
    for idx, category in enumerate(CATEGORIES):
        with cols[idx]:
            is_active = st.session_state.selected_category == category
            btn_type = "primary" if is_active else "secondary"
            if st.button(category, key=f"cat_btn_{idx}", use_container_width=True, type=btn_type):
                st.session_state.selected_category = category
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

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

    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols_row = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(filtered_products):
                prod = filtered_products[idx]
                cat_name = prod["category"]
                
                image_to_show = CATEGORY_IMAGES.get(cat_name, DEFAULT_IMAGE)
                if prod["image"] and prod["image"].strip() != "":
                    if prod["image"].startswith("http"):
                        image_to_show = prod["image"]
                    else:
                        if os.path.exists(prod["image"]):
                            image_to_show = prod["image"]
                
                with cols_row[j]:
                    with st.container():
                        st.image(image_to_show, use_column_width=True)
                        
                        st.markdown(
                            f"""
                            <div style="
                                background: #0b2538;
                                border: 1px solid rgba(255, 255, 255, 0.08);
                                border-radius: 0 0 16px 16px;
                                padding: 18px;
                                margin-bottom: 15px;
                                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
                                text-align: right;
                                direction: rtl;
                            ">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <div style="font-size: 19px; font-weight: 900; color: #ffffff;">
                                        {prod['name']}
                                    </div>
                                    <div style="font-size: 11px; background: rgba(13, 148, 136, 0.2); color: #2dd4bf; padding: 2px 8px; border-radius: 10px; font-weight: bold;">
                                        {cat_name}
                                    </div>
                                </div>
                                <div style="font-size: 13px; color: #94a3b8; margin-bottom: 12px; min-height: 38px; line-height: 1.5;">
                                    {prod['description'] or 'وجبة بحرية طازجة ومميزة مُجهزة بأعلى معايير الجودة'}
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 10px;">
                                    <div style="font-size: 17px; font-weight: 900; color: #38bdf8;">
                                        {prod['price']} جنيه
                                    </div>
                                    <div style="font-size: 11px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 8px; font-weight: bold;">
                                        ⭐ طازج يومياً
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        if st.button(f"🛒 أضف للسلة", key=f"add_{prod['id']}", use_container_width=True):
                            if "cart" not in st.session_state:
                                st.session_state.cart = []
                            
                            found = False
                            for item in st.session_state.cart:
                                if item["id"] == prod["id"]:
                                    item["quantity"] += 1
                                    found = True
                                    break
                            if not found:
                                st.session_state.cart.append(
                                    {
                                        "id": prod["id"],
                                        "name": prod["name"],
                                        "price": prod["price"],
                                        "quantity": 1,
                                    }
                                )
                            st.success(f"تمت إضافة '{prod['name']}' إلى السلة بنجاح!")
                            st.rerun()
