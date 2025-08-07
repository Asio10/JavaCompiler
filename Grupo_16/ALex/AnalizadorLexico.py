from Error.Error import Error
from ALex.Token import Token
from TS.TablaSimbolos import TablaSimbolos
from ASin.AnalizadorSintactico import AnalizadorSintactico

class AnalizadorLexico:
    def __init__(self, contenido, tsg):
        self.contenido = contenido
        self.posicion_actual = 0  # Usamos una posición para ir leyendo el string
        self.linea = 1
        self.c = self.leer_caracter()
        self.palabras_reservadas = self.generar_tabla_palabras_reservadas()
        self.matriz_transiciones = self.generar_matriz_transiciones()
        self.tsg = tsg
        self.tsl = None
        self.zonaDecl = False
        self.tablaActivaTSG = True
        self.aSin = None

    def set_aSin(self, aSin): # Analizador Sintáctico, para cuando declaramos implicitamente, guardar el despG
        self.aSin = aSin

    def set_zona_decl(self, boleano: bool):
        """Asigna el valor de zonaDecl."""
        self.zonaDecl = boleano

    def set_es_tsg(self, n: bool):
        """Asigna el valor de tablaActivaTSG."""
        self.tablaActivaTSG = n

    def set_tsl(self, tsl):
        """Asigna la tabla de símbolos local (TSL)."""
        self.tsl = tsl

    def decl_implicita(self, cadena):
        entrada_tabla = self.tsg.check_tabla(cadena)
        if (entrada_tabla is None):  # Se añade
            entrada_tabla = self.tsg.añadir_entrada(cadena)
            self.tsg.añadir_tipo(entrada_tabla, "integer")
            self.tsg.añadir_despl(entrada_tabla, self.aSin.desplG)
            self.aSin.desplG += 1
        return entrada_tabla        

    def leer_caracter(self):
        if self.posicion_actual < len(self.contenido):
            caracter = self.contenido[self.posicion_actual]
            self.posicion_actual += 1
            return caracter
        else:
            return ''  # Si hemos leído todo el contenido, devolvemos una cadena vacía

    def generar_tabla_palabras_reservadas(self):
        """Genera la tabla de palabras reservadas."""
        palabras_reservadas = {
            "boolean": 1, "do": 2, "function": 3, "if": 4,
            "input": 5, "int": 6, "output": 7, "return": 8, "string": 9,
            "var": 10, "void": 11, "while": 12
        }
        return palabras_reservadas

    def generar_matriz_transiciones(self):
        """Genera la matriz de transiciones del autómata."""
        matriz = {}
        # Estado 0
        matriz[(0, '\n')] = (0, "H")
        matriz[(0, ' ')] = (0, "H")
        matriz[(0, '\t')] = (0, "H")
        matriz[(0, '-')] = (1, "G1")
        matriz[(0, "d")] = (2, "D1")    # Dígito
        matriz[(0, 'i')] = (3, "I1")    # Identificador
        matriz[(0, '"')] = (4, "C1")
        matriz[(0, '/')] = (5, "H")
        matriz[(0, '=')] = (6, "A6")
        matriz[(0, ',')] = (7, "A7")
        matriz[(0, ';')] = (8, "A8")
        matriz[(0, '(')] = (9, "A9")
        matriz[(0, ')')] = (10, "A10")
        matriz[(0, '{')] = (11, "A11")
        matriz[(0, '}')] = (12, "A12")
        matriz[(0, '+')] = (13, "A13")
        matriz[(0, '!')] = (14, "A14")
        matriz[(0, '<')] = (15, "A15")
        matriz[(0, 'eof')] = (16, "A16")

        # ESTADO 1: Autodecremento: --
        matriz[(1, '-')] = (2, "G2")

        # ESTADO 2 : Numeros enteros
        matriz[(2, 'd')] = (2, "D2")    # Es digito
        matriz[(2, 'o')] = (18, "D3")    # Es o.c

		# ESTADO 3: Identificador
        matriz[(3, 'i')] = (3,"C2")
        matriz[(3, 'o')] = (19,"I3")    # Es o.c

		# ESTADO 4: Cadema
        matriz[(4, 'c')] = (4, "C2")    # Cualquier char
        matriz[(4, '"')] = (20, "C3")

		# ESTADO 5: Comentario
        matriz[(5, '*')] = (21, "H")

        # ESTADO 21: Comentario
        matriz[(21, 'c')] = (21, "H")
        matriz[(21, '*')] = (22, "H")

		# ESTADO 22: Comentario
        matriz[(22, '/')] = (0, "H")
        matriz[(22, 'o')] = (21, "H")
        matriz[(22, '*')] = (22, "H")

        return matriz

    def obtener_token(self):
        """Genera un token siguiendo el autómata."""
        estado = 0
        cadena = ""
        numero = 0
        while True:
            # Verificar errores específicos antes de buscar una transición (para que no salte el 106 primero)
            if estado == 4 and self.c == '':  # Cadena no cerrada
                Error.lanzar_error(100, linea=self.linea, c=self.c)
                return
            if estado == 4 and self.c == '\n':  # Salto de línea en cadena
                Error.lanzar_error(101, linea=self.linea, c=self.c)
                return
            if estado == 5 and self.c != '*':  # Comentario no cerrado
                Error.lanzar_error(105, linea=self.linea,c=self.c)
                return
            if estado == 1 and self.c != '-':  # Operador no válido
                Error.lanzar_error(102, linea=self.linea, c=self.c)
                return

            transicion = AnalizadorLexico.get_futura_accion(self, estado)

            if transicion is None:
                Error.lanzar_error(106, linea=self.linea, c=self.c)
                return
            
            estado, accion = transicion
            if accion:
                if accion.startswith('A'):  # Acciones asociadas a operadores y símbolos (TOKENS SIMPLES)
                    if accion == "A6":
                        self.c = self.leer_caracter()
                        return Token(17,linea = self.linea)  # '='
                    elif accion == "A7":
                        self.c = self.leer_caracter()
                        return Token(18, linea = self.linea)  # ','
                    elif accion == "A8":
                        self.c = self.leer_caracter()
                        return Token(19, linea = self.linea)  # ';'
                    elif accion == "A9":
                        self.c = self.leer_caracter()
                        return Token(20, linea = self.linea)  # '('
                    elif accion == "A10":
                        self.c = self.leer_caracter()
                        return Token(21, linea = self.linea)  # ')'
                    elif accion == "A11":
                        self.c = self.leer_caracter()
                        return Token(22, linea = self.linea)  # '{'
                    elif accion == "A12":
                        self.c = self.leer_caracter()
                        return Token(23, linea = self.linea)  # '}'
                    elif accion == "A13":
                        self.c = self.leer_caracter()
                        return Token(24, linea = self.linea)  # '+'
                    elif accion == "A14":
                        self.c = self.leer_caracter()
                        return Token(25, linea = self.linea)  # '!'
                    elif accion == "A15":
                        self.c = self.leer_caracter()
                        return Token(26, linea = self.linea)  # '<'
                    elif accion == "A16":
                        self.c = self.leer_caracter()
                        return Token(27, linea = self.linea)  # 'EOF'
                    
                elif accion.startswith('C'):  # Acciones asociadas a cadenas
                    if accion == "C1":
                        self.c = self.leer_caracter()  # Ignora comillas
                    elif accion == "C2":
                        cadena += self.c
                        self.c = self.leer_caracter()
                    elif accion == "C3":  # Fin de cadena
                        if len(cadena) > 64:
                            Error.lanzar_error(103, linea = self.linea, c = cadena)
                            return
                        self.c = self.leer_caracter()
                        return Token(15, cadena, linea = self.linea)
                    
                elif accion.startswith('D'):  # Acciones asociadas a enteros
                    if accion == "D1":
                        numero = int(self.c)
                        self.c = self.leer_caracter()
                    elif accion == "D2":
                        numero = numero * 10 + int(self.c)
                        self.c = self.leer_caracter()
                    elif accion == "D3":    # Fin de número
                        if int(numero) > 32767:
                            Error.lanzar_error(104, linea=self.linea, c=numero)
                            return
                        return Token(14, None ,int(numero), linea = self.linea)
                    
                elif accion.startswith('G'):  # Acciones para operadores +=
                    if accion == "G1":
                        self.c = self.leer_caracter()
                    elif accion == "G2":
                        self.c = self.leer_caracter()
                        return Token(13, linea = self.linea)    # '--'
                    
                elif accion == "H":         # Ignora comentarios y espacios
                    if self.c == '\n':
                        self.linea += 1
                    self.c = self.leer_caracter()

                elif accion.startswith('I'):  # Identificadores y palabras reservadas
                    if accion == "I1":
                        cadena = self.c
                        self.c = self.leer_caracter()
                    elif accion == "I3":
                        if cadena in self.palabras_reservadas:
                            return Token(self.palabras_reservadas[cadena], linea = self.linea)  # Palabra reservada
                        else:
                            entrada_tabla = None
                            if self.tablaActivaTSG:
                                entrada_tabla = self.tsg.check_tabla(cadena)
                                
                                if self.zonaDecl:
                                    if entrada_tabla is None:
                                        entrada_tabla = self.tsg.añadir_entrada(cadena)
                                    elif entrada_tabla is not None:
                                        Error.lanzar_error(600, linea=self.linea, c=numero)
                                    
                                elif not self.zonaDecl:
                                    if entrada_tabla is None:
                                        entrada_tabla = self.decl_implicita(cadena)
                                    if entrada_tabla is not None:
                                        pass        # No hace falta hacer nada porque ya está
                                
                            else:
                                entrada_tabla = self.tsl.check_tabla(cadena)

                                if self.zonaDecl:
                                    if entrada_tabla is None:
                                        entrada_tabla = self.tsl.añadir_entrada(cadena)
                                    elif entrada_tabla is not None:
                                        Error.lanzar_error(600, linea=self.linea, c=numero)
                                    
                                elif not self.zonaDecl:
                                    if entrada_tabla is None:
                                        entrada_tabla = self.tsg.check_tabla(cadena)
                                        if entrada_tabla is None:
                                            entrada_tabla = self.decl_implicita(cadena)
                                    elif entrada_tabla is not None:
                                        pass    # No hace falta hacer nada ya está, lo pongo para aclararme
                                
                            if entrada_tabla is None:
                                Error.lanzar_error(601, linea=self.linea, c=cadena)

                            return Token(16, pos= entrada_tabla, linea=self.linea)
                    

    def get_futura_accion(self, estado):
        """ Devuelve la futura acción o error basado en el estado y el carácter actual."""
        # EOF (Fin de archivo)
        if self.c == '':
            return self.matriz_transiciones.get((estado, 'eof'), None)

        # Evaluamos los casos de los diferentes estados
        if estado == 0:
            # Comienzo de un número (dígito)
            if self.c == -1:
                return self.matriz_transiciones.get((estado, 'eof'), None)
            if self.c.isdigit():
                return self.matriz_transiciones.get((estado, 'd'), None)
            # Comienzo de identificador o palabra reservada (letra o subrayado)
            if self.c.isalpha():
                return self.matriz_transiciones.get((estado, 'i'), None)
            # Símbolos simples ; , = ... 
            else:
                return self.matriz_transiciones.get((estado, self.c), None)
            
        elif estado == 1:
            # Error si + no es seguido de un =
            if self.c != '-':
                Error.lanzar_error(102, linea=self.linea, c=self.c)
            # Si el siguiente carácter es -
            else:
                return self.matriz_transiciones.get((estado, self.c), None)

        elif estado == 2:
            # Bucle para dígitos (números enteros)
            if self.c.isdigit():
                return self.matriz_transiciones.get((estado, 'd'), None)
            # Caracter que no es dígito (otro carácter)
            if not self.c.isdigit():
                return self.matriz_transiciones.get((estado, 'o'), None)
            
        elif estado == 3:
            # Bucle para identificador (letras, dígitos o subrayado)
            if self.c.isdigit() or self.c.isalpha() or self.c == '_':
                return self.matriz_transiciones.get((estado, 'i'), None)
            # Otro carácter (O.C)
            else:
                return self.matriz_transiciones.get((estado, 'o'), None)

        elif estado == 4:
            # Error, si no se cierra la cadena correctamente
            if self.c == '':
                Error.lanzar_error(100, linea=self.linea, c=self.c)
            # Salto de línea en cadena, error
            if self.c == '\n':
                Error.lanzar_error(101, linea=self.linea, c=self.c)
            # Bucle para cadena de caracteres (cualquier cosa menos comilla)
            if self.c != '"':
                return self.matriz_transiciones.get((estado, 'c'), None)
            # Fin de cadena, es comilla
            else:
                # Solo podrían ser comillas
                return self.matriz_transiciones.get((estado, self.c), None)


        elif estado == 5:
            # Error si no hay * en el comentario
            if self.c != '*':
                Error.lanzar_error(105, linea=self.linea, c=self.c)
            # Si es *
            else:
                return self.matriz_transiciones.get((estado, self.c), None)

        elif estado == 21:
            # Si es salto de línea
            if self.c != '*':
                return self.matriz_transiciones.get((estado, 'c'), None)
            else:
                return self.matriz_transiciones.get((estado, self.c), None)
            
        elif estado == 22:
            if self.c == '*':
                return self.matriz_transiciones.get((estado, '*'), None)
            if self.c != '/':
                return self.matriz_transiciones.get((estado, 'o'), None)
            else:
                return self.matriz_transiciones.get((estado, self.c), None)    

        return None
        

    def decl_implicita(self, cadena):
        entrada_tabla = self.tsg.check_tabla(cadena)
        if (entrada_tabla is None):  # Se añade
            entrada_tabla = self.tsg.añadir_entrada(cadena)
            self.tsg.añadir_tipo(entrada_tabla, "integer")
            self.tsg.añadir_despl(entrada_tabla, self.aSin.desplG)
            self.aSin.desplG += 1
        return entrada_tabla        