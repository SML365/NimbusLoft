# --- Import Dependencies --- #
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QCursor
import sys

# --- Window Contents --- #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Window Attributes --- #
        self.setWindowFlags(
                            Qt.WindowType.FramelessWindowHint | # Frameless window
                            Qt.WindowStaysOnTopHint | # Always stays on top
                            Qt.Tool # Doesn't show up in alt + tab and taskbar
                            )
        
        self.setAttribute(Qt.WA_TranslucentBackground)

        # --- Settings Button --- #
    
        # --- Close button --- #
        self.close_button = QPushButton("Quit") # Define button
        self.close_button.clicked.connect(self.close) # Button action
        self.close_button.setFixedSize(40, 20)
        self.close_button.setStyleSheet("""
                                        QPushButton 
                                        {                                        
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: rgba(30, 30, 30, 0.0);

                                            /* Fonts */
                                            font-size: 14px;
                                            font-weight: 500;

                                        
                                            /* Borders */
                                            border: none;
                                            border-radius: 6px;
                                        }

                                        QPushButton:hover
                                        {
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: rgba(255, 65, 65, 0.5);
                                        }
                                        """)
        
        # --- Layout --- #
        main_layout = QVBoxLayout()
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.close_button)
        top_bar_widget = QWidget()
        top_bar_widget.setLayout(top_bar)

        main_layout.addWidget(top_bar_widget)
        main_layout.addStretch()

        # --- Container --- #
        container = QWidget()
        container.setStyleSheet("""
                                /* Colors */
                                background-color: rgba(30, 30, 30, 0.5);

                                /* Fonts */
                                font-family: Consolas;

                                /* Borders */
                                border: 1px solid rgba(255, 255, 255, 0.1);
                                border-radius: 8px;
                                """)
                                
        
        self.setCentralWidget(container)
        container.setLayout(main_layout)

    # --- Methods --- #

    # --- Show/Hide Window --- #
    

if __name__ == "__main__":
    # --- Application Setup --- #
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen().geometry()

    # --- Window Setup --- #
    width = 680
    height = 120
    x =  (screen.width() - width) // 2
    y = 10
    window = MainWindow() # Empty window container
    window.resize(width, height) # Resize window
    window.move(x, y)
    window.show() # Windows are invisible by default

    # --- Event Loop --- #
    sys.exit(app.exec())