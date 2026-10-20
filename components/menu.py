import streamlit as st

# عرض عنوان المطعم بخط كبير في منتصف الصفحة
st.markdown(
    """
    <div style="
        text-align: center;
        margin: 40px 0 20px 0;
        direction: rtl;
    ">
        <h1 style="
            font-size: 48px;
            font-weight: 900;
            color: #07566a;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
            margin-bottom: 10px;
        ">
            مطاعم أسماك وادي النيل 🐟
        </h1>
        <p style="
            font-size: 18px;
            color: #68777d;
            font-weight: 600;
        ">
            طعم البحر .. بطعم مصري أصيل
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
