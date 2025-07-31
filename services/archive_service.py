import os
import shutil
from datetime import datetime

class ArchiveService:
    FLAGS_DIR = "temp_flags"
    PDF_FLAG = os.path.join(FLAGS_DIR, "pdf_sent.flag")
    EXCEL_FLAG = os.path.join(FLAGS_DIR, "excel_sent.flag")

    @staticmethod
    def create_flag(flag_path):
        os.makedirs(ArchiveService.FLAGS_DIR, exist_ok=True)
        try:
            with open(flag_path, "w") as f:
                f.write(str(datetime.now()))
        except OSError as e:
            print(f"[FLAG ERROR] Could not create flag at {flag_path}: {e}")

    @staticmethod
    def flags_exist():
        return os.path.exists(ArchiveService.PDF_FLAG) and os.path.exists(ArchiveService.EXCEL_FLAG)

    @staticmethod
    def clear_flags():
        if os.path.exists(ArchiveService.PDF_FLAG):
            os.remove(ArchiveService.PDF_FLAG)
        if os.path.exists(ArchiveService.EXCEL_FLAG):
            os.remove(ArchiveService.EXCEL_FLAG)

    @staticmethod
    def archive_file(file_path, file_type="pdf"):
        today = datetime.today().strftime("%Y-%m")
        archive_dir = os.path.join("archive", file_type, today)
        try:
            os.makedirs(archive_dir, exist_ok=True)
        except  OSError as e:
            print(f"[ERROR] Failed to create folder: {e}")
        shutil.copy(file_path, os.path.join(archive_dir, os.path.basename(file_path)))

    @staticmethod
    def archive_all_pdfs():
        for file in os.listdir():
            if file.startswith("salary_slip_") and file.endswith(".pdf"):
                ArchiveService.archive_file(file, "pdf")

    @staticmethod
    def attempt_archive_all():
        if ArchiveService.flags_exist():
            ArchiveService.archive_file("filtered_employees.xlsx", "excel")
            ArchiveService.archive_all_pdfs()
            ArchiveService.clear_flags()
            print("[ARCHIVED] All files archived.")
        else:
            print("[WAIT] Not all flags present. Skipping archive.")
