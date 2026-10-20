import streamlit as st

# عرض عنوان المطعم بخط كبير في منتصف الصفحة مع إمكانية التحكم في الألوان والحجم
st.markdown(
    """
    <div style="
        text-align: center;
        margin: 40px 0 20px 0;
        direction: rtl;
    ">
        <h1 style="
            font-size: 52px; /* يمكنك زيادة أو تقليل حجم الخط من هنا */
            font-weight: 900;
            color: #07566a; /* لون العنوان الرئيسي (أزرق داكن فاخر) */
            text-shadow: 2px 2px 4px rgba(0,0,0,0.08);
            margin-bottom: 10px;
        ">
            مطاعم أسماك وادي النيل 🐟
        </h1>
        <p style="
            font-size: 20px; /* حجم الخط النص الفرعي */
            color: #ffb703; /* لون ترحيبي ذهبي دافئ متناسق */
            font-weight: 700;
        ">
            طعم البحر .. بطعم مصري أصيل
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
