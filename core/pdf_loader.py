"""
PDF text extraction functionality
"""
from pypdf import PdfReader
from pypdf.errors import PdfStreamError

def extract_text_from_pdfs(pdf_files):
    """
    Extract text from a list of PDF files
    
    Args:
        pdf_files: List of file-like objects (from Streamlit file_uploader)
    
    Returns:
        tuple: (extracted_text, skipped_files)
    """
    text = ""
    skipped_files = []
    
    for pdf in pdf_files:
        try:
            # Reset stream pointer (Streamlit quirk)
            pdf.seek(0)
            
            pdf_reader = PdfReader(pdf)
            
            for page in pdf_reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
        
        except PdfStreamError:
            skipped_files.append(pdf.name)
        
        except Exception as e:
            skipped_files.append(pdf.name)
    
    return text, skipped_files

def validate_extracted_text(text, skipped_files):
    """
    Validate extracted text and return status
    
    Args:
        text (str): Extracted text
        skipped_files (list): List of files that couldn't be processed
    
    Returns:
        dict: Status information with 'success', 'warning', 'error' keys
    """
    result = {
        "success": False,
        "warning": None,
        "error": None
    }
    
    if skipped_files:
        result["warning"] = (
            f"Skipped {len(skipped_files)} file(s) due to read errors: "
            + ", ".join(skipped_files)
        )
    
    if not text.strip():
        result["error"] = "No readable text found in the uploaded PDFs."
        return result
    
    result["success"] = True
    return result