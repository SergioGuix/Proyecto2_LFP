from tkinter import ttk
from tkinter import *
import tkinter.scrolledtext as st
import tkinter.font
import tkinter.font as tkFont
from tkinter.filedialog import askopenfile
import csv
from encodings import utf_8
from turtle import listen
from LigaBot import LigaBot
from TablaLiga import TablaLiga
from tkinter import messagebox
from Sintactico import Sintactico
from PIL import Image, ImageTk
from AnalizadorLexico import AnalizadorLexico
import webbrowser

class GUI_liga:
    def __init__(self, root):
        self.wind = root
        self.wind.title("La Liga Bot")
        self.wind.geometry("850x550")
        self.wind.resizable(0,0)
        self.wind.iconbitmap("fondo2.ico")
        # self.wind.config(bg = "midnightblue")
        self.wind['bg'] = '#003153'
        self.lista_liga = []
        self.lista_tabla = []
        self.lista_aux = []
        self.se_encontro_quipo = False
        self.se_encontro = False
        self.pos_x = 0
        self.pos_y = 0
        self.count = 0
        self.sintactico = None
        self.analizador_lexico = None
        self.inicializarGUI()
        

    def inicializarGUI(self):
        self.frame_chat = LabelFrame(self.wind, bg = "white", relief="sunken", bd = 5, width = 590, height =400)
        self.frame_chat.place(relx=0.05, rely = 0.10)

        self.frame_superior = LabelFrame(self.wind, bg = "#003153",  bd = 0, width = 820, height =50)
        self.frame_superior.place(relx=0.02, rely = 0.01)

        self.frame_derecho = LabelFrame(self.wind, bg = "#003153", bd = 0, width = 200, height =370)
        self.frame_derecho.place(relx=0.75, rely = 0.12)

        self.frame_inferior = LabelFrame(self.wind, bg = "white", relief="sunken", bd = 5, width = 590, height =55)
        self.frame_inferior.place(relx=0.05, rely = 0.88)

        self.label_titulo = Label(self.frame_superior, text="La Liga Bot", bg="#003153", fg ="white")
        self.font_tuple2 = ("Comic Sans MS", 20, "bold")
        self.label_titulo.configure(font = self.font_tuple2)
        self.label_titulo.place(x = 40, y = 10, width =420, height =38)
        self.txt = Entry(self.frame_inferior, bg="LightGray")
        self.txt.place(x = 10, y = 10, width =420, height =30)

        mensaje_bienvenida = "\t\tBienvenido a La Liga Bot. Ingrese un comando..."
        self.text_area = st.ScrolledText(self.frame_chat, width = 45, height = 13, bg = "white")
        self.text_area.place(x = 10, y = 10, width =570, height =370)
        self.font_tuple = ("Comic Sans MS", 10, "bold")
        self.text_area.insert(INSERT, mensaje_bienvenida)
        self.text_area.configure(font = self.font_tuple)
        

        # self.text_area.configure(state ='disabled')

    

        self.btn_enviar = Button(self.frame_inferior, bg="MediumSeaGreen", text="Enviar")
        self.btn_enviar['command'] = self.obtenerTextoDeUsuario
        self.btn_enviar.place(x = 448, y = 10, width =100, height =30)

        self.btn_reporte_errores = Button(self.frame_derecho, bg="LightGray", text="Reporte de errores")
        self.btn_reporte_errores['command'] = self.ReporteDeErrores
        self.btn_reporte_errores.place(x = 30, y = 20, width =140, height =30)

        self.btn_limpiar_errores = Button(self.frame_derecho, bg="LightGray", text="Limpiar log de errores")
        self.btn_limpiar_errores.place(x = 30, y = 70, width =140, height =30)
        self.btn_limpiar_errores['command'] = self.LimpiarErrores

        self.btn_reporte_tokens = Button(self.frame_derecho, bg="LightGray", text="Reporte de Tokens")
        self.btn_reporte_tokens.place(x = 30, y = 120, width =140, height =30) #ReporteTokens
        self.btn_reporte_tokens['command'] = self.ReporteTokens

        self.btn_limpiar_tokens = Button(self.frame_derecho, bg="LightGray", text="Limpiar log de tokens")
        self.btn_limpiar_tokens.place(x = 30, y = 170, width =140, height =30)

        self.btn_manual_usuario = Button(self.frame_derecho, bg="LightGray", text="Manual de usuario")
        self.btn_manual_usuario.place(x = 30, y = 220, width =140, height =30)
        self.btn_manual_usuario['command'] = self.AbrirManualUsuario #AbrirManualUsario

        self.btn_manual_tecnico = Button(self.frame_derecho, bg="LightGray", text="Manual técnico")
        self.btn_manual_tecnico.place(x = 30, y = 270, width =140, height =30)
        self.btn_manual_tecnico['command'] = self.AbrirManualTecnico

        self.btn_cargar_archivo = Button(self.frame_derecho, bg="DodgerBlue", text="Cargar Archivo CSV")
        self.btn_cargar_archivo['command'] = self.seleccionarArchivo
        self.btn_cargar_archivo.place(x = 12, y = 330, width =170, height =30)
    
    def obtenerTextoDeUsuario(self):
        texto =  "\n"+"\n"+ self.txt.get()
        self.font_tuple = ("Comic Sans MS", 10, "bold")
        self.text_area.configure(font = self.font_tuple)
        self.text_area.insert(INSERT, texto)

        self.analizador_lexico  = AnalizadorLexico(self.txt.get())
        analizador = AnalizadorLexico(self.txt.get())
        # analizador.PrintTokens()
        self.sintactico = Sintactico(analizador.tokens)
        print(self.sintactico.OpcionEscogida())

        error = 'no'

        if self.sintactico.OpcionEscogida() == '1':
            equipo1 = analizador.tokens[1].valid_lexeme
            equipo2 = analizador.tokens[3].valid_lexeme
            temporada = analizador.tokens[5].valid_lexeme
            
            simbolos = ['<', '>', '"']
            for i in range(len(simbolos)):
                temporada = temporada.replace(simbolos[i], "")
                equipo1 = equipo1.replace(simbolos[i], "")
                equipo2 = equipo2.replace(simbolos[i], "")
            print('\n=============== Afuera del Metodo =====================')
            print('Equipo Local: ' + equipo1)
            print('Equipo Visitante: ' + equipo2)
            print('Temporada: ' + temporada)
            print('====================================\n')
            self.resultadoDeUnPartido(equipo1, equipo2, temporada)

        elif self.sintactico.OpcionEscogida() == '2':
            jornada = analizador.tokens[1].valid_lexeme
            temporada = analizador.tokens[3].valid_lexeme
            print('Tamaño del arreglo tokens ', len(analizador.tokens))

            try:
                analizador.tokens[5].valid_lexeme
            except:
                error='si'

            if error == 'si':
                nombre_archivo_html = 'jornada'
            else:
                nombre_archivo_html = analizador.tokens[5].valid_lexeme

            simbolos = ['<', '>', '"']
            for i in range(len(simbolos)):
                temporada = temporada.replace(simbolos[i], "")
                jornada = jornada.replace(simbolos[i], "")
              
            print('\n====================================')
            print('Jornada: ' + jornada)
            print('Temporada: ' + temporada)
            print('Nombre HTML: ' + nombre_archivo_html)
            print('====================================\n')
            self.resultadoDeUnaJornada(jornada, temporada, nombre_archivo_html)
        
        elif self.sintactico.OpcionEscogida() == '3':  #GOLES TOTAL "Valencia" TEMPORADA <1998-1999>
            condicion_gol = analizador.tokens[1].valid_lexeme
            equipo = analizador.tokens[2].valid_lexeme
            temporada = analizador.tokens[4].valid_lexeme

            simbolos = ['<', '>', '"']
            for i in range(len(simbolos)):
                equipo = equipo.replace(simbolos[i], "")
                temporada = temporada.replace(simbolos[i], "")

            print('\n=============== Afuera del Metodo #3 =====================')
            print('Equipo : ' + equipo)
            print('Condicion Gol: ' + condicion_gol)
            print('Temporada: ' + temporada)
            print('====================================\n')
            self.totalDeGolesEnUnaTemporada(equipo, temporada, condicion_gol)

        elif self.sintactico.OpcionEscogida() == '4':
            error = 'no'
            temporada = analizador.tokens[2].valid_lexeme
            simbolos = ['<', '>', '"']
            for i in range(len(simbolos)):
                temporada = temporada.replace(simbolos[i], "")

            try:
                analizador.tokens[3].valid_lexeme
                nombre_archivo_html = analizador.tokens[4].valid_lexeme
            except:
                error='si'
                nombre_archivo_html = 'temporada'

            # if error == 'si':
            #     nombre_archivo_html = 'temporada'
            # else:
            #     nombre_archivo_html = analizador.tokens[4].valid_lexeme

            print('\n=============== Afuera del Metodo #4=====================')
            print('Nombre de archivo HTML: ' + nombre_archivo_html)
            print('Temporada: ' + temporada)
            print('====================================\n')
            self.tablaGeneralDeTemporada(temporada, nombre_archivo_html)
        
        elif self.sintactico.OpcionEscogida() == '5':
            nombre_archivo_html = ""
            jornada_inicial = ""
            jornada_final = ""
            equipo = analizador.tokens[1].valid_lexeme
            temporada = analizador.tokens[3].valid_lexeme

            simbolos = ['<', '>', '"']
            for i in range(len(simbolos)):
                equipo = equipo.replace(simbolos[i], "")
                temporada = temporada.replace(simbolos[i], "")
   

            if analizador.tokens[4].valid_lexeme == '-ji':
                nombre_archivo_html = 'partidos'
                jornada_inicial = analizador.tokens[5].valid_lexeme
                jornada_final = analizador.tokens[7].valid_lexeme
            elif analizador.tokens[4].valid_lexeme == '-f':
                nombre_archivo_html = analizador.tokens[5].valid_lexeme
                jornada_inicial = '1'
                jornada_final = '37'

           
            
            print('\n=============== Afuera del Metodo #5 =====================')
            print('Equipo ' + equipo)
            print('Temporada: ' + temporada)
            print('Jornada Inicial: ' + jornada_inicial)
            print('Jornada Final: ' + jornada_final)
            print('Nombre HTML ' + nombre_archivo_html)
            print('====================================\n')

            self.temporadaDeUnEquipo(equipo, temporada, jornada_inicial, jornada_final, nombre_archivo_html)

        elif self.sintactico.OpcionEscogida() == '6':
            numero_equipos = 0
            top_condicion = analizador.tokens[1].valid_lexeme
            temporada = analizador.tokens[3].valid_lexeme

            simbolos = ['<', '>', '"']
            for i in range(len(simbolos)):
                temporada = temporada.replace(simbolos[i], "")

            
            try:
                analizador.tokens[5].valid_lexeme
            except:
                error='si'

            if error == 'si':
                numero_equipos = 5
            else:
                numero_equipos = analizador.tokens[5].valid_lexeme


            print('\n=============== Afuera del Metodo #6 =====================')
            print('Condicion Top ' + top_condicion)
            print('Temporada: ' + temporada)
            print('Numero de equipos: ' , numero_equipos)
            print('====================================\n')

            self.TopDeEquipos(top_condicion, temporada, numero_equipos)
        elif self.sintactico.OpcionEscogida() == '7':
            self.SalidaBot()
        elif self.sintactico.OpcionEscogida() == '0':
            messagebox.showinfo('Mensaje' , 'Error Sintactico!')
            
    #Metodo para selccionar el archivo csv y posteriormente cargarlo
    def seleccionarArchivo(self):
        archivo = askopenfile(mode = 'r', filetypes = [('Archivos CSV', '.csv')])
        print(archivo)
        # lista = []
        with open('LaLigaBot-LFP.csv',  encoding='utf-8') as archivo:
            reader = csv.reader(archivo, delimiter=',')
            for row in reader:
                # print("Fecha: {0}, Temporada: {1}, Jornada: {2}, Equipo1: {3}, Equipo2: {4}, Goles1: {5}, Goles2: {6}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                self.lista_liga.append(LigaBot(row[0], row[1], row[2], row[3], row[4], row[5], row[6], 0, 0))
            for i in self.lista_liga:
                print('Fecha: ' + i.fecha + ' ' + 'Temporada: ' + i.temporada + ' Jornada: ' + i.jornada
                + ' Equipo1: ' + i.equipo1 + '  Equipo2:' + i.equipo2 + ' Goles1: ' + i.goles1 + ' Goles2:' + i.goles2 + ' Puntos1: ' , i.puntos1 , 'Puntos2: ', i.puntos2)
            messagebox.showinfo('Mensaje', 'Archivo cargado!')
    
    #1 Muestra el resultado de un partido, se especifican los equipos y la temporada
    def resultadoDeUnPartido(self, equipo1, equipo2, temporada):
        se_encontro_quipo1 = True
        se_encontro_temporada  = True
        self.pos_y += 15
        print('\n=============== Dentro del metodo =====================')
        print('Equipo Local: ' + equipo1)
        print('Equipo Visitante: ' + equipo2)
        print('Temporada: ' + temporada)
        print('====================================\n')

        for i in range(0, len(self.lista_liga)):
            if self.lista_liga[i].equipo1 == equipo1 and self.lista_liga[i].equipo2 == equipo2:
                if self.lista_liga[i].temporada == temporada:
                    var = "\n"+"\n" + 'El resultado de este partido fue : ' + self.lista_liga[i].equipo1 + ' ' + self.lista_liga[i].goles1 + " - " + self.lista_liga[i].equipo2 + ' ' + self.lista_liga[i].goles2
                    print('El resultado de este partido fue: ' + self.lista_liga[i].equipo1 + ' ' + self.lista_liga[i].goles1 + " - " + self.lista_liga[i].equipo2 + ' ' + self.lista_liga[i].goles2)
                    se_encontro_quipo1 = False
                    se_encontro_temporada  = False
                    # self.pos_y += 30
                    # self.label = Label(self.frame_chat, text = var, anchor = "w",  bg = "white")
                    # self.label.place(x = 10, y = self.pos_y, width = 400, height =30)
                    # self.text_area.insert(END, var)
                    # self.text_area.configure(font = "Comic Sans MS", 10, "bold")
                    self.font_tuple = ("Comic Sans MS", 10, "bold")
                    self.text_area.configure(font = self.font_tuple)
                    self.text_area.insert(INSERT, var)
        
        if se_encontro_quipo1 == True:
            messagebox.showinfo('Mensaje' , 'Equipo no encontrado!')
        if se_encontro_temporada == True:
            messagebox.showinfo('Mensaje: No se encontro este partido en la temporada! ', temporada)

    #2 Muestra en un archivo HTML el resultado de todos los partidos disputados en una jornada, se especifican la jornada y la temporada
    def resultadoDeUnaJornada(self, jornada, temporada, nombre_archivo_html):
        nombre_archivo_html = nombre_archivo_html + '.html'
        f = open(nombre_archivo_html, 'w', encoding='utf-8')
        variable_inicial = """
                    <!doctype html>
                    <html lang="en">
                    <head>
                        <!-- Required meta tags -->
                        <meta charset="utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link rel="stylesheet" href="css/styles.css">
                        <link rel="icon" href="logo_centro.png">
                        <!-- Bootstrap CSS -->
                        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

                        <title> LaLiga | Goles Temporada</title>
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
                            <h1>RESULTADOS DE UNA JORNADA LALIGA BBVA</h1>
                        </section>

                        <!-- <section>
                            <img style="height:500px; width: 500px; position: left; " src="/img/messi.jpg" alt="">
                        </section> -->
        """
        encabezado_tabla = """
                <section class="tabla-goles-temporada">
                <table class="table table-dark table-striped">
                    <thead>
                        <tr>
                            <th>No.</th>
                            <th>Temporada</th>
                            <th>Jornada</th>
                            <th>Equipo Local</th>
                            <th>Equipo Vistante</th>
                            <th>Resultado</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        f.write(variable_inicial)
        f.write(encabezado_tabla)

        self.pos_y += 30
        contador = 0
        for i in range(0, len(self.lista_liga)):
            if self.lista_liga[i].jornada == jornada and self.lista_liga[i].temporada == temporada:
                resultado =  self.lista_liga[i].goles1 + ' - ' + self.lista_liga[i].goles2
                contador += 1
                f.write("<tr>")
                f.write("<td>") 
                f.write(str(contador)) 
                f.write("</td>")

                f.write("<td>") 
                f.write(self.lista_liga[i].temporada) 
                f.write("</td>")

                f.write("<td>") 
                f.write(self.lista_liga[i].jornada) 
                f.write("</td>")


                f.write("<td>") 
                f.write(self.lista_liga[i].equipo1 ) 
                f.write("</td>")

                f.write("<td>") 
                f.write(self.lista_liga[i].equipo2 ) 
                f.write("</td>")

                f.write("<td>") 
                f.write(resultado) 
                f.write("</td>")
                f.write("</tr>") 
                
                print('El resultado de este partido fue: ' + self.lista_liga[i].equipo1 + ' ' + self.lista_liga[i].goles1 + " - " + self.lista_liga[i].equipo2 + ' ' + self.lista_liga[i].goles2)

        table_final = """   
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
        f.write(table_final) 
        f.close()
        mensaje = 'Generando archivo de resultados jornada ' + jornada + ' temporada ' + temporada
        messagebox.showinfo('Mensaje', mensaje)
        print('Nombre de archivo: ' + nombre_archivo_html)
        webbrowser.open_new_tab(nombre_archivo_html)

    #3 Muestra el total de goles anotados por un equipo, se especifica la condición de los goles, el equipo y la temporada:  
    def totalDeGolesEnUnaTemporada(self, equipo, temporada, condicion_gol):
        # equipo = "Barcelona"
        # temporada = "2019-2020"
        condicion = condicion_gol
        print('CONDICION = ' + condicion)
        total_goles = 0
        # visitante = "visitante"
        # total = "total"
        
        for i in range(0, len(self.lista_liga)):

            if condicion == 'LOCAL':

                if self.lista_liga[i].equipo1 == equipo and self.lista_liga[i].temporada == temporada:
                    total_goles += int(self.lista_liga[i].goles1)    
                    print('Goles 1 = ' + self.lista_liga[i].goles1)           
                    print('Los goles anotados por el ' + self.lista_liga[i].equipo1 + 'en condicion de ' + condicion + " en la temporada " + temporada + " fueron " + self.lista_liga[i].goles1)
                    
            elif condicion == 'VISITANTE':

                if self.lista_liga[i].equipo2 == equipo and self.lista_liga[i].temporada == temporada:
                    total_goles += int(self.lista_liga[i].goles2)
                    print('Los goles anotados por el ' + self.lista_liga[i].equipo2 + 'en condicion de ' + condicion + " en la temporada " + temporada + " fueron " + self.lista_liga[i].goles2)

            elif condicion == 'TOTAL':

                if self.lista_liga[i].equipo1 == equipo and self.lista_liga[i].temporada == temporada:
                    total_goles += int(self.lista_liga[i].goles1)
                    print('Los goles anotados por el ' + self.lista_liga[i].equipo1 + 'en condicion de ' + condicion + " en la temporada " + temporada + " fueron " + self.lista_liga[i].goles1)
      
                if self.lista_liga[i].equipo2 == equipo and self.lista_liga[i].temporada == temporada:
                    total_goles += int(self.lista_liga[i].goles2)
                    print('Los goles anotados por el ' + self.lista_liga[i].equipo2 + 'en condicion de ' + condicion + " en la temporada " + temporada + " fueron " + self.lista_liga[i].goles2)

        mensaje_bot = "\n" + "\n" + "Los goles anotados por el " + equipo + " en condicion de " + condicion + " en la temporada " + temporada + " fueron " + str(total_goles)
        print(str(mensaje_bot))
        # self.pos_y += 30
        # self.label_bot = Label(self.frame_chat, text = str(mensaje_bot), anchor = "w", bg = "white")
        # self.label_bot.place(x = 0, y = self.pos_y, width = 480, height =30)

        self.font_tuple = ("Comic Sans MS", 10, "bold")
        self.text_area.configure(font = self.font_tuple)
        self.text_area.insert(INSERT, mensaje_bot)
    
    # 4 Muestra la clasificación de La Liga (ordenamiento respecto a puntos), se especifica la temporada:
    def tablaGeneralDeTemporada(self, temp, nombre_archivo_html):
        equipo = ''
        total_pts = 0
        temporada = temp

        self.lista_aux.clear()
        self.lista_tabla.clear()
       
        #Se asignan puntos a los equipos, con respecto a los resultados
        for i in range(len(self.lista_liga)):
            if self.lista_liga[i].temporada == temporada:                
                if int(self.lista_liga[i].goles1) > int(self.lista_liga[i].goles2):
                    self.lista_liga[i].puntos1 +=3
                elif int(self.lista_liga[i].goles2) > int(self.lista_liga[i].goles1):
                    self.lista_liga[i].puntos2 +=3
                elif int(self.lista_liga[i].goles2) == int(self.lista_liga[i].goles1):
                    self.lista_liga[i].puntos2 +=1
                    self.lista_liga[i].puntos1 +=1


        # Sumatoria de puntos de toda la temporada
        for i in range(0, len(self.lista_liga)):
            if self.lista_liga[i].temporada == temporada:
                total_pts = 0
                equipo = self.lista_liga[i].equipo1
                for x in range(0, len(self.lista_liga)):
                    if temporada == self.lista_liga[x].temporada and self.lista_liga[x].equipo1 == equipo:
                        total_pts += int(self.lista_liga[x].goles1)

                    elif temporada == self.lista_liga[x].temporada and self.lista_liga[x].equipo2 == equipo:
                        total_pts += int(self.lista_liga[x].goles2)
                # creamos un arreglo de tipo TablaLiga para agregar equipos con el total de puntos
                self.lista_tabla.append(TablaLiga(self.lista_liga[i].equipo1, total_pts, self.lista_liga[i].temporada))

        # for i in range(len(self.lista_liga)):
        #     if self.lista_liga[i].temporada == temporada:
        #         if self.lista_liga[i].equipo1 == 'Barcelona':          
        #             if int(self.lista_liga[i].goles1) > int(self.lista_liga[i].goles2):
        #                 print('Gano ' + self.lista_liga[i].equipo1 + ' puntos: ' , self.lista_liga[i].puntos1)
        #             elif int(self.lista_liga[i].goles2) == int(self.lista_liga[i].goles1):
        #                 print('Empato ' + self.lista_liga[i].equipo1 + ' puntos: ' , self.lista_liga[i].puntos1)
        #         elif self.lista_liga[i].equipo2 == 'Barcelona':          
        #             if int(self.lista_liga[i].goles1) < int(self.lista_liga[i].goles2):
        #                 print('Gano ' + self.lista_liga[i].equipo2 + ' puntos: ' , self.lista_liga[i].puntos2)
        #             elif int(self.lista_liga[i].goles2) == int(self.lista_liga[i].goles1):
        #                 print('Empato ' + self.lista_liga[i].equipo2 + ' puntos: ' , self.lista_liga[i].puntos2)

        # agregamos los equipos ya con los puntos conseguidos en la temporada a la lisata_aux
        # y verificamos que al agregar un equipo no se repita el la lista_aux
        for i in range(len(self.lista_tabla)):
            total = 0 
            equipo = self.lista_tabla[i].equipo
            self.se_encontro = False
            for x in range(len(self.lista_tabla)):
                if self.lista_tabla[x].equipo == equipo:
                    # total += self.lista_tabla[x].total_pts
                    total = self.lista_tabla[x].total_pts
                    continue
            for a in range(len(self.lista_aux)):
                if equipo == self.lista_aux[a].equipo:
                    self.se_encontro = True

            if self.se_encontro == False:
                self.lista_aux.append(TablaLiga(equipo, total, self.lista_tabla[i].temporada))

       
        #Ordenamiento Burbuja
        print('======== ORDENAR EQUIPOS ===========')
        longitud = len(self.lista_aux)
        for i in range(1,longitud):
            for j in range(0,longitud-i):
                if(self.lista_aux[j+1].total_pts > self.lista_aux[j].total_pts):
                    aux = self.lista_aux[j];
                    self.lista_aux[j] = self.lista_aux[j+1];
                    self.lista_aux[j+1] = aux;
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

                        <title> LaLiga |Tabla </title>
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
                            <h1>Tabla General De Temporada """
        
        variable_inicial3 = """ </h1>
                        </section>

                        <!-- <section>
                            <img style="height:500px; width: 500px; position: left; " src="/img/messi.jpg" alt="">
                        </section> -->

                        <section class="tabla-goles-temporada">
                            <table class="table table-dark table-striped">
                                <thead>
                                    <tr>
                                        <th>No.</th>
                                        <th>Temporada</th>
                                        <th>Equipo</th>
                                        <th>Puntos</th>
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
        # nombre_archivo_html = nombre_archivo_html + '.html'
        temporada = ''
        nombre_archivo_html = nombre_archivo_html + ".html"
        f = open(nombre_archivo_html, 'w', encoding='utf-8')
        f.write(variable_inicial)
        f.write(temp)
        f.write(variable_inicial3)
        print('\n=========== TABLA LIGA  ==============') 
        for i in range(0, len(self.lista_aux)):
            temporada = self.lista_aux[i].temporada
            f.write("<tr>")
            f.write("<td>") 
            f.write(str(i+1)) 
            f.write("</td>")

            f.write("<td>") 
            f.write(self.lista_aux[i].temporada) 
            f.write("</td>")

            f.write("<td>") 
            f.write(self.lista_aux[i].equipo) 
            f.write("</td>")

            f.write("<td>") 
            f.write(str(self.lista_aux[i].total_pts)) 
            f.write("</td>")
            f.write("</tr>") 
            print( i+1 , ') ' + ' Equipo: '+ self.lista_aux[i].equipo + ' Puntos: ' , self.lista_aux[i].total_pts , ' Temporada: ' + self.lista_aux[i].temporada)
        f.write(variable_final) 
        f.close()
        mensaje = 'Generando archivo de Clasificacion de La Liga Temporada ' + temporada
        messagebox.showinfo('Mensaje', mensaje)
        print('Nombre de archivo: ' + nombre_archivo_html)
        webbrowser.open_new_tab(nombre_archivo_html)

    #5 Muestra todos los resultados de un equipo durante una temporada de La Liga, se especifica el equipo, 
    # la temporada y opcionalmente un rango de jornadas:
    def temporadaDeUnEquipo(self, equipo, temporada, jornada_inicial, jornada_final, nombre_archivo_html):
        nombre_archivo_html = nombre_archivo_html + '.html'
        contador = 0
        f = open(nombre_archivo_html, 'w', encoding='utf-8')
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

                    <title> LaLiga |Temporada Equipo </title>
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
                        <h1>Temporada De Un Equipo </h1>
                    </section>

                    <section class="tabla-goles-temporada">
                        <table class="table table-dark table-striped">
                            <thead>
                                <tr>
                                    <th>No.</th>
                                    <th>Temporada</th>
                                    <th>Jornada</th>
                                    <th>Condicion</th>
                                    <th>Equipo</th>
                                    <th>Resultado</th>
                                </tr>
                            </thead>


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
        for i in range(0, len(self.lista_liga)):
            if self.lista_liga[i].temporada == temporada:
                if int(self.lista_liga[i].jornada) >= int(jornada_inicial) and int(self.lista_liga[i].jornada) <= int(jornada_final):
                    if self.lista_liga[i].equipo1 == equipo:
                        contador += 1
                        f.write("<tr>")
                        f.write("<td>") 
                        f.write(str(contador)) 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write(self.lista_liga[i].temporada) 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write(self.lista_liga[i].jornada) 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write("Local") 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write(self.lista_liga[i].equipo1) 
                        f.write("</td>")
                        resultado = self.lista_liga[i].goles1 + " - " + self.lista_liga[i].goles2
                        f.write("<td>") 
                        f.write(resultado) 
                        f.write("</td>")
                        f.write("</tr>") 

                        print(' Condicion Local: ' + self.lista_liga[i].equipo1 + ' Equipo 2:' + self.lista_liga[i].equipo2 + ' Jornada: ' + self.lista_liga[i].jornada  +  ' Temporada: ' + self.lista_liga[i].temporada + ' ' + self.lista_liga[i].goles1 + " - " + self.lista_liga[i].goles2)
                    elif self.lista_liga[i].equipo2 == equipo:
                        contador += 1
                        f.write("<tr>")
                        f.write("<td>") 
                        f.write(str(contador)) 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write(self.lista_liga[i].temporada) 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write(self.lista_liga[i].jornada) 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write("Visitante") 
                        f.write("</td>")

                        f.write("<td>") 
                        f.write(self.lista_liga[i].equipo2) 
                        f.write("</td>")
                        resultado = self.lista_liga[i].goles2 + " - " + self.lista_liga[i].goles1
                        f.write("<td>") 
                        f.write(resultado) 
                        f.write("</td>")
                        f.write("</tr>") 
                        
                        print(' Condicion Visitante: ' + self.lista_liga[i].equipo2 + ' Equipo 1:' + self.lista_liga[i].equipo1 + ' Jornada: ' + self.lista_liga[i].jornada  + ' Temporada: ' + self.lista_liga[i].temporada + ' ' + self.lista_liga[i].goles2 + " - " + self.lista_liga[i].goles1)
                    # else:
                        # mensaje = 'No se encontro el equipo ' + equipo
                        # messagebox.showinfo('Mensaje', mensaje)

        f.write(variable_final) 
        f.close()
        mensaje = 'Generando archivo de resultados temporada ' + temporada + ' \n del ' + equipo
        messagebox.showinfo('Mensaje', mensaje)
        print('Nombre de archivo: ' + nombre_archivo_html)
        webbrowser.open_new_tab(nombre_archivo_html)
    #6 Muestra el top (superior o inferior) de los equipos clasificados según los puntos conseguidos.
    def TopDeEquipos(self, top_condicion, temporada, rango_superior):
        # rango_superior = 5
        # top = 'SUPERIOR'

        self.lista_aux.clear()
        self.lista_tabla.clear()

        for i in range(len(self.lista_liga)):
            self.lista_liga[i].puntos1 = 0
            self.lista_liga[i].puntos2 = 0
        # Se asignan puntos a los equipos, con respecto a los resultados
        for i in range(len(self.lista_liga)):
            if self.lista_liga[i].temporada == temporada:                
                if int(self.lista_liga[i].goles1) > int(self.lista_liga[i].goles2):
                    self.lista_liga[i].puntos1 +=3
                elif int(self.lista_liga[i].goles2) > int(self.lista_liga[i].goles1):
                    self.lista_liga[i].puntos2 +=3
                elif int(self.lista_liga[i].goles2) == int(self.lista_liga[i].goles1):
                    self.lista_liga[i].puntos2 +=1
                    self.lista_liga[i].puntos1 +=1

        # Sumatoria de puntos de toda la temporada
        for i in range(0, len(self.lista_liga)):
            if self.lista_liga[i].temporada == temporada:
                total_pts = 0
                equipo = self.lista_liga[i].equipo1
                for x in range(0, len(self.lista_liga)):
                    if temporada == self.lista_liga[x].temporada and self.lista_liga[x].equipo1 == equipo:
                        total_pts += int(self.lista_liga[x].goles1)

                    elif temporada == self.lista_liga[x].temporada and self.lista_liga[x].equipo2 == equipo:
                        total_pts += int(self.lista_liga[x].goles2)
                # creamos un arreglo de tipo TablaLiga para agregar equipos con el total de puntos
                self.lista_tabla.append(TablaLiga(self.lista_liga[i].equipo1, total_pts, self.lista_liga[i].temporada))

        # agregamos los equipos ya con los puntos conseguidos en la temporada a la lisata_aux
        # y verificamos que al agregar un equipo no se repita el la lista_aux
        for i in range(len(self.lista_tabla)):
            total = 0 
            equipo = self.lista_tabla[i].equipo
            self.se_encontro = False
            for x in range(len(self.lista_tabla)):
                if self.lista_tabla[x].equipo == equipo:
                    # total += self.lista_tabla[x].total_pts
                    total = self.lista_tabla[x].total_pts
                    continue
            for a in range(len(self.lista_aux)):
                if equipo == self.lista_aux[a].equipo:
                    self.se_encontro = True

            if self.se_encontro == False:
                self.lista_aux.append(TablaLiga(equipo, total, self.lista_tabla[i].temporada))
        

        if top_condicion == 'SUPERIOR':
            mensaje = '\n\nEl Top superior de la temporada ' + temporada + ' fue:\n'
            self.font_tuple = ("Comic Sans MS", 10, "bold")
            self.text_area.configure(font = self.font_tuple)
            self.text_area.insert(INSERT, mensaje)
            #Ordenamiento Burbuja
            print('======== ORDENAR EQUIPOS CON MAS PUNTOS ===========')
            longitud = len(self.lista_aux)
            for i in range(1,longitud):
                for j in range(0,longitud-i):
                    if(self.lista_aux[j+1].total_pts > self.lista_aux[j].total_pts):
                        aux = self.lista_aux[j];
                        self.lista_aux[j] = self.lista_aux[j+1];
                        self.lista_aux[j+1] = aux;
            for i in range(int(rango_superior)):
                mensaje = '\n'+ str(i+1) + ') ' +  ' Temporada: ' + self.lista_aux[i].temporada +' Equipo: '+ self.lista_aux[i].equipo + ' Puntos: ' + str(self.lista_aux[i].total_pts)
                print(mensaje)
                self.font_tuple = ("Comic Sans MS", 10, "bold")
                self.text_area.configure(font = self.font_tuple)
                self.text_area.insert(INSERT, mensaje)

        elif top_condicion == 'INFERIOR':
            mensaje = '\n\nEl Top Inferior de la temporada ' + temporada + ' fue:\n'
            self.font_tuple = ("Comic Sans MS", 10, "bold")
            self.text_area.configure(font = self.font_tuple)
            self.text_area.insert(INSERT, mensaje)
            #Ordenamiento Burbuja
            print('======== ORDENAR EQUIPOS CON MENOS PUNTOS ===========')
            longitud = len(self.lista_aux)
            print('cantidad de equipos: ',  longitud)
            for i in range(1,longitud):
                for j in range(0,longitud-i):
                    if(self.lista_aux[j+1].total_pts < self.lista_aux[j].total_pts):
                        aux = self.lista_aux[j];
                        self.lista_aux[j] = self.lista_aux[j+1];
                        self.lista_aux[j+1] = aux;
            
            for i in range(int(rango_superior)):
                mensaje =  '\n'+ str(i+1) + ') ' +  ' Temporada: ' + self.lista_aux[i].temporada +' Equipo: '+ self.lista_aux[i].equipo + ' Puntos: ' + str(self.lista_aux[i].total_pts)
                print(mensaje)
                self.font_tuple = ("Comic Sans MS", 10, "bold")
                self.text_area.configure(font = self.font_tuple)
                self.text_area.insert(INSERT, mensaje)
    #7 Finaliza la ejecución del programa:
    def SalidaBot(self):
        mensaje = 'Gracias por utilizar este software! AD1OS'
        messagebox.showinfo('Mensaje', mensaje)
        self.wind.destroy()
    # Reporte De Errores
    def ReporteDeErrores(self):
        self.analizador_lexico.PrintErrores()
        self.sintactico.ReporteErroresSintactico()
    def ReporteTokens(self):
        self.analizador_lexico.PrintTokens()
    
    def LimpiarErrores(self):
        self.sintactico.LimpiarErroresSintacticos()
    
    def AbrirManualTecnico(self):
        webbrowser.open_new_tab("Manual Técnico.pdf")

    def AbrirManualUsuario(self):
        webbrowser.open_new_tab("Manual de usuario.pdf")

# def main():
  
    # entrada = input("Ingrese texto...")
    
    # analizador = AnalizadorLexico(entrada)
    # analizador.PrintTokens()
    # sintactico = Sintactico(analizador.tokens)   
    


if __name__ == '__main__':
    # main()

    root = Tk()
    GUI_liga = GUI_liga(root)
    root.mainloop()