import streamlit as st


def section_title(title, subtitle=""):

    st.markdown(
        f"""
<div style="
    text-align:center;
    margin:65px 0 30px;
">

    <div style="
        font-size:34px;
        font-weight:900;
        color:#07566a;
    ">
        {title}
    </div>

    <div style="
        margin-top:8px;
        color:#68777d;
        font-size:15px;
    ">
        {subtitle}
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


def render_offers():

    st.markdown(
        '<div id="offers"></div>',
        unsafe_allow_html=True
    )


    section_title(
        "🎁 عروض وادي النيل",
        "عروض مميزة تناسب العائلة والأصدقاء"
    )


    offers = [

        (
            "عرض العائلة",
            "وجبة بحرية متكاملة للعائلة",
            "خصم خاص"
        ),

        (
            "عرض نهاية الأسبوع",
            "اختيارات مميزة بأسعار خاصة",
            "لفترة محدودة"
        ),

        (
            "عرض الجمبري",
            "استمتع بأطباق الجمبري المميزة",
            "اطلب الآن"
        ),

    ]


    cols = st.columns(3)


    for col, offer in zip(
        cols,
        offers
    ):

        title, description, label = offer


        with col:

            st.markdown(
                f"""
<div style="
    padding:30px;

    min-height:190px;

    border-radius:25px;

    background:
        linear-gradient(
            135deg,
            #07566a,
            #0b8296
        );

    color:white;

    box-shadow:
        0 15px 35px
        rgba(7,86,106,.18);

    margin-bottom:20px;
">

    <div style="
        font-size:13px;
        opacity:.85;
    ">
        🎁 عرض خاص
    </div>

    <div style="
        font-size:25px;
        font-weight:900;
        margin-top:10px;
    ">
        {title}
    </div>

    <div style="
        margin-top:8px;
        opacity:.9;
    ">
        {description}
    </div>

    <div style="
        margin-top:20px;
        font-weight:900;
    ">
        {label}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


def render_why_us():

    st.markdown(
        '<div id="why-us"></div>',
        unsafe_allow_html=True
    )


    section_title(
        "لماذا أسماك وادي النيل؟",
        "لأن التجربة عندنا تبدأ من جودة المكونات"
    )


    items = [

        (
            "🐟",
            "جودة الأسماك",
            "نختار أفضل المكونات بعناية."
        ),

        (
            "👨‍🍳",
            "خبرة الطهي",
            "نكهات مصرية أصيلة بلمسة عصرية."
        ),

        (
            "🚚",
            "خدمة مميزة",
            "نهتم بتجربة العميل من البداية للنهاية."
        ),

        (
            "❤️",
            "ثقة عملائنا",
            "رضا العملاء هو هدفنا الأول."
        ),

    ]


    cols = st.columns(4)


    for col, item in zip(
        cols,
        items
    ):

        icon, title, text = item


        with col:

            st.markdown(
                f"""
<div style="
    background:#ffffff;

    padding:25px;

    border-radius:22px;

    text-align:center;

    min-height:190px;

    border:
        1px solid #edf0f1;

    box-shadow:
        0 8px 25px
        rgba(0,0,0,.04);
">

    <div style="
        font-size:38px;
    ">
        {icon}
    </div>

    <div style="
        color:#07566a;
        font-size:19px;
        font-weight:900;
        margin-top:8px;
    ">
        {title}
    </div>

    <div style="
        color:#75838a;
        margin-top:8px;
        font-size:14px;
    ">
        {text}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


def render_branches():

    st.markdown(
        '<div id="branches"></div>',
        unsafe_allow_html=True
    )


    section_title(
        "📍 فروعنا",
        "نحن أقرب إليك"
    )


    branches = [

        (
            "فرع وادي النيل",
            "القاهرة",
            "متاح للطلب والتوصيل"
        ),

        (
            "فرع الجيزة",
            "الجيزة",
            "متاح للطلب والاستلام"
        ),

        (
            "فرع أكتوبر",
            "مدينة 6 أكتوبر",
            "متاح للطلب والتوصيل"
        ),

    ]


    cols = st.columns(3)


    for col, branch in zip(
        cols,
        branches
    ):

        name, location, status = branch


        with col:

            st.markdown(
                f"""
<div style="
    background:white;

    border-radius:22px;

    padding:25px;

    border:
        1px solid #edf0f1;

    margin-bottom:20px;

    box-shadow:
        0 8px 25px
        rgba(0,0,0,.04);
">

    <div style="
        font-size:35px;
    ">
        🏪
    </div>

    <div style="
        color:#07566a;
        font-size:20px;
        font-weight:900;
        margin-top:8px;
    ">
        {name}
    </div>

    <div style="
        margin-top:8px;
        color:#66757c;
    ">
        📍 {location}
    </div>

    <div style="
        margin-top:10px;
        color:#16845a;
        font-size:13px;
        font-weight:700;
    ">
        ● {status}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


def render_reviews():

    st.markdown(
        '<div id="reviews"></div>',
        unsafe_allow_html=True
    )


    section_title(
        "⭐ آراء عملائنا",
        "ثقتكم هي نجاحنا"
    )


    reviews = [

        (
            "محمد أحمد",
            "⭐⭐⭐⭐⭐",
            "الأكل ممتاز والطعم رائع جدًا."
        ),

        (
            "سارة محمود",
            "⭐⭐⭐⭐⭐",
            "تجربة جميلة وخدمة محترمة."
        ),

        (
            "أحمد علي",
            "⭐⭐⭐⭐⭐",
            "الجمبري ممتاز وأنصح به جدًا."
        ),

    ]


    cols = st.columns(3)


    for col, review in zip(
        cols,
        reviews
    ):

        name, stars, text = review


        with col:

            st.markdown(
                f"""
<div style="
    background:white;

    padding:25px;

    border-radius:22px;

    border:
        1px solid #edf0f1;

    margin-bottom:25px;

    box-shadow:
        0 8px 25px
        rgba(0,0,0,.04);
">

    <div style="
        color:#b47b27;
        font-size:18px;
    ">
        {stars}
    </div>

    <div style="
        color:#536269;
        line-height:1.9;
        margin-top:12px;
    ">
        "{text}"
    </div>

    <div style="
        color:#07566a;
        font-weight:900;
        margin-top:15px;
    ">
        {name}
    </div>

</div>
""",
                unsafe_allow_html=True,
            )
