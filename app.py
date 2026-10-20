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

render_hero()

render_menu()

render_cart()

render_checkout()

render_offers()

render_why_us()

render_branches()

render_reviews()

render_footer()
