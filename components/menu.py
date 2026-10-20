# معالجة ذكية وآمنة للصور المحلية أو روابط الإنترنت
                image_to_show = CATEGORY_IMAGES.get(cat_name, DEFAULT_IMAGE)
                
                if prod["image"] and prod["image"].strip() != "":
                    if prod["image"].startswith("http"):
                        image_to_show = prod["image"]
                    else:
                        # إذا كانت الصورة مرفوعة محلياً داخل مجلد uploads
                        if os.path.exists(prod["image"]):
                            image_to_show = prod["image"]
                
                with cols_row[j]:
                    with st.container():
                        # حاوية صورة ثابتة ومستقرة تماماً
                        st.markdown(
                            f"""
                            <div style="width: 100%; height: 200px; overflow: hidden; border-radius: 16px 16px 0 0; background-color: #0b2538;">
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        # عرض الصورة بضمان تام عبر أداة Streamlit الرسمية
                        st.image(image_to_show, use_column_width=True)
