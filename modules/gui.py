import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import Qt, QUrl, pyqtSignal
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from config import Config

# Custom Page to capture JS console logs
class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"JS Console: {message} (Line {lineNumber})")

class AvatarWindow(QMainWindow):
    user_input_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(100, 100, 350, 500)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # --- Drag Bar ---
        self.title_bar = QFrame()
        self.title_bar.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-top-left-radius: 10px; border-top-right-radius: 10px;")
        self.title_bar.setFixedHeight(30)
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        title_label = QLabel("AI Assistant")
        title_label.setStyleSheet("color: white; font-weight: bold; font-size: 12px; background: transparent;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("color: white; background: transparent; border: none; font-weight: bold;")
        close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        close_btn.clicked.connect(self.close)
        title_layout.addWidget(close_btn)

        layout.addWidget(self.title_bar)
        # ----------------

        # 3D Avatar View
        self.webview = QWebEngineView()
        self.webview.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.webview.setStyleSheet("background: transparent;")
        
        # Enable Remote Access for file://
        self.page = WebEnginePage(self.webview)
        self.page.setBackgroundColor(Qt.GlobalColor.transparent)
        settings = self.page.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        self.webview.setPage(self.page)
        
        # Allow right-click to pass through to parent (or handle it)
        # Actually, WebEngine has its own context menu. We want to replace it or add to it.
        # Setting NoContextMenu makes it ignore right clicks, passing them to parent?
        self.webview.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        
        # Load local HTML
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "avatar_view.html"))
        print(f"DEBUG: Loading Avatar HTML from: {html_path}")
        self.webview.setUrl(QUrl.fromLocalFile(html_path))
        
        layout.addWidget(self.webview, stretch=3)

        # Subtitle Area
        self.subtitle_area = QTextEdit()
        self.subtitle_area.setStyleSheet("background-color: rgba(0, 0, 0, 150); color: white; border-radius: 5px; padding: 5px; font-size: 10pt; border: none;")
        self.subtitle_area.setReadOnly(True)
        self.subtitle_area.setMaximumHeight(100)
        self.subtitle_area.hide()
        layout.addWidget(self.subtitle_area)

        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a command...")
        self.input_field.setStyleSheet("background-color: rgba(255, 255, 255, 200); color: black; border-radius: 5px; padding: 5px;")
        self.input_field.returnPressed.connect(self.handle_input)
        layout.addWidget(self.input_field)

        # Dragging logic
        self.old_pos = None

    def handle_input(self):
        text = self.input_field.text()
        if text:
            self.user_input_signal.emit(text)
            self.input_field.clear()

    def update_subtitle(self, text):
        if text:
            self.subtitle_area.append(f"Assistant: {text}")
            self.subtitle_area.show()
            sb = self.subtitle_area.verticalScrollBar()
            sb.setValue(sb.maximum())

    def set_state(self, state):
        print(f"DEBUG: set_state called with '{state}'")
        # Call JavaScript functions (Strict API Compliance)
        if "dance" in state or "dancing" in state:
            self.webview.page().runJavaScript("dance()")
        elif "talking" in state or "happy" in state:
            self.webview.page().runJavaScript("wagTail()")
        else:
            self.webview.page().runJavaScript("setIdle()")

    def mousePressEvent(self, event):
        # Only allow dragging from the title bar
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if click is within title bar area (top 30 pixels)
            if event.position().y() <= 30:
                self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

    def contextMenuEvent(self, event):
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        quit_action = menu.addAction("Quit")
        action = menu.exec(event.globalPos())
        if action == quit_action:
            QApplication.quit()
