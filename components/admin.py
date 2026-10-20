import streamlit as st
import os
from database.database import get_connection

def render_admin():
    st.markdown('<div id="admin"></div>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="text-align:right; margin:30px 0 20px 0; direction:rtl;">
            <h2 style="color:#ffffff; font-size:28px; font-weight:900;">⚙️ لوحة التحكم الإدارية</h2>
            <p style="color:#94a3b8; font-size:14px;">إضافة وتعديل الوجبات ورفع الصور الحقيقية مباشرة</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2 = st.tabs(["➕ إضافة وجبة جديدة", "📦 إدارة الوجبات الحالية"])

    with tab1:
        st.markdown("<h4 style='color: #38bdf8; text-align: right;'>إضافة طبق جديد للمنيو</h4>", unsafe_allow_html=True)
        
        with st.form("add_product_form"):
            name = st.text_input("اسم الوجبة")
            price = st.number_input("السعر (بالجنيه)", min_value=0.0, step=5.0)
            
            conn = get_connection()
            categories = conn.execute("SELECT id, name FROM categories").fetchall()
            cat_dict = {c["name"]: c["id"] for c in categories}
            category_name = st.selectbox("التصنيف", list(cat_dict.keys()) if cat_dict else ["الأسماك"])
            
            description = st.text_area("وصف الوجبة والمكونات")
            
            uploaded_file = st.file_uploader("📷 رفع صورة الوجبة الحقيقية (PNG, JPG)", type=["png", "jpg", "jpeg"])
            
            submitted = st.form_submit_button("حفظ وإضافة الوجبة", use_container_width=True)
            
            if submitted:
                if not name:
                    st.error("الرجاء إدخال اسم الوجبة على الأقل.")
                else:
                    image_path = ""
                    if uploaded_file is not None:
                        os.makedirs("uploads", exist_ok=True)
                        image_path = f"uploads/{uploaded_file.name}"
                        with open(image_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                    
                    cat_id = cat_dict.get(category_name, 1)
                    
                    try:
                        conn.execute(
                            """
                            INSERT INTO products (name, description, price, category_id, image, available)
                            VALUES (?, ?, ?, ?, ?, 1)
                            """,
                            (name, description, price, cat_id, image_path)
                        )
                        conn.commit()
                        st.success(f"تمت إضافة الوجبة '{name}' بنجاح!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ: {e}")
                    finally:
                        conn.close()

    with tab2:
        st.markdown("<h4 style='color: #38bdf8; text-align: right;'>عرض وحذف الوجبات</h4>", unsafe_allow_html=True)
        conn = get_connection()
        products = conn.execute("SELECT id, name, price FROM products").fetchall()
        conn.close()
        
        for p in products:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{p['name']}** - {p['price']} جنيه")
            with col2:
                if st.button("حذف", key=f"del_prod_{p['id']}"):
                    c = get_connection()
                    c.execute("DELETE FROM products WHERE id = ?", (p['id'],))
                    c.commit()
                    c.close()
                    st.success("تم حذف الوجبة بنجاح")
                    st.rerun()
