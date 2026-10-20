import streamlit as st


def render_navbar():
    cart_count = sum(
        item["quantity"]
        for item in st.session_state.get("cart", [])
    )

    st.markdown(
        f"""
        <style>
        .navbar {{
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(7, 86, 106, 0.1);
            border-radius: 0 0 25px 25px;
            padding: 12px 25px;
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(7, 86, 106, 0.08);
            position: sticky;
            top: 0;
            z-index: 999;
        }}
        .nav-inner {{
            max-width: 1320px;
            margin: auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
            direction: rtl;
        }}
        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
            font-size: 22px;
            font-weight: 900;
            color: #07566a;
            text-decoration: none;
        }}
        .brand img {{
            width: 45px;
            height: 45px;
            border-radius: 50%;
            object-fit: cover;
            border: 2px solid #ffb703;
        }}
        .hotline-badge {{
            background: linear-gradient(135deg, #07566a, #032027);
            color: white;
            padding: 8px 18px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 4px 15px rgba(7,86,106,0.3);
        }}
        .cart-badge {{
            background: #eef4f6;
            color: #07566a;
            padding: 8px 16px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 14px;
            border: 1px solid rgba(7,86,106,0.15);
        }}
        </style>

        <div class="navbar">
            <div class="nav-inner">
                <a href="#home" class="brand">
                    <img src="https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=150&q=80" alt="logo">
                    أسماك وادي النيل
                </a>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <div class="hotline-badge">
                        ☎️ الخط الساخن: 19974
                    </div>
                    <div class="cart-badge">
                        🛒 السلة ({cart_count})
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
