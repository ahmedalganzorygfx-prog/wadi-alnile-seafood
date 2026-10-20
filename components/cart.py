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

    if "cart" not in st.session_state:
        st.session_state.cart = []

    cart = st.session_state.cart

    if not cart:
        st.info("🛒 السلة فارغة حالياً. أضف بعض الوجبات البحرية اللذيذة من المنيو!")
        return

    total_price = 0

    for idx, item in enumerate(cart):
        item_total = item["price"] * item["quantity"]
        total_price += item_total

        cols = st.columns([3, 2, 2, 1])
        with cols[0]:
            st.markdown(f"**{item['name']}**")
        with cols[1]:
            st.markdown(f"السعر: {item['price']} جنيه")
        with cols[2]:
            new_qty = st.number_input(
                "الكمية",
                min_value=1,
                value=int(item["quantity"]),
                key=f"cart_qty_{item['id']}_{idx}",
            )
            if new_qty != item["quantity"]:
                st.session_state.cart[idx]["quantity"] = new_qty
                st.rerun()
        with cols[3]:
            if st.button("❌", key=f"cart_del_{item['id']}_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()

    st.markdown("---")
    
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; direction: rtl; background: #f8fbfb; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0;">
            <span style="font-size: 18px; font-weight: 900; color: #07566a;">الإجمالي الكلي:</span>
            <span style="font-size: 20px; font-weight: 900; color: #0d9488;">{total_price} جنيه</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ تفريغ السلة بالكامل", use_container_width=True):
        st.session_state.cart = []
        st.rerun()
