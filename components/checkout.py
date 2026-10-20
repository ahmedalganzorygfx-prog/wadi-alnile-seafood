import streamlit as st
from database.database import get_connection


def render_checkout():
    cart = st.session_state.get("cart", [])
    if not cart:
        return

    st.markdown(
        """
        <div style="text-align:center; margin:50px 0 20px; direction:rtl;">
            <h2 style="color:#07566a; font-weight:900;">📋 إتمام الطلب</h2>
            <p style="color:#68777d;">أدخل بياناتك لتأكيد طلبك من أسماك وادي النيل</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("checkout_form"):
        col1, col2 = st.columns(2)

        with col1:
            customer_name = st.text_input("👤 الاسم الكامل *")
            customer_phone = st.text_input("📞 رقم الهاتف *")

        with col2:
            order_type = st.selectbox("📦 نوع الاستلام", ["توصيل منزلي", "استلام من الفرع"])

            conn = get_connection()
            branches_cursor = conn.execute("SELECT name FROM branches").fetchall()
            branch_list = [b["name"] for b in branches_cursor] if branches_cursor else ["فرع الدقي", "فرع الهرم"]

            if order_type == "استلام من الفرع":
                branch_name = st.selectbox("📍 اختر الفرع للاستلام", branch_list)
                address = "-"
            else:
                branch_name = "-"
                address = st.text_area("🏠 عنوان التوصيل بالتفصيل (المدينة، الشارع، رقم العمارة، الشقة)")

        notes = st.text_area("📝 ملاحظات إضافية (اختياري)", placeholder="مثال: بدون بقدونس، زيادة تتبيلة...")

        total_amount = sum(item["price"] * item["quantity"] for item in cart)

        st.markdown(
            f"""
            <div style="background:#f0f4f5; padding:15px; border-radius:12px; text-align:center; margin:20px 0; font-size:18px; font-weight:bold; color:#07566a; direction:rtl;">
                المبلغ الإجمالي المطلوب: {total_amount} جنيه
            </div>
            """,
            unsafe_allow_html=True,
        )

        submitted = st.form_submit_button("🚀 تأكيد وإرسال الطلب", use_container_width=True)

        if submitted:
            if not customer_name.strip() or not customer_phone.strip():
                st.error("⚠️ برجاء إدخال الاسم ورقم الهاتف على الأقل للمتابعة.")
            elif order_type == "توصيل منزلي" and not address.strip():
                st.error("⚠️ برجاء إدخال عنوان التوصيل بالتفصيل.")
            else:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        INSERT INTO orders (customer_name, customer_phone, order_type, branch_name, address, notes, total_amount, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 'قيد المراجعة')
                        """,
                        (customer_name, customer_phone, order_type, branch_name, address, notes, total_amount)
                    )

                    order_id = cursor.lastrowid

                    for item in cart:
                        cursor.execute(
                            """
                            INSERT INTO order_items (order_id, product_name, price, quantity)
                            VALUES (?, ?, ?, ?)
                            """,
                            (order_id, item["name"], item["price"], item["quantity"])
                        )

                    conn.commit()

                    st.session_state.cart = []
                    st.success(f"🎉 تم استلام طلبك بنجاح! رقم الطلب الخاص بك هو: #{order_id}")
                    st.info("☎️ سيتم التواصل معك قريباً من خلال الخط الساخن 19974 لتأكيد الطلب.")
                    st.balloons()

                except Exception as e:
                    st.error(f"حدث خطأ أثناء حفظ الطلب: {e}")
