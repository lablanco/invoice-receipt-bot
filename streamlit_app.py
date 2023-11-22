import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import pdf2image
import fitz

# Function to handle file upload and OCR
def process_invoice(file):
    blocks_info = []
    try:
        if file.type == "application/pdf":
            pdf_image = pdf2image.convert_from_bytes(file.read())
            st.image(pdf_image)

            file.seek(0,0)

            pdf_document = fitz.open(stream=file.read(), filetype="pdf")

            page = pdf_document.load_page(0)  # Load the first page
            blocks_info = page.get_text("blocks")
            texto = page.get_text("text")
            st.write(texto)

        else:
            st.image(file)
    
            # Open the image using Pillow
            img = Image.open(file)
            # OCR using pytesseract
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            text = pytesseract.image_to_string(img)

        # Split the text into lines and filter out empty lines
            lines = [line.strip() for line in text.split('\n') if line.strip()]

            # Create a DataFrame with each line as a row
            data = {"Text": lines}
            df = pd.DataFrame(data)
            
            st.subheader("Extracted Data:")

            # Display data in a table
            st.table(df)

    except Exception as e:
        print(f"Error extracting text and block information: {e}")
    return blocks_info

# Function for the chatbot
def chatbot():
    st.subheader("Chatbot")
    user_input = st.text_input("You: ")
    
    # Simple responses for demonstration purposes
    if user_input:
        st.text("Bot: Thanks for your input! If you have any questions about uploading invoices or receipts, feel free to ask.")

# Main function
def main():
    st.title("Factura IA - Invoice and Receipt ")
    
    # Sidebar with navigation
    menu = ["Upload", "Chatbot"]
    choice = st.sidebar.selectbox("Navigation", menu)

    if choice == "Upload":
        st.subheader("Upload Invoices and Receipts")
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "png", "jpg", "jpeg"])
        if uploaded_file is not None:
            process_invoice(uploaded_file)
    elif choice == "Chatbot":
        chatbot()

if __name__ == "__main__":
    main()
