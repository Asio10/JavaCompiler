# Analizador.py
from ALex.AnalizadorLexico import AnalizadorLexico  # Importa tu analizador léxico
from ALex.Token import Token
from ASin.AnalizadorSintactico import AnalizadorSintactico  # Importa el analizador sintáctico
from TS.TablaSimbolos import TablaSimbolos

# Definición de la constante EOF si no está definida
EOF = 27  # Asegúrate de que coincide con el código de fin de archivo en tu analizador léxico

class ProcesadorArchivo:
    def __init__(self, nombre_archivo, archivo_salida_tokens, archivo_salida_simbolos, archivo_salida_parse):
        """Inicializa el procesador con el nombre del archivo a procesar y los archivos de salida."""
        self.nombre_archivo = nombre_archivo
        self.archivo_salida_tokens = archivo_salida_tokens
        self.archivo_salida_simbolos = archivo_salida_simbolos
        self.archivo_salida_parse = archivo_salida_parse

    def procesar_archivo(self):
        """Procesa el archivo completo, incluyendo análisis léxico y sintáctico."""
        # Leer el contenido del archivo fuente
        with open(self.nombre_archivo, 'r') as archivo_fuente:
            contenido = archivo_fuente.read()

        # Crear instancias del analizador léxico y sintáctico
        tsg = TablaSimbolos(0)
        analizador_lexico = AnalizadorLexico(contenido, tsg)
        tablas_simbolos = []
        analizador_sintactico = AnalizadorSintactico(tsg, analizador_lexico, tablas_simbolos)
        analizador_lexico.set_aSin(analizador_sintactico)    # Para que se puedan comunicar bilateralmente

        # Abrir archivos de salida
        with open(self.archivo_salida_tokens, 'w') as archivo_tokens, \
             open(self.archivo_salida_simbolos, 'w') as archivo_simbolos, \
             open(self.archivo_salida_parse, 'w') as archivo_parse:

            # Escribir el encabezado en el archivo parse.txt
            archivo_parse.write("descendente ")

            while True:
                # Obtener el siguiente token
                token = analizador_lexico.obtener_token()

                # Escribir el token en el archivo de tokens
                token_str = token.to_string()
                archivo_tokens.write(token_str + '\n')

                # Pasar el token al analizador sintáctico y obtener el parseo
                parse_steps = analizador_sintactico.process_token(token)

                # Escribir los pasos de parseo en el archivo parse.txt
                if parse_steps:
                    archivo_parse.write(parse_steps + ' ')  # Agregar un espacio entre números

                # Verificar si es el token EOF
                if token.get_codigo() == EOF:
                    break

            # Escribir la tabla de símbolos al finalizar
            analizador_lexico.tsg.print(archivo_simbolos)
            for tabla in tablas_simbolos:
                tabla.print(archivo_simbolos)

            # Finalizar el análisis sintáctico y escribir cualquier parseo restante
            final_parse = analizador_sintactico.finalize()
            if final_parse:
                archivo_parse.write(final_parse + ' ')

        # No es necesario modificar nada más en Analizador.py

# Función principal para ejecutar el procesamiento
def main():
    nombre_archivo = "fuente.txt"  # Archivo de entrada
    archivo_salida_tokens = "tokens.txt"  # Archivo de salida para los tokens
    archivo_salida_simbolos = "simbolos.txt"  # Archivo de salida para la tabla de símbolos
    archivo_salida_parse = "parse.txt"  # Archivo de salida para el resultado del análisis sintáctico

    # Crear una instancia del procesador de archivo
    procesador = ProcesadorArchivo(
        nombre_archivo, 
        archivo_salida_tokens, 
        archivo_salida_simbolos, 
        archivo_salida_parse
    )

    # Procesar el archivo completo
    procesador.procesar_archivo()

if __name__ == "__main__":
    main()
