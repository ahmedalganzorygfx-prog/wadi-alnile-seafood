import streamlit as st

from database.database import init_database

from components.navbar import render_navbar
from components.hero import render_hero
from components.menu import render_menu
from components.cart import render_cart
from components.checkout import render_checkout
from components.cards import (
    render_offers,
    render_why_us,
    render_branches,
    render_reviews,
)
from components.footer import render_footer


# =========================================================
# إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="أسماك وادي النيل | طعم البحر .. بطعم مصري أصيل",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# تهيئة Session State للسلة
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []


# =========================================================
# تهيئة قاعدة البيانات والجداول
# =========================================================

init_database()


# =========================================================
# عرض مكونات الموقع
# =========================================================

render_navbar()

# عرض عنوان المطعم بخط كبير في منتصف الصفحة
st.markdown(
    """
    <div style="
        text-align: center;
        margin: 40px 0 20px 0;
        direction: rtl;
    ">
        <h1 style="
            font-size: 52px;
            font-weight: 900;
            color: #07566a;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
            margin-bottom: 10px;
        ">
            مطاعم أسماك وادي النيل 🐟
        </h1>
        <p style="
            font-size: 20px;
            color: #ffb703;
            font-weight: 700;
        ">
            طعم البحر .. بطعم مصري أصيل
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

render_hero()

render_menu()

render_cart()

render_checkout()

render_offers()

render_why_us()

render_branches()

render_reviews()

render_footer()
