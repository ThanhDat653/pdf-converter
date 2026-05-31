# PDF Document Converter Pro

Ứng dụng desktop Windows bằng Python (PySide6) để xử lý PDF và xuất Word/Excel/JSON.

## Cấu trúc
Mã nguồn nằm trong thư mục `/project` theo Clean Architecture:
- `ui/`: giao diện
- `core/`: điều phối, cấu hình, logging
- `models/`: dataclass chuẩn
- `readers/`, `extractors/`, `plugins/`: pipeline xử lý PDF/OCR/table
- `engines/`: extraction/export orchestration
- `exporters/`: xuất Word/Excel/JSON
- `workers/`: QThread worker
- `tests/`: unit tests cơ bản

## Chạy local
```bash
cd project
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r ../requirements.txt
python main.py
```

## Build EXE
```bat
build_exe.bat
```

## Tính năng chính
- Chọn file PDF
- Tự nhận diện PDF text/scan
- Trích xuất bảng -> Excel
- Trích xuất nội dung -> Word
- OCR cho scan PDF (PaddleOCR)
- Fuzzy header matching với `rapidfuzz` (ngưỡng mặc định 80%)
- Cập nhật progress realtime với `QThread`
- Preview dữ liệu trên `QTableView`
- Xuất kèm JSON metadata

## Kiểm thử
```bash
cd project
python -m unittest discover -s tests -v
```

## Sample PDF test workflow
Tham khảo: `project/samples/sample_pdf_test_workflow.md`
