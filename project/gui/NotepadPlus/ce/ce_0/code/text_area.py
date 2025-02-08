from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TkinterFormatter

class TextArea:
    def __init__(self):
        self.content = ""

    def insert_text(self, text: str):
        self.content += text

    def get_content(self) -> str:
        return self.content

    def highlight_syntax(self, language: str):
        if language == 'python':
            lexer = PythonLexer()
            formatter = TkinterFormatter()
            return highlight(self.content, lexer, formatter)
        return self.content  # Fallback to plain text if no language matches

    def indent_code(self):
        lines = self.content.splitlines()
        indented_lines = ['    ' + line for line in lines]
        self.content = '\n'.join(indented_lines)