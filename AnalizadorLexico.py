from TypeToken import TypeToken
from Token import Token
from tkinter import messagebox
import webbrowser
class AnalizadorLexico():

    tipo = TypeToken.DESCONOCIDO

    def __init__(self,inputFile):
        self.state = 0
        self.row = 1
        self.column = 0
        self.lexeme = ''
        self.tokens = []
        self.generate = True
        self.count = 0
        self.es_letra = False

        inputFile = inputFile + "#"
        actual = ''
        length = len(inputFile)

        for i in range(length):
            actual = inputFile[i]
            if self.state == 0:
                
                if actual.isalpha():
                    self.state = 1
                    self.lexeme += actual
                    self.column +=1
                    continue
                elif actual == '"':
                    self.state = 2
                    self.lexeme += actual
                    self.column += 1
                    continue
                elif actual.isdigit():
                    self.state = 3
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                    continue
                elif actual == '<':
                    self.state = 4
                    self.lexeme += actual
                    self.column += 1
                    continue
                elif actual == '-':
                    self.state = 5
                    self.lexeme += actual
                    self.column += 1
                    continue
                elif actual == " ":
                    self.column += 1
                    self.state = 0
                    continue
                elif actual == "":
                    self.column += 1
                    self.state = 0
                    continue
                elif actual == '\n':
                    self.row += 1
                    self.column#  i == (length-1)0
                    self.state = 0
                elif actual == '\t':
                    self.column += 5
                    self.state = 0
                elif actual == '#' and i == (length-1):
                    print('*********** Analisis finalizado ***************')
                else:
                    self.lexeme += actual
                    self.column += 1
                    self.AddToken(TypeToken.DESCONOCIDO.name)



            #Estado para manejar letras
            if self.state == 1:
                if actual.isalpha():
                    self.state = 1
                    self.lexeme += actual
                    self.column +=1
                    continue
                else: 
                    if actual == ' ' or actual == '#':
                        self.lexeme.replace("#", " ")
                        if self.IsReservedWord(self.lexeme):
                            self.AddToken(self.tipo.name)
                            self.column += 1
                        else:
                            if self.lexeme.isalpha():
                                self.AddToken(TypeToken.LETRAS.name)
                                self.column += 1
                            else:
                                self.state = 1
                                self.lexeme += actual
                                self.column += 1
                                self.AddToken(TypeToken.DESCONOCIDO.name)
                    else:
                        self.lexeme += actual
                        self.column += 1
                        self.state = 1
                        self.AddToken(TypeToken.DESCONOCIDO.name)
                        continue       
                    # else:
                    #     self.state = 1
                    #     self.lexeme += actual
                    #     self.column += 1
                    #     # self.AddToken(TypeToken.DESCONOCIDO.name)
                    #     continue
                        # self.AddToken(TypeToken.LETRAS.name)
                        # self.column += 1
                        

            
            #Estado para manejar cadenas
            if self.state == 2:
                if actual != '"':
                    self.state = 2
                    self.lexeme += actual
                    self.column += 1
                elif actual == '"':
                    self.lexeme += actual
                    self.column += 1
                    self.AddToken(TypeToken.CADENA.name)
                    self.column += 1

            #Estado para manejar digitos
            if self.state == 3:
                if actual.isdigit() and self.count <= 2:
                    self.state = 3
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                    continue
                elif actual.isdigit() and self.count > 2:
                    self.state = 3
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                    self.AddToken(TypeToken.DESCONOCIDO.name)
                    continue
                elif actual == ' ' and self.count <= 2:
                    self.state = 3
                    self.count += 1
                    self.AddToken(TypeToken.NUMERO.name)
                    self.column += 1
                    continue
                elif actual == '#' and self.count <= 2:
                    self.state = 3
                    self.count += 1
                    self.AddToken(TypeToken.NUMERO.name)
                    self.column += 1
                    continue
                else:
                    self.AddToken(TypeToken.DESCONOCIDO.name)

                                    
            

             #Primer estado para manejar rango de años   
            if self.state == 4:
                if actual.isdigit():
                    self.state = 4
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                elif self.count == 4 and actual == '-':
                    self.state = 16
                    self.lexeme += actual
                    self.column += 1
                    self.count = 0
                    continue
                else:
                    self.AddToken(TypeToken.DESCONOCIDO.name)
            # Segundo estado para manejar rango de años
            if self.state == 16:
                if actual.isdigit():
                    self.state = 16
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                    continue
                elif actual == '>':
                    self.state = 7
                    self.lexeme += actual
                    # self.column += 1
                    self.AddToken(TypeToken.AÑO.name)
                else:
                    self.AddToken(TypeToken.DESCONOCIDO.name)

            #Estado para manejar -f, -ji, -jf, -n
            if self.state == 5:
                if actual.isalpha():
                    self.state = 5
                    self.lexeme += actual
                    self.column += 1
                    continue
                elif self.lexeme == '-f' and actual == ' ':
                    self.state = 9
                    self.AddToken(TypeToken.GUION_F.name)
                    self.column += 1
                    self.state = 100
                    continue
                elif self.lexeme == '-ji' and actual == ' ':
                    self.state = 11
                    self.AddToken(TypeToken.GUION_JI.name)
                    self.column += 1
                    continue
                elif self.lexeme == '-jf':
                    self.state = 12
                    self.AddToken(TypeToken.GUION_JF.name)
                    self.column += 1
                    continue
                elif self.lexeme == '-n':
                    self.state = 13
                    self.AddToken(TypeToken.GUION_N.name)
                    self.column += 1
                    continue
                else:
                    self.column += 1
                    self.AddToken(TypeToken.DESCONOCIDO.name)
            
            #Estado para manejar nombre de archivo
            if self.state == 100:
                if actual.isalpha():
                    self.state = 100
                    self.lexeme += actual
                    self.column +=1
                    self.es_letra = True
                    continue
                else:   
                    if self.es_letra == True:
                        if actual.isalpha() or actual.isdigit() or actual == '_':
                            self.lexeme += actual
                            self.column += 1
                            self.state = 100
                            self.es_letra = True
                            continue
                        else:
                            self.AddToken(TypeToken.NOMBRE_ARCHIVO.name)
                            self.column += 1
                            continue
                    else:
                        if actual.isdigit():
                            self.lexeme += actual
                            self.column += 1
                            self.AddToken(TypeToken.NUMERO.name)
                            continue
                        else:
                            self.lexeme += actual
                            self.column += 1
                            self.AddToken(TypeToken.DESCONOCIDO.name)
                            continue


            #Estado para manejar nombres de archivos
            # if self.state == 9:
            #     if actual.isalpha() or actual == ' ':
            #         self.state = 9
            #         self.lexeme += actual
            #         self.column += 1
            #         continue
            #     elif actual.isdigit() or actual.isalpha() or actual == '_' and actual != ' ':
            #         self.state = 9
            #         self.lexeme += actual
            #         self.column += 1
            #         continue
            #     else:
            #         self.AddToken(TypeToken.GUION_F.name)
       


            #Estado para manejar -ji
            if self.state == 11:
                if actual == "" or actual == " " and self.count == 0:
                    self.state = 11
                    self.lexeme += actual
                    self.column += 1
                    continue
                elif actual.isdigit() and self.count <= 2:
                    self.state = 11
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                    continue
                elif actual == ' ':
                    self.AddToken(TypeToken.GUION_JI.name)
                    
                elif self.count > 2:
                        self.lexeme += actual
                        self.AddToken(TypeToken.DESCONOCIDO.name)
                        continue
                
                   
            #Estado para manejar -jf
            if self.state == 12:
                if actual == "" or actual == " " and self.count == 0:
                    self.state = 12
                    self.lexeme += actual
                    self.column += 1
                    continue
                elif actual.isdigit() and self.count <= 2:
                    self.state = 12
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                    continue
                elif actual == ' ' and self.count <= 2 or actual == '#':
                    self.AddToken(TypeToken.GUION_JF.name)
                elif self.count > 2:
                        self.AddToken(TypeToken.DESCONOCIDO.name)
                else:
                    self.AddToken(TypeToken.DESCONOCIDO.name)

            #Estado para manejar -n
            if self.state == 13:
                if actual == "" or actual == " " and self.count == 0:
                    self.state = 13
                    self.lexeme += actual
                    self.column += 1
                    continue
                elif actual.isdigit() and self.count <= 2:
                    self.state = 13
                    self.lexeme += actual
                    self.column += 1
                    self.count += 1
                    continue
                elif actual == ' ' and self.count <= 2 or actual == '#':
                    self.AddToken(TypeToken.GUION_N.name)
                elif self.count > 2:
                        self.AddToken(TypeToken.DESCONOCIDO.name)
                else:
                    self.AddToken(TypeToken.DESCONOCIDO.name)

            # if self.state == 13:
            #     if actual.isdigit() and self.count < 2:
            #         self.state = 13
            #         self.lexeme += actual
            #         self.column += 1
            #         self.count += 1
            #     else:
            #         if actual == ' ':
            #             self.AddToken(TypeToken.GUION_N.name)
            #         else:
            #             self.state = 13
            #             self.lexeme += actual
            #             self.column += 1
            #             self.count += 1
            #             self.AddToken(TypeToken.DESCONOCIDO.name)
           

    def AddToken(self, type):
        self.tokens.append(Token(self.lexeme, type, self.row, self.column))
        self.lexeme = ''
        self.state = 0
        self.count = 0
        self.es_letra = False

    def IsReservedWord(self, word):
        word = word.upper()

        if word == 'RESULTADO':
            self.tipo = TypeToken.RESULTADO
            return True
        elif word == 'VS':
            self.tipo = TypeToken.VS
            return True
        elif word == 'TEMPORADA':
            self.tipo = TypeToken.TEMPORADA
            return True
        elif word == 'JORNADA':
            self.tipo = TypeToken.JORNADA
            return True
        elif word == '-F':
            self.tipo = TypeToken.GUION_F
            return True
        elif word == 'GOLES':
            self.tipo = TypeToken.GOLES
            return True
        elif word == 'LOCAL':
            self.tipo = TypeToken.CONDICION_GOL
            return True
        elif word == 'VISITANTE':
            self.tipo = TypeToken.CONDICION_GOL
            return True
        elif word == 'TOTAL':
            self.tipo = TypeToken.CONDICION_GOL
            return True
        elif word == 'TABLA':
            self.tipo = TypeToken.TABLA
            return True
        elif word == 'PARTIDOS':
            self.tipo = TypeToken.PARTIDOS
            return True
        elif word == '-JI':
            self.tipo = TypeToken.GUION_JI
            return True
        elif word == '-JF':
            self.tipo = TypeToken.GUION_JF
            return True
        elif word == 'TOP':
            self.tipo = TypeToken.TOP
            return True
        elif word == 'SUPERIOR':
            self.tipo = TypeToken.CONDICION_TOP
            return True
        elif word == 'INFERIOR':
            self.tipo = TypeToken.CONDICION_TOP
            return True
        elif word == '-N':
            self.tipo = TypeToken.GUION_N
            return True
        elif word == 'ADIOS':
            self.tipo = TypeToken.ADIOS
            return True

        else:
            return False

    def PrintTokens(self):
        f = open('ReporteTokens.html', 'w', encoding='utf-8')
        contador = 0
        variable_inicial = """
                        <!doctype html>
                    <html lang="en">
                    <head>
                        <!-- Required meta tags -->
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link rel="stylesheet" href="css/styles.css">
                        <link rel="icon" href="logo_centro.png">
                        <!-- Bootstrap CSS -->
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

                        <title> LaLiga | Reporte Token</title>
                    </head>
                    <body class = "body-se">
                        
                        <section class="encabezado">
                            <!-- <h1>Hello, world!</h1> -->
                            <img style="height: 80px; width: 650px; margin-left: 50px; box-shadow: 7px 13px 37px black;"src="/img/logo_izquierdo.png">
                            <img style="height: 130px; width: 120px; margin-top: 0px; margin-left:70px; box-shadow: 7px 13px 37px black;"src="/img/logo_centro.png">
                            <img style="height: 80px; width: 680px; margin-left: 70px; box-shadow: 7px 13px 37px black;"src="/img/logo_derecho.PNG">
                        </section>
                        
                        <!-- <img src="fondoPrincipal.png" style="width:100%"> -->
                        
                        <section class = "subtitulo">
                            <h1>Reporte Tokens </h1>
                        </section>

                        <section class="tabla-goles-temporada">
                            <table class="table table-dark table-striped">
                                <thead>
                                    <tr>
                                        <th>No.</th>
                                        <th>Lexema</th>
                                        <th>Tipo Token</th>
                                        <th>columna</th>
                                    </tr>
                                </thead>

                                <tbody>
        """
        variable_final = """
                        </tbody>

                        </table>
                    </section>
                    <!-- Optional JavaScript; choose one of the two! -->

                    <!-- Option 1: Bootstrap Bundle with Popper -->
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

                    <!-- Option 2: Separate Popper and Bootstrap JS -->
                    <!--
                    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
                    -->
                </body>
                </html>
        """
        f.write(variable_inicial)
        for token in self.tokens:
            if token.type != TypeToken.DESCONOCIDO.name:
                contador += 1
                f.write("<tr>")
                f.write("<td>") 
                f.write(str(contador)) 
                f.write("</td>")

                f.write("<td>") 
                f.write(token.valid_lexeme) 
                f.write("</td>")

                f.write("<td>") 
                f.write(str(token.type)) 
                f.write("</td>")

                f.write("<td>") 
                f.write(str(token.column)) 
                f.write("</td>")
                f.write("</tr>")
                print(token.valid_lexeme + " -> Tipo: " + str(token.type) + " Fila: " + str(token.row) + " Columna: " + str(token.column))
    
        f.write(variable_final) 
        f.close()
        mensaje = 'Generando archivo de Reportes de Tokens'
        messagebox.showinfo('Mensaje', mensaje)
        webbrowser.open_new_tab("ReporteTokens.html")
    def PrintErrores(self):
        f = open('BugReport.html', 'w', encoding='utf-8')
        contador = 0
        variable_inicial = """
                <!doctype html>
                <html lang="en">
                <head>
                    <!-- Required meta tags -->
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="stylesheet" href="css/styles.css">
                    <link rel="icon" href="logo_centro.png">
                    <!-- Bootstrap CSS -->
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

                    <title> LaLiga | Token Errores</title>
                </head>
                <body class = "body-se">
                    
                    <section class="encabezado">
                        <!-- <h1>Hello, world!</h1> -->
                        <img style="height: 80px; width: 650px; margin-left: 50px; box-shadow: 7px 13px 37px black;"src="/img/logo_izquierdo.png">
                        <img style="height: 130px; width: 120px; margin-top: 0px; margin-left:70px; box-shadow: 7px 13px 37px black;"src="/img/logo_centro.png">
                        <img style="height: 80px; width: 680px; margin-left: 70px; box-shadow: 7px 13px 37px black;"src="/img/logo_derecho.PNG">
                    </section>
                    
                    <!-- <img src="fondoPrincipal.png" style="width:100%"> -->
                    
                    <section class = "subtitulo">
                        <h1>Reporte Tokens De Errores Lexicos</h1>
                    </section>

                    <section class="tabla-goles-temporada">
                        <table class="table table-dark table-striped">
                            <thead>
                                <tr>
                                    <th>No.</th>
                                    <th>Lexema</th>
                                    <th>Tipo Token</th>
                                    <th>Fila</th>
                                    <th>Columna</th>
                                </tr>
                            </thead>

                            <tbody>
        """
        variable_final = """
                    </tbody>

                    </table>
                </section>
                <!-- Optional JavaScript; choose one of the two! -->

                <!-- Option 1: Bootstrap Bundle with Popper -->
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" crossorigin="anonymous"></script>

                <!-- Option 2: Separate Popper and Bootstrap JS -->
                <!--
                <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>
                -->
            </body>
            </html>
        """
        f.write(variable_inicial)
        print('=============== Tokens desconocidos  ===================')
        for token in self.tokens:
            if token.type == TypeToken.DESCONOCIDO.name:
                contador += 1
                f.write("<tr>")
                f.write("<td>") 
                f.write(str(contador)) 
                f.write("</td>")

                f.write("<td>") 
                f.write(token.valid_lexeme) 
                f.write("</td>")

                f.write("<td>") 
                f.write(str(token.type)) 
                f.write("</td>")

                f.write("<td>") 
                f.write(str(token.row)) 
                f.write("</td>")

                f.write("<td>") 
                f.write(str(token.column)) 
                f.write("</td>")
                f.write("</tr>") 
                print(token.valid_lexeme + " -> Tipo: " + str(token.type) + " Fila: " + str(token.row) + " Columna: " + str(token.column))

        f.write(variable_final) 
        f.close()
        mensaje = 'Generando archivo de Reportes de Errores'
        messagebox.showinfo('Mensaje', mensaje)
        webbrowser.open_new_tab("BugReport.html")