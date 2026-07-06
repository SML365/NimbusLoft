# --- Import Dependencies --- #
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QFileIconProvider, QScrollArea, QMenu, QStyle
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QFileInfo, QSize, QMimeData, QUrl, Signal
from PySide6.QtGui import QCursor, QFontMetrics, QDrag, QAction, QDesktopServices
from BlurWindow.blurWindow import blur
from pathlib import Path
from dataclasses import dataclass
import sys
import os
import time


# --- Variable Definitions --- #
global wx
global wy
files = []
shelf_state = 1
version = "v1.2.0"
icon_provider = QFileIconProvider()
global firstboot
firstboot = 1

# --- Drag and Drop Dataclasses --- #
@dataclass
class ClipboardItem:
    path: Path | None = None
    url: str | None = None
    name: str | None = None
    is_dir: bool | None = False
    size: int | None = 0
    color_code: str | None = "rgba(55, 55, 55, 0.5)"
    hover_color: str | None = "rgba(75, 75, 75, 0.5)"

# --- File Card --- #
class FileCard(QFrame):
    hovered = Signal(str, int, str)

    def __init__(self, item: ClipboardItem):
        super().__init__()
        self.setMouseTracking(True)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout)
        self.setFixedHeight(45)
        self.setFixedWidth(150)
        self.setStyleSheet(f"""
                            QFrame
                            {{
                                /* Colors */
                                background-color: {item.color_code};

                                /* Borders */
                                border-radius: 6px;
                            }}
                            
                            QFrame:hover
                            {{
                                /* Colors */
                                background-color: {item.hover_color};
                            }}
                            """)

        if item.path is not None:
            icon = icon_provider.icon(QFileInfo(str(item.path)))
        else:
            icon = self.style().standardIcon(QStyle.SP_ComputerIcon)

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(QSize(24, 24)))
        icon_label.setFixedWidth(24)
        icon_label.setFixedHeight(24)
        icon_label.setStyleSheet("""
                                QLabel
                                {
                                    /* Colors */
                                    background-color: rgba(0, 0, 0, 0.0);
                                
                                    /* Borders */
                                    border: none;
                                }
                                """)

        name_label = QLabel(item.name)
        name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        name_label.setStyleSheet("""
                                QLabel
                                {
                                    /* Colors */
                                    background-color: rgba(0, 0, 0, 0.0);
                                 
                                    /* Fonts */
                                    font-size: 14px;
                                    font-weight: 550;
                                 
                                    /* Borders */
                                    border: none;
                                }
                                """)
        font_metrics = QFontMetrics(name_label.font())
        elided_name = font_metrics.elidedText(
            item.name,
            Qt.TextElideMode.ElideRight,
            90
        )

        name_label.setText(elided_name)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)

        self.item = item

    def enterEvent(self, event):
        self.hovered.emit(self.item.name, self.item.size, self.item.url or "")
        event.accept()


    def leaveEvent(self, event):
        self.hovered.emit("", 0, "")
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.position().toPoint()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return

        if (event.position().toPoint() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        
        drag = QDrag(self)
        mime = QMimeData()

        if self.item.url:
            mime.setUrls([QUrl(self.item.url)])
            mime.setText(self.item.url)
        else:
            mime.setUrls([QUrl.fromLocalFile(str(self.item.path))])

        drag.setMimeData(mime)

        icon = icon_provider.icon(QFileInfo(str(self.item.path)))
        drag.setPixmap(icon.pixmap(32, 32))

        drag.exec(Qt.CopyAction | Qt.MoveAction)

        return
    
    # --- Right-Click Menu --- #
    def contextMenuEvent(self, event):
        menu = QMenu()

        open_action = QAction("Open", self)
        open_in_explorer_action = QAction("Open in Explorer", self)
        remove_action = QAction("Remove", self)
        cc_menu_action = QMenu("Color Code", self)

        open_action.triggered.connect(self.open_file)
        open_in_explorer_action.triggered.connect(self.open_in_explorer)
        remove_action.triggered.connect(self.remove_file)

        menu.addAction(open_action)
        menu.addSeparator()
        menu.addAction(open_in_explorer_action)
        menu.addAction(remove_action)
        menu.addMenu(cc_menu_action)

        cc_menu_action.addAction("Default", lambda: self.set_color_code("rgba(55, 55, 55, 0.5)"))
        cc_menu_action.addAction("Blue", lambda: self.set_color_code("rgba(120, 130, 240, 0.5)"))
        cc_menu_action.addAction("Cyan", lambda: self.set_color_code("rgba(0, 200, 200, 0.5)"))
        cc_menu_action.addAction("Green", lambda: self.set_color_code("rgba(0, 200, 0, 0.5)"))
        cc_menu_action.addAction("Orange", lambda: self.set_color_code("rgba(255, 160, 20, 0.5)"))
        cc_menu_action.addAction("Pink", lambda: self.set_color_code("rgba(255, 105, 180, 0.5)"))
        cc_menu_action.addAction("Purple", lambda: self.set_color_code("rgba(130, 137, 218, 0.5)"))
        cc_menu_action.addAction("Red", lambda: self.set_color_code("rgba(255, 50, 50, 0.5)"))
        cc_menu_action.addAction("Yellow", lambda: self.set_color_code("rgba(240, 200, 0, 0.5)"))

        menu.exec(event.globalPos())

    def open_file(self):
        if self.item.url == None:
            os.startfile(str(self.item.path))
        else:
            QDesktopServices.openUrl(QUrl(self.item.url))

    def open_in_explorer(self):
        os.startfile(os.path.dirname(str(self.item.path)))

    def remove_file(self):
        parent_layout = self.parentWidget().layout()
        parent_layout.removeWidget(self)
        self.deleteLater()

    def set_color_code(self, color):
        self.item.color_code = color
        self.item.hover_color = color.replace("0.5", "0.7")
        self.update_style()

    def update_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                /* Colors */
                background-color: {self.item.color_code};

                /* Borders */
                border-radius: 6px;
            }}

            QFrame:hover {{
                /* Colors */
                background-color: {self.item.hover_color};
            }}
        """)

# --- Window Contents --- #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Variables --- #
        self.items = []

        # --- Window Attributes --- #
        self.setWindowFlags(
                            Qt.WindowType.FramelessWindowHint | # Frameless window
                            Qt.WindowStaysOnTopHint | # Always stays on top
                            Qt.Tool # Doesn't show up in alt + tab and taskbar
                            )
        
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAcceptDrops(True)

        # --- Timer Setup --- #
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)

        # --- NimbusLoft Text --- #
        self.title_text = QLabel(f"NimbusLoft {version}")
        self.title_text.setFixedSize(450, 25)
        self.title_text.setStyleSheet("""
                                    QLabel
                                    {
                                        /* Colors */
                                        color: #FFFFFF;
                                        background-color: rgba(30, 30, 30, 0.0);

                                        /* Fonts */  
                                        font-size: 16px;
                                        font-weight: 700;
                                      
                                        /* Borders */
                                        border: none;
                                    }
                                    """)


        # --- Clear Button --- #
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_files) # Does nothing so far
        self.clear_button.setFixedSize(50, 25)
        self.clear_button.setStyleSheet("""
                                        QPushButton
                                        {
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: rgba(30, 30, 30, 0.0);
                                           
                                            /* Fonts */
                                            font-size: 14px;
                                            font-weight: 550;

                                            /* Borders */
                                            border: none;
                                            border-radius: 6px;
                                            padding: 2px;                                       
                                        }
                                        
                                        QPushButton:hover
                                        {
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: rgba(100, 255, 100, 0.5);
                                        }
                                        """)

    
        # --- Close button --- #
        self.close_button = QPushButton("Quit")
        self.close_button.clicked.connect(sys.exit)
        self.close_button.setFixedSize(42, 25)
        self.close_button.setStyleSheet("""
                                        QPushButton 
                                        {                                        
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: rgba(30, 30, 30, 0.0);

                                            /* Fonts */
                                            font-size: 14px;
                                            font-weight: 550;

                                        
                                            /* Borders */
                                            border: none;
                                            border-radius: 6px;
                                            padding: 2px;
                                        }

                                        QPushButton:hover
                                        {
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: rgba(255, 65, 65, 0.6);
                                        }
                                        """)
        
        # --- Layout Definitions --- #
        main_layout = QVBoxLayout()
        self.file_container = QWidget()
        top_bar = QHBoxLayout()

        # --- File Container Layout --- #
        self.file_layout = QHBoxLayout(self.file_container)
        self.file_layout.setSpacing(4)
        self.file_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self.file_layout.setContentsMargins(4, 4, 4, 4)
        self.file_container.setFixedHeight(53)
        self.file_container.setLayout(self.file_layout)
        self.file_container.setStyleSheet("""
                                        QWidget
                                        {
                                            /* Colors */
                                            background: transparent;
                             
                                            /* Borders */
                                            border: none;
                                            border-radius: 6px;
                                        }
                                        """)

        # --- Scroll Area Layout --- #
        scroll = QScrollArea()
        scroll.setWidget(self.file_container)
        scroll.setWidgetResizable(True)
        scroll.setSizeAdjustPolicy(QScrollArea.AdjustIgnored)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)

        # --- Top Bar Layout --- #
        top_bar.addWidget(self.title_text)
        top_bar.addStretch()
        top_bar.addWidget(self.clear_button)
        top_bar.addWidget(self.close_button)
        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar)

        # --- Show the Widgets --- #
        main_layout.addWidget(top_bar_widget)
        
        main_layout.addWidget(scroll)

        # --- Container --- #
        container = QWidget()
        blur(self.winId())
        container.setStyleSheet("""
                                QWidget
                                {
                                    /* Colors */
                                    background-color: rgba(30, 30, 30, 0.5);

                                    /* Fonts */
                                    font-family: Segoe UI;

                                    /* Borders */
                                    border: 1px solid rgba(255, 255, 255, 0.1);
                                    border-radius: 8px;
                                }
                                """)
                                
        
        self.setCentralWidget(container)
        container.setLayout(main_layout)

    # --- Methods --- #
    def update_position(self):
        global shelf_state
        pos = QCursor.pos()

        if pos.y() < 5 and shelf_state == 0:
            if pos.x() > (screen.width() / 2) - (self.width() / 2) and pos.x() < (screen.width() / 2) + (self.width() / 2):
                self.open_shelf()
                shelf_state = 1

        if pos.y() > 140 and shelf_state == 1 and QApplication.activePopupWidget() is None:
            self.close_shelf()
            shelf_state = 0

    def clear_files(self):
        while self.file_layout.count():
            item = self.file_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()
            
        self.items.clear()

        self.title_text.setText(f"NimbusLoft {version}")
        self.centralWidget().update()

    def update_title(self, name, size=None, url=None):
        if name:
            if size is not None:
                if size >= 1024 * 1024 * 1024:
                    size = f"{size / (1024 * 1024 * 1024):.2f} GB"
                elif size >= 1024 * 1024:
                    size = f"{size / (1024 * 1024):.2f} MB"
                elif size >= 1024:
                    size = f"{size / 1024:.2f} KB"
                else:
                    size = f"{size} B"

                if url == None or url == "":
                    self.title_text.setText(f"{name} - {size}")
                else:
                    self.title_text.setText(f"{name} - {url}")
            else:
                self.title_text.setText(f"{name}")
        else:
            self.title_text.setText(f"NimbusLoft {version}")

    def add_clipboard_item(self, item: ClipboardItem):
        self.items.append(item)
        card = FileCard(item)
        card.hovered.connect(self.update_title)
        self.file_layout.addWidget(card)
        self.centralWidget().update()
        
    # --- Show/Hide Window --- #
    def open_shelf(self):
        global wx
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)

        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(QPoint(wx, 10))

        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()
    
    def close_shelf(self):
        global firstboot
        if firstboot == 1:
            time.sleep(1)
            firstboot = 0
        
        global wx
        
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(400)

        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(QPoint(wx, -140))

        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    # --- Drag + Drop Files --- #
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    path = Path(url.toLocalFile())

                    item = ClipboardItem(
                        path = path,
                        name = path.name,
                        url = None,
                        is_dir=path.is_dir(),
                        size=None if path.is_dir() else path.stat().st_size,
                        color_code=None
                    )

                else:
                    item = ClipboardItem(
                        path=None,
                        name=url.host() or url.toString(),
                        url=url.toString(),
                        is_dir=None,
                        size=0,
                        color_code=None
                    )

                self.add_clipboard_item(item)

            event.acceptProposedAction()
    
# --- Main Application --- #
if __name__ == "__main__":
    # --- Application Setup --- #
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen().geometry()

    # --- Window Setup --- #
    width = 680
    height = 120
    wx = (screen.width() - width) // 2
    wy= 10
    window = MainWindow() # Empty window container
    window.resize(width, height) # Resize window
    window.move(wx, wy)
    window.show() # Windows are invisible by default

    # --- Event Loop --- #
    sys.exit(app.exec())