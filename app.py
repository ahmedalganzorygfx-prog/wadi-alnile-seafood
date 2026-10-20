import streamlit as st

from database.database import init_database
from components.navbar import render_navbar
from components.menu import render_menu
from components.cart import render_cart
from components.checkout import render_checkout
from components.admin import render_admin
from components.branches import render_branches
from components.cards import (
    render_offers,
    render_why_us,
    render_reviews,
)
from components.footer import render_footer

# =========================================================
# إعداد الصفحة وإخفاء الشريط الجانبي
# =========================================================

st.set_page_config(
    page_title="أسماك وادي النيل | طعم البحر .. بطعم مصري أصيل",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {display: none;}
    [data-testid="collapsedControl"] {display: none;}
    header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
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
# عرض مكونات الموقع وترتيبها في منتصف الصفحة
# =========================================================

render_navbar()

# العنوان والشعار في منتصف الصفحة تماماً
st.markdown(
    """
    <div style="
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin: 30px auto;
        direction: rtl;
        width: 100%;
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

# قائمة الطعام (المنيو)
render_menu()

# سلة المشتريات
render_cart()

# شاشة إتمام الطلب
render_checkout()

# لوحة التحكم الإدارية
render_admin()

# فروع المطعم وأرقام التواصل
render_branches()

# الأقسام الترويجية والإضافية
render_offers()
render_why_us()
render_reviews()

# تذييل الصفحة (Footer)
render_footer()
