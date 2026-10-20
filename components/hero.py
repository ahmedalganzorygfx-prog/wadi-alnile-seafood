import streamlit as st


def render_hero():
    st.markdown(
        """
        <style>
        .hero-box {
            position: relative;
            min-height: 480px;
            border-radius: 34px;
            overflow: hidden;
            margin: 10px 0 55px 0;
            background: linear-gradient(90deg, rgba(3,32,39,.95), rgba(3,45,54,.78), rgba(3,45,54,.20)), url('https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=1800&q=90');
            background-size: cover;
            background-position: center;
            display: flex;
            align-items: center;
            padding: 50px;
            direction: rtl;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        .hero-inner {
            max-width: 650px;
            color: white;
        }
        .hero-main-title {
            font-size: 42px;
            font-weight: 900;
            margin-bottom: 20px;
            line-height: 1.3;
            color: white !important;
        }
        .hero-sub {
            font-size: 18px;
            color: #b8ced2;
            margin-bottom: 30px;
            line-height: 1.8;
        }
        .hero-action-btn {
            background: #ffb703;
            color: #032027 !important;
            padding: 12px 30px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 16px;
            text-decoration: none;
            box-shadow: 0 5px 20px rgba(255,183,3,0.4);
            display: inline-block;
        }
        </style>

        <div class="hero-box">
            <div class="hero-inner">
                <div class="hero-main-title">طعم البحر .. بطعم مصري أصيل 🐟</div>
                <div class="hero-sub">استمتع بأفخر أنواع الأسماك الطازجة، والجمبري، والمأكولات البحرية المُجهزة بأعلى معايير الجودة والنظافة لتلبي ذوقك الرفيع.</div>
                <a href="#menu" class="hero-action-btn">تصفح المنيو الآن</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
