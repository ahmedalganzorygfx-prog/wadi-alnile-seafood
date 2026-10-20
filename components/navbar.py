import streamlit as st

def render_navbar():
    # كود CSS لإخفاء زر القائمة الجانبية الافتراضي لستريمليت وجعل شريط التنقل علوياً بالكامل
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # شريط التنقل العلوي الأفقي
    st.markdown(
        """
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #07566a;
            padding: 12px 25px;
            border-radius: 12px;
            direction: rtl;
            color: white;
            box-shadow: 0 4px 12px rgba(7,86,106,0.15);
            margin-bottom: 20px;
        ">
            <div style="font-size: 20px; font-weight: 900; color: #ffb703;">
                🐟 وادي النيل للأسماك
            </div>
            <div style="font-size: 14px; font-weight: 600; color: #e2e8f0;">
                📞 الخط الساخن: <span style="color: #ffb703; font-weight: 900;">19974</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # أزرار التنقل السريع الأفقية
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🏠 الرئيسية", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("🍽️ المنيو", use_container_width=True):
            st.rerun()
    with col3:
        if st.button("🛒 سلة المشتريات", use_container_width=True):
            st.rerun()
    with col4:
        if st.button("📋 إتمام الطلب", use_container_width=True):
            st.rerun()
    
    st.markdown("<hr style='margin: 10px 0 25px 0; border: 0; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
