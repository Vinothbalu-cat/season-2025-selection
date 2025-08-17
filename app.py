import streamlit as st
import pandas as pd
from io import BytesIO

# -----------------------------
# 1. Page Config
# -----------------------------
st.set_page_config(page_title="Vino Balu Software Factory", layout="wide")

# -----------------------------
# 2. Custom CSS for Watermark
# -----------------------------
st.markdown(
    """
    <style>
    .watermark {
        position: fixed;
        bottom: 10px;
        right: 10px;
        opacity: 0.3;
        font-size: 14px;
        color: #888;
        z-index: 1000;
    }
    </style>
    <div class="watermark">© Vino Balu Software Factory</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# 3. Sidebar Navigation
# -----------------------------
menu = st.sidebar.radio("Navigation", ["🏠 Home", "ℹ️ About", "📧 Contact"])

# -----------------------------
# 4. Home Page
# -----------------------------
if menu == "🏠 Home":
    st.title("🛍️ Season 2025 Product Selection")
    st.markdown(
        """
    **Factory:** Vino Balu Software Factory  
    **Owner:** Vinoth Kumar  
    ---
    Upload your product list, review items, and select what you need for the upcoming season.
    """
    )

    # Generate Template
    def create_template():
        sample_data = {
            "Image": [
                "https://via.placeholder.com/150?text=Shirt+1",
                "https://via.placeholder.com/150?text=Shirt+2",
                "https://via.placeholder.com/150?text=Tshirt+1",
                "https://via.placeholder.com/150?text=Tshirt+2",
                "https://via.placeholder.com/150?text=Jacket+1",
            ],
            "Product ID": [
                "SFD-UBER-001",
                "SFD-UBER-002",
                "SFD-UBER-003",
                "SFD-UBER-004",
                "SFD-UBER-005",
            ],
            "Product Type": ["Shirt", "Shirt", "T-shirt", "T-shirt", "Jacket"],
            "Units": [100, 120, 80, 90, 60],
        }
        df_template = pd.DataFrame(sample_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_template.to_excel(writer, index=False, sheet_name="Template")
        return output.getvalue()

    st.subheader("📥 Step 1: Download Excel Template")
    template_file = create_template()
    st.download_button(
        label="Download Template Excel",
        data=template_file,
        file_name="Product_Selection_Template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Upload Section
    st.subheader("📤 Step 2: Upload Your Product File")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)

        required_cols = ["Image", "Product ID", "Product Type", "Units"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"Uploaded file must contain columns: {required_cols}")
        else:
            if "Selected" not in df.columns:
                df["Selected"] = "NO"
            if "Comments" not in df.columns:
                df["Comments"] = ""

            st.success(
                "✅ File uploaded successfully! Review and select products below:"
            )

            product_types = df["Product Type"].dropna().unique().tolist()
            tabs = st.tabs(product_types)

            for idx, ptype in enumerate(product_types):
                with tabs[idx]:
                    st.markdown(f"### {ptype}")
                    ptype_df = df[df["Product Type"] == ptype]
                    for i in ptype_df.index:
                        col1, col2, col3 = st.columns([1, 2, 2])
                        with col1:
                            if pd.notna(df.at[i, "Image"]):
                                st.image(df.at[i, "Image"], width=100)
                        with col2:
                            st.write(f"**{df.at[i, 'Product ID']}**")
                            st.write(f"Units: {df.at[i, 'Units']}")
                        with col3:
                            selected = st.checkbox(
                                "Select",
                                value=(df.at[i, "Selected"] == "YES"),
                                key=f"chk_{i}",
                            )
                            comment = st.text_input(
                                "Comment", value=df.at[i, "Comments"], key=f"cmt_{i}"
                            )
                            df.at[i, "Selected"] = "YES" if selected else "NO"
                            df.at[i, "Comments"] = comment

            st.markdown("---")
            st.subheader("✅ Step 3: Download Updated File")
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Selection")
            st.download_button(
                label="Download Updated Excel",
                data=output.getvalue(),
                file_name="Updated_Product_Selection.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

# -----------------------------
# 5. About Page
# -----------------------------
elif menu == "ℹ️ About":
    st.title("About Vino Balu Software Factory")
    st.markdown(
        """
    **Vino Balu Software Factory** is a next-generation technology firm focused on building 
    innovative and user-friendly solutions. Our mission is to simplify complex business workflows 
    through smart, scalable, and secure applications.

    **Owner:** Vinoth Kumar  
    **Core Values:**  
    - ✔ Innovation  
    - ✔ Quality  
    - ✔ Customer Satisfaction  

    We believe in delivering **digital excellence**.
    """
    )

# -----------------------------
# 6. Contact Page
# -----------------------------
elif menu == "📧 Contact":
    st.title("Contact Us")
    st.markdown(
        """
    **Email:** [postboxvino@gmail.com](mailto:postboxvino@gmail.com)  (+ 91 - 6382197567)
    **Location:** Bangalore, India  
    **Working Hours:** Mon–Fri (9 AM – 6 PM IST)
    """
    )
    st.info(
        "For any assistance, reach out to us via email. We’ll respond within 24 hours."
    )
