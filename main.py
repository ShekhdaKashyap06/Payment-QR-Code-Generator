import streamlit as st
import qrcode
from PIL import Image
import io

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="UPI QR Generator",
    page_icon="💳",
    layout="centered"
)

# ----------------------------
# Custom CSS
# ----------------------------
st.markdown("""
<style>

.main{
    background:#f4f6f8;
}

.title{
    text-align:center;
    color:#1E88E5;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    margin-bottom:30px;
}

.stButton>button{
    width:100%;
    background:#1E88E5;
    color:white;
    font-size:18px;
    border-radius:10px;
    height:50px;
}

.stDownloadButton>button{
    width:100%;
    background:#43A047;
    color:white;
    border-radius:10px;
}

.box{
    padding:20px;
    border-radius:12px;
    background:white;
    box-shadow:0px 0px 15px rgba(0,0,0,.1);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Title
# ----------------------------

st.markdown("<div class='title'>💳 UPI QR Generator</div>", unsafe_allow_html=True)

st.markdown(
"<div class='subtitle'>Generate QR Codes for Google Pay, PhonePe & Paytm</div>",
unsafe_allow_html=True)

# ----------------------------
# Form
# ----------------------------

with st.container():


    upi_id = st.text_input(
        "UPI ID",
        placeholder="example@oksbi"
    )

    name = st.text_input(
        "Receiver Name",
        placeholder="John Doe"
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=1.0,
        value=100.0,
        step=1.0
    )

    note = st.text_input(
        "Payment Note (Optional)",
        placeholder="Coffee Payment"
    )

    generate = st.button("Generate QR Code")

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# QR Generation
# ----------------------------

if generate:

    if upi_id == "" or name == "":

        st.error("Please fill all required fields.")

    else:

        upi_url = (
            f"upi://pay?"
            f"pa={upi_id}"
            f"&pn={name}"
            f"&am={amount}"
            f"&cu=INR"
            f"&tn={note}"
        )

        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )

        qr.add_data(upi_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()

        img.save(buffer, format="PNG")

        st.success("QR Code Generated Successfully!")

        st.image(
            buffer,
            caption="Scan using Google Pay / PhonePe / Paytm",
            width=300
        )

        st.download_button(
            "📥 Download QR Code",
            data=buffer.getvalue(),
            file_name="UPI_QR.png",
            mime="image/png"
        )

        with st.expander("Payment Information"):

            st.write("**Receiver:**", name)
            st.write("**UPI ID:**", upi_id)
            st.write("**Amount:** ₹", amount)
            st.write("**Currency:** INR")
            st.write("**Note:**", note if note else "None")