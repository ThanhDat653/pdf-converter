"""Main application window."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QProgressBar,
    QRadioButton,
    QSpinBox,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from models.task import Task


class MainWindow(QMainWindow):
    """Main UI for selecting PDF, options, and launching conversion."""

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config
        self.controller = None
        self.selected_pdf: Path | None = None
        self._build_ui()
        self._apply_theme()

    def bind_controller(self, controller) -> None:
        """Attach controller after dependency construction."""
        self.controller = controller

    def _build_ui(self) -> None:
        self.setWindowTitle("PDF Document Converter Pro")
        self.resize(1100, 760)

        root = QWidget(self)
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        file_layout = QHBoxLayout()
        self.choose_button = QPushButton("Chọn File PDF")
        self.file_label = QLabel("Chưa chọn file")
        self.choose_button.clicked.connect(self._choose_file)
        file_layout.addWidget(self.choose_button)
        file_layout.addWidget(self.file_label)
        layout.addLayout(file_layout)

        mode_group = QGroupBox("Loại xử lý")
        mode_layout = QVBoxLayout(mode_group)
        self.table_mode = QRadioButton("Trích xuất bảng -> Excel")
        self.text_mode = QRadioButton("Trích xuất toàn bộ nội dung -> Word")
        self.text_mode.setChecked(True)
        mode_layout.addWidget(self.table_mode)
        mode_layout.addWidget(self.text_mode)
        layout.addWidget(mode_group)

        self.header_input = QTextEdit()
        self.header_input.setPlaceholderText("Nhập header mỗi dòng, ví dụ:\nSTT\nTên chương\nMã kỹ thuật")
        layout.addWidget(self.header_input)

        options_row = QHBoxLayout()
        self.auto_header = QCheckBox("Tự động nhận diện Header")
        self.auto_header.setChecked(True)
        self.use_ocr = QCheckBox("OCR nếu PDF Scan")
        self.use_ocr.setChecked(True)
        options_row.addWidget(self.auto_header)
        options_row.addWidget(self.use_ocr)
        layout.addLayout(options_row)

        page_row = QHBoxLayout()
        self.page_from = QSpinBox()
        self.page_to = QSpinBox()
        for spinner in (self.page_from, self.page_to):
            spinner.setMinimum(1)
            spinner.setMaximum(99999)
        self.page_from.setValue(1)
        self.page_to.setValue(1)
        page_row.addWidget(QLabel("Từ trang:"))
        page_row.addWidget(self.page_from)
        page_row.addWidget(QLabel("Đến trang:"))
        page_row.addWidget(self.page_to)
        layout.addLayout(page_row)

        self.progress = QProgressBar()
        self.status_label = QLabel("Sẵn sàng")
        layout.addWidget(self.progress)
        layout.addWidget(self.status_label)

        self.preview = QTableView()
        layout.addWidget(self.preview)

        actions = QHBoxLayout()
        self.start_button = QPushButton("Bắt đầu")
        self.cancel_button = QPushButton("Hủy")
        self.open_file_button = QPushButton("Mở File")
        self.open_folder_button = QPushButton("Mở Thư Mục")
        self.start_button.clicked.connect(self._start)
        self.cancel_button.clicked.connect(self._cancel)
        self.open_file_button.clicked.connect(self._open_file)
        self.open_folder_button.clicked.connect(self._open_folder)
        actions.addWidget(self.start_button)
        actions.addWidget(self.cancel_button)
        actions.addWidget(self.open_file_button)
        actions.addWidget(self.open_folder_button)
        layout.addLayout(actions)

    def _apply_theme(self) -> None:
        theme = self.config.get("theme", "dark")
        if theme == "dark":
            css_path = Path(__file__).resolve().parent / "styles" / "dark_theme.qss"
            if css_path.exists():
                self.setStyleSheet(css_path.read_text(encoding="utf-8"))

    def _choose_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn PDF", "", "PDF (*.pdf)")
        if not file_path:
            return
        self.selected_pdf = Path(file_path)
        self.file_label.setText(self.selected_pdf.name)

    def _build_task(self) -> Task | None:
        if self.selected_pdf is None:
            QMessageBox.warning(self, "Thiếu dữ liệu", "Vui lòng chọn file PDF.")
            return None
        headers = [line.strip() for line in self.header_input.toPlainText().splitlines() if line.strip()]
        page_to = self.page_to.value()
        mode = "table" if self.table_mode.isChecked() else "text"
        return Task(
            pdf_path=self.selected_pdf,
            extract_mode=mode,
            page_from=self.page_from.value(),
            page_to=page_to,
            use_ocr_for_scan=self.use_ocr.isChecked(),
            auto_detect_header=self.auto_header.isChecked(),
            headers=headers,
        )

    def _start(self) -> None:
        if self.controller is None:
            return
        task = self._build_task()
        if task is not None:
            self.progress.setValue(0)
            self.status_label.setText("Đang khởi động")
            self.controller.start_task(task)

    def _cancel(self) -> None:
        if self.controller is not None:
            self.controller.cancel_task()

    def _open_file(self) -> None:
        if self.controller is not None:
            self.controller.open_output_file()

    def _open_folder(self) -> None:
        if self.controller is not None:
            self.controller.open_output_folder()

    def update_progress(self, value: int) -> None:
        self.progress.setValue(value)

    def update_status(self, text: str) -> None:
        self.status_label.setText(text)

    def update_preview(self, rows: list[dict]) -> None:
        model = QStandardItemModel(self)
        if not rows:
            self.preview.setModel(model)
            return
        headers = list(rows[0].keys())
        model.setHorizontalHeaderLabels(headers)
        for row in rows[:100]:
            model.appendRow([QStandardItem(str(row.get(key, ""))) for key in headers])
        self.preview.setModel(model)

    def on_completed(self, message: str) -> None:
        self.status_label.setText(message)
        QMessageBox.information(self, "Thành công", message)

    def on_failed(self, message: str) -> None:
        self.status_label.setText("Lỗi")
        QMessageBox.critical(self, "Lỗi", message)
