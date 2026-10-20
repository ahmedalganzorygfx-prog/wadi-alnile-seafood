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
            background: rgba(255,255,255,.95);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(0,0,0,.06);
            border-radius: 0 0 25px 25px;
            padding: 14px 22px;
            margin-bottom: 25px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.05);
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
            gap: 12px;
            font-size: 21px;
            font-weight: 900;
            color: #07566a;
            text-decoration: none;
        }}
        .hotline-badge {{
            background: #07566a;
            color: white;
            padding: 8px 18px;
            border-radius: 50px;
            font-weight: bold;
            font-size: 14px;
            box-shadow: 0 4px 15px rgba(7,86,106,0.3);
        }}
        </style>

        <div class="navbar">
            <div class="nav-inner">
                <a href="#home" class="brand">
                    🐟 أسماك وادي النيل
                </a>
                <div style="display: flex; gap: 15px; align-items: center;">
                    <div class="hotline-badge">
                        ☎️ الخط الساخن: 19974
                    </div>
                    <div style="background:#eef4f6; color:#07566a; padding:8px 15px; border-radius:50px; font-weight:bold; font-size:14px;">
                        🛒 السلة ({cart_count})
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
