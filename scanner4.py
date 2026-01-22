import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox


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
    
    def es_palabra_reservada(self, palabra):
        if palabra == "auto":
            return True
        elif palabra == "break":
            return True
        elif palabra == "case":
            return True
        elif palabra == "char":
            return True
        elif palabra == "const":
            return True
        elif palabra == "continue":
            return True
        elif palabra == "default":
            return True
        elif palabra == "do":
            return True
        elif palabra == "double":
            return True
        elif palabra == "else":
            return True
        elif palabra == "enum":
            return True
        elif palabra == "extern":
            return True
        elif palabra == "float":
            return True
        elif palabra == "for":
            return True
        elif palabra == "goto":
            return True
        elif palabra == "if":
            return True
        elif palabra == "int":
            return True
        elif palabra == "long":
            return True
        elif palabra == "register":
            return True
        elif palabra == "return":
            return True
        elif palabra == "short":
            return True
        elif palabra == "signed":
            return True
        elif palabra == "sizeof":
            return True
        elif palabra == "static":
            return True
        elif palabra == "struct":
            return True
        elif palabra == "switch":
            return True
        elif palabra == "typedef":
            return True
        elif palabra == "union":
            return True
        elif palabra == "unsigned":
            return True
        elif palabra == "void":
            return True
        elif palabra == "volatile":
            return True
        elif palabra == "while":
            return True
        elif palabra == "_Packed":
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
            self.palabras_reservadas_encontradas.append((palabra, numero_linea))
            self.tokens.append(('PALABRA_RESERVADA', palabra, numero_linea))
            self.contador_palabras_reservadas += 1
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


class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("C Lexical Analyzer Pro")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0d1117')
        self.centrar_ventana()
        self.scanner = CScanner()
        self.archivo_actual = None
        self.crear_interfaz()
    
    def centrar_ventana(self):
        self.root.update_idletasks()
        width = 1400
        height = 900
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        # Colores modernos premium
        bg_primary = '#0d1117'
        bg_secondary = '#161b22'
        bg_tertiary = '#21262d'
        bg_card = '#1c2128'
        accent_blue = '#58a6ff'
        accent_green = '#3fb950'
        accent_orange = '#f78166'
        accent_purple = '#bc8cff'
        text_primary = '#f0f6fc'
        text_secondary = '#8b949e'
        border_color = '#30363d'
        
        # Frame principal con gradiente simulado
        main_container = tk.Frame(self.root, bg=bg_primary)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header superior moderno
        header = tk.Frame(main_container, bg=bg_secondary, height=120)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Logo y título
        title_container = tk.Frame(header, bg=bg_secondary)
        title_container.pack(expand=True)
        
        # Icono grande
        icon_label = tk.Label(title_container, text="⚡", bg=bg_secondary, 
                             fg=accent_blue, font=('Segoe UI', 48))
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Títulos
        text_container = tk.Frame(title_container, bg=bg_secondary)
        text_container.pack(side=tk.LEFT)
        
        title = tk.Label(text_container, text="C Lexical Analyzer Pro", 
                        bg=bg_secondary, fg=text_primary,
                        font=('Segoe UI', 32, 'bold'))
        title.pack(anchor='w')
        
        subtitle = tk.Label(text_container, text="Advanced Token Recognition Engine • Character-by-Character Analysis", 
                           bg=bg_secondary, fg=text_secondary,
                           font=('Segoe UI', 11))
        subtitle.pack(anchor='w')
        
        # Barra de acción moderna
        action_bar = tk.Frame(main_container, bg=bg_tertiary, height=80)
        action_bar.pack(fill=tk.X, padx=0, pady=0)
        action_bar.pack_propagate(False)
        
        action_content = tk.Frame(action_bar, bg=bg_tertiary)
        action_content.pack(expand=True)
        
        # Botones con estilo moderno
        btn_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'relief': tk.FLAT,
            'cursor': 'hand2',
            'padx': 30,
            'pady': 12,
            'borderwidth': 0
        }
        
        self.btn_abrir = tk.Button(action_content, text="📂  Open File", 
                                   command=self.abrir_archivo,
                                   bg=accent_blue, fg='#ffffff',
                                   activebackground='#4a8fd9',
                                   **btn_style)
        self.btn_abrir.pack(side=tk.LEFT, padx=8)
        
        self.btn_analizar = tk.Button(action_content, text="▶  Analyze", 
                                      command=self.analizar,
                                      bg=accent_green, fg='#ffffff',
                                      state=tk.DISABLED,
                                      activebackground='#2f9142',
                                      disabledforeground='#6e7681',
                                      **btn_style)
        self.btn_analizar.pack(side=tk.LEFT, padx=8)
        
        self.btn_limpiar = tk.Button(action_content, text="🗑  Clear", 
                                     command=self.limpiar,
                                     bg=accent_orange, fg='#ffffff',
                                     activebackground='#d66952',
                                     **btn_style)
        self.btn_limpiar.pack(side=tk.LEFT, padx=8)
        
        # Separador visual
        sep = tk.Frame(action_content, bg=border_color, width=2, height=40)
        sep.pack(side=tk.LEFT, padx=20)
        
        # Indicador de archivo
        file_indicator = tk.Frame(action_content, bg=bg_tertiary)
        file_indicator.pack(side=tk.LEFT, padx=10)
        
        file_icon = tk.Label(file_indicator, text="📄", bg=bg_tertiary, 
                           font=('Segoe UI', 16))
        file_icon.pack(side=tk.LEFT, padx=(0, 8))
        
        self.label_archivo = tk.Label(file_indicator, text="No file loaded", 
                                      bg=bg_tertiary, fg=text_secondary,
                                      font=('Segoe UI', 10))
        self.label_archivo.pack(side=tk.LEFT)
        
        # Contenedor principal con padding
        workspace = tk.Frame(main_container, bg=bg_primary)
        workspace.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Panel izquierdo - Editor de código
        left_section = tk.Frame(workspace, bg=bg_primary)
        left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Header del editor
        editor_header = tk.Frame(left_section, bg=bg_card, height=50)
        editor_header.pack(fill=tk.X)
        editor_header.pack_propagate(False)
        
        editor_title_frame = tk.Frame(editor_header, bg=bg_card)
        editor_title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        editor_icon = tk.Label(editor_title_frame, text="</> ", 
                              bg=bg_card, fg=accent_purple,
                              font=('Segoe UI', 14, 'bold'))
        editor_icon.pack(side=tk.LEFT)
        
        editor_label = tk.Label(editor_title_frame, text="Source Code", 
                               bg=bg_card, fg=text_primary,
                               font=('Segoe UI', 12, 'bold'))
        editor_label.pack(side=tk.LEFT)
        
        # Línea decorativa
        tk.Frame(left_section, bg=accent_blue, height=2).pack(fill=tk.X)
        
        # Área de código con números de línea simulados
        code_container = tk.Frame(left_section, bg=bg_secondary)
        code_container.pack(fill=tk.BOTH, expand=True)
        
        self.text_codigo = scrolledtext.ScrolledText(
            code_container, 
            wrap=tk.NONE,
            bg=bg_secondary, 
            fg='#c9d1d9',
            font=('Consolas', 11),
            insertbackground=accent_blue,
            relief=tk.FLAT, 
            padx=15, 
            pady=15,
            selectbackground=accent_blue,
            selectforeground='#ffffff',
            borderwidth=0,
            highlightthickness=0
        )
        self.text_codigo.pack(fill=tk.BOTH, expand=True)
        
        # Panel derecho - Resultados
        right_section = tk.Frame(workspace, bg=bg_primary, width=550)
        right_section.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        right_section.pack_propagate(False)
        
        # Header de resultados
        results_header = tk.Frame(right_section, bg=bg_card, height=50)
        results_header.pack(fill=tk.X)
        results_header.pack_propagate(False)
        
        results_title_frame = tk.Frame(results_header, bg=bg_card)
        results_title_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        results_icon = tk.Label(results_title_frame, text="📊 ", 
                               bg=bg_card, fg=accent_green,
                               font=('Segoe UI', 14, 'bold'))
        results_icon.pack(side=tk.LEFT)
        
        results_label = tk.Label(results_title_frame, text="Analysis Results", 
                                bg=bg_card, fg=text_primary,
                                font=('Segoe UI', 12, 'bold'))
        results_label.pack(side=tk.LEFT)
        
        # Línea decorativa
        tk.Frame(right_section, bg=accent_green, height=2).pack(fill=tk.X)
        
        # Panel de estadísticas con cards
        stats_container = tk.Frame(right_section, bg=bg_primary)
        stats_container.pack(fill=tk.X, padx=15, pady=20)
        
        self.stats_labels = {}
        
        stats_config = [
            ("Keywords", "palabras_reservadas", accent_purple, "🔑"),
            ("Variables", "variables", accent_blue, "📝"),
            ("Integers", "enteros", accent_green, "🔢"),
            ("Floats", "reales", accent_green, "🔢"),
            ("Operators", "operadores", accent_orange, "⚙️"),
            ("Grouping", "agrupaciones", "#e3b341", "{ }"),
            ("Strings", "cadenas", "#a5d6ff", "\" \""),
            ("Total Tokens", "total", text_primary, "∑")
        ]
        
        # Grid de 2 columnas
        for idx, (nombre, key, color, icon) in enumerate(stats_config):
            row = idx // 2
            col = idx % 2
            
            stat_card = tk.Frame(stats_container, bg=bg_card, 
                               highlightbackground=border_color,
                               highlightthickness=1)
            stat_card.grid(row=row, column=col, padx=6, pady=6, sticky='ew')
            
            # Contenido del card
            card_content = tk.Frame(stat_card, bg=bg_card)
            card_content.pack(fill=tk.BOTH, padx=15, pady=12)
            
            # Icono y nombre
            top_row = tk.Frame(card_content, bg=bg_card)
            top_row.pack(fill=tk.X)
            
            icon_label = tk.Label(top_row, text=icon, bg=bg_card, 
                                 font=('Segoe UI', 16))
            icon_label.pack(side=tk.LEFT, padx=(0, 8))
            
            name_label = tk.Label(top_row, text=nombre, bg=bg_card, 
                                 fg=text_secondary,
                                 font=('Segoe UI', 9))
            name_label.pack(side=tk.LEFT, anchor='w')
            
            # Valor
            value_label = tk.Label(card_content, text="0", bg=bg_card, 
                                  fg=color,
                                  font=('Segoe UI', 24, 'bold'),
                                  anchor='w')
            value_label.pack(fill=tk.X, pady=(5, 0))
            
            self.stats_labels[key] = value_label
        
        # Configurar grid
        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)
        
        # Área de detalles con tabs modernos
        details_section = tk.Frame(right_section, bg=bg_primary)
        details_section.pack(fill=tk.BOTH, expand=True, padx=15, pady=(10, 15))
        
        # Tabs header
        tabs_header = tk.Frame(details_section, bg=bg_secondary)
        tabs_header.pack(fill=tk.X)
        
        self.current_tab = tk.StringVar(value="all")
        self.tab_buttons = {}
        
        tab_buttons_config = [
            ("All Tokens", "all"),
            ("Keywords", "keywords"),
            ("Variables", "variables"),
            ("Numbers", "numbers"),
            ("Operators", "operators"),
            ("Grouping", "grouping"),
            ("Strings", "strings")
        ]
        
        for text, value in tab_buttons_config:
            btn = tk.Button(
                tabs_header,
                text=text,
                bg=bg_tertiary if value == "all" else bg_secondary,
                fg=text_primary if value == "all" else text_secondary,
                font=('Segoe UI', 9, 'bold' if value == "all" else 'normal'),
                relief=tk.FLAT,
                cursor='hand2',
                padx=15,
                pady=10,
                borderwidth=0,
                activebackground=bg_tertiary,
                command=lambda v=value, t=text: self.cambiar_tab(v, t)
            )
            btn.pack(side=tk.LEFT)
            self.tab_buttons[value] = btn
        
        # Área de resultados detallados
        details_card = tk.Frame(details_section, bg=bg_card,
                               highlightbackground=border_color,
                               highlightthickness=1)
        details_card.pack(fill=tk.BOTH, expand=True)
        
        self.text_resultados = scrolledtext.ScrolledText(
            details_card,
            wrap=tk.WORD,
            bg=bg_secondary,
            fg='#c9d1d9',
            font=('Consolas', 10),
            relief=tk.FLAT,
            padx=15,
            pady=15,
            selectbackground=accent_blue,
            selectforeground='#ffffff',
            borderwidth=0,
            highlightthickness=0
        )
        self.text_resultados.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags con colores modernos
        self.text_resultados.tag_configure("header", 
            foreground=accent_orange, 
            font=('Consolas', 11, 'bold'))
        self.text_resultados.tag_configure("keyword", 
            foreground=accent_purple)
        self.text_resultados.tag_configure("variable", 
            foreground=accent_blue)
        self.text_resultados.tag_configure("number", 
            foreground=accent_green)
        self.text_resultados.tag_configure("operator", 
            foreground='#c9d1d9')
        self.text_resultados.tag_configure("agrupacion",
            foreground='#e3b341')
        self.text_resultados.tag_configure("cadena",
            foreground='#a5d6ff')
        self.text_resultados.tag_configure("line", 
            foreground=text_secondary)
        self.text_resultados.tag_configure("token_type",
            foreground=text_secondary,
            font=('Consolas', 9))
    
    def cambiar_tab(self, tab_name, tab_text):
        """Cambia entre diferentes vistas de resultados"""
        # Guardar colores
        bg_secondary = '#161b22'
        bg_tertiary = '#21262d'
        text_primary = '#f0f6fc'
        text_secondary = '#8b949e'
        
        # Actualizar estilo de todos los botones
        for key, btn in self.tab_buttons.items():
            if key == tab_name:
                btn.config(bg=bg_tertiary, fg=text_primary, font=('Segoe UI', 9, 'bold'))
            else:
                btn.config(bg=bg_secondary, fg=text_secondary, font=('Segoe UI', 9, 'normal'))
        
        self.current_tab.set(tab_name)
        
        # Filtrar y mostrar resultados según el tab
        self.filtrar_resultados(tab_name)
    
    def filtrar_resultados(self, filtro):
        """Filtra y muestra los tokens según la categoría seleccionada"""
        if not hasattr(self.scanner, 'tokens') or not self.scanner.tokens:
            return
        
        self.text_resultados.delete(1.0, tk.END)
        
        if filtro == "all":
            # Mostrar todos los tokens
            self.text_resultados.insert(tk.END, "═" * 60 + "\n", "header")
            self.text_resultados.insert(tk.END, "  TOKEN SEQUENCE (ALL)\n", "header")
            self.text_resultados.insert(tk.END, "═" * 60 + "\n\n", "header")
            
            for i, (tipo, valor, linea) in enumerate(self.scanner.tokens, 1):
                self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                
                tipo_map = {
                    "PALABRA_RESERVADA": "KEYWORD",
                    "VARIABLE": "VAR    ",
                    "ENTERO": "INT    ",
                    "REAL": "FLOAT  ",
                    "OPERADOR": "OPER   ",
                    "AGRUPACION": "GROUP  ",
                    "CADENA": "STRING "
                }
                tipo_corto = tipo_map.get(tipo, tipo.ljust(7))
                self.text_resultados.insert(tk.END, f"[{tipo_corto}]  ", "token_type")
                
                tag = self.obtener_tag_por_tipo(tipo)
                self.text_resultados.insert(tk.END, f"{valor}", tag)
                self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
        
        elif filtro == "keywords":
            self.text_resultados.insert(tk.END, "═" * 60 + "\n", "header")
            self.text_resultados.insert(tk.END, f"  KEYWORDS ({len(self.scanner.palabras_reservadas_encontradas)})\n", "header")
            self.text_resultados.insert(tk.END, "═" * 60 + "\n\n", "header")
            
            if self.scanner.palabras_reservadas_encontradas:
                for i, (palabra, linea) in enumerate(self.scanner.palabras_reservadas_encontradas, 1):
                    self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                    self.text_resultados.insert(tk.END, f"{palabra}", "keyword")
                    self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
            else:
                self.text_resultados.insert(tk.END, "  No keywords found.\n", "line")
        
        elif filtro == "variables":
            self.text_resultados.insert(tk.END, "═" * 60 + "\n", "header")
            self.text_resultados.insert(tk.END, f"  VARIABLES ({len(self.scanner.variables)})\n", "header")
            self.text_resultados.insert(tk.END, "═" * 60 + "\n\n", "header")
            
            if self.scanner.variables:
                for i, (var, linea) in enumerate(self.scanner.variables, 1):
                    self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                    self.text_resultados.insert(tk.END, f"{var}", "variable")
                    self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
            else:
                self.text_resultados.insert(tk.END, "  No variables found.\n", "line")
        
        elif filtro == "numbers":
            total_nums = len(self.scanner.enteros) + len(self.scanner.reales)
            self.text_resultados.insert(tk.END, "═" * 60 + "\n", "header")
            self.text_resultados.insert(tk.END, f"  NUMBERS ({total_nums})\n", "header")
            self.text_resultados.insert(tk.END, "═" * 60 + "\n\n", "header")
            
            if self.scanner.enteros:
                self.text_resultados.insert(tk.END, "INTEGERS:\n", "header")
                for i, (num, linea) in enumerate(self.scanner.enteros, 1):
                    self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                    self.text_resultados.insert(tk.END, f"{num}", "number")
                    self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
                self.text_resultados.insert(tk.END, "\n")
            
            if self.scanner.reales:
                self.text_resultados.insert(tk.END, "FLOATS:\n", "header")
                for i, (num, linea) in enumerate(self.scanner.reales, 1):
                    self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                    self.text_resultados.insert(tk.END, f"{num}", "number")
                    self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
            
            if not self.scanner.enteros and not self.scanner.reales:
                self.text_resultados.insert(tk.END, "  No numbers found.\n", "line")
        
        elif filtro == "operators":
            self.text_resultados.insert(tk.END, "═" * 60 + "\n", "header")
            self.text_resultados.insert(tk.END, f"  OPERATORS ({len(self.scanner.operadores_encontrados)})\n", "header")
            self.text_resultados.insert(tk.END, "═" * 60 + "\n\n", "header")
            
            if self.scanner.operadores_encontrados:
                for i, (op, linea) in enumerate(self.scanner.operadores_encontrados, 1):
                    self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                    self.text_resultados.insert(tk.END, f"'{op}'", "operator")
                    self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
            else:
                self.text_resultados.insert(tk.END, "  No operators found.\n", "line")
        
        elif filtro == "grouping":
            self.text_resultados.insert(tk.END, "═" * 60 + "\n", "header")
            self.text_resultados.insert(tk.END, f"  GROUPING SYMBOLS ({len(self.scanner.agrupaciones_encontradas)})\n", "header")
            self.text_resultados.insert(tk.END, "═" * 60 + "\n\n", "header")
            
            if self.scanner.agrupaciones_encontradas:
                for i, (agrup, linea) in enumerate(self.scanner.agrupaciones_encontradas, 1):
                    self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                    self.text_resultados.insert(tk.END, f"'{agrup}'", "agrupacion")
                    self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
            else:
                self.text_resultados.insert(tk.END, "  No grouping symbols found.\n", "line")
        
        elif filtro == "strings":
            self.text_resultados.insert(tk.END, "═" * 60 + "\n", "header")
            self.text_resultados.insert(tk.END, f"  STRINGS ({len(self.scanner.cadenas_encontradas)})\n", "header")
            self.text_resultados.insert(tk.END, "═" * 60 + "\n\n", "header")
            
            if self.scanner.cadenas_encontradas:
                for i, (cadena, linea) in enumerate(self.scanner.cadenas_encontradas, 1):
                    self.text_resultados.insert(tk.END, f"{i:4d}  ", "line")
                    self.text_resultados.insert(tk.END, f"{cadena}", "cadena")
                    self.text_resultados.insert(tk.END, f"  (line {linea})\n", "line")
            else:
                self.text_resultados.insert(tk.END, "  No strings found.\n", "line")
    
    def obtener_tag_por_tipo(self, tipo):
        """Retorna el tag de color según el tipo de token"""
        if tipo == "PALABRA_RESERVADA":
            return "keyword"
        elif tipo == "VARIABLE":
            return "variable"
        elif tipo in ["ENTERO", "REAL"]:
            return "number"
        elif tipo == "AGRUPACION":
            return "agrupacion"
        elif tipo == "CADENA":
            return "cadena"
        else:
            return "operator"
    
    def abrir_archivo(self):
        filename = filedialog.askopenfilename(
            title="Select C Source File",
            filetypes=[("C Files", "*.c"), ("All Files", "*.*")]
        )
        
        if filename:
            self.archivo_actual = filename
            nombre_corto = filename.split('/')[-1]
            self.label_archivo.config(
                text=f"{nombre_corto}", 
                fg='#3fb950',
                font=('Segoe UI', 10, 'bold')
            )
            self.btn_analizar.config(state=tk.NORMAL, bg='#3fb950')
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                self.text_codigo.delete(1.0, tk.END)
                self.text_codigo.insert(1.0, contenido)
                
                # Mensaje de éxito temporal
                self.mostrar_notificacion("✓ File loaded successfully", "#3fb950")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file:\n{str(e)}")
    
    def mostrar_notificacion(self, mensaje, color):
        """Muestra una notificación temporal"""
        notif = tk.Label(self.root, text=mensaje, bg=color, fg='#ffffff',
                        font=('Segoe UI', 10, 'bold'), padx=20, pady=10)
        notif.place(relx=0.5, rely=0.95, anchor='center')
        self.root.after(2000, notif.destroy)
    
    def analizar(self):
        if not self.archivo_actual:
            messagebox.showwarning("Warning", "Please open a C file first")
            return
        
        # Animación de carga (simulada)
        self.btn_analizar.config(text="⟳  Analyzing...", state=tk.DISABLED)
        self.root.update()
        
        resultado = self.scanner.procesar_archivo(self.archivo_actual)
        
        if resultado:
            self.mostrar_resultados()
            self.btn_analizar.config(text="▶  Analyze", state=tk.NORMAL)
            self.mostrar_notificacion("✓ Analysis completed successfully", "#3fb950")
        else:
            self.btn_analizar.config(text="▶  Analyze", state=tk.NORMAL)
            messagebox.showerror("Error", "Analysis failed")
    
    def mostrar_resultados(self):
        # Animar actualización de estadísticas
        self.animar_contador("palabras_reservadas", self.scanner.contador_palabras_reservadas)
        self.animar_contador("variables", self.scanner.contador_variables)
        self.animar_contador("enteros", self.scanner.contador_enteros)
        self.animar_contador("reales", self.scanner.contador_reales)
        self.animar_contador("operadores", self.scanner.contador_operadores)
        self.animar_contador("agrupaciones", self.scanner.contador_agrupaciones)
        self.animar_contador("cadenas", self.scanner.contador_cadenas)
        self.animar_contador("total", len(self.scanner.tokens))
        
        # Resetear al tab "All Tokens"
        self.current_tab.set("all")
        
        # Actualizar estilo de tabs
        bg_secondary = '#161b22'
        bg_tertiary = '#21262d'
        text_primary = '#f0f6fc'
        text_secondary = '#8b949e'
        
        for key, btn in self.tab_buttons.items():
            if key == "all":
                btn.config(bg=bg_tertiary, fg=text_primary, font=('Segoe UI', 9, 'bold'))
            else:
                btn.config(bg=bg_secondary, fg=text_secondary, font=('Segoe UI', 9, 'normal'))
        
        # Mostrar todos los tokens por defecto
        self.filtrar_resultados("all")
    
    def animar_contador(self, key, valor_final):
        """Anima el contador de un valor a otro"""
        label = self.stats_labels[key]
        valor_actual = int(label.cget("text"))
        
        if valor_actual < valor_final:
            incremento = max(1, (valor_final - valor_actual) // 10)
            nuevo_valor = min(valor_actual + incremento, valor_final)
            label.config(text=str(nuevo_valor))
            if nuevo_valor < valor_final:
                self.root.after(20, lambda: self.animar_contador(key, valor_final))
        else:
            label.config(text=str(valor_final))
    
    def limpiar(self):
        self.text_codigo.delete(1.0, tk.END)
        self.text_resultados.delete(1.0, tk.END)
        self.archivo_actual = None
        self.label_archivo.config(text="No file loaded", fg='#8b949e', font=('Segoe UI', 10))
        self.btn_analizar.config(state=tk.DISABLED, bg='#21262d')
        
        for key in self.stats_labels:
            self.stats_labels[key].config(text="0")
        
        self.scanner.reset()
        self.mostrar_notificacion("✓ Workspace cleared", "#f78166")


def main():
    root = tk.Tk()
    app = ScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()