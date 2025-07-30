
from PyPDF2 import PdfWriter, PdfReader
from models.employee import Employee

class EncryptPdfService:
    @staticmethod
    def encrypt_pdf_with_cnp(file_name,password):
        employee=Employee
        out = PdfWriter()

        file = PdfReader(file_name)

        num = len(file.pages)

        for idx in range(num):
            page = file.pages[idx]

            out.add_page(page)

        out.encrypt(password)

        with open(file_name,"wb") as f:
            out.write(f)
