from TypeToken import TypeToken
from Token import Token
from ReporteErroresSintacticos import ReporteErroresSintacticos
import csv
from encodings import utf_8
from tkinter import messagebox
import webbrowser


class Sintactico:
    preanalisis = TypeToken.DESCONOCIDO
    posicion = 0
    lista = []
    errorSintactico = False

    def __init__(self,lista):
        self.errorSintactico = False
        self.lista = lista
        self.lista.append(Token("$", TypeToken.ULTIMO.name, 0, 0))
        self.posicion = 0
        self.preanalisis = self.lista[self.posicion].type
        self.opcion = "0"
        self.lista_errores_sintacticos = []
        self.contador = 0
        self.Inicio()

    def Match(self,tipo):
        if self.preanalisis != tipo:
            if self.lista[self.posicion].valid_lexeme == "#":
                print("null " + "-- Sintactico", " -- Se esperaba "+str(tipo))
                se_esperaba = "Se esperaba " + str(tipo)
                self.lista_errores_sintacticos.append(ReporteErroresSintacticos("null ", se_esperaba, self.lista[self.posicion].column ))
                self.errorSintactico = True
            else:
                print(self.lista[self.posicion].valid_lexeme, "-- Sintactico", " -- Se esperaba "+str(tipo))
                se_esperaba = "Se esperaba " + str(tipo)
                self.lista_errores_sintacticos.append(ReporteErroresSintacticos(self.lista[self.posicion].valid_lexeme, se_esperaba, self.lista[self.posicion].column))
                self.errorSintactico = True
              
        
        if self.preanalisis != TypeToken.ULTIMO.name:
            self.posicion += 1
            self.preanalisis = self.lista[self.posicion].type
        
        
        if self.preanalisis == TypeToken.ULTIMO.name:
            
            print('\n=============== Fin del analisis sintactico ===============\n')
            if self.errorSintactico != True:
                print('\n*************** El analisis SINTACTICO es CORRECTO *******************\n')
                if self.lista[0].type == TypeToken.RESULTADO.name:
                    self.opcion = "1"
                elif self.lista[0].type == TypeToken.JORNADA.name:
                    self.opcion = "2"
                elif self.lista[0].type == TypeToken.GOLES.name:
                    self.opcion = "3"
                elif self.lista[0].type == TypeToken.TABLA.name:
                    self.opcion = "4"
                elif self.lista[0].type == TypeToken.PARTIDOS.name:
                    self.opcion = "5"
                elif self.lista[0].type == TypeToken.TOP.name:
                    self.opcion = "6"
                elif self.lista[0].type == TypeToken.ADIOS.name:
                    self.opcion = "7"
                
            else:
                print('\n*************** El analisis SINTACTICO es INCORRECTO *******************\n')



    def Inicio(self):
        print('\n=============== Inicio del analisis sintactico ===============\n')
        if TypeToken.RESULTADO.name == self.preanalisis:
            self.ResultadoDeUnPartido()
        elif TypeToken.JORNADA.name == self.preanalisis:
            if self.lista[4].type == TypeToken.GUION_F.name:
                self.ResultadoDeUnaJornada2()
            else:
                self.ResultadoDeUnaJornada()
        elif TypeToken.GOLES.name == self.preanalisis:
            self.TotalGolesTemporada()
            self.Repetir()
        elif TypeToken.TABLA.name == self.preanalisis:
            if self.lista[3].type == TypeToken.GUION_F.name:
                self.TablaGeneralTemporada2()
            else:
                self.TablaGeneralTemporada()
        elif TypeToken.PARTIDOS.name == self.preanalisis:
            if self.lista[4].type == TypeToken.GUION_JI.name:
                self.TemporadaDeUnEquipo()
            elif self.lista[4].type == TypeToken.GUION_F.name:
                self.TemporadaDeUnEquipo2()
        elif TypeToken.TOP.name == self.preanalisis:
            if self.lista[4].type == TypeToken.GUION_N.name:
                self.TopDeEquipos2()
            else:
                self.TopDeEquipos()
        elif TypeToken.ADIOS.name == self.preanalisis:
            self.SalidaDelBot()

    def OpcionEscogida(self):
        return self.opcion
    def ListaTokens(self):
        return self.lista

    def VerificarOpcion(self, opcion):
        if opcion == '1':
            print('Resultado de un partido')
        else:
            print('Comando desconocido')
    def Repetir(self):
        print('\n=============== Repetir del analisis sintactico ===============\n')
        if TypeToken.RESULTADO.name == self.preanalisis:
            self.ResultadoDeUnPartido()
            # self.Repetir()
        elif TypeToken.JORNADA.name == self.preanalisis:
            self.ResultadoDeUnaJornada()
            # self.Repetir()
        elif TypeToken.GOLES.name == self.preanalisis:
            self.TotalGolesTemporada()
            self.Repetir()
        elif TypeToken.TABLA.name == self.preanalisis:
            self.TablaGeneralTemporada()
            # self.Repetir()
        elif TypeToken.PARTIDOS.name == self.preanalisis:
            self.TemporadaDeUnEquipo()
            # self.Repetir()
        elif TypeToken.TOP.name == self.preanalisis:
            self.TopDeEquipos()
            self.Repetir()
        elif TypeToken.ADIOS.name == self.preanalisis:
            self.SalidaDelBot()

    #1
    def ResultadoDeUnPartido(self):
        self.Match(TypeToken.RESULTADO.name)
        self.Match(TypeToken.CADENA.name)
        self.Match(TypeToken.VS.name)
        self.Match(TypeToken.CADENA.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)
    

        
    #2
    def ResultadoDeUnaJornada(self):
        self.Match(TypeToken.JORNADA.name)
        self.Match(TypeToken.NUMERO.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)
        

    #2
    def ResultadoDeUnaJornada2(self):
        self.Match(TypeToken.JORNADA.name)
        self.Match(TypeToken.NUMERO.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)
        self.Match(TypeToken.GUION_F.name) #NOMBRE DEL ACRCHIVO ES OPCIONAL
        self.Match(TypeToken.NOMBRE_ARCHIVO.name) #NOMBRE DEL ACRCHIVO ES OPCIONAL

    #3
    def TotalGolesTemporada(self):
        self.Match(TypeToken.GOLES.name)
        self.Match(TypeToken.CONDICION_GOL.name)
        self.Match(TypeToken.CADENA.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)

    #4
    def TablaGeneralTemporada(self):
        self.Match(TypeToken.TABLA.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)

    #4.1
    def TablaGeneralTemporada2(self):
        self.Match(TypeToken.TABLA.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)
        self.Match(TypeToken.GUION_F.name) 
        self.Match(TypeToken.NOMBRE_ARCHIVO.name)

     #5
    def TemporadaDeUnEquipo(self):
        # if self.lista[4].type == TypeToken.GUION_JI.name:
        self.Match(TypeToken.PARTIDOS.name)
        self.Match(TypeToken.CADENA.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)
        self.Match(TypeToken.GUION_JI.name)
        self.Match(TypeToken.NUMERO.name)
        self.Match(TypeToken.GUION_JF.name)
        self.Match(TypeToken.NUMERO.name)
   
     #5.1
    def TemporadaDeUnEquipo2(self):
        self.Match(TypeToken.PARTIDOS.name)
        self.Match(TypeToken.CADENA.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)
        self.Match(TypeToken.GUION_F.name)
        self.Match(TypeToken.NOMBRE_ARCHIVO.name)

        # PARTIDOS "Real Madrid" TEMPORADA <1999-2000> -ji 1 -jf 18

    #6
    def TopDeEquipos(self):
        self.Match(TypeToken.TOP.name)
        self.Match(TypeToken.CONDICION_TOP.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)


    #6.1
    def TopDeEquipos2(self):
        self.Match(TypeToken.TOP.name)
        self.Match(TypeToken.CONDICION_TOP.name)
        self.Match(TypeToken.TEMPORADA.name)
        self.Match(TypeToken.AÑO.name)
        self.Match(TypeToken.GUION_N.name) 
        self.Match(TypeToken.NUMERO.name)

    def SalidaDelBot(self):
        self.Match(TypeToken.ADIOS.name)

    def ReporteErroresSintactico(self):
        f = open("ReporteErroresSintacticos.html", 'w', encoding='utf-8')
        variable_inicial ="""
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

                            <title> LaLiga |Errores Sintacticos</title>
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
                                <h1>Reporte Tokens De Errores Sintacticos</h1>
                            </section>

                            <section class="tabla-goles-temporada">
                                <table class="table table-dark table-striped">
                                    <thead>
                                        <tr>
                                            <th>No.</th>
                                            <th>Token</th>
                                            <th>Se esperaba</th>
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
        
        for i in range(len(self.lista_errores_sintacticos)):
            self.contador += 1
            f.write("<tr>")
            f.write("<td>") 
            f.write(str(self.contador)) 
            f.write("</td>")

            f.write("<td>") 
            f.write(self.lista_errores_sintacticos[i].lexeme)  
            f.write("</td>")

            f.write("<td>") 
            f.write(self.lista_errores_sintacticos[i].se_espera) 
            f.write("</td>")

            f.write("<td>") 
            f.write(str(self.lista_errores_sintacticos[i].column))  
            f.write("</td>")
            f.write("</tr>")
        
        f.write(variable_final)
        f.close()
        webbrowser.open_new_tab("ReporteErroresSintacticos.html")

    def LimpiarErroresSintacticos(self):
        self.lista_errores_sintacticos.clear()