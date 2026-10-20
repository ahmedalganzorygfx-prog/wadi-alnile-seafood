import streamlit as st
from database.database import get_connection

CATEGORIES = [
    "الحلويات",
    "المشروبات",
    "الشوربة",
    "السلطات",
    "الأرز",
    "السي فود",
    "الجمبري",
    "الأسماك",
    "الكل",
]

# صور افتراضية عالية الجودة لكل تصنيف لضمان عدم اختفاء أي صورة
CATEGORY_IMAGES = {
    "الأسماك": "https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?auto=format&fit=crop&w=600&q=80",
    "الجمبري": "https://images.unsplash.com/photo-1565680314210-5ab350e965cc?auto=format&fit=crop&w=600&q=80",
    "السي فود": "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80",
    "الأرز": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80",
    "السلطات": "https://images.unsplash.com/photo-1540420773420-3366772f4999?auto=format&fit=crop&w=600&q=80",
    "الشوربة": "https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80",
    "المشروبات": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=600&q=80",
    "الحلويات": "https://images.unsplash.com/photo-1551024601-bec78aea704b?auto=format&fit=crop&w=600&q=80",
}

DEFAULT_IMAGE = "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=600&q=80"

def get_smart_image(product_name, category_name, db_image):
    # إذا كانت هناك صورة مرفوعة حقيقية وصالحة
    if db_image and db_image.strip() != "":
        return db_image
    
    # العودة لصورة التصنيف المضمونة
    return CATEGORY_IMAGES.get(category_name, DEFAULT_IMAGE)
