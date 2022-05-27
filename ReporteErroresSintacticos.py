class ReporteErroresSintacticos():
    def __init__(self, lexeme, se_espera, column):
        self.lexeme = lexeme
        self.se_espera = se_espera
        self.column = column