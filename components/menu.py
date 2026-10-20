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

# صور معبرة افتراضية لكل تصنيف (يمكن استبدالها بروابط أو مسارات صور حقيقية لاحقاً)
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

    # عرض المنتجات في شبكة (Grid) مع صور معبرة وتصميم بطاقات احترافي
    cols_per_row = 3
    for i in range(0, len(filtered_products), cols_per_row):
        cols_row = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(filtered_products):
                prod = filtered_products[idx]
                cat_name = prod["category"]
                # استخدام صورة المنتج إن وجدت، وإلا استخدام الصورة الافتراضية الخاصة بالتصنيف
                img_url = prod["image"] if prod["image"] else CATEGORY_IMAGES.get(cat_name, "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80")
                
                with cols_row[j]:
                    with st.container():
                        st.markdown(
                            f"""
                            <div style="
                                background: linear-gradient(180deg, #ffffff 0%, #f8fbfb 100%);
                                border: 1px solid rgba(7, 86, 106, 0.12);
                                border-radius: 20px;
                                overflow: hidden;
                                margin-bottom: 20px;
                                box-shadow: 0 10px 25px rgba(7, 86, 106, 0.06);
                                text-align: right;
                                direction: rtl;
                                transition: transform 0.3s ease, box-shadow 0.3s ease;
                            ">
                                <div style="width: 100%; height: 180px; overflow: hidden;">
                                    <img src="{img_url}" alt="{prod['name']}" style="width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease;">
                                </div>
                                <div style="padding: 20px;">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                        <div style="font-size: 20px; font-weight: 900; color: #07566a;">
                                            {prod['name']}
                                        </div>
                                        <div style="font-size: 11px; background: #eef4f6; color: #07566a; padding: 3px 10px; border-radius: 12px; font-weight: bold;">
                                            {cat_name}
                                        </div>
                                    </div>
                                    <div style="font-size: 13px; color: #68777d; margin-bottom: 15px; min-height: 40px; line-height: 1.6;">
                                        {prod['description'] or 'وجبة بحرية طازجة ومميزة مُجهزة بأعلى معايير الجودة'}
                                    </div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #edf2f4; padding-top: 12px;">
                                        <div style="font-size: 18px; font-weight: 900; color: #0d9488;">
                                            {prod['price']} جنيه
                                        </div>
                                        <div style="font-size: 11px; background: #e6f4f1; color: #0d9488; padding: 3px 8px; border-radius: 10px; font-weight: bold;">
                                            ⭐ طازج يومياً
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button(f"🛒 أضف للسلة", key=f"add_{prod['id']}", use_container_width=True):
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
