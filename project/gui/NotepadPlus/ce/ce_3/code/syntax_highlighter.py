from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

class SyntaxHighlighter:
    def highlight_code(self, code: str, language: str) -> str:
        if language.lower() == 'python':
            formatter = HtmlFormatter()
            return highlight(code, PythonLexer(), formatter)
        return code  # Return plain code if language is not supported