import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QUrl

from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebEngineCore import QWebEngineDownloadRequest
import requests


class Browser(QMainWindow):
    def __init__(self, page):
        super().__init__()

        self.setWindowTitle("Shift Generator")
        self.setGeometry(100, 100, 1920, 1080)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.web_view = QWebEngineView(self)
        self.web_view.setPage(page)
        layout.addWidget(self.web_view)

class WebEnginePage(QWebEnginePage):
    def __init__(self):
        super().__init__()

        # Connect the downloadRequested signal to the custom slot
        self.profile().downloadRequested.connect(self.downloadRequested)


    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        if navigation_type == QWebEnginePage.NavigationTypeFormSubmitted:
            print(f"Form submitted with URL: {url.toString()}")
        print(f"Navigation type: {navigation_type}")
        return super().acceptNavigationRequest(url, navigation_type, is_main_frame)

    def downloadRequested(self, item: QWebEngineDownloadRequest):
        # Handle the download request
        # download_path = "~/Downloads/"  # Set your desired download path
        print(item)
        item.setDownloadFileName(f"{item.downloadFileName()}.csv")
        item.accept()

def getHtmlContent(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":

    server_url = "http://localhost:8888/"
    html_content= getHtmlContent(server_url)

    app = QApplication(sys.argv)
    webEnginePage = WebEnginePage()
    webEnginePage.setHtml(html_content, QUrl(server_url))

    fake_browser = Browser(webEnginePage)
    fake_browser.show()
    
    sys.exit(app.exec())
