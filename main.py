from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
import re


class AdblockUrlInterceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        url = info.requestUrl().toString()
        if "ads" in url or "advertisements" in url:
            info.block(True)


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("My Web Browser")
        self.setGeometry(100, 100, 800, 600)

        # Create main layout
        main_layout = QVBoxLayout()

        # Create toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Create navigation actions
        self.back_action = QAction(QIcon("back.png"), "Back", self)
        self.back_action.triggered.connect(self.go_back)
        toolbar.addAction(self.back_action)

        self.forward_action = QAction(QIcon("forward.png"), "Forward", self)
        self.forward_action.triggered.connect(self.go_forward)
        toolbar.addAction(self.forward_action)

        self.reload_action = QAction(QIcon("reload.png"), "Reload", self)
        self.reload_action.triggered.connect(self.reload_page)
        toolbar.addAction(self.reload_action)

        self.home_action = QAction(QIcon("home.png"), "Home", self)
        self.home_action.triggered.connect(self.go_home)
        toolbar.addAction(self.home_action)

        toolbar.addSeparator()

        # Create search bar
        self.search_bar = QLineEdit()
        self.search_bar.setStyleSheet("color: black;")
        self.search_bar.returnPressed.connect(self.search)
        toolbar.addWidget(self.search_bar)

        # Create search button with icon
        search_icon = QIcon("search.png")
        self.search_button = QPushButton(self)
        self.search_button.setIcon(search_icon)
        self.search_button.clicked.connect(self.search)
        toolbar.addWidget(self.search_button)

        # Create ad-block button
        adblock_icon = QIcon("adblock.png")
        self.adblock_button = QPushButton(adblock_icon, "", self)
        self.adblock_button.setCheckable(True)
        self.adblock_button.toggled.connect(self.toggle_adblock)
        toolbar.addWidget(self.adblock_button)

        # Create dark theme toggle button
        dark_theme_icon = QIcon("dark_theme.png")
        self.dark_theme_button = QPushButton(dark_theme_icon, "", self)
        self.dark_theme_button.setCheckable(True)
        self.dark_theme_button.toggled.connect(self.toggle_dark_theme)
        toolbar.addWidget(self.dark_theme_button)

        # Add the toolbar to the main layout
        main_layout.addWidget(toolbar)

        # Create web view
        self.webview = QWebEngineView()
        main_layout.addWidget(self.webview)

        # Set central widget with main layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create web page object
        self.webpage = QWebEnginePage()
        self.webview.setPage(self.webpage)

        # Set default theme to light
        self.set_light_theme()

    def search(self):
        search_text = self.search_bar.text().strip()
        if search_text:
            if "." in search_text:
                if not search_text.startswith("http://") and not search_text.startswith("https://"):
                    search_text = "http://" + search_text
                self.webview.load(QUrl(search_text))
            else:
                search_url = f"https://www.google.com/search?q={search_text}"
                self.webview.load(QUrl(search_url))

        self.search_bar.clear()

    def go_back(self):
        self.webview.back()

    def go_forward(self):
        self.webview.forward()

    def reload_page(self):
        self.webview.reload()

    def go_home(self):
        self.webview.load(QUrl("https://www.google.com"))

    def set_light_theme(self):
        self.setStyleSheet("background-color: #FFFFFF;")

    def set_dark_theme(self):
        self.setStyleSheet("background-color: #1F1F1F;")

    def toggle_dark_theme(self, checked):
        self.is_dark_theme = checked
        if checked:
            self.set_dark_theme()
        else:
            self.set_light_theme()
        self.update_text_color()

    def set_light_theme(self):
        self.setStyleSheet("background-color: #FFFFFF;")

    def set_dark_theme(self):
        self.setStyleSheet("background-color: #1F1F1F;")

    def update_text_color(self):
        if self.is_dark_theme:
            text_color = "white"
        else:
            text_color = "black"
        self.search_bar.setStyleSheet(f"color: {text_color};")
        self.search_button.setStyleSheet(f"color: {text_color};")

    def toggle_adblock(self, checked):
        if checked:
            self.enable_adblock()
        else:
            self.disable_adblock()

    def enable_adblock(self):
        adblock_interceptor = AdblockUrlInterceptor()
        self.webpage.profile().setUrlRequestInterceptor(adblock_interceptor)

    def disable_adblock(self):
        self.webpage.profile().setUrlRequestInterceptor(None)

    def validate_url(self, url):
        # Regular expression pattern for URL validation
        regex_pattern = r"^(http|https)://[a-zA-Z0-9-_.]+.[a-zA-Z]{2,}(?:/[\w-_.]*)*$"

        # Compile the regex pattern
        pattern = re.compile(regex_pattern)

        # Check if the URL matches the pattern
        if pattern.match(url):
            return True
        else:
            return False

    def searchs(self):
        search_text = self.search_bar.text().strip()
        if search_text:
            if self.validate_url(search_text):
                self.webview.load(QUrl(search_text))
            else:
                search_url = f"https://www.google.com/search?q={search_text}"
                self.webview.load(QUrl(search_url))

        self.search_bar.clear()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Set application style to match Google Chrome
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(60, 60, 60))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    window = BrowserWindow()
    window.show()

    # Load the Google homepage
    window.go_home()

    sys.exit(app.exec_())