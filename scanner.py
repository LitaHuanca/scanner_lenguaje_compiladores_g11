import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

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

class ScannerGUI(ctk.CTk):
    def __init__(self, scanner_logic):
        super().__init__()
        self.scanner = scanner_logic
        self.archivo_actual = None
        
        self.title("Analizador sintáctico - Grupo 11")
        self.geometry("1400x900")

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
            "total": "#FF2E63" 
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

        self.build_dashboard_tab()

        self.build_explorer_tab()

        self.build_detail_tab()

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
            ("TOTAL TOKENS", "∑", self.dash_colors["total"], "total")
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

    def abrir_archivo(self):
        filename = filedialog.askopenfilename(filetypes=[("C Files", "*.c"), ("Text Files", "*.txt")])
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
            self.tabview.set("DASHBOARD")

    def actualizar_dashboard(self):
        # Mapeo directo
        self.dash_widgets["palabras reservadas"].configure(text=str(len(self.scanner.palabras_reservadas_encontradas)))
        self.dash_widgets["variables"].configure(text=str(len(self.scanner.variables)))
        self.dash_widgets["enteros"].configure(text=str(len(self.scanner.enteros)))
        self.dash_widgets["reales"].configure(text=str(len(self.scanner.reales)))
        self.dash_widgets["operadores"].configure(text=str(len(self.scanner.operadores_encontrados)))
        self.dash_widgets["agrupacion"].configure(text=str(len(self.scanner.agrupaciones_encontradas)))
        self.dash_widgets["cadenas"].configure(text=str(len(self.scanner.cadenas_encontradas)))
        self.dash_widgets["total"].configure(text=str(len(self.scanner.tokens)))

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

    def limpiar(self):
        self.text_codigo.delete("1.0", tk.END)
        self.text_detail.delete("1.0", tk.END)
        self.archivo_actual = None
        self.scanner.reset()
        for w in self.dash_widgets.values(): w.configure(text="0")
        for k in self.exp_widgets:
            self.exp_widgets[k]["count"].configure(text="0")
            self.exp_widgets[k]["list"].configure(height=0)
def main():
    scanner_logica = CScanner() 
    app = ScannerGUI(scanner_logica)
    app.mainloop()


if __name__ == "__main__":
    main()