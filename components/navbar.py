import streamlit as st

def render_navbar():
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
