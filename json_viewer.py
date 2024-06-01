import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QTextBrowser
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class JsonSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
       
    def initUI(self):
        self.setWindowTitle('JSON File Selector')
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #333; color: #fff;")

        self.folder_button = QPushButton('Select Folder')
        self.folder_button.setStyleSheet("background-color: #555; color: #fff;")
        self.folder_button.clicked.connect(self.selectFolder)
        self.layout.addWidget(self.folder_button)

        self.json_dropdown = QComboBox()
        self.json_dropdown.setStyleSheet("background-color: #555; color: #fff;")
        self.layout.addWidget(self.json_dropdown)

        self.number_dropdown = QComboBox()
        self.number_dropdown.setStyleSheet("background-color: #555; color: #fff;")
        self.layout.addWidget(self.number_dropdown)

        self.text_browser = QTextBrowser()
        self.text_browser.setStyleSheet("background-color: #555; color: #fff;")
        self.layout.addWidget(self.text_browser)

    def selectFolder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            self.populateJsonFiles(folder_path)

    def populateJsonFiles(self, folder_path):
        json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
        self.json_dropdown.clear()
        self.json_dropdown.addItems(json_files)
        self.json_dropdown.currentIndexChanged.connect(lambda: self.loadJson(folder_path))

    def loadJson(self, folder_path):
        selected_json_file = self.json_dropdown.currentText()
        selected_json_path = os.path.join(folder_path, selected_json_file)
        if os.path.exists(selected_json_path):
            with open(selected_json_path, 'r') as file:
                data = json.load(file)
                self.number_dropdown.clear()
                self.text_browser.clear()
                prompt_reply_dict = {}
                for item in data:
                    number = item.get('number')
                    prompt = item.get('prompt')
                    response = item.get('response')
                    if number is not None and prompt is not None and response is not None:
                        prompt_reply_dict[number] = (prompt, response)
                        self.number_dropdown.addItem(str(number))
                self.number_dropdown.currentIndexChanged.connect(lambda: self.displayPromptReply(prompt_reply_dict))

    def displayPromptReply(self, prompt_reply_dict):
        selected_number = int(self.number_dropdown.currentText())
        prompt, response = prompt_reply_dict.get(selected_number, ("", ""))
        markdown_text = f"<h3>Prompt:</h3><p>{prompt}</p><h3>Response:</h3><p>{response}</p>"
        self.text_browser.setHtml(markdown_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JsonSelector()
    window.show()
    sys.exit(app.exec_())
