import streamlit as st


def render_footer():

    st.markdown(
        """
<div style="
    margin-top:80px;

    background:#062f38;

    color:white;

    border-radius:
        30px 30px 0 0;

    padding:
        50px 35px 25px;
">

<div style="
    display:grid;

    grid-template-columns:
        repeat(
            auto-fit,
            minmax(220px,1fr)
        );

    gap:35px;

    max-width:1200px;

    margin:auto;
">


<div>

    <div style="
        font-size:24px;
        font-weight:900;
    ">
        🐟 أسماك وادي النيل
    </div>

    <div style="
        color:#b8ced2;
        line-height:2;
        margin-top:10px;
    ">
        طعم البحر .. بطعم مصري أصيل
    </div>

</div>


<div>

    <div style="
        font-size:18px;
        font-weight:900;
    ">
        روابط سريعة
    </div>

    <div style="
        color:#b8ced2;
        line-height:2.2;
        margin-top:10px;
    ">
        الرئيسية<br>
        المنيو<br>
        العروض<br>
        الفروع
    </div>

</div>


<div>

    <div style="
        font-size:18px;
        font-weight:900;
    ">
        خدمة العملاء
    </div>

    <div style="
        color:#b8ced2;
        line-height:2.2;
        margin-top:10px;
    ">
        ☎ الخط الساخن: 19974
        <br>
        📝 الشكاوى والمقترحات
        <br>
        ⭐ تقييم الخدمة
    </div>

</div>


<div>

    <div style="
        font-size:18px;
        font-weight:900;
    ">
        تابعنا
    </div>

    <div style="
        font-size:25px;
        margin-top:15px;
    ">
        Facebook
        <br>
        Instagram
        <br>
        TikTok
    </div>

</div>


</div>


<hr style="
    border:none;
    border-top:
        1px solid
        rgba(255,255,255,.12);
    margin:35px 0 20px;
">


<div style="
    text-align:center;
    color:#9eb6bb;
    font-size:14px;
">

    © 2026 سلسلة مطاعم أسماك وادي النيل

    <br><br>

    ✦ تصميم وتنفيذ المنصة الرقمية ✦

</div>


</div>
""",
        unsafe_allow_html=True,
    )
