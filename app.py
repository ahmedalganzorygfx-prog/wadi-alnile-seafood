import streamlit as st
import urllib.parse

# إعدادات الصفحة
st.set_page_config(
    page_title="مطاعم أسماك وادي النيل",
    page_icon="🐟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم ولغة الواجهة (CSS لتطبيق الهوية والألوان والشكل المطلوب RTL)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        direction: rtl;
        background-color: #f1f5f9;
    }
    
    /* شريط العنوان العلوي */
    .header-box {
        background-color: #0f172a;
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }

    /* بانر الشعار في منتصف الصفحة */
    .hero-banner {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0284c7 100%);
        padding: 30px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.2);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }

    /* بطاقة المنتج */
    .product-card {
        background: white;
        padding: 15px;
        border-radius: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
        text-align: right;
    }
    
    .price-tag {
        color: #0369a1;
        font-weight: 900;
        font-size: 1.1rem;
    }

    /* تنسيق الحقول وعناصر الإدخال لغة عربية */
    .stTextInput label, .stSelectbox label, .stNumberInput label {
        text-align: right !important;
        direction: rtl !important;
    }
    </style>
""", unsafe_allow_html=True)

# قاعدة بيانات المنتجات مع الصور والأسعار والتصنيفات
menu_products = [
    {"id": 1, "name": "شوربة سي فود مخلية", "category": "الشوربات", "price": 275.00, "img": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&auto=format&fit=crop&q=80"},
    {"id": 2, "name": "شوربة الجمبري", "category": "الشوربات", "price": 275.00, "img": "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=400&auto=format&fit=crop&q=80"},
    {"id": 3, "name": "ملوخية بالجمبري", "category": "الشوربات", "price": 128.00, "img": "https://images.unsplash.com/photo-1541529086526-db283c563270?w=400&auto=format&fit=crop&q=80"},
    {"id": 4, "name": "رغيف جمبري مخصوص", "category": "الساندوتشات", "price": 200.00, "img": "https://images.unsplash.com/photo-1550547660-d9450f859349?w=400&auto=format&fit=crop&q=80"},
    {"id": 5, "name": "رغيف سمك فيليه", "category": "الساندوتشات", "price": 104.00, "img": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400&auto=format&fit=crop&q=80"},
    {"id": 6, "name": "رغيف حواوشي وادي النيل", "category": "الساندوتشات", "price": 104.00, "img": "https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400&auto=format&fit=crop&q=80"},
    {"id": 7, "name": "أرز وادي النيل بالجمبري", "category": "الأرز والـمكرونة", "price": 200.00, "img": "https://images.unsplash.com/photo-1633964913295-ceb43826e7c9?w=400&auto=format&fit=crop&q=80"},
    {"id": 8, "name": "مكرونة سي فود بصوص الكريمة", "category": "الأرز والـمكرونة", "price": 176.00, "img": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400&auto=format&fit=crop&q=80"},
    {"id": 9, "name": "مكرونة سي فود بصوص الطماطم", "category": "الأرز والـمكرونة", "price": 200.00, "img": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=400&auto=format&fit=crop&q=80"},
    {"id": 10, "name": "وجبة مقلي (جمبري، فيليه، سبيط)", "category": "الوجبات", "price": 240.00, "img": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=400&auto=format&fit=crop&q=80"},
    {"id": 11, "name": "وجبة جمبري فاهيتا", "category": "الوجبات", "price": 400.00, "img": "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&auto=format&fit=crop&q=80"},
    {"id": 12, "name": "طاجن ميكس سي فود", "category": "الطواجن", "price": 400.00, "img": "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&auto=format&fit=crop&q=80"},
    {"id": 13, "name": "سلطة ميكس مأكولات بحرية", "category": "السلطات والمقبلات", "price": 120.00, "img": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&auto=format&fit=crop&q=80"},
    {"id": 14, "name": "طحينة وادي النيل الخاصة", "category": "السلطات والمقبلات", "price": 45.00, "img": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400&auto=format&fit=crop&q=80"}
]

# تهيئة عربة التسوق
if "cart" not in st.session_state:
    st.session_state.cart = {}

# الهيدر العلوي
st.markdown("""
    <div class="header-box">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.5rem;">🐟</span>
            <span style="font-size: 1.2rem; font-weight: 900; color: #38bdf8;">أسماك وادي النيل</span>
        </div>
        <div style="font-size: 0.9rem; background: #0284c7; padding: 5px 12px; border-radius: 8px; font-weight: bold;">
            الخط الساخن: 01103949998
        </div>
    </div>
""", unsafe_allow_html=True)

# بانر الشعار في منتصف الصفحة
st.markdown("""
    <div class="hero-banner">
        <div style="font-size: 3rem; margin-bottom: 5px;">🐬</div>
        <h2 style="font-size: 2rem; font-weight: 900; color: #38bdf8; margin-bottom: 5px;">سلسلة مطاعم أسماك وادي النيل</h2>
        <p style="font-size: 1rem; color: #e2e8f0; font-weight: 600;">أطزج الأسماك والمأكولات البحرية الطازجة يومياً من البحر لمائدتك</p>
    </div>
""", unsafe_allow_html=True)

# شريط البحث العلوي
search_query = st.text_input("بحث", placeholder="ابحث عن منتج أو وجبة...", label_visibility="collapsed")

# أزرار التصنيفات الأفقية (Tabs)
categories = [
    "الكل", 
    "الشوربات", 
    "الساندوتشات", 
    "الأرز والـمكرونة", 
    "الوجبات", 
    "الطواجن", 
    "السلطات والمقبلات"
]

selected_category = st.radio("التصنيفات", categories, horizontal=True, label_visibility="collapsed")

st.divider()

# تقسيم الشاشة (المنتجات يمين / سلة التسوق يسار)
products_col, cart_col = st.columns([2, 1], gap="large")

with products_col:
    # فلترة المنتجات بناءً على البحث أو التصنيف
    filtered_items = menu_products
    if search_query:
        filtered_items = [p for p in menu_products if search_query.lower() in p["name"].lower()]
    elif selected_category != "الكل":
        filtered_items = [p for p in menu_products if p["category"] == selected_category]

    if not filtered_items:
        st.warning("عذراً، لم نجد منتجات مطابقة لبحثك.")
    else:
        # عرض المنتجات في شبكة من عمودين
        grid_cols = st.columns(2)
        for idx, product in enumerate(filtered_items):
            target_col = grid_cols[idx % 2]
            with target_col:
                with st.container(border=True):
                    st.image(product["img"], use_container_width=True, height=140)
                    st.markdown(f"**{product['name']}**")
                    st.markdown(f"<span class='price-tag'>{product['price']:.2f} ج.م</span>", unsafe_allow_html=True)
                    
                    if st.button("إضافة 🛒", key=f"add_{product['id']}", use_container_width=True):
                        if product["id"] in st.session_state.cart:
                            st.session_state.cart[product["id"]]["qty"] += 1
                        else:
                            st.session_state.cart[product["id"]] = {
                                "name": product["name"],
                                "price": product["price"],
                                "qty": 1
                            }
                        st.toast(f"تمت إضافة '{product['name']}' للسلة!", icon="✅")

with cart_col:
    st.markdown("### 🛒 سلة طلباتك")
    
    if not st.session_state.cart:
        st.info("السلة فارغة حالياً. اختر وجباتك المفضلة!")
    else:
        total_amount = 0
        items_to_remove = []
        
        for item_id, details in st.session_state.cart.items():
            subtotal = details["price"] * details["qty"]
            total_amount += subtotal
            
            c1, c2, c3 = st.columns([3, 2, 2])
            with c1:
                st.write(f"**{details['name']}**")
            with c2:
                new_qty = st.number_input(
                    "الكمية", 
                    min_value=0, 
                    value=details["qty"], 
                    key=f"qty_{item_id}", 
                    label_visibility="collapsed"
                )
                if new_qty == 0:
                    items_to_remove.append(item_id)
                else:
                    st.session_state.cart[item_id]["qty"] = new_qty
            with c3:
                st.write(f"`{subtotal:.2f} ج`")
        
        for item_id in items_to_remove:
            del st.session_state.cart[item_id]
            st.rerun()
            
        st.divider()
        st.markdown(f"#### الإجمالي الكلي: `{total_amount:.2f} ج.م`")
        
        st.markdown("#### بيانات التوصيل:")
        cust_name = st.text_input("اسمك الكريم:")
        cust_phone = st.text_input("رقم الهاتف:")
        cust_address = st.text_input("عنوان التوصيل بالتفصيل:")
        
        if st.button("تأكيد الطلب عبر واتساب 📲", type="primary", use_container_width=True):
            if not cust_name or not cust_phone or not cust_address:
                st.error("الرجاء إدخال الاسم، رقم الهاتف، وعنوان التوصيل.")
            else:
                msg = f"🛒 *طلب جديد من موقع مطاعم أسماك وادي النيل*\n\n"
                msg += f"👤 الاسم: {cust_name}\n"
                msg += f"📞 الهاتف: {cust_phone}\n"
                msg += f"📍 العنوان: {cust_address}\n\n"
                msg += "📋 *المنتجات:*\n"
                for item_id, details in st.session_state.cart.items():
                    msg += f"- {details['name']} ({details['qty']}x) - {details['price'] * details['qty']} ج.م\n"
                msg += f"\n💰 *الإجمالي الكلي:* {total_amount:.2f} ج.م"
                
                whatsapp_url = f"https://wa.me/201103949998?text={urllib.parse.quote(msg)}"
                st.success("تم تجهيز الطلب! اضغط أدناه للإرسال الفوري عبر واتساب:")
                st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="background-color:#16a34a; color:white; padding:10px; border-radius:10px; width:100%; border:none; font-weight:bold; cursor:pointer;">إرسال الطلب للواتساب 🚀</button></a>', unsafe_allow_html=True)

# الفوتر أسفل الصفحة
st.divider()
st.markdown("### 📍 فروعنا الرئيسية والخط الساخن")
f1, f2, f3 = st.columns(3)
with f1:
    st.markdown("**فرع المهندسين**")
    st.write("82 شارع وادي النيل، الجيزة.")
with f2:
    st.markdown("**فرع التجمع الخامس**")
    st.write("الحي الثالث، بجوار مول عنابة.")
with f3:
    st.markdown("**فرع 6 أكتوبر**")
    st.write("محور 26 يوليو، بجوار شيل أوت.")
