import streamlit as st


def render_footer():
    st.markdown(
        """
        <div style="
            margin-top:80px;
            background:#062f38;
            color:white;
            border-radius:30px 30px 0 0;
            padding:50px 35px 25px;
            direction:rtl;
        ">
            <div style="
                display:grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap:35px;
                max-width:1200px;
                margin:auto;
            ">
                <div>
                    <h2>🐟 أسماك وادي النيل</h2>
                    <p style="color:#b8ced2; line-height:2; margin-top:10px;">
                        طعم البحر .. بطعم مصري أصيل. نقدم أشهى المأكولات البحرية الطازجة بمعايير عالمية.
                    </p>
                </div>
                <div>
                    <h3 style="color:#ffb703; margin-bottom:15px;">☎️ خدمة العملاء</h3>
                    <p style="color:#b8ced2; line-height:1.8;">الخط الساخن: 19974</p>
                    <p style="color:#b8ced2; line-height:1.8;">متاحون طوال أيام الأسبوع من 12 ظهرًا حتى 2 صباحًا</p>
                </div>
                <div>
                    <h3 style="color:#ffb703; margin-bottom:15px;">🔗 روابط سريعة</h3>
                    <p><a href="#home" style="color:#b8ced2; text-decoration:none;">الرئيسية</a></p>
                    <p><a href="#menu" style="color:#b8ced2; text-decoration:none;">المنيو</a></p>
                    <p><a href="#cart" style="color:#b8ced2; text-decoration:none;">سلة المشتريات</a></p>
                </div>
            </div>
            <div style="text-align:center; border-top:1px solid rgba(255,255,255,0.1); margin-top:40px; padding-top:20px; color:#8ca5ab; font-size:14px;">
                جميع الحقوق محفوظة © 2026 سلسلة مطاعم أسماك وادي النيل
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
