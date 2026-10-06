import subprocess, time, urllib.request, sys, platform, urllib.error

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class OSIdentifier:
    def __init__(self) -> None:
        self.os_name = platform.system()
        self.os_version = platform.version()
        self.os_release = platform.release()

    def identify(self):
        return f"{self.os_name} {self.os_release} ({self.os_version})"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.os_identity = OSIdentifier()
        self.setWindowTitle("Knowledge Engine")
        self.resize(1024, 640)

        # Start Streamlit process
        self.streamlit_process = subprocess.Popen(
            ["streamlit", "run", "entry.py", "--server.port", "8501", "--server.headless", "true"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for Streamlit to be ready
        self.wait_for_streamlit("http://localhost:8501")

        # Buat WebEngine View
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("http://localhost:8501"))
        
        # Set sebagai central widget
        self.setCentralWidget(self.browser)

    def wait_for_streamlit(self, url, timeout=15):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                with urllib.request.urlopen(url, timeout=1) as response:
                    if response.getcode() == 200:
                        return True
            except (urllib.error.URLError, urllib.error.HTTPError):
                time.sleep(0.5)
        return False
            
    def closeEvent(self, event):
        # Kill Streamlit process on window close
        self.streamlit_process.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

