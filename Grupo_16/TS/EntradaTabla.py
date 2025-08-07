class EntradaTabla:
    def __init__(self, pos, cadena):
        self.posicion = pos
        self.cadena = cadena
        self.num_params = None
        self.tipo = None
        self.tipo_params = []
        self.tipo_devolucion = None
        self.etiqueta = None
        self.despl = 0

    def set_despl(self, despl):
        self.despl = despl

    def set_tipo(self, tipo):
        self.tipo = tipo

    def set_num_params(self, num_params):
        self.num_params = num_params

    def set_tipo_params(self, tipo_params):
        self.tipo_params = tipo_params.copy()

    def add_tipo_param(self, tipo_param):
        """Añade un tipo a la lista tipo_params."""
        self.tipo_params.append(tipo_param)

    def set_tipo_devolucion(self, tipo_dev):
        self.tipo_devolucion = tipo_dev

    def set_etiq(self, etiq):
        self.etiqueta = etiq


    def get_posicion(self):
        """Devuelve la posición."""
        return self.posicion

    def get_cadena(self):
        """Devuelve la cadena."""
        return self.cadena

    def get_num_params(self):
        """Devuelve el número de parámetros."""
        return self.num_params

    def get_tipo(self):
        """Devuelve el tipo."""
        return self.tipo

    def get_tipo_params(self):
        """Devuelve la lista de tipos de parámetros."""
        return self.tipo_params

    def get_tipo_devolucion(self):
        """Devuelve el tipo de devolución."""
        return self.tipo_devolucion

    def get_etiqueta(self):
        """Devuelve la etiqueta."""
        return self.etiqueta

    def get_despl(self):
        """Devuelve el desplazamiento."""
        return self.despl