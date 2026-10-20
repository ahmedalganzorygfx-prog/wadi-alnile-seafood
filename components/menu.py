# معالجة ذكية وآمنة للصور المحلية أو روابط الإنترنت
                image_to_show = CATEGORY_IMAGES.get(cat_name, DEFAULT_IMAGE)
                if prod["image"] and prod["image"].strip() != "":
                    if prod["image"].startswith("http"):
                        image_to_show = prod["image"]
                    else:
                        if os.path.exists(prod["image"]):
                            image_to_show = prod["image"]
                
                with cols_row[j]:
                    with st.container():
                        # استخدام دالة st.image الرسمية لضمان ظهور الصور بشكل دائم ومتناسق
                        st.image(image_to_show, use_column_width=True)
                        
                        st.markdown(
                            f"""
                            <div style="
                                background: #0b2538;
                                border: 1px solid rgba(255, 255, 255, 0.08);
                                border-radius: 0 0 16px 16px;
                                padding: 18px;
                                margin-bottom: 15px;
                                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
                                text-align: right;
                                direction: rtl;
                            ">
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                                    <div style="font-size: 19px; font-weight: 900; color: #ffffff;">
                                        {prod['name']}
                                    </div>
                                    <div style="font-size: 11px; background: rgba(13, 148, 136, 0.2); color: #2dd4bf; padding: 2px 8px; border-radius: 10px; font-weight: bold;">
                                        {cat_name}
                                    </div>
                                </div>
                                <div style="font-size: 13px; color: #94a3b8; margin-bottom: 12px; min-height: 38px; line-height: 1.5;">
                                    {prod['description'] or 'وجبة بحرية طازجة ومميزة مُجهزة بأعلى معايير الجودة'}
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 10px;">
                                    <div style="font-size: 17px; font-weight: 900; color: #38bdf8;">
                                        {prod['price']} جنيه
                                    </div>
                                    <div style="font-size: 11px; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 2px 8px; border-radius: 8px; font-weight: bold;">
                                        ⭐ طازج يومياً
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        
                        if st.button(f"🛒 أضف للسلة", key=f"add_{prod['id']}", use_container_width=True):
                            if "cart" not in st.session_state:
                                st.session_state.cart = []
                            
                            found = False
                            for item in st.session_state.cart:
                                if item["id"] == prod["id"]:
                                    item["quantity"] += 1
                                    found = True
                                    break
                            if not found:
                                st.session_state.cart.append(
                                    {
                                        "id": prod["id"],
                                        "name": prod["name"],
                                        "price": prod["price"],
                                        "quantity": 1,
                                    }
                                )
                            st.success(f"تمت إضافة '{prod['name']}' إلى السلة بنجاح!")
                            st.rerun()
