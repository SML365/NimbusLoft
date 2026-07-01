# --- Import Dependencies --- #
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, QPoint
from PySide6.QtGui import QCursor
import sys


# --- Variable Definitions --- #
shelf_state = 0

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

        # --- Timer Setup --- #
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(50)

        # --- Clear Button --- #
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.close) # Does nothing so far
        self.clear_button.setFixedSize(50, 20)
        self.clear_button.setStyleSheet("""
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
        self.settings_button.setFixedSize(70, 20)
        self.settings_button.setStyleSheet("""
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
        self.close_button.setFixedSize(42, 20)
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
                                            padding: 2px;
                                        }

                                        QPushButton:hover
                                        {
                                            /* Colors */
                                            color: #FFFFFF;
                                            background-color: rgba(255, 65, 65, 0.6);
                                        }
                                        """)
        
        # --- Layout --- #
        main_layout = QVBoxLayout()
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        top_bar.addWidget(self.clear_button)
        top_bar.addWidget(self.settings_button)
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

    def update_position(self):
        global shelf_state
        pos = QCursor.pos()
        print(pos)

        if pos.y() < 5 and shelf_state == 0:
            self.open_shelf()
            shelf_state = 1

        if pos.y() > 140 and shelf_state == 1:
            self.close_shelf()
            shelf_state = 0
        
    # --- Show/Hide Window --- #
    def open_shelf(self):
        global wx
        global wy
        window.move(wx, 10)
    
    def close_shelf(self):
        global wx
        global wy
        window.move(wx, 0 - self.height())
    

if __name__ == "__main__":
    # --- Application Setup --- #
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen().geometry()

    # --- Window Setup --- #
    width = 680
    height = 120
    global wx
    global wy
    wx = (screen.width() - width) // 2
    wy= 10
    window = MainWindow() # Empty window container
    window.resize(width, height) # Resize window
    window.move(wx, wy)
    window.show() # Windows are invisible by default

    # --- Event Loop --- #
    sys.exit(app.exec())