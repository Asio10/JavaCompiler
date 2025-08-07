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

from Error.Error import Error
from ALex.Token import Token
from ASin.EntradaPila import EntradaPila 
from TS.TablaSimbolos import TablaSimbolos
from typing import TYPE_CHECKING    # Para que no haya dependencias circulares al llamar a Asin
if TYPE_CHECKING:
    from ALex.AnalizadorLexico import AnalizadorLexico


class AnalizadorSintactico:
    def __init__(self, tsg, aLex, tablas):
        self.pila = []
        self.code = None
        self.token = None
        self.prev_token = None  # Para mantener el token anterior

        # Inicialización de la pila de análisis sintáctico
        self.pila.append(EntradaPila(token=EOF))
        self.pila.append(EntradaPila(no_terminal="P"))
        self.aux_pila = []  # Se utiliza para almacenar entradas semánticas
        self.accepted = False
        self.error = False
        self.parse = ""  # Cadena para almacenar los números de producción aplicados
        self.tsg = tsg
        self.tsl = None
        self.aLex = aLex
        self.idTS = 1       # La 0 es la TSG
        self.tablaActivaTSG = True
        self.desplG = 0
        self.desplL = 0
        self.tablas = tablas


    def process_token(self, token):
        """Procesa un token y actualiza el estado del analizador sintáctico."""
        self.prev_token = self.token  # Actualizar el token anterior
        self.token = token
        self.code = self.token.get_codigo()
        parse_steps = ""

        while True:
            if not self.pila:
                # Si la pila está vacía y hemos aceptado, terminamos
                if self.accepted:
                    return parse_steps.strip()
                else:
                    # Error: pila vacía antes de aceptar
                    Error.lanzar_error(300, self.token.getLinea(), self.prev_token, self.token)
                    self.error = True
                    return parse_steps.strip()

            entrada = self.pila.pop()

            if entrada.get_token() is not None:  # Terminal
                if entrada.get_token()  == self.code:
                    # Coincide el terminal, avanzamos al siguiente token
                    self.aux_pila.append(EntradaPila(token = self.code, tk=self.token))  # Pasar a AUX
                    if entrada.get_token() == EOF:
                        # Si el token es EOF y coincide con EOF en la pila, aceptamos
                        self.accepted = True
                    return parse_steps.strip()
                else:
                    # Error sintáctico
                    Error.lanzar_error(302, self.token.getLinea(), self.prev_token, self.token)
                    self.error = True
                    return parse_steps.strip()
                
            elif entrada.get_regla() is not None:  # Acción semántica
                regla_str = entrada.get_regla()
                nueva_entrada = self.ejecutar_sem(regla_str, self.aux_pila)
                if nueva_entrada is not None:
                    self.aux_pila.append(nueva_entrada)

            elif entrada.get_no_terminal() is not None:  # No terminal
                nt = entrada.get_no_terminal()
                produccion = self.aplicar_produccion(nt)
                if self.error:
                    return parse_steps.strip()
                if produccion:
                    parse_steps += produccion + " "
            else:
                Error.lanzar_error(302, self.token.getLinea(), self.prev_token, self.token)
                self.error = True
                return parse_steps.strip()


    def aplicar_produccion(self, estado):
        if estado == "P":
            return self.CasoP()
        elif estado == "B":
            return self.CasoB()
        elif estado == "C":
            return self.CasoC()
        elif estado == "S":
            return self.CasoS()
        elif estado == "E":
            return self.CasoE()
        elif estado == "M":
            return self.CasoM()
        elif estado == "U":
            return self.CasoU()
        elif estado == "U1":
            return self.CasoU1()
        elif estado == "V":
            return self.CasoV()
        elif estado == "Z":
            return self.CasoZ()
        elif estado == "T":
            return self.CasoT()
        elif estado == "F":
            return self.CasoF()
        elif estado == "H":
            return self.CasoH()
        elif estado == "A":
            return self.CasoA()
        elif estado == "K":
            return self.CasoK()
        elif estado == "L":
            return self.CasoL()
        elif estado == "Q":
            return self.CasoQ()
        elif estado == "I":
            return self.CasoI()
        elif estado == "X":
            return self.CasoX()
        else:
            Error.lanzar_error(302, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""


    def CasoP(self):
        if self.code == EOF:
            self.pila.append(EntradaPila(token=EOF))
            return "3"  # P -> eof
        elif self.code == FUNCTION:
            self.pila.append(EntradaPila(no_terminal="P"))
            self.pila.append(EntradaPila(no_terminal="F"))
            return "2"  # P -> F P
        elif self.code in [IF, DO, VAR, OUTPUT, INPUT, RETURN, IDENTIFICADOR]:
            self.pila.append(EntradaPila(regla="1.1"))  
            self.pila.append(EntradaPila(no_terminal="P"))
            self.pila.append(EntradaPila(no_terminal="B"))
            return "1"  # P -> B P
        else:
            Error.lanzar_error(300, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""

    def CasoT(self):
        if self.code == INT:
            self.pila.append(EntradaPila(regla="4.1"))
            self.pila.append(EntradaPila(token=INT))
            return "4"  # T -> int
        elif self.code == BOOLEAN:
            self.pila.append(EntradaPila(regla="5.1"))
            self.pila.append(EntradaPila(token=BOOLEAN))
            return "5"  # T -> boolean
        elif self.code == STRING:
            self.pila.append(EntradaPila(regla="6.1"))
            self.pila.append(EntradaPila(token=STRING))
            return "6"  # T -> string
        else:
            Error.lanzar_error(339, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""

    def CasoE(self):
        if self.code in [PAREN_ABRE, CONSTANTE_ENTERA, CADENA, IDENTIFICADOR, NOT]:
            self.pila.append(EntradaPila(regla="7.1"))
            self.pila.append(EntradaPila(no_terminal="M"))
            self.pila.append(EntradaPila(no_terminal="U"))
            return "7"  # E -> U M
        else:
            Error.lanzar_error(329, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""
        

    def CasoM(self):
        if self.code == MENOR_QUE:
            self.pila.append(EntradaPila(regla="8.1"))
            self.pila.append(EntradaPila(no_terminal="M"))
            self.pila.append(EntradaPila(no_terminal="U"))
            self.pila.append(EntradaPila(token=MENOR_QUE))
            return "8"  # M -> < U M
        else:
            self.pila.append(EntradaPila(regla="9.1"))
            return "9"  # M -> Lambda

    def CasoU(self):
        if self.code in [PAREN_ABRE, CONSTANTE_ENTERA, CADENA, IDENTIFICADOR, NOT]:
            self.pila.append(EntradaPila(regla="10.1"))
            self.pila.append(EntradaPila(no_terminal="U1"))
            self.pila.append(EntradaPila(no_terminal="V"))
            return "10"  # U -> V U1
        else:
            Error.lanzar_error(329, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""

    def CasoU1(self):
        if self.code == SUMA:
            self.pila.append(EntradaPila(regla="11.1"))
            self.pila.append(EntradaPila(no_terminal="U1"))
            self.pila.append(EntradaPila(no_terminal="V"))
            self.pila.append(EntradaPila(token=SUMA))
            return "11"  # U1 -> + V U1
        else:
            self.pila.append(EntradaPila(regla="12.2"))
            return "12"  # U1 -> Lambda

    def CasoV(self):
        if self.code == PAREN_ABRE:
            self.pila.append(EntradaPila(regla="13.1"))
            self.pila.append(EntradaPila(token=PAREN_CIERRA))
            self.pila.append(EntradaPila(no_terminal="E"))
            self.pila.append(EntradaPila(token=PAREN_ABRE))
            return "13"  # V -> ( E )
        elif self.code == CONSTANTE_ENTERA:
            self.pila.append(EntradaPila(regla="14.1"))
            self.pila.append(EntradaPila(token=CONSTANTE_ENTERA))
            return "14"  # V -> ent
        elif self.code == CADENA:
            self.pila.append(EntradaPila(regla="15.1"))
            self.pila.append(EntradaPila(token=CADENA))
            return "15"  # V -> cad
        elif self.code == IDENTIFICADOR:
            self.pila.append(EntradaPila(regla="16.1"))
            self.pila.append(EntradaPila(no_terminal="Z"))
            self.pila.append(EntradaPila(token=IDENTIFICADOR))
            return "16"  # V -> id Z
        elif self.code == NOT:
            self.pila.append(EntradaPila(regla="17.1"))
            self.pila.append(EntradaPila(no_terminal="E"))
            self.pila.append(EntradaPila(token=NOT))
            return "17"  # V -> ! E
        else:
            Error.lanzar_error(329, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""

    def CasoZ(self):
        if self.code == AUTODECREMENTO:
            self.pila.append(EntradaPila(regla="18.1"))
            self.pila.append(EntradaPila(token=AUTODECREMENTO))
            return "18"  # Z -> --
        elif self.code == PAREN_ABRE:
            self.pila.append(EntradaPila(regla="19.1"))
            self.pila.append(EntradaPila(token=PAREN_CIERRA))
            self.pila.append(EntradaPila(no_terminal="L"))
            self.pila.append(EntradaPila(token=PAREN_ABRE))
            return "19"  # Z -> ( L )
        else:
            self.pila.append(EntradaPila(regla="20.1"))
            return "20"  # Z -> Lambda


    def CasoB(self):
        if self.code == IF:
            self.pila.append(EntradaPila(regla="22.2"))
            self.pila.append(EntradaPila(no_terminal="S"))
            self.pila.append(EntradaPila(token=PAREN_CIERRA))
            self.pila.append(EntradaPila(regla="22.1"))
            self.pila.append(EntradaPila(no_terminal="E"))
            self.pila.append(EntradaPila(token=PAREN_ABRE))
            self.pila.append(EntradaPila(token=IF))
            return "22"  # B -> if ( E ) S
        elif self.code == DO:
            self.pila.append(EntradaPila(regla="23.1"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(token=PAREN_CIERRA))
            self.pila.append(EntradaPila(no_terminal="E"))
            self.pila.append(EntradaPila(token=PAREN_ABRE))
            self.pila.append(EntradaPila(token=WHILE))
            self.pila.append(EntradaPila(token=LLAVE_CIERRA))
            self.pila.append(EntradaPila(no_terminal="C"))
            self.pila.append(EntradaPila(token=LLAVE_ABRE))
            self.pila.append(EntradaPila(token=DO))
            return "23"  # B -> do { C } while ( E ) ;
        elif self.code == VAR:
            self.pila.append(EntradaPila(regla="24.3"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(regla="24.2"))
            self.pila.append(EntradaPila(token=IDENTIFICADOR))
            self.pila.append(EntradaPila(no_terminal="T"))
            self.pila.append(EntradaPila(regla="24.1"))
            self.pila.append(EntradaPila(token=VAR))
            return "24"  # B -> var T id ;
        elif self.code in [OUTPUT, INPUT, RETURN, IDENTIFICADOR]:
            self.pila.append(EntradaPila(regla="21.1"))
            self.pila.append(EntradaPila(no_terminal="S"))
            return "21"  # B -> S
        else:
            Error.lanzar_error(302, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""


    def CasoC(self):
        if self.code in [IF, DO, VAR, OUTPUT, INPUT, RETURN, IDENTIFICADOR]:
            self.pila.append(EntradaPila(regla="25.1"))
            self.pila.append(EntradaPila(no_terminal="C"))
            self.pila.append(EntradaPila(no_terminal="B"))
            return "25"  # C -> B C
        else:
            self.pila.append(EntradaPila(regla="26.1"))
            return "26"  # C -> Lambda

    def CasoS(self):
        if self.code == OUTPUT:
            self.pila.append(EntradaPila(regla="27.1"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(no_terminal="E"))
            self.pila.append(EntradaPila(token=OUTPUT))
            return "27"  # S -> output E ;
        elif self.code == INPUT:
            self.pila.append(EntradaPila(regla="28.1"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(token=IDENTIFICADOR))
            self.pila.append(EntradaPila(token=INPUT))
            return "28"  # S -> input id ;
        elif self.code == RETURN:
            self.pila.append(EntradaPila(regla="29.1"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(no_terminal="X"))
            self.pila.append(EntradaPila(token=RETURN))
            return "29"  # S -> return X ;
        elif self.code == IDENTIFICADOR:
            self.pila.append(EntradaPila(regla="30.1"))
            self.pila.append(EntradaPila(no_terminal="I"))
            self.pila.append(EntradaPila(token=IDENTIFICADOR))
            return "30"  # S -> id I
        else:
            Error.lanzar_error(329, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""
        
    def CasoX(self):
        if self.code in [PAREN_ABRE, CONSTANTE_ENTERA, CADENA, IDENTIFICADOR, NOT]:
            self.pila.append(EntradaPila(regla="31.1"))
            self.pila.append(EntradaPila(no_terminal="E"))
            return "31"  # X -> E
        else:
            self.pila.append(EntradaPila(regla="32.1"))
            return "32"  # X -> Lambda

    def CasoI(self):
        if self.code == PAREN_ABRE:
            self.pila.append(EntradaPila(regla="33.1"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(token=PAREN_CIERRA))
            self.pila.append(EntradaPila(no_terminal="L"))
            self.pila.append(EntradaPila(token=PAREN_ABRE))
            return "33"  # I -> ( L ) ;
        elif self.code == IGUAL:
            self.pila.append(EntradaPila(regla="34.2"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(no_terminal="E"))
            self.pila.append(EntradaPila(token=IGUAL))
            return "34"  # I -> = E ;
        elif self.code == AUTODECREMENTO:
            self.pila.append(EntradaPila(regla="46.1"))
            self.pila.append(EntradaPila(token=PUNTO_Y_COMA))
            self.pila.append(EntradaPila(token=AUTODECREMENTO))
            return "46"  # I -> -- ;
        else:
            Error.lanzar_error(310, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""

    def CasoL(self):
        if self.code in [PAREN_ABRE, CONSTANTE_ENTERA, CADENA, IDENTIFICADOR, NOT]:
            self.pila.append(EntradaPila(regla="35.1"))
            self.pila.append(EntradaPila(no_terminal="Q"))
            self.pila.append(EntradaPila(no_terminal="E"))
            return "35"  # L -> E Q
        else:
            self.pila.append(EntradaPila(regla="36.1"))
            return "36"  # L -> Lambda        



    def CasoQ(self):
        if self.code == COMA:
            self.pila.append(EntradaPila(regla="37.1"))
            self.pila.append(EntradaPila(no_terminal="Q"))
            self.pila.append(EntradaPila(no_terminal="E"))
            self.pila.append(EntradaPila(token=COMA))
            return "37"  # Q -> , E Q
        else:
            self.pila.append(EntradaPila(regla="38.1"))
            return "38"  # Q -> Lambda

    def CasoF(self):
        if self.code == FUNCTION:
            self.pila.append(EntradaPila(regla="39.5"))
            self.pila.append(EntradaPila(token=LLAVE_CIERRA))
            self.pila.append(EntradaPila(regla="39.4"))
            self.pila.append(EntradaPila(no_terminal="C"))
            self.pila.append(EntradaPila(token=LLAVE_ABRE))
            self.pila.append(EntradaPila(token=PAREN_CIERRA))
            self.pila.append(EntradaPila(regla="39.3"))
            self.pila.append(EntradaPila(no_terminal="A"))
            self.pila.append(EntradaPila(token=PAREN_ABRE))
            self.pila.append(EntradaPila(regla="39.2"))
            self.pila.append(EntradaPila(token=IDENTIFICADOR))
            self.pila.append(EntradaPila(no_terminal="H"))
            self.pila.append(EntradaPila(token=FUNCTION))
            self.pila.append(EntradaPila(regla="39.1"))
            return "39"  # F -> function H id ( A ) { C }
        else:
            Error.lanzar_error(316, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""

    def CasoH(self):
        if self.code == VOID:
            self.pila.append(EntradaPila(regla="41.1"))
            self.pila.append(EntradaPila(token=VOID))
            return "41"  # H -> void
        elif self.code in [INT, BOOLEAN, STRING]:
            self.pila.append(EntradaPila(regla="40.1"))
            self.pila.append(EntradaPila(no_terminal="T"))
            return "40"  # H -> T
        else:
            Error.lanzar_error(340, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""

    def CasoA(self):
        if self.code == VOID:
            self.pila.append(EntradaPila(regla="43.1"))
            self.pila.append(EntradaPila(token=VOID))
            return "43"  # A -> void
        elif self.code in [INT, BOOLEAN, STRING]:
            self.pila.append(EntradaPila(regla="42.1"))
            self.pila.append(EntradaPila(no_terminal="K"))
            self.pila.append(EntradaPila(token=IDENTIFICADOR))
            self.pila.append(EntradaPila(no_terminal="T"))
            return "42"  # A -> T id K
        else:
            Error.lanzar_error(343, self.token.getLinea(), self.prev_token, self.token)
            self.error = True
            return ""
        
    def CasoK(self):
        if self.code == COMA:
            self.pila.append(EntradaPila(regla="44.1"))
            self.pila.append(EntradaPila(no_terminal="K"))
            self.pila.append(EntradaPila(token=IDENTIFICADOR))
            self.pila.append(EntradaPila(no_terminal="T"))
            self.pila.append(EntradaPila(token=COMA))
            return "44"  # K -> , T id K
        else:
            self.pila.append(EntradaPila(regla="45.1"))
            return "45"  # K -> Lambda


    def finalize(self):
        """Llamado al final del análisis para verificar si se aceptó correctamente."""
        if not self.accepted and not self.error:
            # Si no se aceptó ni hubo error, verificar si hay tokens pendientes
            if self.pila == [EntradaPila(token=EOF)] and self.code == EOF:
                self.accepted = True
                return self.parse.strip()
            else:
                Error.lanzar_error(303, self.token.getLinea(), self.prev_token, self.token)
        return ""
    

    def ejecutar_sem(self, regla_str, aux_pila):
        """
        Ejecuta la acción semántica identificada por 'regla_str' (p.e. '4.1'),
        usando la pila auxiliar 'aux_pila'.
        Retorna:
        - una nueva EntradaPila con atributos (tipo, ancho, tipoRet, etc.), o
        - None si la acción no 'produce' un símbolo nuevo en la pila auxiliar.
        """
        nueva_entrada = EntradaPila() 

        match regla_str:
            
            # P -> B P {1.1}
            # if (B.tipoRet ≠ Ø) then error(“No se puede hacer un ‘return’ fuera de una función.”)
            case "1.1":
                # Verificar que hay al menos 1 elemento en aux_pila
                if len(aux_pila) < 1:
                    Error.lanzar_error(700, self.token.getLinea(), self.prev_token, self.token)
                    return None
                b_entry = aux_pila.pop()
                if b_entry.get_tipo_ret() is not None and b_entry.get_tipo_ret() != "Ø":
                    Error.lanzar_error(500, self.token.getLinea(), self.prev_token, self.token)
                # No añadimos nada especial a la pila
                return None

            # T -> int {4.1}
            case "4.1":
                aux_pila.pop() 
                nueva_entrada.set_tipo("integer")
                nueva_entrada.set_ancho(1)
                return nueva_entrada

            # T -> boolean {5.1}
            case "5.1":
                aux_pila.pop()
                nueva_entrada.set_tipo("logic")
                nueva_entrada.set_ancho(1)
                return nueva_entrada

            # T -> string {6.1}
            case "6.1":
                aux_pila.pop()
                nueva_entrada.set_tipo("string")
                nueva_entrada.set_ancho(64)
                return nueva_entrada

            
            # E -> U M {7.1}
            # E.tipo := if M.tipo=Ø then U.tipo
            #           elif U.tipo=M.tipo=integer then logic
            #           else error
            case "7.1":
                if len(aux_pila) < 2:
                    Error.lanzar_error(701, self.token.getLinea(), self.prev_token, self.token)
                    return None

                m_entry = aux_pila.pop()  # M
                u_entry = aux_pila.pop()  # U

                tipo_u = u_entry.get_tipo()
                tipo_m = m_entry.get_tipo()

                if tipo_m == "Ø":
                    nueva_entrada.set_tipo(tipo_u)
                elif tipo_u == "integer" and tipo_m == "integer":
                    nueva_entrada.set_tipo("logic")
                else:
                    Error.lanzar_error(502, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                return nueva_entrada


            # M -> < U M {8.1}
            # M.tipo := if (U.tipo = M1.tipo = integer) then integer
            #           elif (M1.tipo=Ø) then U.tipo
            #           else error
            case "8.1":
                if len(aux_pila) < 2:
                    Error.lanzar_error(703, self.token.getLinea(), self.prev_token, self.token)
                    return None
                m1_entry = aux_pila.pop()  # la M "siguiente"
                u_entry  = aux_pila.pop()  # U
                aux_pila.pop() # <
                tipo_u   = u_entry.get_tipo()
                tipo_m1  = m1_entry.get_tipo()

                # M actual depende de (U, M1)
                if tipo_u == "integer" and tipo_m1 == "integer":
                    nueva_entrada.set_tipo("integer")
                elif tipo_m1 == "Ø":
                    nueva_entrada.set_tipo(tipo_u)
                else:
                    Error.lanzar_error(503, self.token.getLinea(), self.prev_token, self.token)
                    return None

                return nueva_entrada

            # M -> lambda {9.1} => M.tipo = Ø
            case "9.1":
                nueva_entrada.set_tipo("Ø")
                return nueva_entrada

            
            # U -> V U1 {10.1}
            # U.tipo := if U1.tipo=Ø then V.tipo
            #           elif V.tipo=U1.tipo=integer then integer
            #           else error
            case "10.1":
                if len(aux_pila) < 2:
                    Error.lanzar_error(704, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                u1_entry = aux_pila.pop()
                v_entry  = aux_pila.pop()
                tipo_v   = v_entry.get_tipo()
                tipo_u1  = u1_entry.get_tipo()

                if tipo_u1 == "Ø":
                    nueva_entrada.set_tipo(tipo_v)
                elif tipo_v == "integer" and tipo_u1 == "integer":
                    nueva_entrada.set_tipo("integer")
                else:
                    Error.lanzar_error(504, self.token.getLinea(), self.prev_token, self.token)
                    return None
                return nueva_entrada

            # U1 -> + V U1 {11.1}
            # U1.tipo := if U1.tipo=Ø then V.tipo
            #            elif V.tipo=U1.tipo=integer then integer
            #            else error
            case "11.1":
                if len(aux_pila) < 2:
                    Error.lanzar_error(704, self.token.getLinea(), self.prev_token, self.token)
                    return None
                u1b_entry = aux_pila.pop()  # la U1 que sigue
                v_entry   = aux_pila.pop()
                aux_pila.pop() # +

                tipo_v    = v_entry.get_tipo()
                tipo_u1b  = u1b_entry.get_tipo()


                if tipo_u1b == "Ø":
                    nueva_entrada.set_tipo(tipo_v)
                elif tipo_v == "integer" and tipo_u1b == "integer":
                    nueva_entrada.set_tipo("integer")
                else:
                    Error.lanzar_error(505, self.token.getLinea(), self.prev_token, self.token)
                    return None

                return nueva_entrada

            # U1 -> lambda {12.2} => U1.tipo = Ø
            case "12.2":
                nueva_entrada.set_tipo("Ø")
                return nueva_entrada

            
            # V -> ( E ) {13.1} => V.tipo := E.tipo
            case "13.1":
                if len(aux_pila) < 3:
                    Error.lanzar_error(705, self.token.getLinea(), self.prev_token, self.token)
                    return None
                aux_pila.pop()   # ')'
                e_entry      = aux_pila.pop()   # E
                aux_pila.pop()   # '('
                nueva_entrada.set_tipo(e_entry.get_tipo())
                return nueva_entrada

            # V -> ent {14.1} => V.tipo = integer
            case "14.1":
                aux_pila.pop()  # 'ent'
                nueva_entrada.set_tipo("integer")
                return nueva_entrada

            # V -> cad {15.1} => V.tipo = string
            case "15.1":
                aux_pila.pop()  # 'cad'
                nueva_entrada.set_tipo("string")
                return nueva_entrada

            # V -> id Z {16.1}
            # if Z.tipo=Ø => V.tipo = tipo(id)
            # elif tipo(id)=Z.tipo => V.tipo = Z.tipo
            # else error
            case "16.1":
                if len(aux_pila) < 4:
                    Error.lanzar_error(706, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                # Extraer en orden inverso: Z, id, T, COMA (si existe)
                z_entry  = aux_pila.pop()  # Z
                id_entry = aux_pila.pop()  # id

                pos_id   = int(id_entry.get_tk().get_pos())

                # with open("tabAux.txt", 'w') as archivo_simbolos:
                #      self.tsl.print(archivo_simbolos)

                tipo_id = None
                if not self.tablaActivaTSG:     # Se busca primero en la local
                    tipo_id = self.tsl.busca_tipo(pos_id)
                if tipo_id is None:             # Si no se encuentra, se busca en la global (no excluyente)
                        tipo_id = self.tsg.busca_tipo(pos_id)

                tipo_z  = z_entry.get_tipo()


                # Z.tipo=Ø => v = tipo(id)
                if tipo_z == "Ø":
                    nueva_entrada.set_tipo(tipo_id) 

                elif tipo_z == "decremento":
                    if tipo_id == "integer":
                        nueva_entrada.set_tipo("integer")
                    else:
                        Error.lanzar_error(507, self.token.getLinea(), self.prev_token, self.token)
                        return None
                
                elif tipo_z == "callFunc":
                    tipo_id = self.tsg.busca_tipo(pos_id) # para los casos que estamos dentro de una funcion llamando a otra
                    if tipo_id == "function":
        
                        num_params_func = self.tsg.busca_num_params(pos_id)

                        if tipo_id != "function":
                            Error.lanzar_error(508, self.token.getLinea(), self.prev_token, self.token)
                            return None

                        num_params_llamada = z_entry.get_num_params()   # n real
                        if num_params_func != num_params_llamada:
                            Error.lanzar_error(509, self.token.getLinea(), self.prev_token, self.token) #  f"Se esperaban {num_params_func} params y se han pasado {num_params_llamada}"
                            return None
                        
                        arrTS = self.tsg.busca_tipo_params(pos_id)  # Lista de tipos esperados
                        arrL  = z_entry.get_tipo_params()           # Lista de tipos pasados (L)

                        for i in range(num_params_func):
                            if arrTS[i] != arrL[i]:

                                Error.lanzar_error(510, self.token.getLinea(), self.prev_token, self.token) # Error => "No coincide el tipo en la posición i"
                                return None

                        tipo_ret = self.tsg.busca_tipo_ret(pos_id)
                        nueva_entrada.set_tipo(tipo_ret)
                    else:
                        Error.lanzar_error(550, self.token.getLinea(), self.prev_token, self.token) # Error => "No coincide el tipo en la posición i"

                else:
                    # with open("tabAux.txt", 'w') as archivo_simbolos:
                    #   self.tsg.print(archivo_simbolos)
                    Error.lanzar_error(511, self.token.getLinea(), self.prev_token, self.token)
                    return None

                return nueva_entrada

            # V -> ! E {17.1}
            # if E.tipo=logic => V.tipo=logic else error
            case "17.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(707, self.token.getLinea(), self.prev_token, self.token)
                    return None
                e_entry = aux_pila.pop()
                aux_pila.pop()  # '!'
                if e_entry.get_tipo() == "logic":
                    nueva_entrada.set_tipo("logic")
                else:
                    Error.lanzar_error(512, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                return nueva_entrada

            # Z -> -- {18.1} => Z.tipo=decremento
            case "18.1":
                aux_pila.pop()  # '--
                nueva_entrada.set_tipo("decremento")
                return nueva_entrada

            # Z -> ( L ) {19.1} => Z.tipo = L.tipo
            case "19.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(708, self.token.getLinea(), self.prev_token, self.token)
                    return None
                aux_pila.pop()   # ')'
                l_entry = aux_pila.pop()
                aux_pila.pop()   # '('

                nueva_entrada.set_tipo("callFunc")
                nueva_entrada.add_tipo_params_list(l_entry.get_tipo_params())
                return nueva_entrada

            # Z -> lambda {20.1} => Z.tipo=Ø
            case "20.1":
                nueva_entrada.set_tipo("Ø")
                return nueva_entrada

            
            # B -> S {21.1} => B.tipoRet = S.tipoRet
            case "21.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(709, self.token.getLinea(), self.prev_token, self.token)
                    return None
                s_entry = aux_pila.pop()
                nueva_entrada.set_tipo_ret(s_entry.get_tipo_ret())
                return nueva_entrada

            # B -> if ( E {22.1} ) S {22.2}
            #  {22.1}: if (E.tipo != logic) error
            #  {22.2}: B.tipoRet = S.tipoRet
            case "22.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(710, self.token.getLinea(), self.prev_token, self.token)
                    return None
                e_entry = aux_pila.pop()
                aux_pila.pop()  # '('
                aux_pila.pop()  # 'if'

                with open("tabAux.txt", 'w') as archivo_simbolos:
                     self.tsg.print(archivo_simbolos)
                if e_entry.get_tipo() != "logic":
                    Error.lanzar_error(513, self.token.getLinea(), self.prev_token, self.token)
                
                return None

            case "22.2":
                if len(aux_pila) < 1:
                    Error.lanzar_error(711, self.token.getLinea())
                    return None
                s_entry = aux_pila.pop()
                aux_pila.pop()  # ')'
                nueva_entrada.set_tipo_ret(s_entry.get_tipo_ret())
                return nueva_entrada

            # B -> do { C } while ( E  ) ; {23.1}
            #  {23.1}: if E.tipo != logic => error
            case "23.1":
                if len(aux_pila) < 2:
                    Error.lanzar_error(712, self.token.getLinea(), self.prev_token, self.token)
                    return None
                # Extraer E y C de la pila auxiliar
                aux_pila.pop()  # ';'
                aux_pila.pop() # ')'
                e_entry = aux_pila.pop()
                aux_pila.pop() # '('
                aux_pila.pop() # 'while'
                aux_pila.pop() # '}'
                c_entry = aux_pila.pop()
                aux_pila.pop() # '{'
                aux_pila.pop() # 'do'

                if e_entry.get_tipo() != "logic":
                    Error.lanzar_error(514, self.token.getLinea(), self.prev_token, self.token)

                nueva_entrada.set_tipo_ret(c_entry.get_tipo_ret())
                return nueva_entrada

            # B -> var {24.1} T id {24.2} ; {24.3}
            #  {24.1}: zona_decl=true
            #  {24.2}: if ya existe => error, else añadeTipo ...
            case "24.1":
                self.aLex.set_zona_decl(True)
                return None
            
            case "24.2":
                self.aLex.set_zona_decl(False)
                return None

            case "24.3":
                # Para asegurar que las entradas son correctas, usamos pop
                # tope -1 => id
                # tope -2 => T
                if len(aux_pila) < 2:
                    Error.lanzar_error(713, self.token.getLinea(), self.prev_token, self.token)
                    return None
                

                aux_pila.pop()  # ';'
                id_entry = aux_pila.pop()
                t_entry = aux_pila.pop()
                aux_pila.pop()

                pos_id   = int(id_entry.get_tk().get_pos())

                if self.tablaActivaTSG:
                    self.tsg.añadir_tipo(pos_id, t_entry.get_tipo())
                    self.tsg.añadir_despl(pos_id, self.desplG)
                    self.desplG += t_entry.get_ancho()
                    
                else:
                    self.tsl.añadir_tipo(pos_id, t_entry.get_tipo())
                    self.tsl.añadir_despl(pos_id, self.desplL)
                    self.desplL += t_entry.get_ancho()

                nueva_entrada.set_tipo_ret("Ø")
                return nueva_entrada

            
            # C -> B C {25.1} => C.tipoRet = ...
            #    if (C1.tipoRet=Ø) then B.tipoRet else
            #       si coincide con B => B, else error
            case "25.1":
                if len(aux_pila) < 2:
                    Error.lanzar_error(714, self.token.getLinea(), self.prev_token, self.token)
                    return None
                # print("--------------------")
                # for entrada in aux_pila:
                #     print(entrada)

                c1_entry = aux_pila.pop()  # la "segunda" C
                b_entry  = aux_pila.pop()  # B

                tipo_b   = b_entry.get_tipo_ret()
                tipo_c1  = c1_entry.get_tipo_ret()

                if tipo_c1 == "Ø":
                    nueva_entrada.set_tipo_ret(tipo_b)
                elif tipo_b == "Ø":
                    nueva_entrada.set_tipo_ret(tipo_c1)
                elif tipo_c1 == tipo_b:
                    nueva_entrada.set_tipo_ret(tipo_b)
                else:
                    # error: la función no puede devolver 2 tipos distintos
                    Error.lanzar_error(515, self.token.getLinea(), self.prev_token, self.token)
                    return None

                return nueva_entrada

            # C -> lambda {26.1} => C.tipoRet=Ø
            case "26.1":
                nueva_entrada.set_tipo_ret("Ø")
                return nueva_entrada

            
            # S -> output E ; {27.1}
            # if E.tipo != string && E.tipo != integer => error
            # S.tipoRet=Ø
            case "27.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(715, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                aux_pila.pop()  # ;
                e_entry = aux_pila.pop()
                aux_pila.pop()  # output

                if e_entry.get_tipo() not in ("string", "integer"):
                    Error.lanzar_error(516, self.token.getLinea(), self.prev_token, self.token)
                    return None
                nueva_entrada.set_tipo_ret("Ø")
                return nueva_entrada

            # S -> input id ; {28.1}
            # if tipo(id) != string && != integer => error
            # S.tipoRet=Ø
            case "28.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(716, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                aux_pila.pop()  # ;
                id_entry = aux_pila.pop()
                aux_pila.pop()  # input

                pos_id   = int(id_entry.get_tk().get_pos())

                tipo_id = None
                if not self.tablaActivaTSG:     # Se busca primero en la local
                    tipo_id = self.tsl.busca_tipo(pos_id)
                if tipo_id is None:             # Si no se encuentra, se busca en la global (no excluyente)
                        tipo_id = self.tsg.busca_tipo(pos_id)

                if tipo_id not in ("string", "integer"):
                    
                    Error.lanzar_error(517, self.token.getLinea(), self.prev_token, self.token)
                    return None
                nueva_entrada.set_tipo_ret("Ø")
                return nueva_entrada

            # S -> return X ; {29.1}
            # S.tipoRet = X.tipo
            case "29.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(717, self.token.getLinea(), self.prev_token, self.token)
                    return None

                aux_pila.pop()  # ;
                x_entry = aux_pila.pop()
                aux_pila.pop()  # return

                nueva_entrada.set_tipo_ret(x_entry.get_tipo())
                return nueva_entrada

            # S -> id I {30.1}
            # S.tipoRet=Ø, 
            # S.tipo = if (BuscaTipo(id) = I.tipo->tipoRet) then ...
            # (Aquí simplificamos y solo chequeamos o asignamos)
            case "30.1":
                if len(aux_pila) < 2:
                    Error.lanzar_error(718, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                i_entry  = aux_pila.pop()
                id_entry = aux_pila.pop()

                pos_id   = int(id_entry.get_tk().get_pos())
                # print("pos_id: ", pos_id)

                tipo_id = None
                if not self.tablaActivaTSG:     # Se busca primero en la local
                    tipo_id = self.tsl.busca_tipo(pos_id)
                if tipo_id is None:             # Si no se encuentra, se busca en la global (no excluyente)
                        tipo_id = self.tsg.busca_tipo(pos_id)

                tipo_i  = i_entry.get_tipo()

                if tipo_i == "decremento":
                    if tipo_id == "integer":
                        nueva_entrada.set_tipo("integer")
                    else:
                        Error.lanzar_error(518, self.token.getLinea(), self.prev_token, self.token)
                        return None
                elif tipo_id == tipo_i:
                    nueva_entrada.set_tipo(tipo_i)
                elif tipo_i == "callFunc" and tipo_id == "function":
                    if len(aux_pila) < 1:
                        Error.lanzar_error(719, self.token.getLinea(), self.prev_token, self.token)
                        return None
                    num_params_func = self.tsg.busca_num_params(pos_id)

                    num_params_llamada = i_entry.get_num_params()   
                    if num_params_func != num_params_llamada:
                        Error.lanzar_error(519, self.token.getLinea(), self.prev_token, self.token) #  f"Se esperaban {num_params_func} params y se han pasado {num_params_llamada}"
                        return None
                    
                    arrTS = self.tsg.busca_tipo_params(pos_id)  # Lista de tipos esperados
                    arrL  = i_entry.get_tipo_params()           # Lista de tipos pasados (L)

                    
                    for idx in range(num_params_func):
                        if arrTS[idx] != arrL[idx]:
                            Error.lanzar_error(520, self.token.getLinea(), self.prev_token, self.token) # Error => "No coincide el tipo en la posición i"
                            return None

                    # OK => V.tipo = tipo de retorno de la función
                    nueva_entrada.set_tipo_ret("Ø")
                    tipo_ret = self.tsg.busca_tipo_ret(pos_id)
                    nueva_entrada.set_tipo(tipo_ret)
                    return nueva_entrada
                else:
                    with open("tabAux.txt", 'w') as archivo_simbolos:
                      self.tsg.print(archivo_simbolos)
                    Error.lanzar_error(521, self.token.getLinea(), self.prev_token, self.token)
                    return None

                
                nueva_entrada.set_tipo_ret("Ø")
                return nueva_entrada

            # X -> E {31.1} => X.tipo = E.tipo
            case "31.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(720, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                
                e_entry = aux_pila.pop()
                nueva_entrada.set_tipo(e_entry.get_tipo())
                return nueva_entrada

            # X -> lambda {32.1} => X.tipo = void
            case "32.1":
                nueva_entrada.set_tipo("void")
                return nueva_entrada

            
            # I -> ( L ) ; {33.1} => I.tipo = L.tipo
            case "33.1":
                if len(aux_pila) < 3:
                    Error.lanzar_error(721, self.token.getLinea(), self.prev_token, self.token)
                    return None
                # Extraer los tokens y no terminales innecesarios
                aux_pila.pop()  # ;
                aux_pila.pop()  # )
                l_entry = aux_pila.pop()
                aux_pila.pop()  # (

                nueva_entrada.set_tipo("callFunc")
                nueva_entrada.add_tipo_params_list(l_entry.get_tipo_params())
                return nueva_entrada

            # I -> = E ; {34.2} => I.tipo = E.tipo
            case "34.2":
                if len(aux_pila) < 2:
                    Error.lanzar_error(722, self.token.getLinea(), self.prev_token, self.token)
                    return None
                aux_pila.pop()  # ;
                e_entry = aux_pila.pop()
                aux_pila.pop()  # '='

                nueva_entrada.set_tipo(e_entry.get_tipo())
                return nueva_entrada

            
            # L -> E Q {35.1}
            # L.tipo = if Q.tipo=Ø => E.tipo else E.tipo x Q.tipo
            case "35.1":  # L -> E Q
                if len(aux_pila) < 2:
                    Error.lanzar_error(723, self.token.getLinea(), self.prev_token, self.token)
                    return None
                q_entry = aux_pila.pop()
                e_entry = aux_pila.pop()
                nueva_entrada.add_tipo_params(e_entry.get_tipo())

                if q_entry.get_tipo() != "Ø":
                    nueva_entrada.add_tipo_params_list(q_entry.get_tipo_params())
 
                return nueva_entrada

            # L -> lambda {36.1} => L.tipo=Ø
            case "36.1":
                nueva_entrada.set_tipo("void")
                return nueva_entrada

            # Q -> , E Q {37.1}
            # Q.tipo = if Q1.tipo=Ø => E.tipo else E.tipo x Q.tipo
            case "37.1":  # Q -> , E Q
                if len(aux_pila) < 3:
                    Error.lanzar_error(724, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                q_entry = aux_pila.pop()
                e_entry = aux_pila.pop()
                aux_pila.pop()  # ,

                nueva_entrada.add_tipo_params(e_entry.get_tipo())

                # 3) Si Q2 no es vacío, unimos sus tipos
                if q_entry.get_tipo() != "Ø":
                    nueva_entrada.add_tipo_params_list(q_entry.get_tipo_params())

                return nueva_entrada

            # Q -> lambda {38.1} => Q.tipo=Ø
            case "38.1":
                nueva_entrada.set_tipo("Ø")
                return nueva_entrada

            
            # F -> {39.1} function H id {39.2} ( A {39.3} ) { C {39.4}}  {39.5}
            #
            # {39.1}: zona_decl = True
            # {39.2}: TSL = CreaTabla(); desplL=0; ...
            # {39.3}: AñadeTipo(id.pos, A.tipo->H.tipo); ...
            # {39.4}: if C.tipoRet != H.tipo => error, libera TSL, zona_decl=false
            case "39.1":
                self.aLex.set_zona_decl(True)
                return None

            case "39.2":
                self.tsl = TablaSimbolos(self.idTS)
                self.aLex.set_tsl(self.tsl)
                self.idTS += 1
                self.desplL = 0
                self.tablaActivaTSG = False
                self.aLex.set_es_tsg(False)
                
                return None

            case "39.3":
                if len(aux_pila) < 3:
                    Error.lanzar_error(725, self.token.getLinea(), self.prev_token, self.token)
                    return None
                # Extraer en orden inverso: A, H, id
                

                a_entry  = aux_pila.pop()
                aux_pila.pop()  # '('
                id_entry = aux_pila.pop()
                h_entry  = aux_pila[-1]
               
                pos_id   = int(id_entry.get_tk().get_pos())

                self.tsg.añadir_tipo(pos_id, "function")
                self.tsg.añadir_tipo_devolucion(pos_id, h_entry.get_tipo())
                
                tipo_params = []
                for (p_id, p_tipo, p_ancho) in a_entry.param_list:
                    self.tsl.añadir_tipo(p_id, p_tipo)
                    self.tsl.añadir_despl(p_id, self.desplL)
                    self.desplL += p_ancho
                    tipo_params.append(p_tipo)

                # self.tsg.añadir_num_y_tipo_params(pos_id, tipo_params)
                self.tsg.añadir_num_y_tipo_params(pos_id, tipo_params)

                self.aLex.set_zona_decl(False)
                return None

            # function H {39.1} id {39.2} ( A {39.3} ) { C {39.4} } {39.5}
            case "39.4":
                if len(aux_pila) < 2:
                    Error.lanzar_error(726, self.token.getLinea(), self.prev_token, self.token)
                    return None
                
                c_entry = aux_pila.pop()
                aux_pila.pop() # '{'
                aux_pila.pop() # ')'
                h_entry = aux_pila.pop()
                aux_pila.pop()  # function
                
                if c_entry.get_tipo_ret() == "Ø" and h_entry.get_tipo() == "void":
                    pass
                elif c_entry.get_tipo_ret() != h_entry.get_tipo():
                    Error.lanzar_error(524, self.token.getLinea(), self.prev_token, self.token)
                
                self.tablas.append(self.tsl)
                self.tsl = None
                self.desplL = 0
                self.tablaActivaTSG = True
                self.aLex.set_es_tsg(True)
                self.aLex.set_tsl(None)
                return None
            
            case "39.5":
                aux_pila.pop() # '}' 
                return None

            
            # H -> T {40.1} => H.tipo = T.tipo
            case "40.1":
                if len(aux_pila) < 1:
                    Error.lanzar_error(727, self.token.getLinea(), self.prev_token, self.token)
                    return None
                t_entry = aux_pila.pop()
                nueva_entrada.set_tipo(t_entry.get_tipo())
                return nueva_entrada

            # H -> void {41.1} => H.tipo = void
            case "41.1":
                nueva_entrada.set_tipo("void")
                return nueva_entrada

            
            # A -> T id K {42.1}
            #  añadeTipo(id, T.tipo); añadeDespl(...) ...
            #  A.tipo = if K.tipo=Ø => T.tipo else T.tipo x K.tipo
            case "42.1":
                if len(aux_pila) < 4:
                    Error.lanzar_error(728, self.token.getLinea(), self.prev_token, self.token)
                    return None
                k_entry   = aux_pila.pop()  # K
                id_entry  = aux_pila.pop()  # id
                t_entry   = aux_pila.pop()  # T
                # Verificar si hay una COMA antes y eliminarla si existe
                if aux_pila and aux_pila[-1].get_token() == COMA:
                    aux_pila.pop()  # COMA

                
                nueva_entrada.set_tipo(t_entry.get_tipo()) 
                nueva_entrada.param_list = []          
                
                pos_id = int(id_entry.get_tk().get_pos())
                nueva_entrada.param_list.append((pos_id, t_entry.get_tipo(), t_entry.get_ancho()))

                # si K no es vacío, concatenamos más parámetros
                if k_entry.get_tipo() != "Ø" and hasattr(k_entry, 'param_list'):
                    nueva_entrada.param_list.extend(k_entry.param_list)

                return nueva_entrada

            # A -> void {43.1} => A.tipo=void
            case "43.1":
                aux_pila.pop()  # 'void'
                nueva_entrada.param_list = []  # sin parámetros
                nueva_entrada.set_tipo("void")
                return nueva_entrada

            # K -> , T id K {44.1}
            #  similar a 42.1
            case "44.1":
                if len(aux_pila) < 4:
                    Error.lanzar_error(729, self.token.getLinea(), self.prev_token, self.token)
                    return None
                # Extraer en orden inverso: K, id, T, COMA
                k1_entry  = aux_pila.pop()  # K
                id_entry  = aux_pila.pop()  # id
                t_entry   = aux_pila.pop()  # T
                aux_pila.pop()  # COMA

                nueva_entrada.param_list = []

                pos_id = int(id_entry.get_tk().get_pos())
                nueva_entrada.param_list.append(
                    (pos_id, t_entry.get_tipo(), t_entry.get_ancho())
                )
                
                # Si K1 tampoco es vacío, extender la lista
                if k1_entry.get_tipo() != "Ø" and hasattr(k1_entry, 'param_list'):
                    nueva_entrada.param_list.extend(k1_entry.param_list)

                nueva_entrada.set_tipo("params") 
                return nueva_entrada

            # K -> lambda {45.1} => K.tipo=Ø
            case "45.1":
                nueva_entrada.set_tipo("Ø")
                nueva_entrada.param_list = []  # sin parámetros
                return nueva_entrada

            
            # I -> -- ; {46.1} => I.tipo=decremento
            case "46.1":
                aux_pila.pop()  # ';'
                aux_pila.pop()  # '--'
                nueva_entrada.set_tipo("decremento")
                return nueva_entrada

            
            # Si no hay coincidencia
            case _:
                Error.lanzar_error(699, self.token.getLinea(), self.prev_token, self.token)
                return None

        return nueva_entrada
