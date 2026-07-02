# --- Import Dependencies --- #
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QFileIconProvider, QScrollArea
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QFileInfo, QSize, QMimeData, QUrl
from PySide6.QtGui import QCursor, QFontMetrics, QDrag
from BlurWindow.blurWindow import blur
from pathlib import Path
from dataclasses import dataclass
import sys


# --- Variable Definitions --- #
global wx
global wy
files = []
shelf_state = 1
version = "v0.0.0"
icon_provider = QFileIconProvider()


# --- Drag and Drop Dataclasses --- #
@dataclass
class ClipboardItem:
    path: Path
    name: str
    is_dir: bool
    size: int | None

# --- File Card --- #
class FileCard(QFrame):
    def __init__(self, item: ClipboardItem):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.setLayout(layout)
        self.setFixedHeight(45)
        self.setFixedWidth(150)
        self.setStyleSheet("""
                            QFrame
                            {
                                /* Colors */
                                background-color: rgba(55, 55, 55, 0.5);

                                /* Borders */
                                border-radius: 6px;
                            }
                            
                            QFrame:hover
                            {
                                /* Colors */
                                background-color: rgba(75, 75, 75, 0.5);
                            }
                            """)

        icon = icon_provider.icon(QFileInfo(str(item.path)))
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

        url = QUrl.fromLocalFile(str(self.item.path))
        mime.setUrls([url])

        drag.setMimeData(mime)

        icon = icon_provider.icon(QFileInfo(str(self.item.path)))
        drag.setPixmap(icon.pixmap(32, 32))

        drag.exec(Qt.CopyAction | Qt.MoveAction)

        super().mouseMoveEvent(event)

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
        self.title_text.setFixedSize(150, 25)
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
        self.clear_button.clicked.connect(self.close) # Does nothing so far
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


        # --- Settings Button --- #
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.close) # Does nothing so far
        self.settings_button.setFixedSize(70, 25)
        self.settings_button.setStyleSheet("""
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
                                                background-color: rgba(120, 130, 255, 0.7);
                                            }
                                            """)
    
        # --- Close button --- #
        self.close_button = QPushButton("Quit")
        self.close_button.clicked.connect(self.close)
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
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("""
                            QScrollBar
                            {
                                /* Colors */
                                background: none;
                             
                                /* Borders */
                                border: none;
                            }
                            """)

        # --- Top Bar Layout --- #
        top_bar.addWidget(self.title_text)
        top_bar.addStretch()
        top_bar.addWidget(self.clear_button)
        top_bar.addWidget(self.settings_button)
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

        if pos.y() > 140 and shelf_state == 1:
            self.close_shelf()
            shelf_state = 0

    def add_clipboard_item(self, item: ClipboardItem):
        self.items.append(item)
        card = FileCard(item)
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
                if not url.isLocalFile():
                    continue
            
                path = Path(url.toLocalFile())

                item = ClipboardItem(
                    path = path,
                    name = path.name,
                    is_dir=path.is_dir(),
                    size=None if path.is_dir() else path.stat().st_size
                )

                self.add_clipboard_item(item)

            event.acceptProposedAction()
        
    

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