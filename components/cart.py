import streamlit as st


def get_cart_total():
    cart = st.session_state.get("cart", [])
    return sum(item["price"] * item["quantity"] for item in cart)


def render_cart():
    cart = st.session_state.get("cart", [])
    if not cart:
        return

    st.markdown(
        """
        <div id="cart"></div>
        <div style="text-align:center; margin:60px 0 25px; direction:rtl;">
            <h2 style="color:#07566a; font-size:36px; font-weight:900;">🛒 سلة المشتريات</h2>
            <p style="color:#68777d;">راجع طلباتك وعدّل الكميات قبل التأكيد</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total = 0
    for idx, item in enumerate(cart):
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        with col1:
            st.markdown(f"**{item['name']}**")
        with col2:
            st.markdown(f"السعر: {item['price']} ج.م")
        with col3:
            # زر تحديث الكمية
            new_qty = st.number_input(
                "الكمية",
                min_value=1,
                max_value=50,
                value=item["quantity"],
                key=f"qty_{idx}",
                label_visibility="collapsed",
            )
            if new_qty != item["quantity"]:
                item["quantity"] = new_qty
                st.rerun()
        with col4:
            if st.button("🗑️", key=f"del_{idx}"):
                cart.pop(idx)
                st.session_state.cart = cart
                st.rerun()

        total += item["price"] * item["quantity"]
        st.markdown("<hr style='margin:5px 0; border:0; border-top:1px solid #eee;'>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="background:#f0f4f5; padding:20px; border-radius:15px; text-align:center; margin:20px 0; direction:rtl;">
            <span style="font-size:20px; font-weight:bold; color:#07566a;">الإجمالي الكلي: {total} جنيه</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🗑️ إفراغ السلة بالكامل", use_container_width=True):
        st.session_state.cart = []
        st.rerun()
