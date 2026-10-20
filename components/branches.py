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
                
                address_html = f'<p style="color: #cbd5e1; font-size: 12px; margin-bottom: 8px;">{branch["address"]}</p>' if "address" in branch else ""
                map_html = f'<a href="{branch["map"]}" target="_blank" style="display: inline-block; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 6px 12px; border-radius: 8px; text-decoration: none; font-size: 12px; font-weight: bold; margin-top: 10px;">🗺️ موقع الفرع على الخريطة</a>' if branch['map'] != "#" else ""

                with cols[j]:
                    st.markdown(
                        f"""
                        <div style="
                            background: #0b2538;
                            border: 1px solid rgba(255, 255, 255, 0.08);
                            border-radius: 16px;
                            padding: 20px;
                            margin-bottom: 20px;
                            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
                            text-align: right;
                            direction: rtl;
                        ">
                            <div style="font-size: 18px; font-weight: 900; color: #ffffff; margin-bottom: 8px;">
                                📍 {branch['name']}
                            </div>
                            {address_html}
                            <div style="font-size: 13px; color: #ffb703; font-weight: bold; margin-bottom: 10px;">
                                📞 الهواتف: <span style="color: #ffffff; font-weight: normal;">{phones_str}</span>
                            </div>
                            {map_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
