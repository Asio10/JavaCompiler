import os
from TS.EntradaTabla import EntradaTabla

class TablaSimbolos:
    def __init__(self, id):
        self.tabla = {}  # Diccionario principal
        self.pos_voy = id * 100
        self.id = id

    def check_tabla(self, identificador):
        if identificador in self.tabla:
            return self.tabla[identificador]['entrada'].posicion
        return None

    def get_nombre_ident(self, pos):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                return data['entrada'].etiqueta
        return None

    def añadir_tipo_y_despl(self, pos, tipo, despl):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                entrada = data['entrada']
                entrada.set_tipo(tipo)
                entrada.set_despl(despl)
                break

    def añadir_despl(self, pos, despl):
        for _,data in self.tabla.items():
            if data['posicion'] == pos:
                entrada = data['entrada']
                entrada.set_despl(despl)
                break

    def añadir_tipo(self, pos, tipo):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                data['entrada'].set_tipo(tipo)
                break

    def añadir_tipo_devolucion(self, pos, tipo):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                data['entrada'].set_tipo_devolucion(tipo)
                break

    def añadir_num_y_tipo_params(self, pos, tipo_params):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                entrada = data['entrada']
                entrada.set_num_params(len(tipo_params))
                entrada.set_tipo_params(tipo_params)
                entrada.set_etiq(entrada.cadena)
                break

    def busca_tipo(self, pos):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                return data['entrada'].tipo
        return None

    def añadir_entrada(self, cadena):
        nueva_entrada = EntradaTabla(self.pos_voy, cadena)
        self.tabla[cadena] = {'posicion': self.pos_voy, 'entrada': nueva_entrada}
        out = self.pos_voy
        self.pos_voy += 1
        return out

    def busca_num_params(self, pos):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                return data['entrada'].num_params
        return None

    def busca_tipo_params(self, pos):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                return data['entrada'].tipo_params
        return None

    def busca_tipo_ret(self, pos):
        for cadena, data in self.tabla.items():
            if data['posicion'] == pos:
                return data['entrada'].tipo_devolucion
        return None

    def print(self, file_out):
        file_out.write(f"TABLA #{self.id} :\n")
        for cadena, data in self.tabla.items():
            aux = data['entrada']
            file_out.write(f" * Lexema : '{aux.cadena}'\n")
            file_out.write("   Atributos :\n")
            file_out.write(f"   + tipo : '{aux.tipo}'\n")
            if aux.tipo == "function":
                file_out.write(f"     + numParam : '{aux.num_params}'\n")
                for idx, tipo_param in enumerate(aux.tipo_params):
                    file_out.write(f"       + TipoParam{idx + 1} : '{tipo_param}'\n")
                file_out.write(f"       + TipoRetorno : '{aux.tipo_devolucion}'\n")
                file_out.write(f"     + EtiqFuncion : '{aux.etiqueta}'\n")
            else:
                file_out.write(f"   + despl : {aux.despl}\n")
            file_out.write("---------------------------------\n")