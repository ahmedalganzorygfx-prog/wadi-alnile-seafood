import streamlit as st

def render_branches():
    st.markdown('<div id="branches"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align: right; margin: 40px 0 20px 0; direction: rtl;">
            <h2 style="color: #ffffff; font-size: 28px; font-weight: 900;">📍 فروعنا ومواقع التوصيل</h2>
            <p style="color: #94a3b8; font-size: 14px;">تواصل معنا أو زورنا في أقرب فرع لأسماك وادي النيل</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    branches_data = [
        {
            "name": "فرع المهندسين",
            "phones": ["01092006002", "01092006003", "19974"],
            "map": "https://goo.gl/maps/SdWDEPCEsrwy4BvW7"
        },
        {
            "name": "فرع حدائق الأهرام",
            "phones": ["01050249997", "01050249996"],
            "map": "https://goo.gl/maps/y4gzmRbVRWZL9dfa8"
        },
        {
            "name": "فرع الشيخ زايد (تيك أواي)",
            "phones": ["01066669732", "01119107773", "01118799952"],
            "map": "#"
        },
        {
            "name": "طريق الواحات",
            "phones": ["01093304338", "01033025034"],
            "map": "https://maps.app.goo.gl/25VyqTqom95GznD37"
        },
        {
            "name": "المحور المركزي بالشيخ زايد",
            "phones": ["01050555726", "01050555725"],
            "map": "https://maps.app.goo.gl/w6p8K7uw728shbDG7"
        },
        {
            "name": "فرع الساحل الشمالي",
            "phones": ["01050244426", "01050244425"],
            "address": "قرية قرطاج - الكيلو 81 - طريق إسكندرية مطروح",
            "map": "https://maps.app.goo.gl/Dep4XWTvjHtHRvi5"
        }
    ]

    cols_per_row = 3
    for i in range(0, len(branches_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(branches_data):
                branch = branches_data[idx]
                phones_str = " - ".join(branch["phones"])
                
                with cols[j]:
                    with st.container(border=True):
                        st.markdown(f"<div style='text-align: right; direction: rtl;'><strong>📍 {branch['name']}</strong></div>", unsafe_allow_html=True)
                        
                        if "address" in branch:
                            st.markdown(f"<div style='text-align: right; direction: rtl; color: #cbd5e1; font-size: 12px; margin-top: 5px;'>{branch['address']}</div>", unsafe_allow_html=True)
                        
                        st.markdown(f"<div style='text-align: right; direction: rtl; font-size: 13px; color: #ffb703; margin-top: 8px;'>📞 الهواتف: <span style='color: #ffffff;'>{phones_str}</span></div>", unsafe_allow_html=True)
                        
                        if branch["map"] != "#":
                            st.markdown(f"<div style='text-align: right; direction: rtl; margin-top: 10px;'><a href='{branch['map']}' target='_blank' style='color: #38bdf8; text-decoration: none; font-size: 12px; font-weight: bold;'>🗺️ موقع الفرع على الخريطة</a></div>", unsafe_allow_html=True)
