from ply import lex, yacc
import json
import re

#permitir errores en link?
#falta aceptar listas vacias/lambda
#arreglar los opcionales, multiples o en distinto orden EN MARCHA
#falta generar HTML
#falta especificar errores

# Definición de tokens
tokens = [
    'LLAVE_A', 'LLAVE_C', 'CORCHETE_A', 'CORCHETE_C', 'COMILLAS', 'COMA', 'DOS_PUNTOS', 'CADENA',
    'INTEGER', 'FLOAT', 'BOOL', 'DATE', 'PROTOCOLO',
    'NOMBRE_EMPRESA', 'FUNDACION', 'DIRECCION', 'INGRESOS_ANUALES', 'PYME', 'LINK', 'DEPARTAMENTOS',
    'NOMBRE', 'JEFE', 'SUBDEPARTAMENTOS', 'EMPLEADOS', 'PROYECTOS', 'ESTADO', 'FECHA_INICIO', 'FECHA_FIN',
    'CALLE', 'CIUDAD', 'PAIS', 'EDAD', 'CARGO', 'SALARIO', 'ACTIVO', 'FECHA_CONTRATACION',
    'EMPRESAS', 'FIRMA_DIG', 'VERSION', 'DOMINIO', 'ESTADOS', 'CARGOS', 'RUTA', 'PUERTO'
    
]

# Expresiones regulares para tokens simples
t_LLAVE_A = r'\{'
t_LLAVE_C = r'\}'
t_CORCHETE_A = r'\['
t_CORCHETE_C = r'\]'
t_COMILLAS = r'"'
t_COMA = r','
t_DOS_PUNTOS = r':'


# Tokens con expresiones regulares y funciones para convertirlos

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t


def t_DATE(t):
    r'\"((19|2[0-9])[0-9]{2}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|30))\"'
    return t

def t_PROTOCOLO(t):
    r'"https://|"http://|"ftps://|"ftp://'
    return t

def t_EMPRESAS(t):
    r'"empresas":'
    return t

def t_NOMBRE_EMPRESA(t):
    r'"nombre_empresa":'
    return t

def t_FUNDACION(t):
    r'"fundacion":'
    return t

def t_DIRECCION(t):
    r'"direccion":'
    return t

def t_INGRESOS_ANUALES(t):
    r'"ingresos_anuales":'
    return t

def t_PYME(t):
    r'"pyme":'
    return t

def t_LINK(t):
    r'"link":'
    return t

def t_DEPARTAMENTOS(t):
    r'"departamentos":'
    return t

def t_NOMBRE(t):
    r'"nombre":'
    return t

def t_JEFE(t):
    r'"jefe":'
    return t

def t_SUBDEPARTAMENTOS(t):
    r'"subdepartamentos":'
    return t

def t_EMPLEADOS(t):
    r'"empleados":'
    return t

def t_PROYECTOS(t):
    r'"proyectos":'
    return t

def t_ESTADO(t):
    r'"estado":'
    return t

def t_FECHA_INICIO(t):
    r'"fecha_inicio":'
    return t

def t_FECHA_FIN(t):
    r'"fecha_fin":'
    return t

def t_CALLE(t):
    r'"calle":'
    return t

def t_CIUDAD(t):
    r'"ciudad":'
    return t

def t_PAIS(t):
    r'"pais":'
    return t

def t_EDAD(t):
    r'"edad":'
    return t

def t_CARGO(t):
    r'"cargo":'
    return t

def t_SALARIO(t):
    r'"salario":'
    return t

def t_ACTIVO(t):
    r'"activo":'
    return t

def t_FECHA_CONTRATACION(t):
    r'"fecha_contratacion":'
    return t

def t_FIRMA_DIG(t):
    r'"firma_digital":'
    return t

def t_VERSION(t):
    r'"version":'
    return t

def t_CARGOS(t):
    r'"Product\sAnalyst"|"Project\sManager"|"UX\sdesigner"|"Marketing"|"Developer"|"Devops"|"DB\sadmin"'
    return t

def t_ESTADOS(t):
    r'"To\sdo"|"In\sprogress"|"Canceled"|"Done"|"On\shold"'
    return t

def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

def t_DOMINIO(t):
    r'[a-zA-Z0-9.-]+'
    if '..' in t.value:
        print(f"Dominio inválido: '{t.value}' contiene puntos consecutivos")
        t.lexer.skip(len(t.value))  # Skip the invalid domain
    else:
        return t

def t_RUTA(t):
    r'/[a-zA-Z0-9./_-]*'
    return t

# Ignorar espacios y tabs
t_ignore = ' \t\n'

# Manejo de errores


def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


lexer = lex.lex()

data = '''
{
  "empresas": [
    {
      "nombre_empresa": "UTN FRRe",
      "fundacion": 2005,
    }
  ]
} '''

lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)


# Regla inicial del parser

def p_sigma(p):
    '''
    sigma : LLAVE_A empresas LLAVE_C
          | LLAVE_A empresas COMA VERSION version COMA FIRMA_DIG firma_dig LLAVE_C
    '''

    if len(p) == 4:
        p[0] = p[2]  # Solo empresas
    elif len(p) == 10:
        p[0] = {
            'empresas': p[2], 
            'version': p[5],
            'firma_dig': p[8]
            }  
        # Con versión y firma digital
    

# Regla para empresas


def p_empresas(p):
    '''
    empresas : EMPRESAS CORCHETE_A empresa CORCHETE_C
    '''

    p[0] = [p[3]]  # Una sola empresa
 
def p_empresa(p):
    '''
    empresa : recur_empresa
            | recur_empresa COMA empresa
    '''
    if len(p) == 2:
        p[0] = [p[1]]  # Una sola empresa
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]  # Concatenate lists of empresas



def p_recur_empresa(p):
    '''
    recur_empresa : LLAVE_A NOMBRE_EMPRESA CADENA COMA FUNDACION INTEGER COMA DIRECCION direccion COMA INGRESOS_ANUALES ingresos COMA PYME BOOL COMA LINK url COMA DEPARTAMENTOS departamentos LLAVE_C
    '''
    p[0] = {
        'nombre_empresa': p[3],
        'fundacion': p[6],
        'direccion': p[9],
        'ingresos_anuales': p[12],
        'pyme': p[15],
        'link': p[18],
        'departamentos': p[21]
    }

def p_ingresos(p):
    '''
    ingresos : FLOAT
             | INTEGER
    '''
    p[0] = p[1]

def p_direccion(p):
    '''
    direccion : LLAVE_A CALLE CADENA COMA CIUDAD CADENA COMA PAIS CADENA LLAVE_C
    '''
    p[0] = {
        'calle': p[3],
        'ciudad': p[6],
        'pais': p[9],
    }

def p_url(p):
    '''
    url : PROTOCOLO DOMINIO op_puerto op_ruta COMILLAS
    '''
    protocol = p[1]
    domain = p[2]
    port = ":" + str(p[3]) if p[3] else ""
    path = p[4] if p[4] else ""
    p[0] = protocol + domain + port + path + '"'

def p_op_puerto(p):
    '''
    op_puerto : DOS_PUNTOS INTEGER
             | vacio
    '''
    if len(p) == 3:
        p[0] = p[2]  # Port number
    else:
        p[0] = None  # No port specified

def p_op_ruta(p):
    '''
    op_ruta : RUTA
             | vacio
    '''
    if len(p) == 2:
        p[0] = p[1]  # Path specified
    else:
        p[0] = ''  # No path specified

def p_vacio(p):
    '''
    vacio :
    '''
    p[0] = None

def p_departamentos(p):
    '''
    departamentos : CORCHETE_A departamento CORCHETE_C

    '''
    p[0] = [p[2]]  # Un solo departamento


def p_departamento(p):
    '''
    departamento : recur_depto
                 | recur_depto COMA departamento
    '''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo departamento
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]   # Varios departamentos
   
def p_recur_depto(p):
    '''
    recur_depto : LLAVE_A NOMBRE CADENA COMA JEFE CADENA COMA SUBDEPARTAMENTOS subdepartamentos LLAVE_C
    '''
    p[0] = {
        'nombre': p[3],
        'jefe': p[6],
        'subdepartamentos': p[9]
    }

def p_subdepartamentos(p):
    '''
    subdepartamentos : CORCHETE_A subdepto CORCHETE_C

    '''
    
    p[0] = [p[2]]  # Un solo subdepartamento

def p_subdepto(p):
    '''
    subdepto : recur_subdepto
             | recur_subdepto COMA subdepto
    '''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo subdepartamento
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]  # Varios subdepartamentos


def p_recur_subdepto(p):
    '''
    recur_subdepto : LLAVE_A NOMBRE CADENA COMA JEFE CADENA COMA EMPLEADOS empleados LLAVE_C
    '''
    p[0] = {
        'nombre': p[3],
        'jefe': p[6],
        'empleados': p[9]
    }

# Regla para empleados
def p_empleados(p):
    '''
    empleados : CORCHETE_A empleado CORCHETE_C

    '''
    
    p[0] = [p[2]]  
  

def p_empleado(p):
    '''
    empleado : recur_empleados
             | recur_empleados COMA empleado
    '''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo 
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]  # Varios


def p_recur_empleados(p):
    '''
    recur_empleados : LLAVE_A NOMBRE CADENA COMA EDAD INTEGER COMA CARGO CARGOS COMA SALARIO ingresos COMA ACTIVO BOOL COMA FECHA_CONTRATACION DATE COMA PROYECTOS proyectos LLAVE_C
    '''
    p[0] = {
        'nombre': p[3],
        'edad': p[6],
        'cargo': p[9],
        'salario': p[12],
        'activo': p[15],
        'fecha_contratacion': p[18],
        'proyectos': p[21]
    }

   
def p_proyectos(p):
    '''
    proyectos : CORCHETE_A proyecto CORCHETE_C

    '''
    
    p[0] = [p[2]]  # Un solo proyecto


def p_proyecto(p):
    '''
    proyecto : recur_proyecto
             | recur_proyecto COMA proyecto
    '''
    if len(p) == 2:
        p[0] = [p[1]]  # Un solo proyecto
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]  # Varios proyectos


def p_recur_proyecto(p):
    '''
    recur_proyecto : LLAVE_A NOMBRE CADENA COMA ESTADO ESTADOS COMA FECHA_INICIO DATE COMA FECHA_FIN DATE LLAVE_C
    '''
    p[0] = {
        'nombre': p[3],
        'estado': p[6],
        'fecha_inicio': p[9],
        'fecha_fin': p[12]
    }

def p_version(p):
    '''
    version : CADENA

    '''
   
    p[0] = p[1]
    

# Regla para firma digital


def p_firma_dig(p):
    '''
    firma_dig : CADENA
            
    '''
   
    p[0] = p[1]
    

# Manejo de errores


def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}, linea {p.lineno}, token {p.type}'")      
    else:
        print("Error de sintaxis en EOF")

# Construir el parser
parser = yacc.yacc(debug=True)

# Test data
data = '''
{
  "empresas": [
    {
      "nombre_empresa": "UTN FRRe",
      "fundacion": 2005,
      "direccion": {
        "calle": "French 414",
        "ciudad": "Resistencia",
        "pais": "Argentina"
      },
      "ingresos_anuales": 200000.25,
      "pyme": false,
      "link": "https://www.frre.utn.edu.ar",
      "departamentos": [
        {
          "nombre": "Sistemas",
          "jefe": "Juan Perez",
          "subdepartamentos": [
            {
              "nombre": "Programacion",
              "jefe": "Fulano",
              "empleados": [
                {
                  "nombre": "Mengano",
                  "edad": 30,
                  "cargo": "Product Analyst",
                  "salario": 1250.65,
                  "activo": true,
                  "fecha_contratacion": "2022-09-10",
                  "proyectos": [
                    {
                      "nombre": "Parser JSON",
                      "estado": "In progress",
                      "fecha_inicio": "2024-03-25",
                      "fecha_fin": "2024-07-03"
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "version": "1.0",
  "firma_digital": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
}

'''
# Lexing
lexer.input(data)
print("Lexing tokens:")
for token in lexer:
    print(token)

# Parsing
result = parser.parse(data)
print(result)

# Función para generar HTML a partir de datos JSON


def generar_html(json_data, nombre_html):
    html = []

    # Inicio del documento HTML
    html.append('<html>')
    html.append('<head><title>Empresas</title>')
    html.append('<style>')
    html.append('.empresa { border: 1px solid gray; padding: 20px; }')
    html.append('.nombre-empresa { font-size: 24px; font-weight: bold; }')
    html.append(
        '.titulo { font-size: 18px; font-weight: bold; margin-bottom: 10px; }')
    html.append(
        '.subtitulo { font-size: 16px; font-weight: bold; margin-bottom: 5px; }')
    html.append('.dato { margin-left: 20px; }')
    html.append('</style>')
    html.append('</head>')
    html.append('<body>')

    # Procesamiento de cada empresa
    empresas = json_data.get('empresas', [])
    for empresa in empresas:
        html.append('<div class="empresa">')

        # Nombre de la empresa
        nombre_empresa = empresa.get('nombre_empresa', '')
        html.append(f'<div class="nombre-empresa">{nombre_empresa}</div>')

        # Fundación y dirección
        fundacion = empresa.get('fundacion', '')
        direccion = empresa.get('direccion', {})
        calle = direccion.get('calle', '')
        ciudad = direccion.get('ciudad', '')
        pais = direccion.get('pais', '')

        html.append('<div class="titulo">Fundación:</div>')
        html.append(f'<div class="dato">{fundacion}</div>')

        html.append('<div class="titulo">Dirección:</div>')
        html.append('<ul>')
        html.append(f'<li><span class="subtitulo">Calle:</span> {calle}</li>')
        html.append(
            f'<li><span class="subtitulo">Ciudad:</span> {ciudad}</li>')
        html.append(f'<li><span class="subtitulo">País:</span> {pais}</li>')
        html.append('</ul>')

        # Ingresos anuales y enlace
        ingresos_anuales = empresa.get('ingresos_anuales', '')
        link = empresa.get('link', '')

        html.append(f'<div class="titulo">Ingresos anuales:</div>')
        html.append(f'<div class="dato">{ingresos_anuales}</div>')
        html.append(f'<div class="titulo">Enlace:</div>')
        html.append(f'<div class="dato"><a href="{link}">{link}</a></div>')

        # Departamentos
        html.append('<div class="titulo">Departamentos:</div>')
        html.append('<ul>')
        departamentos = empresa.get('departamentos', [])
        for depto in departamentos:
            nombre_depto = depto.get('nombre', '')
            html.append(f'<li><div class="subtitulo">{
                        nombre_depto}</div></li>')

            # Subdepartamentos
            subdepartamentos = depto.get('subdepartamentos', [])
            for subdepto in subdepartamentos:
                nombre_subdepto = subdepto.get('nombre', '')
                html.append(f'<li><div class="dato">{
                            nombre_subdepto}</div></li>')

                # Empleados
                empleados = subdepto.get('empleados', [])
                if empleados:
                    html.append('<ul>')
                    for empleado in empleados:
                        nombre_empleado = empleado.get('nombre', '')
                        edad = empleado.get('edad', '')
                        cargo = empleado.get('cargo', '')
                        salario = empleado.get('salario', '')
                        activo = empleado.get('activo', '')
                        fecha_contratacion = empleado.get(
                            'fecha_contratacion', '')

                        html.append('<li>')
                        html.append(
                            f'<div class="subtitulo">Nombre:</div><div class="dato">{nombre_empleado}</div>')
                        html.append(
                            f'<div class="subtitulo">Edad:</div><div class="dato">{edad}</div>')
                        html.append(
                            f'<div class="subtitulo">Cargo:</div><div class="dato">{cargo}</div>')
                        html.append(
                            f'<div class="subtitulo">Salario:</div><div class="dato">{salario}</div>')
                        html.append(
                            f'<div class="subtitulo">Activo:</div><div class="dato">{activo}</div>')
                        html.append(
                            f'<div class="subtitulo">Fecha de contratación:</div><div class="dato">{fecha_contratacion}</div>')

                        # Proyectos
                        proyectos = empleado.get('proyectos', [])
                        if proyectos:
                            html.append('<table border="1">')
                            html.append(
                                '<tr><th>Nombre del Proyecto</th><th>Estado</th><th>Fecha de Inicio</th><th>Fecha de Fin</th></tr>')
                            for proyecto in proyectos:
                                nombre_proyecto = proyecto.get('nombre', '')
                                estado = proyecto.get('estado', '')
                                fecha_inicio = proyecto.get('fecha_inicio', '')
                                fecha_fin = proyecto.get('fecha_fin', '')

                                html.append(f'<tr><td>{nombre_proyecto}</td><td>{estado}</td><td>{
                                            fecha_inicio}</td><td>{fecha_fin}</td></tr>')
                            html.append('</table>')

                        html.append('</li>')

                    html.append('</ul>')

        html.append('</ul>')
        html.append('</div>')

    # Cierre del documento HTML
    html.append('</body>')
    html.append('</html>')

    # Escribir el HTML generado en un archivo
    nombre_archivo_html = f'{nombre_html}.html'
    with open(nombre_archivo_html, 'w', encoding='utf-8') as archivo_html:
        archivo_html.write('\n'.join(html))

    print(f"HTML generado correctamente en {nombre_archivo_html}")

# Función principal


def principal():
    nombre_archivo = input("Ingrese el nombre del archivo JSON: ")
    entrada = cargar_json_desde_archivo(nombre_archivo)
    if entrada:
        parser.parse(entrada)

# Función para cargar el JSON desde un archivo


def cargar_json_desde_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            return archivo.read()
    except FileNotFoundError:
        print(f"Archivo no encontrado: {nombre_archivo}")
        return None


if __name__ == "__main__":
    principal()
