import streamlit as st


def section_title(title, subtitle=""):
    st.markdown(
        f"""
        <div style="text-align:center; margin:65px 0 30px; direction:rtl;">
            <div style="font-size:34px; font-weight:900; color:#07566a;">{title}</div>
            <div style="margin-top:8px; color:#68777d; font-size:15px;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_offers():
    section_title("🎁 عروض وادي النيل", "أقوى العروض والوجبات التوفيرية")
    cols = st.columns(2)
    with cols[0]:
        st.markdown(
            """
            <div style="background:linear-gradient(135deg, #07566a, #032027); color:white; padding:30px; border-radius:24px; direction:rtl;">
                <h3>🌊 عرض العائلة البحري</h3>
                <p style="color:#b8ced2; margin:15px 0;">سمك دنيس + كيلو جمبري مشوي + أرز صيادية + شوربة سي فود + سلطات</p>
                <div style="font-size:22px; font-weight:bold; color:#ffb703;">فقط 999 جنيه بدلًا من 1200 جنيه</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            """
            <div style="background:linear-gradient(135deg, #032027, #07566a); color:white; padding:30px; border-radius:24px; direction:rtl;">
                <h3>🦐 وجبة الساحل الفاخرة</h3>
                <p style="color:#b8ced2; margin:15px 0;">نصف كيلو جمبري مقرمش + سمك قاروص + أرز وكاتشب وسلطة طحينة</p>
                <div style="font-size:22px; font-weight:bold; color:#ffb703;">فقط 599 جنيه بدلًا من 700 جنيه</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_why_us():
    section_title("⭐ لماذا أسماك وادي النيل؟", "جودة وثقة تمتد لسنوات")
    cols = st.columns(3)
    features = [
        ("🐟 طازج يومياً", "أسماك بحرية طازجة تصلنا يومياً من أجود الموانئ المصرية."),
        ("👨‍🍳 شيفات محترفون", "نخبة من أفضل الطهاة المتخصصين في إعداد المأكولات البحرية."),
        ("🛡️ معايير نظافة عالية", "تطبيق صارم لأعلى معايير التعقيم والجودة في كافة مراحل التحضير."),
    ]
    for col, (title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div style="background:white; padding:25px; border-radius:20px; border:1px solid #eee; text-align:center; direction:rtl; box-shadow:0 5px 15px rgba(0,0,0,0.03);">
                    <div style="font-size:22px; font-weight:bold; color:#07566a; margin-bottom:10px;">{title}</div>
                    <div style="color:#68777d; font-size:14px; line-height:1.6;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_branches():
    section_title("📍 فروعنا المنتشرة", "زورنا في أقرب فرع ليك")
    cols = st.columns(3)
    branches = [
        ("فرع الدقي", "شارع مصدق، الجيزة", "01000000001"),
        ("فرع الهرم", "استوديو الأهرام، الجيزة", "01000000002"),
        ("فرع مدينة نصر", "شارع مكرم عبيد، القاهرة", "01000000003"),
    ]
    for col, (name, address, phone) in zip(cols, branches):
        with col:
            st.markdown(
                f"""
                <div style="background:white; padding:25px; border-radius:20px; border:1px solid #eee; text-align:center; direction:rtl; box-shadow:0 5px 15px rgba(0,0,0,0.03);">
                    <div style="font-size:20px; font-weight:bold; color:#07566a; margin-bottom:8px;">{name}</div>
                    <div style="color:#68777d; font-size:14px; margin-bottom:10px;">{address}</div>
                    <div style="color:#10b981; font-weight:bold; font-size:14px;">📞 {phone}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_reviews():
    section_title("💬 آراء عملائنا الكرام", "نعتز بثقتكم الغالية")
    cols = st.columns(2)
    reviews = [
        ("أحمد م.", "أفضل مطعم أسماك جربته في الجيزة، الأكل طازج جداً والتوصيل سريع.", "⭐⭐⭐⭐⭐"),
        ("سارة ك.", "الجمبري المشوي عندهم حكاية! تتبيلة ممتازة ونظافة عالية.", "⭐⭐⭐⭐⭐"),
    ]
    for col, (name, comment, stars) in zip(cols, reviews):
        with col:
            st.markdown(
                f"""
                <div style="background:white; padding:25px; border-radius:20px; border:1px solid #eee; direction:rtl; box-shadow:0 5px 15px rgba(0,0,0,0.03);">
                    <div style="font-size:16px; font-weight:bold; color:#07566a; margin-bottom:5px;">{name}</div>
                    <div style="color:#ffb703; margin-bottom:10px;">{stars}</div>
                    <div style="color:#68777d; font-size:14px;">{comment}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
