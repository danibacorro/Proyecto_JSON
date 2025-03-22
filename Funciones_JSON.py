import json

def cargar_datos():
    with open("Gasto en publicidad institucional Junta de Andalucia.json", "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def menu():
    datos = cargar_datos()
    activo = True
    while activo:
        print("\n", "*"*25)
        print('''¿Qué quieres hacer?:\n 
1. Mostrar información de los contratos de "Empresa Pública para la Gestión del Turismo y del Deporte de Andalucía, S.A."
2. Contar los contratos de un año por cuatrimestres.
3. Buscar organismos con contratos superiores a un valor.
4. Filtrar contratos por año.
5. Mostrar información de los contratos subvencionados.
6. Salir.''')
        try:
            opcion = int(input("\n: "))
        
            if opcion == 1:
                mostrar_info(datos)
            elif opcion == 2:
                año = int(input("\nIngrese el año: "))
                contar_contratos(datos, año)
            elif opcion == 3:
                try:
                    valor = float(input("\nIngrese el valor mínimo del contrato(€): "))
                    if valor < 0:
                        print("\nEl valor ha de ser positivo.")
                    else:    
                        buscar_por_valor(datos, valor)
                except ValueError:
                    print("\nSe ha producido un error, debes introducir un número entero.")
            elif opcion == 4:
                try:
                    año = int(input("\nIngrese el año: "))
                    if año <= 2013 or año >= 2025:
                        print("\nNo se han encontrado contratos.")
                    else:
                        filtrar_por_año(datos, año)
                except ValueError:
                    print("\nSe ha producido un error, debes introducir un número entero.")
            elif opcion == 5:
                subvencionados(datos)
            elif opcion == 6:
                print("\nSaliendo del programa...\n¡Hasta pronto!\n")
                activo = False
            else:
                print("\nOpción no válida. Intente nuevamente.")
        except ValueError:
            print("\nOpción no válida. Intente nuevamente.")

def mostrar_info(datos):
    print("\nID\t Año\t Cuatrimestre")
    print("-"*38)
    for contrato in datos:
        for organismo in contrato.get("organism", []):
            if organismo.get("organism") == "Empresa Pública para la Gestión del Turismo y del Deporte de Andalucía, S.A.":
                for periodo in contrato.get("period", []):
                    print(contrato['id'], "\t", periodo['year'], "\t", periodo['quarter'])

def contar_contratos(datos, año):
    cuatrimestres = {"Primer cuatrimestre": 0, "Segundo cuatrimestre": 0, "Tercer cuatrimestre": 0}
    print("\n"+ str(año) + ":\n")
    print("Cuatrimestre\t\tContratos")
    print("-"*34)
    for contrato in datos:
        for periodo in contrato.get("period", []):
            if int(periodo.get("year")) == año:
                cuatrimestres[periodo["quarter"]] += 1
    for cuatrimestre, cantidad in cuatrimestres.items():
        print(cuatrimestre, "\t   ", str(cantidad))

def buscar_por_valor(datos, valor):
    listado = set()
    print("\033[4;37m"+"\nOrganismo/s con contratos superiores al valor indicado:\n"+"\033[0;37m")
    for contrato in datos:
        for nombre in contrato.get("contract", []):
            if nombre.get("contract_amount") and float(nombre["contract_amount"]) > valor:
                for organismo in contrato.get("organism", []):
                    listado.add(organismo['organism'])
    if listado:
        for organismo in listado:
            print(organismo)
            print("-"*80)
    else:
        print("No se han encontrado organismos con contratos de valor superior al indicado.")

def filtrar_por_año(datos, año):
    print("\nLos datos se mostrarán en el siguiente orden:\nID - Empresa - Contrato")
    for contrato in datos:
        for periodo in contrato.get("period", []):
            if int(periodo.get("year")) == año:
                for contrato_info in contrato.get("contract", []):
                    print("\n", "\033[33m"+contrato['id']+"\033[37m", " - ", contrato_info.get('contract_purchaser') or 'Sin especificar', " - ", contrato_info.get('contract_name') or 'Sin especificar')

def subvencionados(datos):
    total = 0
    print("\nA continuación se van a listar los contratos subvencionados con el siguiente formato:\nID:\nContrato:\nBeneficiario:")
    for contrato in datos:
        for grant in contrato.get("grant", []):
            if grant.get("grant_name") and grant.get("grant_beneficiary"):
                print("\n", "\033[33m"+contrato['id']+"\033[37m", "\n", grant['grant_name'], "\n", grant['grant_beneficiary'])
                total +=1
    print("\n", "\033[4;37m"+"Total de contratos subvencionados:"+"\033[0;37m", total)