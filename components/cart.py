import streamlit as st


# =========================================================
# حساب إجمالي السلة
# =========================================================

def get_cart_total():

    cart = st.session_state.get("cart", [])

    return sum(
        item["price"] * item["quantity"]
        for item in cart
    )


# =========================================================
# عرض السلة
# =========================================================

def render_cart():

    # =====================================================
    # CSS
    # =====================================================

    css = """
    <style>

    /* =====================================================
       CART SECTION
       ===================================================== */

    .cart-section {
        width: 100%;
        margin-top: 65px;
        margin-bottom: 30px;
    }


    .cart-title {
        text-align: center;

        color: #07566a;

        font-size: 40px;

        font-weight: 900;

        line-height: 1.3;
    }


    .cart-subtitle {
        text-align: center;

        color: #718087;

        font-size: 16px;

        margin-top: 8px;
    }


    /* =====================================================
       EMPTY CART
       ===================================================== */

    .empty-cart {

        background: white;

        border-radius: 25px;

        padding: 60px 20px;

        text-align: center;

        box-shadow:
            0 10px 30px
            rgba(0, 0, 0, 0.05);

        border:
            1px solid #edf0f1;
    }


    .empty-cart-icon {

        font-size: 65px;
    }


    .empty-cart-title {

        color: #07566a;

        font-size: 25px;

        font-weight: 900;

        margin-top: 10px;
    }


    .empty-cart-text {

        color: #718087;

        margin-top: 8px;

        font-size: 15px;
    }


    /* =====================================================
       CART ITEM
       ===================================================== */

    .cart-item {

        background: white;

        border-radius: 20px;

        padding: 18px;

        margin-bottom: 12px;

        border:
            1px solid #edf0f1;

        box-shadow:
            0 5px 20px
            rgba(0, 0, 0, 0.03);

        min-height: 85px;

        direction: rtl;
    }


    .cart-item-name {

        color: #07566a;

        font-size: 18px;

        font-weight: 900;

        line-height: 1.5;
    }


    .cart-item-price {

        color: #718087;

        font-size: 13px;

        margin-top: 5px;
    }


    .cart-item-total {

        padding-top: 18px;

        color: #b47b27;

        font-size: 18px;

        font-weight: 900;

        text-align: center;
    }


    /* =====================================================
       QUANTITY
       ===================================================== */

    .quantity-number {

        text-align: center;

        padding-top: 8px;

        font-size: 16px;

        font-weight: 900;

        color: #07566a;
    }


    /* =====================================================
       TOTAL BOX
       ===================================================== */

    .cart-total {

        background:
            linear-gradient(
                135deg,
                #07566a,
                #0b8296
            );

        color: white;

        border-radius: 24px;

        padding: 28px;

        margin-top: 25px;

        text-align: center;

        box-shadow:
            0 15px 35px
            rgba(7, 86, 106, 0.18);
    }


    .cart-total-label {

        font-size: 15px;

        opacity: 0.85;
    }


    .cart-total-value {

        font-size: 36px;

        font-weight: 900;

        margin-top: 5px;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 900px) {

        .cart-title {
            font-size: 34px;
        }

        .cart-subtitle {
            font-size: 14px;
        }

        .cart-item-name {
            font-size: 16px;
        }

        .cart-item-total {
            font-size: 16px;
        }

        .cart-total-value {
            font-size: 32px;
        }
    }


    @media (max-width: 600px) {

        .cart-section {
            margin-top: 45px;
        }

        .cart-title {
            font-size: 29px;
        }

        .empty-cart {
            padding: 45px 15px;
        }

        .cart-item {
            padding: 14px;
        }

        .cart-total {
            padding: 22px 15px;
        }

        .cart-total-value {
            font-size: 28px;
        }
    }

    </style>
    """


    # =====================================================
    # HTML - عنوان السلة
    # =====================================================

    html = """
    <div id="cart"></div>

    <div class="cart-section">

        <div class="cart-title">
            🛒 سلة المشتريات
        </div>

        <div class="cart-subtitle">
            راجع طلبك قبل المتابعة
        </div>

    </div>
    """


    # =====================================================
    # عرض CSS + HTML
    # =====================================================

    st.markdown(
        css + html,
        unsafe_allow_html=True
    )


    # =====================================================
    # قراءة السلة
    # =====================================================

    cart = st.session_state.get(
        "cart",
        []
    )


    # =====================================================
    # السلة فارغة
    # =====================================================

    if not cart:

        empty_cart = """
        <div class="empty-cart">

            <div class="empty-cart-icon">
                🛒
            </div>

            <div class="empty-cart-title">
                السلة فارغة
            </div>

            <div class="empty-cart-text">
                اختر بعض الأطباق الشهية من المنيو
            </div>

        </div>
        """

        st.markdown(
            empty_cart,
            unsafe_allow_html=True
        )

        return


    # =====================================================
    # عرض المنتجات
    # =====================================================

    total = 0


    for index, item in enumerate(cart):

        item_total = (
            item["price"]
            * item["quantity"]
        )

        total += item_total


        # -------------------------------------------------
        # الأعمدة
        # -------------------------------------------------

        col1, col2, col3, col4 = st.columns(
            [3, 1.5, 1.5, 1]
        )


        # =================================================
        # بيانات المنتج
        # =================================================

        with col1:

            item_html = f"""
            <div class="cart-item">

                <div class="cart-item-name">
                    {item["name"]}
                </div>

                <div class="cart-item-price">
                    {item["price"]:,.0f} جنيه للقطعة
                </div>

            </div>
            """

            st.markdown(
                item_html,
                unsafe_allow_html=True
            )


        # =================================================
        # التحكم في الكمية
        # =================================================

        with col2:

            st.markdown(
                "<div style='height:18px;'></div>",
                unsafe_allow_html=True
            )


            minus_col, qty_col, plus_col = st.columns(3)


            # -------------------------------------------------
            # ناقص
            # -------------------------------------------------

            with minus_col:

                if st.button(
                    "−",
                    key=f"minus_{item['id']}_{index}",
                    use_container_width=True,
                ):

                    if item["quantity"] > 1:

                        item["quantity"] -= 1

                    else:

                        st.session_state.cart.pop(index)

                    st.rerun()


            # -------------------------------------------------
            # العدد
            # -------------------------------------------------

            with qty_col:

                st.markdown(
                    f"""
                    <div class="quantity-number">
                        {item["quantity"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # -------------------------------------------------
            # زائد
            # -------------------------------------------------

            with plus_col:

                if st.button(
                    "+",
                    key=f"plus_{item['id']}_{index}",
                    use_container_width=True,
                ):

                    item["quantity"] += 1

                    st.rerun()


        # =================================================
        # إجمالي المنتج
        # =================================================

        with col3:

            st.markdown(
                f"""
                <div class="cart-item-total">
                    {item_total:,.0f} ج
                </div>
                """,
                unsafe_allow_html=True
            )


        # =================================================
        # حذف المنتج
        # =================================================

        with col4:

            st.markdown(
                "<div style='height:18px;'></div>",
                unsafe_allow_html=True
            )


            if st.button(
                "🗑️",
                key=f"remove_{item['id']}_{index}",
                use_container_width=True,
            ):

                st.session_state.cart.pop(index)

                st.rerun()


    # =====================================================
    # إجمالي الطلب
    # =====================================================

    total = get_cart_total()


    total_html = f"""
    <div class="cart-total">

        <div class="cart-total-label">
            إجمالي الطلب
        </div>

        <div class="cart-total-value">
            {total:,.0f} جنيه
        </div>

    </div>
    """


    st.markdown(
        total_html,
        unsafe_allow_html=True
    )


    st.write("")


    # =====================================================
    # أزرار السلة
    # =====================================================

    col1, col2 = st.columns(2)


    # =====================================================
    # إفراغ السلة
    # =====================================================

    with col1:

        if st.button(
            "🗑️ إفراغ السلة",
            use_container_width=True,
        ):

            st.session_state.cart = []

            st.rerun()


    # =====================================================
    # متابعة الطلب
    # =====================================================

    with col2:

        if st.button(
            "➡️ متابعة الطلب",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.checkout = True

            st.success(
                "تم تجهيز السلة بنجاح. سيتم الانتقال إلى بيانات الطلب في المرحلة القادمة."
            )
