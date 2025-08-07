class Token:
    def __init__(self, newCod, newCad=None, newNum=None, linea = None, pos = None):
        self.codigo = newCod
        self.cadena = newCad
        self.numero = newNum
        self.linea = linea
        if pos is not None:
            try:
                self.pos = int(pos)  # Convert to integer if possible
            except ValueError:
                raise ValueError(f"pos must be an integer or convertible to an integer, but got {pos}")
        else:
            self.pos = None  # Default if not provided

    def get_pos(self):
        return self.pos

    def get_codigo(self):
        return self.codigo

    def get_cadena(self):
        return self.cadena

    def get_numero(self):
        return self.numero
    
    def getLinea(self):
        return self.linea

    def to_string(self):
        if self.cadena is not None:
            return f'< {self.codigo} , "{self.cadena}" >'
        elif self.numero is not None:
            return f'< {self.codigo} , {self.numero} >'
        elif self.pos is not None:
            return f'< {self.codigo} , {self.pos} >'
        else:
            return f'< {self.codigo} , >'
