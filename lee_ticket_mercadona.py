import pdfplumber

v = '0.5'

print(f'Mercadona ticket reader v{v}')
print()

def dump_dict(diccionario):
    for key, value in diccionario.items():
        print(f'[{key}] - {value}')

class ticket_mercadona:
    def __init__(self,direccion,fecha,factura,importe,productos):
        self.direccion = direccion
        self.fecha = fecha
        self.factura = factura
        self.importe =importe
        self.productos = productos

    def __str__():
        text = f'Dirección:{self.direccion}' + f'Fecha:{self.fecha}'
        return text
    
def read_ticket(fichero):

    ticket = pdfplumber.open(fichero)

    pages = ticket.pages[0]

    lineas = pages.extract_text_lines()
    lineas_texto = []
    for line in lineas:
        if 'text' in line.keys():
            lineas_texto.append(line['text'])
            
    if not lineas_texto[0].startswith('MERCADONA'):
        print(f'Ticket no válido: {lineas_texto[0]}')
        return
    print(f'{fichero}')
    print('-----------------')
    
    direccion  = lineas_texto[1]
    id_fin_CP = lineas_texto[2].index(' ')
    CP = lineas_texto[2][:id_fin_CP]
    poblacion =  lineas_texto[2][id_fin_CP+1:]
    telefono = lineas_texto[3][lineas_texto[3].rfind(' ')+1:]
    print(f'Dirección: {direccion}')
    print(f'Población: [{poblacion}] ({CP})')
    print(f'Teléfono: -{telefono}-')


    partes_fecha = lineas_texto[4].split(' ')
    fecha = partes_fecha[0] + ' ' + partes_fecha[1]
    op = partes_fecha[3]
    print(f'Fecha: [{fecha}] OP: [{op}]')
    
    factura = lineas_texto[5][22:]
    print(f'Factura: {factura}')
    if not lineas_texto[6].startswith('Descripción'):
        print(f'Ticket no válido: {lineas_texto[6]}')
        return
    lineas_tickets = []
    i = 7
    print('Productos')
    print('-------------')    
    while not lineas_texto[i].startswith('TOTAL') and not lineas_texto[i].startswith('ENTRADA'):
        if 'kg' in lineas_texto[i+1]:
            linea1 = lineas_texto[i] 
            
            id_fin_cantidad = linea1.index(' ')
            cantidad = int(linea1[:id_fin_cantidad])
            
            producto = linea1[id_fin_cantidad+1:]
            linea2 = lineas_texto[i + 1]
            partes = linea2.split(' ')
            cantidad = float(partes[0].replace(',','.'))
            precio_unidad = float(partes[2].replace(',','.'))
            precio_total = float(partes[4].replace(',','.'))
            print(f'{cantidad} [{producto}]  {precio_unidad}/unidad  Total: {precio_total}')            
            linea = lineas_texto[i] + '-' + lineas_texto[i+1]
            lineas_tickets.append(linea)
            i += 2
            # print(linea)
        else:
            try:
                linea = lineas_texto[i]
                lineas_tickets.append(linea)
                id_fin_cantidad = linea.index(' ')
                cantidad = int(linea[:id_fin_cantidad])
                if cantidad > 1:
                    #print(f'Linea {cantidad}: [{linea}]')
                    id_precio_total = linea.rfind(' ')+1
                    str_precio_total = linea[id_precio_total:].replace(',','.')
                    #print(f'Precio total -{str_precio_total}-')
                    precio_total = float(str_precio_total)
                    str_resto = linea[id_fin_cantidad+1:id_precio_total-1]
                    #print(f'resto [{str_resto}]')
                    id_precio_unidad = str_resto.rfind(' ')
                    str_precio_unidad = str_resto[id_precio_unidad+1:id_precio_total].replace(',','.')
                    #print(f'Precio unidad -{str_precio_unidad}-')
                    precio_unidad = float(str_precio_unidad)

                    producto = str_resto[:id_precio_unidad]
                else:
                    id_precio_total = linea.rfind(' ')+1
                    precio_unidad = precio_total = float(linea[id_precio_total:].replace(',','.'))
                    producto = linea[id_fin_cantidad+1:id_precio_total - 1]
                if cantidad == 1:
                    print(f'{cantidad} [{producto}] Precio total: {precio_total}')
                else:
                    print(f'{cantidad} [{producto}]  {precio_unidad}/unidad  Total: {precio_total}')
            except  Exception as e:
                print(e)
            
            i += 1

#    for linea in lineas_tickets:
#        print(f'{linea}')
    if lineas_texto[i].startswith('ENTRADA'):
        parking = lineas_texto[i]
        print(f'Parking: {parking}')
        i += 1
    total = lineas_texto[i][10:]
    print(f'Total: [{total}]')
    print()

from os import listdir
dir = './pdfs/'
for pdf in listdir(dir):
    read_ticket(dir + pdf)