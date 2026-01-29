import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class AutomataPila:
    """
    Autómata de pila para reconocer estructuras anidadas del lenguaje:
    - if ... else (con opción de else if)
    - while
    """
    def __init__(self):
        self.pila = []
        self.errores = []
        self.historial_pila = []
        self.ultimo_cerrado = None
        self.snapshots = []  # Capturas del estado de la pila para animación
        
    def reset(self):
        self.pila = []
        self.errores = []
        self.historial_pila = []
        self.ultimo_cerrado = None
        self.snapshots = []
    
    def push(self, elemento, linea):
        """Apilar elemento con información de línea"""
        self.pila.append((elemento, linea))
        self.historial_pila.append(f"Línea {linea}: PUSH '{elemento}' -> Pila: {[e[0] for e in self.pila]}")
        # Guardar snapshot para visualización
        self.snapshots.append({
            'operacion': 'PUSH',
            'elemento': elemento,
            'linea': linea,
            'pila': [e[0] for e in self.pila.copy()]
        })
    
    def pop(self, esperado, linea):
        """Desapilar y verificar que coincida con el esperado"""
        if len(self.pila) == 0:
            self.errores.append(f"Línea {linea}: Error - Se encontró cierre de '{esperado}' pero la pila está vacía")
            return False
        
        elemento, linea_apertura = self.pila.pop()
        self.historial_pila.append(f"Línea {linea}: POP '{elemento}' -> Pila: {[e[0] for e in self.pila]}")
        
        # Guardar snapshot para visualización
        self.snapshots.append({
            'operacion': 'POP',
            'elemento': elemento,
            'linea': linea,
            'pila': [e[0] for e in self.pila.copy()]
        })
        
        if elemento != esperado:
            self.errores.append(f"Línea {linea}: Error - Se esperaba cerrar '{elemento}' (abierto en línea {linea_apertura}) pero se encontró cierre de '{esperado}'")
            return False
        
        self.ultimo_cerrado = elemento
        return True
    
    def verificar_else(self, linea):
        """Registrar que apareció un else (no requiere validación con pila)"""
        self.historial_pila.append(f"Línea {linea}: ELSE encontrado (no afecta la pila)")
        return True
    
    def verificar_pila_vacia(self):
        """Verificar que todos los bloques hayan sido cerrados"""
        if len(self.pila) > 0:
            for elemento, linea in self.pila:
                self.errores.append(f"Error - Bloque '{elemento}' abierto en línea {linea} nunca fue cerrado")
            return False
        return True
    
    def obtener_estado(self):
        """Obtener el estado actual de la pila"""
        return [e[0] for e in self.pila]

class CScanner:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.tokens = []
        self.variables = []
        self.palabras_reservadas_encontradas = []
        self.enteros = []
        self.reales = []
        self.operadores_encontrados = []
        self.agrupaciones_encontradas = []
        self.cadenas_encontradas = []
        
        self.contador_variables = 0
        self.contador_palabras_reservadas = 0
        self.contador_enteros = 0
        self.contador_reales = 0
        self.contador_operadores = 0
        self.contador_agrupaciones = 0
        self.contador_cadenas = 0
        
        # Inicializar autómata de pila
        self.automata = AutomataPila()
    
    def es_palabra_reservada(self, palabra):
        # Palabras reservadas del lenguaje (if, else, while)
        palabra_lower = palabra.lower()
        if palabra_lower == "if":
            return True
        elif palabra_lower == "else":
            return True
        elif palabra_lower == "while":
            return True
        else:
            return False
    
    def es_digito(self, c):
        if c == '0':
            return True
        elif c == '1':
            return True
        elif c == '2':
            return True
        elif c == '3':
            return True
        elif c == '4':
            return True
        elif c == '5':
            return True
        elif c == '6':
            return True
        elif c == '7':
            return True
        elif c == '8':
            return True
        elif c == '9':
            return True
        else:
            return False
    
    def es_letra(self, c):
        if (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z'):
            return True
        else:
            return False
    
    def es_agrupacion(self, c):
        if c == '(':
            return True
        elif c == ')':
            return True
        elif c == '[':
            return True
        elif c == ']':
            return True
        elif c == '{':
            return True
        elif c == '}':
            return True
        elif c == ';':
            return True
        elif c == ',':
            return True
        else:
            return False
    
    def es_espacio(self, c):
        if c == ' ':
            return True
        elif c == '\t':
            return True
        elif c == '\n':
            return True
        elif c == '\r':
            return True
        else:
            return False
    
    def procesar_archivo(self, nombre_archivo):
        self.reset()
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            en_comentario_bloque = False
            numero_linea = 0
            for linea in lineas:
                numero_linea += 1
                en_comentario_bloque = self.procesar_linea(
                    linea, numero_linea, en_comentario_bloque
                )
            
            # Verificar que la pila esté vacía al final
            self.automata.verificar_pila_vacia()
            
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            return False
    
    def procesar_linea(self, linea, numero_linea, en_comentario_bloque):
        i = 0
        longitud = len(linea)
        while i < longitud:
            c = linea[i]
            # Comentario en bloque: Buscamos cierre
            if en_comentario_bloque:
                if c == '*' and i + 1 < longitud and linea[i + 1] == '/':
                    en_comentario_bloque = False
                    i += 2
                    continue
                else:
                    i += 1
                    continue
            # Comentario en bloque: Buscamos inicio
            if c == '/' and i + 1 < longitud and linea[i + 1] == '*':
                en_comentario_bloque = True
                i += 2
                continue
            # Detectamos comentario de línea
            if c == '/' and i + 1 < longitud and linea[i + 1] == '/':
                break
            # Detectamos comentario con #
            if c == '#':
                break
            if self.es_espacio(c):
                i += 1
                continue
            # Detectamos strings
            if c == '"':
                inicio = i
                i += 1
                while i < longitud and linea[i] != '"':
                    if linea[i] == '\\' and i + 1 < longitud:
                        i += 2
                    else:
                        i += 1
                if i < longitud:
                    i += 1
                    cadena = linea[inicio:i]
                    self.cadenas_encontradas.append((cadena, numero_linea))
                    self.tokens.append(('CADENA', cadena, numero_linea))
                    self.contador_cadenas += 1
                continue
            if c == "'":
                inicio = i
                i += 1
                while i < longitud and linea[i] != "'":
                    if linea[i] == '\\' and i + 1 < longitud:
                        i += 2
                    else:
                        i += 1
                if i < longitud:
                    i += 1
                    cadena = linea[inicio:i]
                    self.cadenas_encontradas.append((cadena, numero_linea))
                    self.tokens.append(('CADENA', cadena, numero_linea))
                    self.contador_cadenas += 1
                continue
            # Detectamos números
            if self.es_digito(c):
                i = self.procesar_numero(linea, i, numero_linea)
                continue
            # Detectamos punto seguido de número 
            if c == '.' and i + 1 < longitud and self.es_digito(linea[i + 1]):
                i = self.procesar_numero(linea, i, numero_linea)
                continue
            # Detectamos identificadores y palabras reservadas
            if self.es_letra(c) or c == '_':
                i = self.procesar_identificador(linea, i, numero_linea)
                continue
            # Detectamos operadores (carácter por carácter, analizando el siguiente)
            i = self.procesar_operador(linea, i, numero_linea)
        
        return en_comentario_bloque
    
    def procesar_numero(self, linea, inicio, numero_linea):
        i = inicio
        longitud = len(linea)
        tiene_punto = False
        tiene_exponente = False
        if linea[i] == '.':
            tiene_punto = True
            i += 1
        while i < longitud and self.es_digito(linea[i]):
            i += 1
        if i < longitud and linea[i] == '.' and not tiene_punto and not tiene_exponente:
            tiene_punto = True
            i += 1
            while i < longitud and self.es_digito(linea[i]):
                i += 1
        if i < longitud and (linea[i] == 'e' or linea[i] == 'E'):
            tiene_exponente = True
            i += 1
            if i < longitud and (linea[i] == '+' or linea[i] == '-'):
                i += 1
            while i < longitud and self.es_digito(linea[i]):
                i += 1
        while i < longitud:
            if linea[i] == 'f' or linea[i] == 'F':
                i += 1
            elif linea[i] == 'l' or linea[i] == 'L':
                i += 1
            elif linea[i] == 'u' or linea[i] == 'U':
                i += 1
            else:
                break
        numero = linea[inicio:i]
        # Clasificamos como entero o real
        if tiene_punto or tiene_exponente:
            self.reales.append((numero, numero_linea))
            self.tokens.append(('REAL', numero, numero_linea))
            self.contador_reales += 1
        else:
            self.enteros.append((numero, numero_linea))
            self.tokens.append(('ENTERO', numero, numero_linea))
            self.contador_enteros += 1
        
        return i
    
    def procesar_identificador(self, linea, inicio, numero_linea):
        i = inicio
        longitud = len(linea)
        while i < longitud:
            c = linea[i]
            if self.es_letra(c) or self.es_digito(c) or c == '_':
                i += 1
            else:
                break
        palabra = linea[inicio:i]
        # Verificamos si se trata de una palabra reservada
        if self.es_palabra_reservada(palabra):
            palabra_lower = palabra.lower()
            self.palabras_reservadas_encontradas.append((palabra, numero_linea))
            self.tokens.append(('PALABRA_RESERVADA', palabra, numero_linea))
            self.contador_palabras_reservadas += 1
            
            # Gestión del autómata de pila
            if palabra_lower == 'if':
                self.automata.push('if', numero_linea)
            elif palabra_lower == 'else':
                # El else NO se apila, solo verifica que haya un if cerrado previamente
                self.automata.verificar_else(numero_linea)
            elif palabra_lower == 'while':
                self.automata.push('while', numero_linea)
        else:
            self.variables.append((palabra, numero_linea))
            self.tokens.append(('VARIABLE', palabra, numero_linea))
            self.contador_variables += 1
        return i
    
    def procesar_operador(self, linea, i, numero_linea):
        c = linea[i]
        longitud = len(linea)
        siguiente = linea[i + 1] if i + 1 < longitud else ''
        # Verificamos si se trata de una agrupación
        if self.es_agrupacion(c):
            self.agrupaciones_encontradas.append((c, numero_linea))
            self.tokens.append(('AGRUPACION', c, numero_linea))
            self.contador_agrupaciones += 1
            
            # Gestión de llaves para cerrar bloques if/while
            if c == '{':
                # Las llaves abiertas no afectan la pila, solo marcan el inicio del bloque
                pass
            elif c == '}':
                # Al encontrar llave de cierre, desapilamos el bloque correspondiente
                if len(self.automata.pila) > 0:
                    elemento_actual = self.automata.pila[-1][0]
                    # Solo desapilar if/while
                    if elemento_actual == 'if' or elemento_actual == 'while':
                        self.automata.pop(elemento_actual, numero_linea)
            
            return i + 1
        operador = None
        salto = 1
        # Buscamos operadores compuestos
        if c == '+':
            if siguiente == '+':
                operador = '++'
                salto = 2
            elif siguiente == '=':
                operador = '+='
                salto = 2
            else:
                operador = '+'
        elif c == '-':
            if siguiente == '-':
                operador = '--'
                salto = 2
            elif siguiente == '=':
                operador = '-='
                salto = 2
            elif siguiente == '>':
                operador = '->'
                salto = 2
            else:
                operador = '-'
        elif c == '*':
            if siguiente == '=':
                operador = '*='
                salto = 2
            else:
                operador = '*'
        elif c == '/':
            if siguiente == '=':
                operador = '/='
                salto = 2
            else:
                operador = '/'
        elif c == '%':
            if siguiente == '=':
                operador = '%='
                salto = 2
            else:
                operador = '%'
        elif c == '=':
            if siguiente == '=':
                operador = '=='
                salto = 2
            else:
                operador = '='
        elif c == '!':
            if siguiente == '=':
                operador = '!='
                salto = 2
            else:
                operador = '!'
        elif c == '<':
            if siguiente == '=':
                operador = '<='
                salto = 2
            elif siguiente == '<':
                operador = '<<'
                salto = 2
            else:
                operador = '<'
        elif c == '>':
            if siguiente == '=':
                operador = '>='
                salto = 2
            elif siguiente == '>':
                operador = '>>'
                salto = 2
            else:
                operador = '>'
        elif c == '&':
            if siguiente == '&':
                operador = '&&'
                salto = 2
            elif siguiente == '=':
                operador = '&='
                salto = 2
            else:
                operador = '&'
        elif c == '|':
            if siguiente == '|':
                operador = '||'
                salto = 2
            elif siguiente == '=':
                operador = '|='
                salto = 2
            else:
                operador = '|'
        elif c == '^':
            if siguiente == '=':
                operador = '^='
                salto = 2
            else:
                operador = '^'
        elif c == '~':
            operador = '~'
        elif c == '?':
            operador = '?'
        elif c == ':':
            operador = ':'
        elif c == '.':
            operador = '.'
        
        if operador:
            self.operadores_encontrados.append((operador, numero_linea))
            self.tokens.append(('OPERADOR', operador, numero_linea))
            self.contador_operadores += 1
            return i + salto
        else:
            return i + 1

class ScannerGUI(ctk.CTk):
    def __init__(self, scanner_logic):
        super().__init__()
        self.scanner = scanner_logic
        self.archivo_actual = None
        self.snapshot_actual = 0
        
        self.title("Analizador sintáctico con Autómata de Pila - Grupo 11")
        self.geometry("1500x900")

        try:
            self.iconbitmap("icono_analizador.ico") 
        except:
            pass
    
        self.col_pink = "#FF2E63"       
        self.col_bg = "#0D1117"       
        self.col_sidebar = "#161B22"
        self.col_card = "#21262D"   
        self.col_accent = "#FF2E63"   
        
        self.dash_colors = {
            "keywords": "#C678DD",
            "vars": "#61AFEF", 
            "ints": "#98C379",   
            "floats": "#56B6C2", 
            "ops": "#E06C75", 
            "group": "#D19A66", 
            "strings": "#E5C07B", 
            "total": "#FF2E63",
            "errores": "#FF6B6B"
        }

        self.configure(fg_color=self.col_bg)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.crear_sidebar()
        self.crear_area_principal()

    def crear_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.col_sidebar)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(pady=(40, 40))
        ctk.CTkLabel(logo_frame, text="⚡", font=("Segoe UI", 40)).pack(side="left", padx=5)
        ctk.CTkLabel(logo_frame, text="ANALIZADOR\nSINTÁCTICO", font=("Orbitron", 20, "bold"), text_color=self.col_pink).pack(side="left")

        # Información del lenguaje
        info_frame = ctk.CTkFrame(self.sidebar, fg_color=self.col_card, corner_radius=10)
        info_frame.pack(pady=(0, 20), padx=20, fill="x")
        
        ctk.CTkLabel(
            info_frame,
            text="📚 Palabras Reservadas:",
            font=("Segoe UI", 11, "bold"),
            text_color="#CCCCCC"
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        palabras = ["if", "else", "while", "{ } (bloques)"]
        for p in palabras:
            ctk.CTkLabel(
                info_frame,
                text=f"• {p}",
                font=("Courier New", 10),
                text_color="#AAAAAA"
            ).pack(anchor="w", padx=20, pady=2)
        
        ctk.CTkLabel(info_frame, text="", height=5).pack()

        btn_style = {"font": ("Segoe UI", 13, "bold"), "height": 50, "corner_radius": 8, "anchor": "w"}
        
        self.btn_open = ctk.CTkButton(self.sidebar, text="  📂   ABRIR CÓDIGO", command=self.abrir_archivo, 
                                      fg_color="transparent", border_width=1, border_color=self.col_pink, hover_color="#222222", **btn_style)
        self.btn_open.pack(pady=10, padx=20, fill="x")

        self.btn_run = ctk.CTkButton(self.sidebar, text="  ▶   EJECUTAR ANÁLISIS", command=self.analizar, 
                                     fg_color=self.col_pink, hover_color="#D42650", text_color="white", **btn_style)
        self.btn_run.pack(pady=10, padx=20, fill="x")

        self.btn_clear = ctk.CTkButton(self.sidebar, text="  🗑   LIMPIAR TODO", command=self.limpiar, 
                                       fg_color="#2A2A2A", hover_color="#333333", **btn_style)
        self.btn_clear.pack(pady=10, padx=20, fill="x")

        # Visualización gráfica de la pila
        ctk.CTkLabel(
            self.sidebar,
            text="📊 Visualización de Pila:",
            font=("Segoe UI", 11, "bold"),
            text_color="#CCCCCC"
        ).pack(pady=(20, 5))
        
        # Info de la operación actual
        self.label_operacion = ctk.CTkLabel(
            self.sidebar,
            text="",
            font=("Courier New", 10, "bold"),
            text_color=self.col_pink,
            wraplength=200
        )
        self.label_operacion.pack(pady=(0, 5))
        
        self.canvas_pila = tk.Canvas(
            self.sidebar,
            width=210,
            height=200,
            bg="#0F0F0F",
            highlightthickness=1,
            highlightbackground="#333333"
        )
        self.canvas_pila.pack(padx=20, pady=5)
        
        # Controles de animación
        control_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        control_frame.pack(pady=10)
        
        self.btn_prev = ctk.CTkButton(
            control_frame,
            text="◀",
            width=40,
            command=self.snapshot_anterior,
            fg_color=self.col_card,
            hover_color="#333333"
        )
        self.btn_prev.pack(side="left", padx=2)
        
        self.label_snapshot = ctk.CTkLabel(
            control_frame,
            text="Paso: 0/0",
            font=("Courier New", 9),
            width=90
        )
        self.label_snapshot.pack(side="left", padx=10)
        
        self.btn_next = ctk.CTkButton(
            control_frame,
            text="▶",
            width=40,
            command=self.snapshot_siguiente,
            fg_color=self.col_card,
            hover_color="#333333"
        )
        self.btn_next.pack(side="left", padx=2)

    def dibujar_pila(self, pila_estado=None, snapshot_info=None):
        """Dibuja la pila gráficamente en el canvas"""
        self.canvas_pila.delete("all")
        
        if pila_estado is None:
            pila_estado = self.scanner.automata.obtener_estado()
        
        if not pila_estado:
            self.canvas_pila.create_text(
                105, 100,
                text="Pila vacía",
                fill="#666666",
                font=("Courier New", 11)
            )
            return
        
        # Configuración
        box_width = 180
        box_height = 30
        start_x = 15
        start_y = 190
        
        # Indicador de operación en la parte superior del canvas
        if snapshot_info:
            operacion = snapshot_info.get('operacion')
            elemento = snapshot_info.get('elemento')
            linea = snapshot_info.get('linea')
            
            if operacion == 'PUSH':
                op_color = "#4CAF50"  # Verde
                op_symbol = "⬇"
            else:  # POP
                op_color = "#F44336"  # Rojo
                op_symbol = "⬆"
            
            self.canvas_pila.create_text(
                105, 12,
                text=f"{op_symbol} {operacion} '{elemento}'",
                fill=op_color,
                font=("Courier New", 9, "bold")
            )
        
        # Dibujar elementos de la pila (del fondo al tope)
        colores_normal = {
            'if': '#C678DD',
            'while': '#61AFEF'
        }
        
        # Colores resaltados para el elemento siendo operado
        colores_push = {
            'if': '#4CAF50',  # Verde brillante
            'while': '#4CAF50'
        }
        
        colores_pop = {
            'if': '#F44336',  # Rojo brillante
            'while': '#F44336'
        }
        
        for i, elemento in enumerate(pila_estado):
            y = start_y - (i * (box_height + 5))
            
            # Determinar si este es el elemento afectado
            es_tope = (i == len(pila_estado) - 1)
            
            if snapshot_info and es_tope:
                if snapshot_info['operacion'] == 'PUSH':
                    color = colores_push.get(elemento, '#4CAF50')
                    borde_color = "#FFFFFF"
                    borde_ancho = 3
                else:  # POP
                    color = colores_pop.get(elemento, '#F44336')
                    borde_color = "#FFFFFF"
                    borde_ancho = 3
            else:
                color = colores_normal.get(elemento, '#555555')
                borde_color = "#888888" if not es_tope else "#FFFFFF"
                borde_ancho = 1 if not es_tope else 2
            
            # Fondo del elemento
            self.canvas_pila.create_rectangle(
                start_x, y - box_height,
                start_x + box_width, y,
                fill=color,
                outline=borde_color,
                width=borde_ancho
            )
            
            # Texto del elemento
            self.canvas_pila.create_text(
                start_x + box_width/2, y - box_height/2,
                text=elemento.upper(),
                fill="#FFFFFF",
                font=("Courier New", 11, "bold")
            )
            
            # Indicador de tope
            if es_tope:
                self.canvas_pila.create_text(
                    start_x - 10, y - box_height/2,
                    text="▶",
                    fill=self.col_pink,
                    font=("Arial", 10, "bold"),
                    anchor="e"
                )

    def snapshot_anterior(self):
        """Retrocede un paso en el historial de la pila"""
        if self.snapshot_actual > 0:
            self.snapshot_actual -= 1
            self.actualizar_snapshot()
    
    def snapshot_siguiente(self):
        """Avanza un paso en el historial de la pila"""
        if self.snapshot_actual < len(self.scanner.automata.snapshots) - 1:
            self.snapshot_actual += 1
            self.actualizar_snapshot()
    
    def actualizar_snapshot(self):
        """Actualiza la visualización según el snapshot actual"""
        if not self.scanner.automata.snapshots:
            return
        
        snapshot = self.scanner.automata.snapshots[self.snapshot_actual]
        operacion = snapshot['operacion']
        elemento = snapshot['elemento']
        linea = snapshot['linea']
        
        # Dibujar la pila con información del snapshot
        self.dibujar_pila(snapshot['pila'], snapshot)
        
        # Actualizar label de operación con línea y color
        if operacion == 'PUSH':
            color = "#4CAF50"  # Verde
            simbolo = "⬇"
        else:
            color = "#F44336"  # Rojo
            simbolo = "⬆"
        
        texto_operacion = f"{simbolo} Línea {linea}: {operacion} '{elemento}'"
        self.label_operacion.configure(text=texto_operacion, text_color=color)
        
        # Actualizar contador
        total = len(self.scanner.automata.snapshots)
        self.label_snapshot.configure(text=f"Paso: {self.snapshot_actual + 1}/{total}")

    def crear_area_principal(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        self.main_area.columnconfigure(0, weight=2)
        self.main_area.columnconfigure(1, weight=3) 
        self.main_area.rowconfigure(0, weight=1)

        self.editor_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.editor_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        ctk.CTkLabel(self.editor_frame, text="💻 SOURCE CODE", font=("Consolas", 14, "bold"), text_color=self.col_pink).pack(anchor="w", pady=(0,5))
        self.text_codigo = ctk.CTkTextbox(self.editor_frame, font=("Consolas", 13), fg_color="#0F0F0F", 
                                          text_color="#E6E6E6", border_width=1, border_color="#333333")
        self.text_codigo.pack(fill="both", expand=True)

        self.results_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.results_frame.grid(row=0, column=1, sticky="nsew")

        self.tabview = ctk.CTkTabview(self.results_frame, segmented_button_selected_color=self.col_pink, 
                                      segmented_button_selected_hover_color="#D42650", height=40)
        self.tabview.pack(fill="both", expand=True)

        self.tab_dash = self.tabview.add("DASHBOARD")   
        self.tab_exp = self.tabview.add("EXPLORADOR")   
        self.tab_det = self.tabview.add("DETALLE LÍNEA A LÍNEA")
        self.tab_pila = self.tabview.add("HISTORIAL PILA")
        self.tab_err = self.tabview.add("ERRORES SINTÁCTICOS")
        self.tab_visual = self.tabview.add("VISUALIZACIÓN ANIMADA")

        self.build_dashboard_tab()
        self.build_explorer_tab()
        self.build_detail_tab()
        self.build_pila_tab()
        self.build_error_tab()
        self.build_visualization_tab()

    def build_visualization_tab(self):
        """Pestaña con visualización animada de la pila"""
        viz_frame = ctk.CTkFrame(self.tab_visual, fg_color="transparent")
        viz_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Canvas grande para visualización
        self.canvas_animado = tk.Canvas(
            viz_frame,
            bg="#0D1117",
            highlightthickness=0
        )
        self.canvas_animado.pack(fill="both", expand=True, side="left")
        
        # Panel de control lateral
        control_panel = ctk.CTkFrame(viz_frame, width=200, fg_color=self.col_card)
        control_panel.pack(fill="y", side="right", padx=(10, 0))
        
        ctk.CTkLabel(
            control_panel,
            text="🎬 Control de Animación",
            font=("Segoe UI", 12, "bold")
        ).pack(pady=20)
        
        self.btn_play = ctk.CTkButton(
            control_panel,
            text="▶ Play",
            command=self.play_animation,
            fg_color=self.col_pink,
            hover_color="#D42650",
            height=40
        )
        self.btn_play.pack(pady=10, padx=20, fill="x")
        
        self.btn_pause = ctk.CTkButton(
            control_panel,
            text="⏸ Pause",
            command=self.pause_animation,
            fg_color="#555555",
            hover_color="#666666",
            height=40
        )
        self.btn_pause.pack(pady=10, padx=20, fill="x")
        
        self.btn_reset = ctk.CTkButton(
            control_panel,
            text="⏮ Reset",
            command=self.reset_animation,
            fg_color="#555555",
            hover_color="#666666",
            height=40
        )
        self.btn_reset.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            control_panel,
            text="Velocidad:",
            font=("Segoe UI", 11)
        ).pack(pady=(20, 5))
        
        self.speed_slider = ctk.CTkSlider(
            control_panel,
            from_=0.1,
            to=2.0,
            number_of_steps=19,
            command=self.cambiar_velocidad
        )
        self.speed_slider.set(1.0)
        self.speed_slider.pack(pady=5, padx=20, fill="x")
        
        self.speed_label = ctk.CTkLabel(
            control_panel,
            text="1.0x",
            font=("Courier New", 10)
        )
        self.speed_label.pack()
        
        # Info del snapshot actual
        ctk.CTkLabel(
            control_panel,
            text="Estado Actual:",
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(30, 10))
        
        self.info_snapshot = ctk.CTkTextbox(
            control_panel,
            height=150,
            fg_color="#0F0F0F",
            font=("Courier New", 9)
        )
        self.info_snapshot.pack(pady=5, padx=20, fill="x")
        
        self.animating = False
        self.animation_speed = 1000  # ms

    def dibujar_pila_animada(self, snapshot_idx):
        """Dibuja la pila en el canvas animado de manera más elaborada"""
        self.canvas_animado.delete("all")
        
        if snapshot_idx >= len(self.scanner.automata.snapshots):
            return
        
        snapshot = self.scanner.automata.snapshots[snapshot_idx]
        pila = snapshot['pila']
        operacion = snapshot['operacion']
        elemento = snapshot['elemento']
        linea = snapshot['linea']
        
        # Actualizar info
        self.info_snapshot.delete("1.0", tk.END)
        info = f"Operación: {operacion}\n"
        info += f"Elemento: '{elemento}'\n"
        info += f"Línea: {linea}\n"
        info += f"Pila actual: {pila}\n"
        info += f"Profundidad: {len(pila)}"
        self.info_snapshot.insert("1.0", info)
        
        if not pila:
            self.canvas_animado.create_text(
                400, 300,
                text="PILA VACÍA",
                fill="#666666",
                font=("Arial", 24, "bold")
            )
            return
        
        # Configuración mejorada
        canvas_width = self.canvas_animado.winfo_width()
        canvas_height = self.canvas_animado.winfo_height()
        
        if canvas_width < 10:  # Canvas no inicializado aún
            canvas_width = 800
            canvas_height = 600
        
        box_width = 200
        box_height = 50
        spacing = 10
        start_x = (canvas_width - box_width) / 2
        start_y = canvas_height - 50
        
        colores = {
            'if': '#C678DD',
            'while': '#61AFEF'
        }
        
        # Dibujar cada elemento
        for i, elem in enumerate(pila):
            y = start_y - (i * (box_height + spacing))
            color = colores.get(elem, '#555555')
            
            # Sombra
            self.canvas_animado.create_rectangle(
                start_x + 3, y - box_height + 3,
                start_x + box_width + 3, y + 3,
                fill="#000000",
                outline=""
            )
            
            # Caja principal
            self.canvas_animado.create_rectangle(
                start_x, y - box_height,
                start_x + box_width, y,
                fill=color,
                outline="#FFFFFF",
                width=3
            )
            
            # Texto
            self.canvas_animado.create_text(
                start_x + box_width/2, y - box_height/2,
                text=elem.upper(),
                fill="#FFFFFF",
                font=("Arial", 16, "bold")
            )
            
            # Indicador de tope
            if i == len(pila) - 1:
                self.canvas_animado.create_text(
                    start_x - 15, y - box_height/2,
                    text="▶",
                    fill=self.col_pink,
                    font=("Arial", 20, "bold"),
                    anchor="e"
                )
                
                self.canvas_animado.create_text(
                    start_x + box_width + 15, y - box_height/2,
                    text="TOPE",
                    fill=self.col_pink,
                    font=("Arial", 12, "bold"),
                    anchor="w"
                )
        
        # Indicador de operación
        if operacion == 'PUSH':
            op_color = "#4CAF50"
            op_text = f"⬇ PUSH '{elemento}'"
        else:
            op_color = "#F44336"
            op_text = f"⬆ POP '{elemento}'"
        
        self.canvas_animado.create_text(
            canvas_width / 2, 30,
            text=op_text,
            fill=op_color,
            font=("Arial", 18, "bold")
        )
        
        # Número de snapshot
        self.canvas_animado.create_text(
            canvas_width - 50, canvas_height - 20,
            text=f"{snapshot_idx + 1}/{len(self.scanner.automata.snapshots)}",
            fill="#666666",
            font=("Courier New", 10)
        )

    def play_animation(self):
        """Inicia la animación automática"""
        self.animating = True
        self.snapshot_actual = 0
        self.animar_paso()
    
    def pause_animation(self):
        """Pausa la animación"""
        self.animating = False
    
    def reset_animation(self):
        """Reinicia la animación al inicio"""
        self.animating = False
        self.snapshot_actual = 0
        if self.scanner.automata.snapshots:
            self.dibujar_pila_animada(0)
    
    def animar_paso(self):
        """Avanza un paso en la animación"""
        if not self.animating:
            return
        
        if self.snapshot_actual < len(self.scanner.automata.snapshots):
            self.dibujar_pila_animada(self.snapshot_actual)
            self.snapshot_actual += 1
            self.after(self.animation_speed, self.animar_paso)
        else:
            self.animating = False
    
    def cambiar_velocidad(self, valor):
        """Cambia la velocidad de la animación"""
        self.animation_speed = int(1000 / float(valor))
        self.speed_label.configure(text=f"{float(valor):.1f}x")

    def build_dashboard_tab(self):
        self.scroll_dash = ctk.CTkScrollableFrame(self.tab_dash, fg_color="transparent")
        self.scroll_dash.pack(fill="both", expand=True)
        self.scroll_dash.columnconfigure((0,1), weight=1) 

        self.dash_config = [
            ("PALABRAS RESERVADAS", "🔑", self.dash_colors["keywords"], "palabras reservadas"),
            ("VARIABLES", "📝", self.dash_colors["vars"], "variables"),
            ("NÚMEROS ENTEROS", "🔢", self.dash_colors["ints"], "enteros"),
            ("REALES", "💧", self.dash_colors["floats"], "reales"),
            ("OPERADORES", "⚙️", self.dash_colors["ops"], "operadores"),
            ("AGRUPACIÓN", "📦", self.dash_colors["group"], "agrupacion"),
            ("CADENAS", "💬", self.dash_colors["strings"], "cadenas"),
            ("TOTAL TOKENS", "∑", self.dash_colors["total"], "total"),
            ("ERRORES SINTÁCTICOS", "⚠️", self.dash_colors["errores"], "errores")
        ]
        
        self.dash_widgets = {}

        for i, (titulo, icono, color, key) in enumerate(self.dash_config):
            card = ctk.CTkFrame(self.scroll_dash, fg_color=self.col_card, corner_radius=15, border_width=1, border_color="#333333")
            card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")
            
            header = ctk.CTkFrame(card, fg_color="transparent")
            header.pack(fill="x", padx=15, pady=(15, 5))
            ctk.CTkLabel(header, text=icono, font=("Segoe UI Emoji", 24)).pack(side="left")
            ctk.CTkLabel(header, text=f"  {titulo}", font=("Segoe UI", 12, "bold"), text_color="#AAAAAA").pack(side="left")
            
            num_lbl = ctk.CTkLabel(card, text="0", font=("Segoe UI", 40, "bold"), text_color=color)
            num_lbl.pack(pady=(0, 15))
            
            self.dash_widgets[key] = num_lbl

    def build_explorer_tab(self):
        self.scroll_exp = ctk.CTkScrollableFrame(self.tab_exp, fg_color="transparent")
        self.scroll_exp.pack(fill="both", expand=True)
        
        self.exp_widgets = {}
        cats = [
            ("PALABRAS RESERVADAS", "palabras", self.dash_colors["keywords"]),
            ("VARIABLES", "variables", self.dash_colors["vars"]),
            ("ENTEROS", "enteros", self.dash_colors["ints"]),
            ("REALES", "reales", self.dash_colors["floats"]),
            ("OPERADORES", "operadores", self.dash_colors["ops"]),
            ("AGRUPACIÓN", "agrupacion", self.dash_colors["group"]),
            ("CADENAS", "cadenas", self.dash_colors["strings"])
        ]

        for nombre, key, color in cats:
            frame = ctk.CTkFrame(self.scroll_exp, fg_color=self.col_card, corner_radius=10)
            frame.pack(fill="x", pady=5, padx=5)
            
            head = ctk.CTkFrame(frame, fg_color="transparent")
            head.pack(fill="x", padx=10, pady=10)
            ctk.CTkLabel(head, text=nombre, font=("Segoe UI", 11, "bold"), text_color="#CCCCCC").pack(side="left")
            count = ctk.CTkLabel(head, text="0", font=("Segoe UI", 16, "bold"), text_color=color)
            count.pack(side="right")
            
            txt = ctk.CTkTextbox(frame, height=0, fg_color="#151515", text_color="#DDDDDD", font=("Consolas", 11))
            txt.pack(fill="x", padx=10, pady=(0, 5))
            
            self.exp_widgets[key] = {"count": count, "list": txt}

    def build_detail_tab(self):
        self.text_detail = ctk.CTkTextbox(self.tab_det, fg_color="#0D1117", text_color="#C9D1D9", font=("Consolas", 12))
        self.text_detail.pack(fill="both", expand=True)
        self.text_detail.insert("1.0", "Esperando análisis...")

    def build_pila_tab(self):
        self.text_historial_pila = ctk.CTkTextbox(self.tab_pila, fg_color="#0D1117", text_color="#C9D1D9", font=("Consolas", 11))
        self.text_historial_pila.pack(fill="both", expand=True)
        self.text_historial_pila.insert("1.0", "Esperando análisis...")

    def build_error_tab(self):
        self.text_errores = ctk.CTkTextbox(self.tab_err, fg_color="#0D1117", text_color="#FF6B6B", font=("Consolas", 12))
        self.text_errores.pack(fill="both", expand=True)
        self.text_errores.insert("1.0", "Esperando análisis...")

    def abrir_archivo(self):
        filename = filedialog.askopenfilename(filetypes=[("C Files", "*.c"), ("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename:
            self.archivo_actual = filename
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.text_codigo.delete("1.0", tk.END)
                    self.text_codigo.insert("1.0", f.read())
            except: pass

    def analizar(self):
        if not self.archivo_actual:
            content = self.text_codigo.get("1.0", tk.END).strip()
            if not content: return
            with open("temp.c", "w", encoding="utf-8") as f: f.write(content)
            self.archivo_actual = "temp.c"
            
        if self.scanner.procesar_archivo(self.archivo_actual):
            self.actualizar_dashboard()
            self.actualizar_explorador()
            self.actualizar_detalle()
            self.actualizar_historial_pila()
            self.actualizar_errores()
            self.snapshot_actual = 0
            
            if self.scanner.automata.snapshots:
                self.actualizar_snapshot()  # Actualizar la pila del sidebar
                self.dibujar_pila_animada(0)  # Actualizar la visualización grande
            else:
                self.dibujar_pila()
                self.label_snapshot.configure(text="Sin datos")
            
            self.tabview.set("DASHBOARD")
            
            # Mostrar mensaje según resultado
            if len(self.scanner.automata.errores) == 0:
                messagebox.showinfo(
                    "Análisis Completado",
                    "✅ El código es sintácticamente correcto\n"
                    "Todos los bloques están balanceados correctamente"
                )
            else:
                messagebox.showwarning(
                    "Errores Encontrados",
                    f"⚠️ Se encontraron {len(self.scanner.automata.errores)} errores sintácticos\n"
                    "Revisa la pestaña 'ERRORES SINTÁCTICOS'"
                )

    def actualizar_dashboard(self):
        self.dash_widgets["palabras reservadas"].configure(text=str(len(self.scanner.palabras_reservadas_encontradas)))
        self.dash_widgets["variables"].configure(text=str(len(self.scanner.variables)))
        self.dash_widgets["enteros"].configure(text=str(len(self.scanner.enteros)))
        self.dash_widgets["reales"].configure(text=str(len(self.scanner.reales)))
        self.dash_widgets["operadores"].configure(text=str(len(self.scanner.operadores_encontrados)))
        self.dash_widgets["agrupacion"].configure(text=str(len(self.scanner.agrupaciones_encontradas)))
        self.dash_widgets["cadenas"].configure(text=str(len(self.scanner.cadenas_encontradas)))
        self.dash_widgets["total"].configure(text=str(len(self.scanner.tokens)))
        self.dash_widgets["errores"].configure(text=str(len(self.scanner.automata.errores)))

    def actualizar_explorador(self):
        data = {
            "palabras": self.scanner.palabras_reservadas_encontradas,
            "variables": self.scanner.variables,
            "enteros": self.scanner.enteros,
            "reales": self.scanner.reales,
            "operadores": self.scanner.operadores_encontrados,
            "agrupacion": self.scanner.agrupaciones_encontradas,
            "cadenas": self.scanner.cadenas_encontradas
        }
        for key, lista in data.items():
            cnt = len(lista)
            self.exp_widgets[key]["count"].configure(text=str(cnt))
            txt = self.exp_widgets[key]["list"]
            txt.delete("1.0", tk.END)
            if cnt > 0:
                vals = [str(x[0]) for x in lista]
                txt.configure(height=80)
                txt.insert("1.0", ", ".join(vals))
            else:
                txt.configure(height=0)

    def actualizar_detalle(self):
        self.text_detail.delete("1.0", tk.END)
        head = f"{'TIPO':<20} | {'VALOR':<30} | {'LÍNEA':<5}\n" + ("-"*65) + "\n"
        self.text_detail.insert("1.0", head)
        for t, v, l in self.scanner.tokens:
            self.text_detail.insert(tk.END, f"{t:<20} | {str(v):<30} | {str(l):<5}\n")

    def actualizar_historial_pila(self):
        self.text_historial_pila.delete("1.0", tk.END)
        if self.scanner.automata.historial_pila:
            for entrada in self.scanner.automata.historial_pila:
                self.text_historial_pila.insert(tk.END, entrada + "\n")
        else:
            self.text_historial_pila.insert("1.0", "No hay operaciones en la pila")

    def actualizar_errores(self):
        self.text_errores.delete("1.0", tk.END)
        if self.scanner.automata.errores:
            for error in self.scanner.automata.errores:
                self.text_errores.insert(tk.END, "❌ " + error + "\n\n")
        else:
            self.text_errores.insert("1.0", "✅ No se encontraron errores sintácticos\n\nTodos los bloques están correctamente balanceados.")

    def limpiar(self):
        self.text_codigo.delete("1.0", tk.END)
        self.text_detail.delete("1.0", tk.END)
        self.text_historial_pila.delete("1.0", tk.END)
        self.text_errores.delete("1.0", tk.END)
        self.info_snapshot.delete("1.0", tk.END)
        self.canvas_pila.delete("all")
        self.canvas_animado.delete("all")
        self.archivo_actual = None
        self.scanner.reset()
        self.snapshot_actual = 0
        self.animating = False
        for w in self.dash_widgets.values(): w.configure(text="0")
        for k in self.exp_widgets:
            self.exp_widgets[k]["count"].configure(text="0")
            self.exp_widgets[k]["list"].configure(height=0)
        self.label_snapshot.configure(text="Línea --")
        self.dibujar_pila()

def main():
    scanner_logica = CScanner() 
    app = ScannerGUI(scanner_logica)
    app.mainloop()


if __name__ == "__main__":
    main()