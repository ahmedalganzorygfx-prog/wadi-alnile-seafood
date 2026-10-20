import streamlit as st

def render_cart():
    st.markdown('<div id="cart"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align:right; margin:40px 0 20px 0; direction:rtl;">
            <h3 style="color:#07566a; font-size:28px; font-weight:900;">🛒 سلة المشتريات</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cart = st.session_state.get("cart", [])

    if not cart:
        st.info("🛒 السلة فارغة حالياً. أضف بعض الوجبات البحرية اللذيذة من المنيو!")
        return

    total_price = 0

    # عرض عناصر السلة في جدول أو بطاقات منظمة
    for idx, item in enumerate(cart):
        item_total = item["price"] * item["quantity"]
        total_price += item_total

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
        with col2:
            st.markdown(f"السعر: {item['price']} جنيه")
        with col3:
            # التحكم في الكمية
            new_qty = st.number_input(
                "الكمية",
                min_value=1,
                value=item["quantity"],
                key=f"qty_{item['id']}_{idx}",
                label_visibility="collapsed"
            )
            if new_qty != item["quantity"]:
                item["quantity"] = new_qty
                st.rerun()
        with col4:
            if st.button("❌", key=f"del_{item['id']}_{idx}"):
                cart.pop(idx)
                st.session_state.cart = cart
                st.rerun()

    st.markdown("---")
    
    # إجمالي السلة
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; direction: rtl; background: #f8fbfb; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;">
            <span style="font-size: 18px; font-weight: 900; color: #07566a;">الإجمالي الكلي:</span>
            <span style="font-size: 20px; font-weight: 900; color: #0d9488;">{total_price} جنيه</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
