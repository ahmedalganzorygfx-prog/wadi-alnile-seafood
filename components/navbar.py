
import streamlit as st


def render_navbar():

    # =========================================================
    # عدد المنتجات في السلة
    # =========================================================

    cart_count = sum(
        item.get("quantity", 0)
        for item in st.session_state.get("cart", [])
    )


    # =========================================================
    # CSS
    # =========================================================

    css = """
    <style>

    /* =====================================================
       NAVBAR
       ===================================================== */

    .nav-wrapper {
        width: 100%;
        position: relative;
        z-index: 999;
        margin-bottom: 25px;
    }


    .nav-inner {
        max-width: 1400px;
        margin: 0 auto;

        padding: 14px 24px;

        display: flex;
        align-items: center;
        justify-content: space-between;

        gap: 20px;

        background: rgba(255, 255, 255, 0.96);

        border: 1px solid rgba(0, 0, 0, 0.06);

        border-radius: 18px;

        box-shadow:
            0 8px 30px rgba(0, 0, 0, 0.08);

        direction: rtl;
    }


    /* =====================================================
       BRAND
       ===================================================== */

    .nav-brand {
        display: flex;
        align-items: center;

        gap: 10px;

        text-decoration: none !important;

        color: #0b3954 !important;

        font-size: 20px;

        font-weight: 800;

        white-space: nowrap;
    }


    .nav-brand-icon {
        width: 42px;
        height: 42px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 12px;

        background:
            linear-gradient(
                135deg,
                #0b3954,
                #087e8b
            );

        color: white;

        font-size: 22px;

        box-shadow:
            0 6px 15px
            rgba(8, 126, 139, 0.25);
    }


    .nav-brand-text {
        line-height: 1.2;
    }


    .nav-brand-sub {
        display: block;

        margin-top: 3px;

        color: #777;

        font-size: 10px;

        font-weight: 500;
    }


    /* =====================================================
       LINKS
       ===================================================== */

    .nav-links {
        display: flex;

        align-items: center;

        justify-content: center;

        gap: 6px;

        flex: 1;
    }


    .nav-link {
        display: inline-flex;

        align-items: center;

        justify-content: center;

        padding: 10px 13px;

        border-radius: 10px;

        text-decoration: none !important;

        color: #344054 !important;

        font-size: 14px;

        font-weight: 600;

        transition:
            background 0.2s ease,
            color 0.2s ease,
            transform 0.2s ease;
    }


    .nav-link:hover {
        background: #eef8fa;

        color: #087e8b !important;

        transform: translateY(-1px);
    }


    /* =====================================================
       CART
       ===================================================== */

    .nav-cart {
        position: relative;

        display: inline-flex;

        align-items: center;

        justify-content: center;

        min-width: 46px;

        height: 44px;

        padding: 0 13px;

        border-radius: 12px;

        background: #0b3954;

        color: white !important;

        text-decoration: none !important;

        font-size: 18px;

        box-shadow:
            0 6px 16px
            rgba(11, 57, 84, 0.18);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }


    .nav-cart:hover {
        color: white !important;

        transform: translateY(-2px);

        box-shadow:
            0 9px 22px
            rgba(11, 57, 84, 0.25);
    }


    /* =====================================================
       CART BADGE
       ===================================================== */

    .cart-badge {
        position: absolute;

        top: -7px;

        left: -7px;

        min-width: 20px;

        height: 20px;

        padding: 0 5px;

        display: flex;

        align-items: center;

        justify-content: center;

        border-radius: 50%;

        background: #e63946;

        color: white;

        font-size: 10px;

        font-weight: 800;

        border: 2px solid white;
    }


    /* =====================================================
       MOBILE
       ===================================================== */

    @media (max-width: 900px) {

        .nav-inner {
            padding: 12px 14px;

            border-radius: 14px;

            flex-wrap: wrap;
        }


        .nav-brand {
            font-size: 17px;
        }


        .nav-brand-icon {
            width: 38px;

            height: 38px;

            font-size: 19px;
        }


        .nav-links {
            order: 3;

            width: 100%;

            overflow-x: auto;

            justify-content: flex-start;

            padding-top: 4px;

            padding-bottom: 2px;

            scrollbar-width: none;
        }


        .nav-links::-webkit-scrollbar {
            display: none;
        }


        .nav-link {
            flex-shrink: 0;

            font-size: 13px;

            padding: 9px 11px;
        }


        .nav-cart {
            height: 40px;

            min-width: 42px;
        }
    }


    /* =====================================================
       SMALL MOBILE
       ===================================================== */

    @media (max-width: 500px) {

        .nav-inner {
            padding: 10px;
        }


        .nav-brand-text {
            font-size: 15px;
        }


        .nav-brand-sub {
            font-size: 9px;
        }


        .nav-link {
            font-size: 12px;
        }
    }

    </style>
    """


    # =========================================================
    # HTML
    # =========================================================

    html = f"""
    <div class="nav-wrapper">

        <div class="nav-inner">

            <a href="#home" class="nav-brand">

                <span class="nav-brand-icon">
                    🐟
                </span>

                <span class="nav-brand-text">

                    أسماك وادي النيل

                    <span class="nav-brand-sub">
                        طعم البحر .. بطعم مصري أصيل
                    </span>

                </span>

            </a>


            <div class="nav-links">

                <a href="#home" class="nav-link">
                    الرئيسية
                </a>

                <a href="#menu" class="nav-link">
                    🍽️ المنيو
                </a>

                <a href="#offers" class="nav-link">
                    🎁 العروض
                </a>

                <a href="#why-us" class="nav-link">
                    ⭐ لماذا نحن
                </a>

                <a href="#branches" class="nav-link">
                    📍 الفروع
                </a>

                <a href="#reviews" class="nav-link">
                    💬 التقييمات
                </a>

            </div>


            <a
                href="#cart"
                class="nav-cart"
                title="سلة الطلبات"
            >

                🛒

                <span class="cart-badge">
                    {cart_count}
                </span>

            </a>

        </div>

    </div>
    """


    # =========================================================
    # عرض CSS + HTML
    # =========================================================

    st.markdown(
        css + html,
        unsafe_allow_html=True
    )
