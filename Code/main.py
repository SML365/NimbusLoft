# --- Import Dependencies --- #
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout
from PySide6.QtCore import Qt
import sys

# --- Window Contents --- #
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Window Attributes --- #
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            )
        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        # --- Close button --- #
        self.close_button = QPushButton("X") # Define button
        self.close_button.clicked.connect(self.close) # Button action
        self.close_button.setStyleSheet("""
                                        QPushButton {
                                            /* Dimensions */
                                            width: 20px;
                                            height: 20px;
                                        
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: #000000;

                                            /* Fonts */
                                            font-size: 16px;
                                            font-weight: bold;
                                        
                                            /* Borders */
                                            border: none;
                                            border-radius: 5px;
                                        }
                                        """)
        
        # --- Layout --- #
        layout = QVBoxLayout()
        layout.addWidget(self.close_button)

        # --- Container --- #
        container = QWidget()
        container.setStyleSheet("""
                                background-color: rgba(30, 30, 30, 180);
                                border-radius: 12px;
                                """)
        
        self.setCentralWidget(container)
        container.setLayout(layout)
    

if __name__ == "__main__":
    # --- Application Setup --- #
    app = QApplication(sys.argv)

    # --- Window Setup --- #
    window = MainWindow() # Empty window container
    window.resize(680, 120) # Resize window
    window.show() # Windows are invisible by default

    # --- Event Loop --- #
    sys.exit(app.exec())