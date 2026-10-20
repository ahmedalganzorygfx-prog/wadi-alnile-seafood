import streamlit as st

from database.database import get_connection


CATEGORIES = [
    "الكل",
    "الأسماك",
    "الجمبري",
    "السي فود",
    "الأرز",
    "السلطات",
    "الشوربة",
    "المشروبات",
    "الحلويات",
]


def load_products():

    connection = get_connection()

    products = connection.execute(
        """
        SELECT
            products.id,
            products.name,
            products.description,
            products.price,
            products.image,
            products.available,
            categories.name AS category

        FROM products

        LEFT JOIN categories
            ON products.category_id = categories.id

        WHERE products.available = 1

        ORDER BY products.id DESC
        """
    ).fetchall()

    connection.close()

    return products


def add_to_cart(product):

    if "cart" not in st.session_state:

        st.session_state.cart = []


    product_id = product[0]


    for item in st.session_state.cart:

        if item["id"] == product_id:

            item["quantity"] += 1

            st.toast(
                f"تم زيادة كمية {product[1]} 🛒"
            )

            return


    st.session_state.cart.append(
        {
            "id": product[0],
            "name": product[1],
            "description": product[2],
            "price": float(product[3]),
            "image": product[4],
            "quantity": 1,
        }
    )


    st.toast(
        f"تمت إضافة {product[1]} إلى السلة 🛒"
    )


def render_menu():

    st.markdown(
        """
<div id="menu"></div>

<div style="
    text-align:center;
    margin:55px 0 30px;
">

    <div style="
        color:#07566a;
        font-size:40px;
        font-weight:900;
    ">
        🍽️ المنيو
    </div>

    <div style="
        color:#718087;
        font-size:16px;
        margin-top:8px;
    ">
        اكتشف تشكيلتنا المميزة من المأكولات البحرية
    </div>

</div>
""",
        unsafe_allow_html=True,
    )


    products = load_products()


    if not products:

        st.info(
            "لا توجد منتجات في المنيو حاليًا."
        )

        return


    search = st.text_input(
        "🔎 ابحث عن وجبتك",
        placeholder="مثال: جمبري، دنيس، أرز..."
    )


    selected_category = st.radio(
        "التصنيف",
        CATEGORIES,
        horizontal=True,
    )


    filtered_products = products


    if selected_category != "الكل":

        filtered_products = [

            product

            for product in filtered_products

            if product[6] == selected_category
        ]


    if search.strip():

        search_text = search.strip().lower()


        filtered_products = [

            product

            for product in filtered_products

            if
            search_text in product[1].lower()

            or

            search_text in
            (product[2] or "").lower()
        ]


    if not filtered_products:

        st.warning(
            "لم نجد منتجات مطابقة لبحثك."
        )

        return


    columns = st.columns(4)


    for index, product in enumerate(
        filtered_products
    ):

        with columns[index % 4]:

            if product[4]:

                st.image(
                    product[4],
                    use_container_width=True
                )

            else:

                st.markdown(
                    """
<div style="
    height:180px;

    background:
        linear-gradient(
            135deg,
            #edf7f8,
            #d9eef1
        );

    border-radius:20px;

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:65px;
">
    🐟
</div>
""",
                    unsafe_allow_html=True,
                )


            st.markdown(
                f"""
<div style="
    padding:10px 5px 12px;
    text-align:right;
">

    <div style="
        color:#07566a;
        font-size:18px;
        font-weight:900;
    ">
        {product[1]}
    </div>

    <div style="
        color:#718087;
        font-size:13px;
        min-height:42px;
        margin-top:5px;
    ">
        {product[2] or ""}
    </div>

    <div style="
        color:#b47b27;
        font-size:19px;
        font-weight:900;
        margin-top:10px;
    ">
        {product[3]:,.0f} جنيه
    </div>

</div>
""",
                unsafe_allow_html=True,
            )


            if st.button(
                "🛒 أضف للسلة",
                key=f"add_product_{product[0]}",
                use_container_width=True,
            ):

                add_to_cart(product)
