BOOLEAN = 1
DO = 2
FUNCTION = 3
IF = 4
INPUT = 5
INT = 6
OUTPUT = 7
RETURN = 8
STRING = 9
VAR = 10
VOID = 11
WHILE = 12
AUTODECREMENTO = 13  # --
CONSTANTE_ENTERA = 14  # Valor
CADENA = 15  # Lexema
IDENTIFICADOR = 16  # posTS
IGUAL = 17  # =
COMA = 18  # ,
PUNTO_Y_COMA = 19  # ;
PAREN_ABRE = 20  # (
PAREN_CIERRA = 21  # )
LLAVE_ABRE = 22  # {
LLAVE_CIERRA = 23  # }
SUMA = 24  # +
NOT = 25  # !
MENOR_QUE = 26  # <
EOF = 27  # EOF

import sys


class Error:

    @staticmethod
    def lanzar_error(cod_error, linea, prev_token=None, curr_token=None, c=None):
        
        if str(cod_error).startswith('1'):
            # Muestra errores léxicos y sintácticos según el código de error
            if cod_error == 100:
                print(f"Error léxico en la línea: {linea}. Cadena no cerrada correctamente, falta '", file=sys.stderr)
            elif cod_error == 101:
                print(f"Error léxico en la línea: {linea}. No se permiten saltos de línea en las cadenas", file=sys.stderr)
            elif cod_error == 102:
                print(f"Error léxico en la línea: {linea}. El operador '-' no está permitido. A lo mejor querías decir '--'", file=sys.stderr)
            elif cod_error == 103:
                print(f"Error léxico en la línea: {linea}. El tamaño máximo de la cadena es de 64 caracteres", file=sys.stderr)
            elif cod_error == 104:
                print(f"Error léxico en la línea: {linea}. Has rebasado el tamaño máximo de entero (32767): {c} ", file=sys.stderr)
            elif cod_error == 105:
                print(f"Error léxico en la línea: {linea}. El comentario debe comenzar por /*", file=sys.stderr)
            elif cod_error == 106:
                print(f"Error léxico en la línea: {linea}. Carácter no admitido en la transición: '{c}'", file=sys.stderr)

        elif str(cod_error).startswith('3'):
            if(prev_token):
                prevTokenStr = obtenerEquivalencia(prev_token) if prev_token else ''
            if(curr_token):
                currTokenStr = obtenerEquivalencia(curr_token) if curr_token else ''
            
            # Errores sintácticos
            if cod_error == 300:
                print(f"Error sintáctico en la línea: {linea}. El programa no puede comenzar por '{currTokenStr}'", file=sys.stderr)
            elif cod_error == 302:
                print(f"Error sintáctico en la línea: {linea}. No puede ir '{currTokenStr}' aquí.", file=sys.stderr)
            elif cod_error == 303:
                print(f"Error sintáctico en la línea: {linea}. No se esperaba el token '{currTokenStr}' después de una sentencia.", file=sys.stderr)
            elif cod_error == 306:
                print(f"Error sintáctico en la línea: {linea}. Después de 'var' debe ir un identificador", file=sys.stderr)
            elif cod_error == 309:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir una '{{'", file=sys.stderr)
            elif cod_error == 310:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir un '=', '+' o '('", file=sys.stderr)
            elif cod_error == 312:
                print(f"Error sintáctico en la línea: {linea}. Después de 'input' debe ir un identificador", file=sys.stderr)
            elif cod_error == 313:
                print(f"Error sintáctico en la línea: {linea}. Después de 'return' debe ir una expresión o ';'", file=sys.stderr)
            elif cod_error == 316:
                print(f"Error sintáctico en la línea: {linea}. Después de 'function' debe ir un identificador", file=sys.stderr)
            elif cod_error == 320:
                print(f"Error sintáctico en la línea: {linea}. Después de un tipo debe ir un identificador", file=sys.stderr)
            elif cod_error == 322:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir una o más sentencias o '}}'", file=sys.stderr)
            elif cod_error == 325:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir un ')' o una lista de argumentos.", file=sys.stderr)
            elif cod_error == 326:
                print(f"Error sintáctico en la línea: {linea}. Se esperaba un ';' después de la expresión.", file=sys.stderr)
            elif cod_error == 329:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir un '(', una cadena, un entero o un identificador", file=sys.stderr)
            elif cod_error == 331:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir un '+', ',', ';', '<', '(' o ')'", file=sys.stderr)
            elif cod_error == 337:
                print(f"Error sintáctico en la línea: {linea}. Se esperaba un ';' después de la sentencia.", file=sys.stderr)
            elif cod_error == 339:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir 'int', 'boolean', 'string' o 'void'", file=sys.stderr)
            elif cod_error == 341:
                print(f"Error sintáctico en la línea: {linea}. Se esperaba un ')' o ',' después de '{prevTokenStr}'", file=sys.stderr)
            elif cod_error == 343:
                print(f"Error sintáctico en la línea: {linea}. Después de '{prevTokenStr}' debe ir un ';', '(' o un identificador", file=sys.stderr)
            else:
                print(f"Error sintáctico desconocido en la línea: {linea}.", file=sys.stderr)

        elif str(cod_error).startswith('3'):
            if(prev_token):
                prevTokenStr = obtenerEquivalencia(prev_token) if prev_token else ''
            if(curr_token):
                currTokenStr = obtenerEquivalencia(curr_token) if curr_token else ''
            print(f"Error en la línea: {linea}. Falla'{currTokenStr}' ", file=sys.stderr)
            print(f"Codigo de error: {cod_error}", file=sys.stderr)

        elif str(cod_error).startswith('5'): # ERRORES SEMANTICOS DE 500 PA ARRIBA
            if(prev_token):
                prevTokenStr = obtenerEquivalencia(prev_token) if prev_token else ''
            if(curr_token):
                currTokenStr = obtenerEquivalencia(curr_token) if curr_token else ''
            if cod_error ==500:
                print(f"Error semántico en la línea: {linea}. No se puede hacer un ‘return’ fuera de una función.", file=sys.stderr)
            if cod_error ==502:
                print(f"Error semántico en la línea: {linea}. M debe ser lambda o U y M deben ser enteros.", file=sys.stderr)
            if cod_error ==503:
                print(f"Error semántico en la línea: {linea}. M debe ser lambda o U y M deben ser enteros.", file=sys.stderr)
            if cod_error ==504:
                print(f"Error semántico en la línea: {linea}. U debe ser lambda o U y V deben ser enteros.", file=sys.stderr)
            if cod_error ==505:
                print(f"Error semántico en la línea: {linea}. U debe ser lambda o U y V deben ser enteros.", file=sys.stderr)
            if cod_error ==507:
                print(f"Error semántico en la línea: {linea}. Z debe ser lambda o coincidir con el tipo del identificador.", file=sys.stderr)
            if cod_error ==508:
                print(f"Error semántico en la línea: {linea}. Z debe ser una funcion.", file=sys.stderr)
            if cod_error ==509:
                print(f"Error semántico en la línea: {linea}. El numero de parametros de la función no coincide con el numero de parametros de la llamada.", file=sys.stderr)
            #El 10 y el 11 podrian estar mejor descritos
            if cod_error ==510:
                print(f"Error semántico en la línea: {linea}. El tipo del argumento de la lista de parámetros pasados no coincide con el tipo esperado definido en la declaración de la función.", file=sys.stderr)
            if cod_error ==511:
                print(f"Error semántico en la línea: {linea}. Se esperaba la llamada a una función.", file=sys.stderr)
            if cod_error ==512:
                print(f"Error semántico en la línea: {linea}. Después de una ! debe venir una variable lógica.", file=sys.stderr)
            if cod_error ==513:
                print(f"Error semántico en la línea: {linea}. En un if la condición de este (E) debe ser siempre una variable lógica.", file=sys.stderr)
            if cod_error ==514:
                print(f"Error semántico en la línea: {linea}. En un while la condición de este (E) debe ser siempre una variable lógica.", file=sys.stderr)
            if cod_error ==515:
                print(f"Error semántico en la línea: {linea}. La función no puede devolver dos tipos distintos.", file=sys.stderr)
            if cod_error ==516:
                print(f"Error semántico en la línea: {linea}. El output solo puede ser una cadena o un entero.", file=sys.stderr)
            if cod_error ==517:
                print(f"Error semántico en la línea: {linea}. El input solo puede ser una cadena o un entero.", file=sys.stderr)
            if cod_error ==518:
                print(f"Error semántico en la línea: {linea}. Después de un decremento debe aparecer un entero.", file=sys.stderr)
            if cod_error ==519:
                print(f"Error semántico en la línea: {linea}. El número de parámetros debe la función debe ser el mismo que el de la llamada.", file=sys.stderr)
            if cod_error ==520:
                print(f"Error semántico en la línea: {linea}. No coincide con el elemento de la TS.", file=sys.stderr) #este y el de debajo podrian escribirse mejor
            if cod_error ==521:
                print(f"Error semántico en la línea: {linea}. No hay el numero suficiente de elementos o no coinciden los tipos.", file=sys.stderr)
            if cod_error ==524:
                print(f"Error semántico en la línea: {linea}. Los tipos de C y H deben coincidir.", file=sys.stderr)
            if cod_error ==550:
                print(f"Error semántico en la línea: {linea}. Z debe ser una funcion.", file=sys.stderr)
            
            elif str(cod_error).startswith('7'):
                if(prev_token):
                    prevTokenStr = obtenerEquivalencia(prev_token) if prev_token else ''
                if(curr_token):
                    currTokenStr = obtenerEquivalencia(curr_token) if curr_token else ''
                print(f"Error en la línea: {linea}. Falla'{currTokenStr}' ", file=sys.stderr)
                print(f"Codigo de error: {cod_error}", file=sys.stderr)
           
            
        
            # no poner elif ahora o se j*d ehh

            if cod_error == 600:          # Esta en la clase lexico pero es del semántico NO BORRARRRRRRRRRRRRRR
                print(f"Error semántico en la línea: {linea}. No se puede declarar una variable dos veces dentro de un ámbito", file=sys.stderr)
            elif cod_error == 601:          # Esta en la clase lexico pero es del semántico NO BORRARRRRRRRRRRRRRR
                print(f"Error semántico en la línea: {linea}. Error al declarar una variable, comprueba el código (p.e. que no esté repetidad una variable)", file=sys.stderr)
            #else: No entiendo muy bien que se pretende con este else, lo unico que consigue es que salte en todos
             #   print(f"Error semántico en la línea: {linea}. Falla '{prevTokenStr}' o el bloque, compruebe el archivo fuente ", file=sys.stderr)
              #  print(f"Codigo de error: {cod_error}", file=sys.stderr)
        sys.exit(1)




# En el archivo Error.py o donde definas tus constantes y clases
def obtenerEquivalencia(token):
    token_equivalencias = {
        BOOLEAN: "boolean",
        DO: "do",
        FUNCTION: "function",
        IF: "if",
        INPUT: "input",
        INT: "int",
        OUTPUT: "output",
        RETURN: "return",
        STRING: "string",
        VAR: "var",
        VOID: "void",
        WHILE: "while",
        AUTODECREMENTO: "--",
        CONSTANTE_ENTERA: "constante entera",
        CADENA: "cadena",
        IDENTIFICADOR: "identificador",
        IGUAL: "=",
        COMA: ",",
        PUNTO_Y_COMA: ";",
        PAREN_ABRE: "(",
        PAREN_CIERRA: ")",
        LLAVE_ABRE: "{",
        LLAVE_CIERRA: "}",
        SUMA: "+",
        NOT: "!",
        MENOR_QUE: "<",
        EOF: "EOF",
    }
    code = token.get_codigo()
    if code in token_equivalencias:
        return token_equivalencias[code]
    else:
        return str(token.getValor())
