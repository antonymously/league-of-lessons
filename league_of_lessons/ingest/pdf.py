from pdfminer.high_level import extract_text

# text = extract_text("example.pdf")
# print(text)
import tempfile


def load_pdf_document(byts):
    """Load the pdf document using PyMuPDFLoader"""
    # loader = PyMuPDFLoader(file_path=tmp_file_path)
    # text = loader.load()
    text = extract_text(byts)

    return text

def load_files_and_get_chain(files):
    """On streamlit:
    ```st.file_uploader can accept multiple files. The uploaded files can be assigned to st.session_state as a list of bytessIO.

    This function takes a list of those files and returns a list of text. 
    """

    docs = []
    for file in files:
        # with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        #     tmp_file.write(file.getbuffer())
        #     tmp_file_path = tmp_file.name
        
        doc_i = load_pdf_document(file) 
        docs.append(doc_i)

    return docs