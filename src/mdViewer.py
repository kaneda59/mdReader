import sys
import os
import markdown
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

# Note : Pour un rendu Markdown complet en production, il est recommandé d'inclure 
# une bibliothèque comme 'markdown' pour convertir le texte en HTML.
# Par souci de simplicité et de compacité, ce code montre la structure essentielle.

class MarkdownViewer(QMainWindow):
    def __init__(self, file_path=None):
        super().__init__()
        self.file_path = file_path
        self.markdown_content = ""
        self.is_code_mode = False
        
        if file_path and os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                self.markdown_content = f.read()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Markdown Viewer - {os.path.basename(self.file_path) if self.file_path else 'Nouveau'}")
        self.resize(800, 600)

        # Widget Principal
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Barre d'outils
        toolbar = QHBoxLayout()
        
        self.btn_toggle = QPushButton("<-> Code")
        self.btn_toggle.clicked.connect(self.toggle_mode)
        toolbar.addWidget(self.btn_toggle)

        self.btn_copy = QPushButton("Copier")
        self.btn_copy.clicked.connect(self.copy_content)
        toolbar.addWidget(self.btn_copy)

        self.btn_print = QPushButton("Imprimer")
        self.btn_print.clicked.connect(self.print_content)
        toolbar.addWidget(self.btn_print)

        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Zone d'affichage
        self.view_render = QWebEngineView()
        self.view_code = QTextEdit()
        self.view_code.setReadOnly(True)
        self.view_code.setPlainText(self.markdown_content)
        
        layout.addWidget(self.view_render)
        layout.addWidget(self.view_code)
        
        self.update_view()

    def update_view(self):
        if self.is_code_mode:
            self.view_render.hide()
            self.view_code.show()
        else:
            self.view_code.hide()
            
            # Convertit le Markdown en HTML structuré avec support des blocs de code
            html_content = markdown.markdown(self.markdown_content, extensions=['fenced_code'])
            
            # Structure HTML propre avec un style CSS de base pour la lisibilité
            html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; padding: 30px; color: #24292e; line-height: 1.6; }}
                    code {{ background-color: rgba(27,31,35,0.05); padding: 0.2em 0.4em; border-radius: 3px; font-family: monospace; }}
                    pre {{ background-color: #f6f8fa; padding: 16px; border-radius: 3px; overflow: auto; }}
                    pre code {{ background-color: transparent; padding: 0; }}
                    h1, h2, h3 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
                    ul, ol {{ padding-left: 2em; }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            self.view_render.setHtml(html)
            self.view_render.show()

    def toggle_mode(self):
        self.is_code_mode = not self.is_code_mode
        self.update_view()

    def copy_content(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.markdown_content)

    def print_content(self):
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.DialogCode.Accepted:
            if self.is_code_mode:
                self.view_code.print(printer)
            else:
                self.view_render.print(printer)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    path = sys.argv[1] if len(sys.argv) > 1 else None
    viewer = MarkdownViewer(path)
    viewer.show()
    sys.exit(app.exec())