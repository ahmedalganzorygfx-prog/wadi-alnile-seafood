import streamlit as state_st
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

# قاموس الصور الذكي المطابق للأسماء والتصنيفات بدقة
FOOD_IMAGES = {
    # الأسماك
    "سمك": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80",
    "دينيس": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80",
    "قاروص": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80",
    "بلطي": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=600&q=80",
    "بوري": "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?auto=format&fit=crop&w=600&q=80",
    
    # الجمبري
    "جمبري": "https://images.unsplash.com/photo-1565680314210-5ab350e965cc?auto=format&fit=crop&w=600&q=80",
    "كابوريا": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80",
    
    # السي فود والأطباق المشكلة
    "سي فود": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80",
    "استاكوزا": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80",
    "سبيط": "https://images.unsplash.com/photo-1565680314210-5ab350e965cc?auto=format&fit=crop&w=600&q=80",
    "كاليماري": "https://images.unsplash.com/photo-1565680314210-5ab350e965cc?auto=format&fit=crop&w=600&q=80",

    # الأرز
    "أرز": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
    "صيادية": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",

    # السلطات
    "سلطة": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80",
    "طحينة": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80",
    "مخلل": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80",

    # الشوربة
    "شوربة": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",

    # المشروبات
    "مشروب": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=600&q=80",
    "عصير": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=600&q=80",
    "مياه": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?auto=format&fit=crop&w=600&q=80",

    # الحلويات
    "حلو": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=600&q=80",
    "كنافة": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=600&q=80",
    "أم علي": "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=600&q=80",
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80"


def get_smart_image(product_name, category_name, db_image):
    if db_image and db_image.strip() != "":
        return db_image
    
    # البحث بالاسم الكلي أو الكلمات المفتاحية في اسم الوجبة
    lower_name = product_name.lower()
    for keyword, url in FOOD_IMAGES.items():
        if keyword in lower_name:
            return url
            
    # إذا لم توجد كلمة مفتاحية في الاسم، نلجأ لصورة التصنيف
    return FOOD_IMAGES.get(category_name, DEFAULT_IMAGE)


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
    state_st.markdown('<div id="menu"></div>', unsafe_allow_html=True)

    state_st.markdown(
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

    if "selected_category" not in state_st.session_state:
        state_st.session_state.selected_category = "الكل"

    col_left, col_search, col_right = state_st.columns([1, 2, 1])
    with col_search:
        search_query = state_st.text_input("🔍 ابحث عن وجبة...", placeholder="اكتب اسم الوجبة...")

    state_st.markdown("<br>", unsafe_allow_html=True)

    cols = state_st.columns(len(CATEGORIES))
    for idx, category in enumerate(CATEGORIES):
        with cols[idx]:
            is_active = state_st.session_state.selected_category == category
            btn_type = "primary" if is_active else "secondary"
            if state_st.button(category, key=f"cat_btn_{idx}", use_container_width=True, type=btn_type):
                state_st.session_state.selected_category = category
                state_st.rerun()

    state_st.markdown("<br>", unsafe_allow_html=True)

    products = load_products()
    filtered_products = []
    for p in products:
        match_cat = (state_st.session_state.selected_category == "الكل") or (p["category"] == state_st.session_state.selected_category)
        match_search = (not search_query) or (search_query.lower() in p["name"].lower())
        if match_cat and match_search:
            filtered_products.append(p)

    if not filtered_products:
        state_st.warning("⚠️ عذراً، لا توجد وجبات تطابق اختيارك حالياً.")
        return

    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols_row = state_st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(filtered_products):
                prod = filtered_products[idx]
                cat_name = prod["category"]
                
                # جلب الصورة الذكية المطابقة لاسم الوجبة
                img_url = get_smart_image(prod["name"], cat_name, prod["image"])
                
                with cols_row[j]:
                    with state_st.container():
                        state_st.markdown(
                            f"""
                            <div style="width: 100%; height: 200px; overflow: hidden; border-radius: 16px 16px 0 0;">
                                <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover;" />
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        state_st.markdown(
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
                        
                        if state_st.button(f"🛒 أضف للسلة", key=f"add_{prod['id']}", use_container_width=True):
                            if "cart" not in state_st.session_state:
                                state_st.session_state.cart = []
                            
                            found = False
                            for item in state_st.session_state.cart:
                                if item["id"] == prod["id"]:
                                    item["quantity"] += 1
                                    found = True
                                    break
                            if not found:
                                state_st.session_state.cart.append(
                                    {
                                        "id": prod["id"],
                                        "name": prod["name"],
                                        "price": prod["price"],
                                        "quantity": 1,
                                    }
                                )
                            state_st.success(f"تمت إضافة '{prod['name']}' إلى السلة بنجاح!")
                            state_st.rerun()
