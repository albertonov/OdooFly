#!/usr/bin/python
# coding: utf-8
#
import time
import xmlrpclib

# Datos de conexión (adaptar a cada caso)
#
from itertools import product

server = "localhost"
port = 8069
dbname = "odoo"
user_name = "admin"
user_passwd= "admin"


# Conectamos con el servicio 'common' de Odoo
conn = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/2/%s' % (server, port, 'common'))
# Obtenemos identificador (uid) del usuario
uid = conn.authenticate(dbname, user_name, user_passwd, {})
# Conectamos con el servicio 'object' de Odoo
object = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/2/%s' % (server, port, 'object'))


def main():

    print "Introduzca el nombre de la Base de datos"


    print "OdooFly\n\nSeleccione opcion:\n\n\t1. Obtener los aeropuertos con mas llegadas/salidas\n\t2. Mostrar los pasajeros de un vuelo.\n" \
          "\t3. Añadir un nuevo vuelo\n\t4. Limpiar el historial\n\t0. Salir"
    opcion = -1
    while opcion != 0:
        opcion = raw_input('\n\tIntroduzca su opcion: ')

        if opcion == '1':
            aeropuertosMasVisitado()
        elif opcion == '2':
            mostrarPasajeros()
        elif opcion == '3':
            if lanzarNuevoVuelo():
                print "\tVuelo añadido exitosamente"
            else:
                print "\tVuelo cancelado"
        elif opcion == '4':
            limpiarHistorial()

        elif opcion == '0':
            pass

def aeropuertosMasVisitado():
    aeropuertos_ids = object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'search', [[]])

    aeropuertos_destino = object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'read', [aeropuertos_ids], {'fields': ['destino']})
    aeropuertos_origen = object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'read', [aeropuertos_ids], {'fields': ['origen']})
    listaaux1 = []
    listaaux2 = []
    listadestinos = []
    listaorigenes = []

    for x in aeropuertos_destino:
        airport = x
        listaaux1.append(airport['destino'])
    for x in aeropuertos_origen:
        airport = x
        listaaux2.append(airport['origen'])
    for destinos in listaaux1:
        listadestinos.append(destinos[1])
    for origenes in listaaux2:
        listaorigenes.append(origenes[1])
    if len(listadestinos) != 0  or len(listaorigenes) != 0  :
        print "\n\tAeropuerto con mas destinos:"
        most_frequent(listadestinos)
        print "\n\tAeropuerto con mas salidas:"
        most_frequent(listaorigenes)
    else:
        print "\tNo se han establecido vuelos aun"



def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    print "\t"+num + " con " + str(counter) + " viajes de un total de " + str(len(List)) + " viajes"

def mostrarPasajeros():
    #print "\n\tIntroduzca el nombre del vuelo: "
    nme = raw_input("\n\tIntroduzca el nombre del vuelo: ")
    print "\n"
    trayecto_id = object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'search_read', [[['name','=',nme]]], {'fields': ['pasajeros']})
    if len(trayecto_id) != 0:
        listaux= trayecto_id[0]
        lista_pasajeros = listaux['pasajeros']

        print '{:<40}  {:<40}  {:<40} '.format("Nombre", "Telefono", "Email"  ) +"\n------------------------------------------------------------------------------------------------------------------------"

        for ps in lista_pasajeros:
            pasajero = object.execute_kw(dbname, uid, user_passwd, 'res.partner', 'search_read', [[['id','=',str(ps)]]], {'fields': ['name', 'phone', 'email']})
            aux = pasajero [0]
            if not aux['phone']:
                aux['phone'] = '-'
            if not aux['email']:
                aux['email'] = '-'

            print '{:<40}  {:<40}  {:<40} '.format(aux['name'].encode('utf-8') , aux['phone'].encode('utf-8') , aux['email'].encode('utf-8')   )

        print str(len(lista_pasajeros)) + " Pasajeros en total"

    else:
        print "Vuelo no encontrado"


def lanzarNuevoVuelo():
    parar = False
    print "\tIntroduzca CANCEL para cancelar"


    name = raw_input('\tIntroduzca el nombre del vuelo:\n\t> ')
    if name == "CANCEL":
        return False
    fecha_salida = raw_input('\tIntroduzca fecha de salida (mm/dd/aaaa):\n\t> ')
    if fecha_salida == "CANCEL":
        return False
    fecha_llegada = raw_input('\tIntroduzca fecha de llegada (mm/dd/aaaa):\n\t> ')
    if fecha_llegada == "CANCEL":
        return False
    hSalida = raw_input('\tIntroduzca hora de salida:\n\t> ')
    if hSalida == "CANCEL":
        return False
    hLlegada = raw_input('\tIntroduzca hora de llegada:\n\t> ')
    if hLlegada == "CANCEL":
        return False
    nombre_avion = raw_input('\tIntroduzca el nombre del avion:\n\t> ')
    if nombre_avion == "CANCEL":
        return False
    nombre_origen = raw_input('\tIntroduzca el nombre del aeropuerto de salida:\n\t> ')
    if nombre_origen == "CANCEL":
        return False
    nombre_llegada = raw_input('\tIntroduzca el nombre del aeropuerto de llegada:\n\t> ')
    if nombre_llegada == "CANCEL":
        return False


    a =  object.execute_kw(dbname, uid, user_passwd, 'odoofly.avion', 'search_read', [[['name','=',nombre_avion]]], {'fields': ['id', 'numeroAsientos']})
    o = object.execute_kw(dbname, uid, user_passwd, 'odoofly.aeropuerto', 'search_read', [[['name','=',nombre_origen]]], {'fields': ['id']})
    d = object.execute_kw(dbname, uid, user_passwd, 'odoofly.aeropuerto', 'search_read', [[['name', '=', nombre_llegada]]], {'fields': ['id']})
    try:
        avion = a[0]
        origen = o[0]
        destino= d[0]
    except IndexError: #si se produce una excepcion out of range es que algun dato no ha sido localizado en la DB
        print "No se ha podido localizar el aeropuerto o el avion en la base de datos"
        return  False
    ids_pasajeros = []
    print "\tIntroduzca el nombre de los pasajeros (introduzca FIN para terminar de añadir | CANCEL para cancelar el proceso): "
    while not parar:
        ps = raw_input('\n\t> ')

        if ps == 'FIN':
            parar = True
        elif ps == 'CANCEL':
            return False
        else:
            aux = object.execute_kw(dbname, uid, user_passwd, 'res.partner', 'search_read', [[['name','=',str(ps)]]], {'fields': ['id']})
            if len(aux) != 0:
                newPS = aux[0]
                ids_pasajeros.append(newPS['id'])
            else:
                print "Usuario no encontrado"


    if origen['id'] == destino ['id']:
        print "ERROR: No se puede realizar un trayecto entre dos aeropuertos iguales"
        return  False

    if len(ids_pasajeros) > avion['numeroAsientos']:
        print "ERROR: Limite de asientos alcanzado"
        return  False

    try:

        id_trayecto = object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'create', [{
                'name': name,
                'fecha_salida':fecha_salida,
                'fecha_llegada': fecha_llegada,
                'hora_salida': hSalida,
                'hora_llegada': hLlegada,

                'origen': origen['id'],
                'destino': destino['id'],
                'avion_id': avion['id'],

                'pasajeros': [(6, 0, ids_pasajeros)]
            }])

    except xmlrpclib.Fault:
        print "ERROR: La fecha de llegada no puede ser anterior a la de salida"
        return  False


    return True

def limpiarHistorial():
    opcion = ""
    dia_actual = time.strftime("%m/%d/%Y")
    idsVuelos = object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'search_read', [[['fecha_salida','<',dia_actual]]], {'fields': ['id']})
    if len(idsVuelos) == 0:
        print "No se han encontrado vuelos anteriores a hoy"
        return False
    for r in idsVuelos:
        id = r['id']
        mostrarInfoVuelo(id)

    while opcion != "s" and opcion != "n":
        opcion = raw_input("Los siguientes vuelos seran eliminados del historial. ¿Continuar? (s/n)")
        if opcion == "s":
            for r in idsVuelos:
                id = r['id']
                object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'unlink',[id])
        elif opcion == "n":
            pass
        else:
            print "Seleccione n/s" \

def mostrarInfoVuelo(id_vuelo):
    sc = object.execute_kw(dbname, uid, user_passwd, 'odoofly.trayecto', 'search_read',
                      [[['id', '=', id_vuelo]]])
    vuelo = sc[0]
    print '{:<30}  {:<30}  {:<30}  {:<30}  {:<30}  '.format( vuelo['name'].encode('utf-8'), vuelo['fecha_salida'].encode('utf-8'),
                                                                        vuelo['fecha_llegada'].encode('utf-8'),
                                                             (vuelo['origen'])[1],
                                                             (vuelo['destino'])[1])

if __name__ == '__main__':                          #Llamamos al main() para que comience la ejecucion
    main()
