import csv
from encodings import utf_8
from LigaBot import LigaBot
from tkinter.filedialog import askopenfile


archivo = askopenfile(mode = 'r', filetypes = [('Archivos CSV', '.csv')])
print(archivo)

lista = []
with open('LaLigaBot-LFP.csv',  encoding='utf-8') as archivo:
    reader = csv.reader(archivo, delimiter=',')
    for row in reader:
        # print("Fecha: {0}, Temporada: {1}, Jornada: {2}, Equipo1: {3}, Equipo2: {4}, Goles1: {5}, Goles2: {6}".format(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        lista.append(LigaBot(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    for i in lista:
        print('Fecha: ' + i.fecha + ' ' + 'Temporada: ' + i.temporada )