import streamlit as st
from database.database import get_connection

def render_checkout():
    st.markdown('<div id="checkout"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align:right; margin:40px 0 20px 0; direction:rtl;">
            <h3 style="color:#07566a; font-size:28px; font-weight:900;">📋 إتمام الطلب</h3>
            <p style="color:#68777d; font-size:14px;">أدخل بيانات التوصيل لتأكيد طلبك من أسماك وادي النيل</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cart = st.session_state.get("cart", [])
    if not cart:
        return

    st.markdown(
        """
        <style>
        .stTextInput, .stSelectbox, .stTextArea {
            direction: rtl !important;
            text-align: right !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.form("checkout_form"):
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("👤 الاسم الكامل")
            phone = st.text_input("📞 رقم الهاتف")
        with col2:
            branch = st.selectbox("📍 فرع الاستلام / التوصيل", ["فرع الجيزة الرئيسي", "فرع التجمع الخامس", "فرع زايد"])
            order_type = st.selectbox("🛵 نوع الطلب", ["توصيل للمنزل", "استلام من الفرع"])

        address = st.text_area("🏠 عنوان التوصيل بالتفصيل (الشارع، رقم العمارة، الطابق)")
        
        submitted = st.form_submit_button("🚀 تأكيد وإرسال الطلب", use_container_width=True)

        if submitted:
            if not customer_name or not phone or (order_type == "توصيل للمنزل" and not address):
                st.error("⚠️ من فضلك أكمل جميع البيانات المطلوبة (الاسم، الهاتف، والعنوان).")
            else:
                total_amount = sum(item["price"] * item["quantity"] for item in cart)
                
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    
                    cursor.execute(
                        """
                        INSERT INTO orders (customer_name, phone, address, total_amount, status, created_at)
                        VALUES (?, ?, ?, ?, 'قيد المراجعة', datetime('now'))
                        """,
                        (customer_name, phone, address if order_type == "توصيل للمنزل" else "استلام من الفرع", total_amount)
                    )
                    order_id = cursor.lastrowid

                    for item in cart:
                        cursor.execute(
                            """
                            INSERT INTO order_items (order_id, product_id, quantity, price)
                            VALUES (?, ?, ?, ?)
                            """,
                            (order_id, item["id"], item["quantity"], item["price"])
                        )
                    
                    conn.commit()
                    conn.close()

                    st.session_state.cart = []
                    st.success(f"🎉 تم تسجيل طلبك بنجاح رقم #{order_id}! سنتواصل معك قريباً لتأكيد الطلب. الخط الساخن: 19974")
                    st.balloons()
                except Exception as e:
                    st.error(f"حدث خطأ أثناء إتمام الطلب: {e}")
