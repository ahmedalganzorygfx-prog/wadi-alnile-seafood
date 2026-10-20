
import streamlit as st


def render_hero():

    # =========================================================
    # CSS
    # =========================================================

    css = """
    <style>

    .hero {
        position: relative;
        min-height: 510px;
        border-radius: 34px;
        overflow: hidden;
        margin: 10px 0 55px 0;

        background:
            linear-gradient(
                90deg,
                rgba(3,32,39,.95),
                rgba(3,45,54,.78),
                rgba(3,45,54,.15)
            ),

            url(
                "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1800&q=90"
            );

        background-size: cover;
        background-position: center;
    }


    .hero-content {
        min-height: 510px;

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;

        padding: 60px;

        color: white;

        max-width: 800px;
    }


    .hero-badge {
        display: inline-block;

        padding: 8px 16px;

        border-radius: 50px;

        background: rgba(255,255,255,.13);

        border: 1px solid rgba(255,255,255,.20);

        backdrop-filter: blur(10px);

        font-size: 14px;
        font-weight: 700;

        margin-bottom: 18px;
    }


    .hero-title {
        font-size: clamp(38px,5vw,70px);

        line-height: 1.15;

        font-weight: 900;

        margin-bottom: 18px;
    }


    .hero-title span {
        color: #8bd8df;
    }


    .hero-subtitle {
        font-size: 20px;

        line-height: 1.9;

        color: rgba(255,255,255,.90);

        margin-bottom: 28px;

        max-width: 650px;
    }


    .hero-info {
        display: flex;

        gap: 12px;

        flex-wrap: wrap;
    }


    .hero-info-item {
        background: rgba(255,255,255,.10);

        border: 1px solid rgba(255,255,255,.15);

        padding: 10px 16px;

        border-radius: 14px;

        backdrop-filter: blur(8px);

        font-weight: 700;
    }


    @media(max-width:700px) {

        .hero {
            min-height: 620px;
        }

        .hero-content {
            min-height: 620px;

            padding: 30px;
        }

        .hero-title {
            font-size: clamp(34px, 9vw, 48px);
        }

        .hero-subtitle {
            font-size: 17px;
        }
    }

    </style>
    """


    # =========================================================
    # HTML
    # =========================================================

    html = """
    <section id="home">

        <div class="hero">

            <div class="hero-content">

                <div class="hero-badge">
                    🌊 خبرة • جودة • طعم مصري أصيل
                </div>


                <div class="hero-title">

                    سلسلة مطاعم

                    <br>

                    <span>
                        أسماك وادي النيل
                    </span>

                </div>


                <div class="hero-subtitle">

                    طعم البحر .. بطعم مصري أصيل

                    <br>

                    أجود المأكولات البحرية بطابع مصري مميز،
                    وتجربة تجمع بين الجودة والطعم والضيافة.

                </div>


                <div class="hero-info">

                    <div class="hero-info-item">
                        🐟 أسماك طازجة
                    </div>

                    <div class="hero-info-item">
                        🦐 مأكولات بحرية
                    </div>

                    <div class="hero-info-item">
                        🚚 خدمة توصيل
                    </div>

                </div>

            </div>

        </div>

    </section>
    """


    # =========================================================
    # عرض HTML
    # =========================================================

    st.markdown(
        css + html,
        unsafe_allow_html=True
    )


    # =========================================================
    # أزرار الإجراءات
    # =========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "🍽️ استعرض المنيو",
            use_container_width=True,
        ):

            st.toast(
                "مرحبًا بك في منيو أسماك وادي النيل 🐟"
            )


    with col2:

        if st.button(
            "🛒 اطلب الآن",
            use_container_width=True,
        ):

            st.toast(
                "أضف منتجاتك إلى السلة للمتابعة 🛒"
            )


    with col3:

        if st.button(
            "📍 أقرب فرع",
            use_container_width=True,
        ):

            st.toast(
                "سيتم تفعيل البحث عن أقرب فرع في المرحلة القادمة 📍"
            )
