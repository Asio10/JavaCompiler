
class EntradaPila:
    def __init__(self, token=None, no_terminal=None, regla = None, tk = None):
        self.token = token
        self.no_terminal = no_terminal
        self.regla = regla
        self.tipo = None
        self.tipo_params = []
        self.tipo_ret = None
        self.ancho = 0
        self.pos = 0
        self.tk = tk

    def get_tipo(self):
        return self.tipo

    def get_tipo_ret(self):
        return self.tipo_ret

    def get_tipo_params(self):
        return self.tipo_params

    def set_ancho(self, ancho):
        self.ancho = ancho

    def get_ancho(self):
        return self.ancho
    
    def get_tk(self):
        return self.tk

    def set_no_terminal(self, no_terminal):
        self.no_terminal = no_terminal
    
    def set_regla(self, regla):
        self.regla = regla

    def set_tipo(self, tipo):
        self.tipo = tipo

    def add_tipo_params(self, tipo):
        self.tipo_params.append(tipo)

    def add_tipo_params_list(self, tipo_list):
        self.tipo_params.extend(tipo_list)

    def set_tipo_ret(self, tipo_ret):
        self.tipo_ret = tipo_ret

    def get_token(self):
        return self.token

    def get_no_terminal(self):
        return self.no_terminal
    
    def get_regla(self):
        return self.regla

    def get_num_params(self):
        return len(self.tipo_params)

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def set_tk(self, tk):
        self.tk = tk

    def __str__(self):
        return (
            f"EntradaPila(\n"
            f"  token={self.token},\n"
            f"  no_terminal={self.no_terminal},\n"
            f"  regla={self.regla},\n"
            f"  tipo={self.tipo},\n"
            f"  tipo_params={self.tipo_params},\n"
            f"  tipo_ret={self.tipo_ret},\n"
            f"  ancho={self.ancho},\n"
            f"  pos={self.pos}\n"
            f")"
        )