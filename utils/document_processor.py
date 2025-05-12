import pandas as pd
import fitz
import io
from typing import List, Dict, Any, Tuple, Optional

class DocumentProcessor:
    """Handles processing of PDF and Excel files."""

    def __init__(self):
        pass

    def process_pdf(self, file_content: bytes) -> Tuple[str, List[Dict[str, Any]]]:
        """Process PDF file and extract text and metadata."""

        doc = fitz.open(stream=file_content, filetype="pdf")
        full_text = ""
        chunks = []

        for page_num, page in enumerate(doc):
            text = page.get_text()
            full_text += text

            # Create chunk with metadata
            chunks.append({
                "content": text,
                "metadata": {
                    "page": page_num + 1,
                    "source": "pdf",
                    "total_pages": len(doc)
                }
            })

        return full_text, chunks
    
    def process_excel(self, file_content: bytes) -> Tuple[str, List[Dict[str, Any]]]:
        """Process Excel file and extrant text and structured data."""

        excel_file = io.BytesIO(file_content)
        xls = pd.ExcelFile(excel_file)

        full_text = ""
        chunks = []

        for sheet_name in xls.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            sheet_text = f"Sheet: {sheet_name}\n"
            sheet_text += df.to_string(index=False) + "\n\n"
            full_text += sheet_text

            chunks.append({
                "content": sheet_text,
                "metadata": {
                    "sheet": sheet_name,
                    "source": "excel",
                    "columns": df.columns.tolist(),
                    "rows": len(df)
                }
            })

            for col in df.columns:
                col_data = df[col].dropna()
                if not col_data.empty:
                    col_text = f"Column {col}:\n{col_data.to_string()}"
                    chunks.append({
                        "content": col_text,
                        "metadata": {
                            "sheet": sheet_name,
                            "column": col,
                            "source": "excel_column"
                        }
                    })
        
        return full_text, chunks
    
    def process_file(self, file_content: bytes, file_type: str) ->Tuple[str, List[Dict[str, Any]]]:
        """Process file based on its type."""

        if file_type.lower() == "pdf":
            return self.process_pdf(file_content)
        elif file_type.lower() in ["xlsx", "xls"]:
            return self.process_excel(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")