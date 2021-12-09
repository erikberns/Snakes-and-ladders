import random

CANTIDAD_CASILLEROS_BANANA = 5
CANTIDAD_CASILLEROS_MAGICO = 3
ESCALERAS_SERPIENTES = {3: 18, 6: 67, 57: 83, 72: 89, 85: 96, 86: 45, 88: 31, 98: 79, 63: 22,
    58: 37, 48: 12, 36: 17}

def menu()-> None:
    """ 
        Postcondicion: Muestra el menú en pantalla"""

    print ("\n1) Iniciar partida \n"
       "2) Mostrar estadísticas \n"
       "3) Resetear estadísticas \n"
       "4) Salir ")

def nombres()-> str: 
    """
        Precondicion: Pide el nombre del jugador

        Postcondicion: La función retorna ese nombre"""

    jugador_nom = input("\nIngrese nombre del jugador : ")
    
    return jugador_nom


def valor_dado()-> int: #Calculo en que número cae el dado
    """
        Precondicion: Calcula el valor de tipo int del dado (1 a 6) y 
        
        Postcondicion: Retorna ese valor
    """
    dado: int = random.randint(1,6)
    return dado


def crear_casilleros(banana: int, magico: int, rushero: int,
            hongos: int) -> int:
    
    """ Precondicion: banana, magico, rushero y hongos son variables de tipo int

        Postcondicion: Genera los casilleros al azar, y luego revisa si ese número se encuentra en las keys o values de ESCALERAS_SERPIENTES,
                       o si se encuentra ya ocupado por otro tweak, y si se cumple una de esas condiciones, genera otro número al azar hasta 
                       finalizar el ciclo while"""
    
    banana_list: list = []
    magico_list: list = []

    inicios = ESCALERAS_SERPIENTES.keys()
    finales = ESCALERAS_SERPIENTES.values()

    for i in range (CANTIDAD_CASILLEROS_BANANA):
        banana = random.choice(range(21,99))
        
        while (banana in inicios) or (banana in finales) or (banana in banana_list):
            banana = random.choice(range(21,99))
        banana_list.append(banana)

    for i in range (CANTIDAD_CASILLEROS_MAGICO):
        magico = random.choice(range(2,99))
        
        while (magico in inicios) or (magico in finales) or (magico in banana_list) or (magico in magico_list) :
            magico = random.choice(range(2,99))
        magico_list.append(magico)

    rushero = random.choice(range(1,99))
    
    while (rushero in inicios) or (rushero in finales) or (rushero in banana_list) or (rushero in magico_list) or ((rushero % 10) == 0):
        rushero = random.choice(range(1,99))

    hongos = random.choice(range(2,99))
    
    while (hongos in inicios) or (hongos in finales) or (hongos in banana_list) or (hongos in magico_list) or (hongos == rushero) or ((hongos % 10) == 1):
        hongos = random.choice(range(2,99))

    return banana_list, magico_list, rushero, hongos

def victoria(jugador_nom, pos)-> int: 
    """ Precondicion: llama a la variable pos de tipo int

        Postcondicion: si la variable pos es mayor o igual a 100, elije al jugador ganador y lo muestra en pantalla"""
    if pos >= 100:
        print(f"\n {jugador_nom}" + " ES EL GANADOR!! FELICIDADES")
        pos = 100


def juego (estadisticas: dict, jugador_nom: str, pos: int, banana: list, magico: list, rushero: int,
            hongos: int) -> int:

    """     Precondicion: llama a los diccionarios y a los int

            Postcondicion: chequea si la posición del jugador coincide con algún tweak, escalera o serpiente, y si es así devuelve un
            mensaje, con la función retornando la posición del jugador, y suma al contador de esadísticas en caso de caer en un
            casillero especial"""
    
    input_1:str = input(f"\n{jugador_nom} presione enter para tirar el dado: ")
    dado: int = valor_dado()
    print (f"\nA {jugador_nom} le salió {dado} en el dado: ")
    pos_anterior: int = pos
    pos = pos + dado
    if pos_anterior > 0:
        print(f"\n{jugador_nom} se movió desde {pos_anterior} a {pos}")

    inicios = ESCALERAS_SERPIENTES.keys()
    finales = ESCALERAS_SERPIENTES.values()
    
    if pos in ESCALERAS_SERPIENTES.keys(): 
        pos_final = ESCALERAS_SERPIENTES.get(pos)
        
        if pos_final > pos:
            escalera_cont = estadisticas.get("escalera", 0) 
            escalera_cont += 1
            estadisticas['escalera'] = escalera_cont
            print (f"Caíste en una escalera, tu nueva posición es {pos_final}")
            pos = pos_final

        else:
            serpiente_cont = estadisticas.get("serpiente", 0) 
            serpiente_cont += 1
            estadisticas['serpiente'] = serpiente_cont
            print (f"Caíste en una serpiente, tu nueva posición es {pos_final}")
            pos = pos_final


    if pos in banana:
        if not pos < 20:
            pos -= 20
            banana_cont = estadisticas.get("banana", 0) 
            banana_cont += 1
            estadisticas['banana'] = banana_cont
            print (f"Caíste en un casillero Cáscara de Banana, has retrocedido 20 casilleros hasta la posición {pos}")


    if pos in magico:
        pos = random.choice(range(2,99))
        magico_cont = estadisticas.get("magico", 0) 
        magico_cont += 1
        estadisticas['magico'] = magico_cont
        print (f"Caíste en un casillero Mágico, has sido transportado al casillero {pos}")


    if pos == rushero:
        resto = pos % 10
        avanzar_rushero = 10 - resto
        pos += avanzar_rushero  
        rushero_cont = estadisticas.get("rushero", 0)
        rushero_cont += 1
        estadisticas["rushero"] =  rushero_cont
        print (f"Caíste en un casillero Rushero, has sido transportado al casillero {pos}")


    if pos == hongos:
        resto = pos % 10
        pos = (pos-resto) + 1
        hongos_cont = estadisticas.get("hongos", 0)
        hongos_cont += 1
        estadisticas["hongos"] =  hongos_cont
        print (f"Caíste en un casillero de Hongos, has retrocedio al casillero {pos}")


    print (f"{jugador_nom} se encuentra en la posición {pos}")
  

    return pos
                            
def tablero(banana: list, magico: list, rushero: int, hongos: int )-> None:
    """ Precondicion: llama a los tweaks
        
        Postcondicion: devuelve una matriz (tablero) con los números reemplazados por un texto en caso
                       de que algun tweak u escalera/serpiente se halle en esa posición """

    tablero: list = []
    total: int = 100
    for i in range(10):
        tablero.append([])
        for j in range(total, total - 10, -1):
            tablero[i].append(j)
        total = total - 10
    for fila in range(1, 10, 2):
        fila_en_reversa = tablero[fila]
        fila_en_reversa.reverse()

    for fila in tablero:
        for num in range(len(fila)):

            
            if fila[num] in ESCALERAS_SERPIENTES:
                if fila[num] > ESCALERAS_SERPIENTES.get(fila[num]):
                    fila[num] = 'SERP'
                elif fila[num] < ESCALERAS_SERPIENTES.get(fila[num]):
                    fila[num] = 'ESC'
            elif fila[num] in banana:
                fila[num] = 'BAN'
            elif fila[num] in magico:
                fila[num] = 'MAG'
            elif fila[num] == rushero:
                fila[num] = 'RUSH'
            elif fila[num] == hongos:
                fila[num] = 'HON'
            

    return tablero

def printear_tablero(tablero: list) -> None: 
    """   Precondicion: la variable tablero contiene int

          Postcondidicon: mmuestra en pantalla al tablero actualizado con sus tweaks y escaleras/serpientes"""
    
    for fila in tablero:
        for casillero in fila:
            print(casillero, end="\t")
        
        print(end='\n')


def estadisticas_totales(estadisticas: dict) -> dict:
    """     Precondicion: estadisticas es un diccionario que contiene los tweaks y la cantidad de veces que cayeron en ellos
        
            Postcondicion: llama a los values de cada key y los muestra e pantalla"""

    print("\nVeces que cayeron en casilleros Serpiente: ", estadisticas.get('serpiente'))
    print("Veces que cayeron en casilleros Escalera: ", estadisticas.get('escalera'))
    print("Veces que cayeron en casilleros Cascara de banana: ", estadisticas.get('banana'))
    print("Veces que cayeron en casilleros Magico: ", estadisticas.get('magico'))
    print("Veces que cayeron en casilleros Rushero: ", estadisticas.get('rushero'))
    print("Veces que cayeron en casilleros Hongos Locos: ", estadisticas.get('hongos'))

def resetear_en_0_estadisticas_totales(estadisticas: dict) -> dict:

    """     Precondicion: Llama al diccionario estadísticas
        
            Postcondicion: resetea en 0 todos los values del diccionario"""
    estadisticas['serpiente'] = 0
    estadisticas['escalera'] = 0
    estadisticas['banana'] = 0
    estadisticas['magico'] = 0
    estadisticas['rushero'] = 0
    estadisticas['hongos'] = 0
    print ("\nHas reseteado las estadísticas correctamente")

def turno_jugador (estadisticas: dict, jugador_nom: str, pos: int, banana: list, magico: list, rushero: int,
            hongos: int) -> int:

    """     Precondicion: Llama al diccionario estadísticas, junto con las demás variables
        
            Postcondicion: Calcula la posición del jugador, chequea si es igual/mayor a 100 con la función victoria
                       para terminar retornando la posición"""
                

    pos = juego (estadisticas, jugador_nom, pos, banana, magico, rushero, hongos)
    victoria (jugador_nom, pos)

    print ("\n")

    return pos


def main() -> None:
    menu()
    opcion: int = int(input("Ingrese el número según lo que desee hacer: "))
    estadisticas: dict = {'serpiente': 0, 'escalera': 0, 'banana': 0, 'magico': 0, 'rushero': 0, 'hongos': 0}
    banana_main: list = []
    magico_main: list = []
    rushero_main: int = 0
    hongos_main: int = 0
    banana = crear_casilleros(banana_main, magico_main, rushero_main, hongos_main)[0]
    magico = crear_casilleros(banana_main, magico_main, rushero_main, hongos_main)[1]
    rushero = crear_casilleros(banana_main, magico_main, rushero_main, hongos_main)[2]
    hongos = crear_casilleros(banana_main, magico_main, rushero_main, hongos_main)[3]
    pos: int = 0
    while opcion != 0: #Condición para poder cerrar el menú en la opción 4

        if opcion == 1:
            jugador_1_nom = nombres()
            jugador_2_nom = nombres()
            pos_1 = 0
            pos_2 = 0
            turno: int = random.randint (1,2) #Elije un jugador al azar para que empiece la partida

            if turno == 1:
                
                print (f"\nComienza el jugador {jugador_1_nom}")
                
                while pos_1 < 100 and pos_2 < 100:
                    tablero_total = tablero(banana, magico, rushero, hongos)
                    printear_tablero(tablero_total)

                    pos_1 = turno_jugador(estadisticas, jugador_1_nom, pos_1, banana, magico, rushero, hongos)

                    pos_2 = turno_jugador(estadisticas, jugador_2_nom, pos_2, banana, magico, rushero, hongos)

            else:
                print (f"\nComienza el jugador {jugador_2_nom}")

                while pos_1 < 100 and pos_2 < 100:
                    tablero_total = tablero(banana, magico, rushero, hongos)
                    printear_tablero(tablero_total)
                
                    pos_2 = turno_jugador(estadisticas, jugador_2_nom, pos_2, banana, magico, rushero, hongos)

                    pos_1 = turno_jugador(estadisticas, jugador_1_nom, pos_1, banana, magico, rushero, hongos)


            menu()
            opcion: int = int(input("\nIngrese el número según lo que quiera hacer: "))
        
        elif opcion == 2:

            estadisticas_totales(estadisticas)
            menu()
            opcion: int = int(input("\nIngrese el número según lo que quiera hacer: "))

        elif opcion == 3:
            
            resetear_en_0_estadisticas_totales(estadisticas)
            menu()
            opcion: int = int(input("\nIngrese el número según lo que quiera hacer: "))

        elif opcion == 4:
            print ("\nGracias por jugar!\n")
            opcion = 0


main()