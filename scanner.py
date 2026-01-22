# Scanner de Código C con Interfaz Gráfica
# Usa tkinter (incluido en Python estándar)

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox


class CScanner:
    def __init__(self):
        # Palabras reservadas de C según IBM
        self.palabras_reservadas = {
            'auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'int', 'long', 'register', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
            'unsigned', 'void', 'volatile', 'while', '_Packed'
        }
        
        # Operadores de C
        self.operadores = {
            '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
            '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '++', '--',
            '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=',
            '->', '.', '?', ':', ',', ';', '(', ')', '[', ']', '{', '}'
        }
        
        self.reset()
    
    def reset(self):
        """Reinicia todos los contadores y listas"""
        self.tokens = []
        self.variables = []
        self.palabras_reservadas_encontradas = []
        self.enteros = []
        self.reales = []
        self.operadores_encontrados = []
        
        self.contador_variables = 0
        self.contador_palabras_reservadas = 0
        self.contador_enteros = 0
        self.contador_reales = 0
        self.contador_operadores = 0
    
    def es_palabra_reservada(self, palabra):
        return palabra in self.palabras_reservadas
    
    def es_numero(self, cadena):
        """Verifica si es un número entero o real"""
        if not cadena:
            return None
        
        tiene_punto = False
        tiene_exponente = False
        
        i = 0
        if cadena[0] in ['+', '-']:
            i = 1
        
        if i >= len(cadena):
            return None
        
        while i < len(cadena):
            c = cadena[i]
            
            if c.isdigit():
                i += 1
            elif c == '.' and not tiene_punto and not tiene_exponente:
                tiene_punto = True
                i += 1
            elif c in ['e', 'E'] and not tiene_exponente:
                tiene_exponente = True
                i += 1
                if i < len(cadena) and cadena[i] in ['+', '-']:
                    i += 1
            elif c in ['f', 'F', 'l', 'L', 'u', 'U']:
                i += 1
            else:
                return None
        
        if tiene_punto or tiene_exponente:
            return 'real'
        else:
            return 'entero'
    
    def actualizar_estado_comentario(self, linea, en_comentario):
        """Actualiza el estado si estamos dentro de un comentario de bloque"""
        i = 0
        while i < len(linea):
            if not en_comentario:
                if i < len(linea) - 1 and linea[i:i+2] == '/*':
                    en_comentario = True
                    i += 2
                    continue
                elif i < len(linea) - 1 and linea[i:i+2] == '//':
                    break
            else:
                if i < len(linea) - 1 and linea[i:i+2] == '*/':
                    en_comentario = False
                    i += 2
                    continue
            i += 1
        
        return en_comentario
    
    def limpiar_comentarios(self, linea):
        """Elimina comentarios de una línea"""
        resultado = []
        i = 0
        en_string = False
        caracter_string = ''
        
        while i < len(linea):
            if linea[i] in ['"', "'"] and (i == 0 or linea[i-1] != '\\'):
                if not en_string:
                    en_string = True
                    caracter_string = linea[i]
                elif linea[i] == caracter_string:
                    en_string = False
                resultado.append(linea[i])
                i += 1
                continue
            
            if not en_string:
                if i < len(linea) - 1 and linea[i:i+2] == '//':
                    break
                
                if i < len(linea) - 1 and linea[i:i+2] == '/*':
                    j = i + 2
                    while j < len(linea) - 1:
                        if linea[j:j+2] == '*/':
                            i = j + 2
                            break
                        j += 1
                    else:
                        break
                    continue
            
            resultado.append(linea[i])
            i += 1
        
        return ''.join(resultado)
    
    def procesar_linea(self, linea, numero_linea, en_comentario_bloque):
        """Procesa una línea del código"""
        if en_comentario_bloque:
            idx = linea.find('*/')
            if idx != -1:
                linea = linea[idx+2:]
            else:
                return
        
        linea_limpia = self.limpiar_comentarios(linea)
        
        if not linea_limpia.strip():
            return
        
        self.tokenizar(linea_limpia, numero_linea)
    
    def tokenizar(self, linea, numero_linea):
        """Extrae tokens de una línea"""
        i = 0
        
        while i < len(linea):
            if linea[i].isspace():
                i += 1
                continue
            
            if linea[i] in ['"', "'"]:
                comilla = linea[i]
                i += 1
                while i < len(linea) and linea[i] != comilla:
                    if linea[i] == '\\':
                        i += 2
                    else:
                        i += 1
                i += 1
                continue
            
            if linea[i].isdigit() or (linea[i] == '.' and i+1 < len(linea) and linea[i+1].isdigit()):
                inicio = i
                tiene_punto = linea[i] == '.'
                
                while i < len(linea):
                    if linea[i].isdigit():
                        i += 1
                    elif linea[i] == '.' and not tiene_punto:
                        tiene_punto = True
                        i += 1
                    elif linea[i] in ['e', 'E']:
                        i += 1
                        if i < len(linea) and linea[i] in ['+', '-']:
                            i += 1
                    elif linea[i] in ['f', 'F', 'l', 'L', 'u', 'U']:
                        i += 1
                    else:
                        break
                
                numero = linea[inicio:i]
                tipo_num = self.es_numero(numero)
                
                if tipo_num == 'entero':
                    self.enteros.append((numero, numero_linea))
                    self.tokens.append(('ENTERO', numero, numero_linea))
                    self.contador_enteros += 1
                elif tipo_num == 'real':
                    self.reales.append((numero, numero_linea))
                    self.tokens.append(('REAL', numero, numero_linea))
                    self.contador_reales += 1
                continue
            
            if linea[i].isalpha() or linea[i] == '_':
                inicio = i
                while i < len(linea) and (linea[i].isalnum() or linea[i] == '_'):
                    i += 1
                
                palabra = linea[inicio:i]
                
                if self.es_palabra_reservada(palabra):
                    self.palabras_reservadas_encontradas.append((palabra, numero_linea))
                    self.tokens.append(('PALABRA_RESERVADA', palabra, numero_linea))
                    self.contador_palabras_reservadas += 1
                else:
                    self.variables.append((palabra, numero_linea))
                    self.tokens.append(('VARIABLE', palabra, numero_linea))
                    self.contador_variables += 1
                continue
            
            if i < len(linea) - 1:
                op_doble = linea[i:i+2]
                if op_doble in self.operadores:
                    self.operadores_encontrados.append((op_doble, numero_linea))
                    self.tokens.append(('OPERADOR', op_doble, numero_linea))
                    self.contador_operadores += 1
                    i += 2
                    continue
            
            if linea[i] in self.operadores:
                self.operadores_encontrados.append((linea[i], numero_linea))
                self.tokens.append(('OPERADOR', linea[i], numero_linea))
                self.contador_operadores += 1
                i += 1
                continue
            
            i += 1
    
    def procesar_archivo(self, nombre_archivo):
        """Procesa el archivo .c línea por línea"""
        self.reset()
        
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                lineas = archivo.readlines()
            
            en_comentario_bloque = False
            numero_linea = 0
            
            for linea in lineas:
                numero_linea += 1
                self.procesar_linea(linea, numero_linea, en_comentario_bloque)
                en_comentario_bloque = self.actualizar_estado_comentario(
                    linea, en_comentario_bloque
                )
            
            return True
        
        except FileNotFoundError:
            return False, "Archivo no encontrado"
        except Exception as e:
            return False, str(e)


class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Scanner de Código C")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        self.scanner = CScanner()
        self.archivo_actual = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores modernos
        bg_dark = '#1e1e1e'
        bg_medium = '#2d2d2d'
        bg_light = '#3e3e3e'
        fg_color = '#ffffff'
        accent = '#007acc'
        
        style.configure('Title.TLabel', background=bg_dark, foreground=fg_color, 
                       font=('Segoe UI', 24, 'bold'))
        style.configure('Header.TLabel', background=bg_dark, foreground=accent, 
                       font=('Segoe UI', 12, 'bold'))
        style.configure('Normal.TLabel', background=bg_medium, foreground=fg_color, 
                       font=('Consolas', 10))
        style.configure('Stats.TLabel', background=bg_medium, foreground='#4ec9b0', 
                       font=('Segoe UI', 11, 'bold'))
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_frame = tk.Frame(main_frame, bg=bg_dark)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title = ttk.Label(title_frame, text="🔍 Scanner de Código C", 
                         style='Title.TLabel')
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Analizador Léxico de Código C", 
                           bg=bg_dark, fg='#808080', font=('Segoe UI', 10))
        subtitle.pack()
        
        # Frame de botones
        button_frame = tk.Frame(main_frame, bg=bg_dark)
        button_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.btn_abrir = tk.Button(button_frame, text="📁 Abrir Archivo .c", 
                                   command=self.abrir_archivo,
                                   bg=accent, fg='white', font=('Segoe UI', 11, 'bold'),
                                   padx=20, pady=10, relief=tk.FLAT, cursor='hand2',
                                   activebackground='#005a9e')
        self.btn_abrir.pack(side=tk.LEFT, padx=5)
        
        self.btn_analizar = tk.Button(button_frame, text="⚡ Analizar", 
                                      command=self.analizar,
                                      bg='#4ec9b0', fg='white', font=('Segoe UI', 11, 'bold'),
                                      padx=20, pady=10, relief=tk.FLAT, cursor='hand2',
                                      state=tk.DISABLED, activebackground='#3da88a')
        self.btn_analizar.pack(side=tk.LEFT, padx=5)
        
        self.btn_limpiar = tk.Button(button_frame, text="🗑️ Limpiar", 
                                     command=self.limpiar,
                                     bg='#ce9178', fg='white', font=('Segoe UI', 11, 'bold'),
                                     padx=20, pady=10, relief=tk.FLAT, cursor='hand2',
                                     activebackground='#b87a5f')
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Label de archivo
        self.label_archivo = tk.Label(button_frame, text="No hay archivo cargado", 
                                      bg=bg_dark, fg='#808080', font=('Segoe UI', 10, 'italic'))
        self.label_archivo.pack(side=tk.LEFT, padx=20)
        
        # Frame de contenido principal
        content_frame = tk.Frame(main_frame, bg=bg_dark)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Código
        left_panel = tk.Frame(content_frame, bg=bg_medium, relief=tk.FLAT)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        code_header = tk.Label(left_panel, text="📄 CÓDIGO FUENTE", 
                              bg=bg_medium, fg=accent, font=('Segoe UI', 11, 'bold'))
        code_header.pack(pady=10)
        
        self.text_codigo = scrolledtext.ScrolledText(left_panel, wrap=tk.WORD,
                                                     bg=bg_light, fg='#d4d4d4',
                                                     font=('Consolas', 10),
                                                     insertbackground='white',
                                                     relief=tk.FLAT, padx=10, pady=10)
        self.text_codigo.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Panel derecho - Resultados
        right_panel = tk.Frame(content_frame, bg=bg_medium, relief=tk.FLAT)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        results_header = tk.Label(right_panel, text="📊 RESULTADOS DEL ANÁLISIS", 
                                 bg=bg_medium, fg=accent, font=('Segoe UI', 11, 'bold'))
        results_header.pack(pady=10)
        
        # Frame de estadísticas
        stats_frame = tk.Frame(right_panel, bg=bg_light, relief=tk.FLAT)
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.stats_labels = {}
        stats_items = [
            ("Palabras Reservadas", "palabras_reservadas"),
            ("Variables", "variables"),
            ("Números Enteros", "enteros"),
            ("Números Reales", "reales"),
            ("Operadores", "operadores"),
            ("TOTAL TOKENS", "total")
        ]
        
        for i, (nombre, key) in enumerate(stats_items):
            frame = tk.Frame(stats_frame, bg=bg_light)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            label = tk.Label(frame, text=f"{nombre}:", bg=bg_light, 
                           fg='#d4d4d4', font=('Segoe UI', 10), anchor='w')
            label.pack(side=tk.LEFT)
            
            value = tk.Label(frame, text="0", bg=bg_light, 
                           fg='#4ec9b0' if key != 'total' else '#ce9178', 
                           font=('Segoe UI', 10, 'bold'), anchor='e')
            value.pack(side=tk.RIGHT)
            
            self.stats_labels[key] = value
        
        # Área de resultados detallados
        self.text_resultados = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD,
                                                         bg=bg_light, fg='#d4d4d4',
                                                         font=('Consolas', 9),
                                                         relief=tk.FLAT, padx=10, pady=10)
        self.text_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Configurar tags para colores
        self.text_resultados.tag_configure("header", foreground="#ce9178", font=('Consolas', 10, 'bold'))
        self.text_resultados.tag_configure("keyword", foreground="#569cd6")
        self.text_resultados.tag_configure("variable", foreground="#9cdcfe")
        self.text_resultados.tag_configure("number", foreground="#b5cea8")
        self.text_resultados.tag_configure("operator", foreground="#d4d4d4")
        self.text_resultados.tag_configure("line", foreground="#808080")
    
    def abrir_archivo(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo C",
            filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
        )
        
        if filename:
            self.archivo_actual = filename
            self.label_archivo.config(text=f"📄 {filename.split('/')[-1]}", fg='#4ec9b0')
            self.btn_analizar.config(state=tk.NORMAL)
            
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                self.text_codigo.delete(1.0, tk.END)
                self.text_codigo.insert(1.0, contenido)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo:\n{str(e)}")
    
    def analizar(self):
        if not self.archivo_actual:
            messagebox.showwarning("Advertencia", "Primero debe abrir un archivo .c")
            return
        
        resultado = self.scanner.procesar_archivo(self.archivo_actual)
        
        if resultado:
            self.mostrar_resultados()
            messagebox.showinfo("Éxito", "✅ Análisis completado exitosamente!")
        else:
            messagebox.showerror("Error", "❌ Error al analizar el archivo")
    
    def mostrar_resultados(self):
        # Actualizar estadísticas
        self.stats_labels["palabras_reservadas"].config(
            text=str(self.scanner.contador_palabras_reservadas))
        self.stats_labels["variables"].config(
            text=str(self.scanner.contador_variables))
        self.stats_labels["enteros"].config(
            text=str(self.scanner.contador_enteros))
        self.stats_labels["reales"].config(
            text=str(self.scanner.contador_reales))
        self.stats_labels["operadores"].config(
            text=str(self.scanner.contador_operadores))
        self.stats_labels["total"].config(
            text=str(len(self.scanner.tokens)))
        
        # Limpiar área de resultados
        self.text_resultados.delete(1.0, tk.END)
        
        # Mostrar detalles
        if self.scanner.palabras_reservadas_encontradas:
            self.text_resultados.insert(tk.END, "🔑 PALABRAS RESERVADAS:\n", "header")
            for palabra, linea in self.scanner.palabras_reservadas_encontradas:
                self.text_resultados.insert(tk.END, f"  • ", "operator")
                self.text_resultados.insert(tk.END, f"{palabra}", "keyword")
                self.text_resultados.insert(tk.END, f" (línea {linea})\n", "line")
            self.text_resultados.insert(tk.END, "\n")
        
        if self.scanner.variables:
            self.text_resultados.insert(tk.END, "📝 VARIABLES:\n", "header")
            for var, linea in self.scanner.variables:
                self.text_resultados.insert(tk.END, f"  • ", "operator")
                self.text_resultados.insert(tk.END, f"{var}", "variable")
                self.text_resultados.insert(tk.END, f" (línea {linea})\n", "line")
            self.text_resultados.insert(tk.END, "\n")
        
        if self.scanner.enteros:
            self.text_resultados.insert(tk.END, "🔢 NÚMEROS ENTEROS:\n", "header")
            for num, linea in self.scanner.enteros:
                self.text_resultados.insert(tk.END, f"  • ", "operator")
                self.text_resultados.insert(tk.END, f"{num}", "number")
                self.text_resultados.insert(tk.END, f" (línea {linea})\n", "line")
            self.text_resultados.insert(tk.END, "\n")
        
        if self.scanner.reales:
            self.text_resultados.insert(tk.END, "🔢 NÚMEROS REALES:\n", "header")
            for num, linea in self.scanner.reales:
                self.text_resultados.insert(tk.END, f"  • ", "operator")
                self.text_resultados.insert(tk.END, f"{num}", "number")
                self.text_resultados.insert(tk.END, f" (línea {linea})\n", "line")
            self.text_resultados.insert(tk.END, "\n")
        
        if self.scanner.operadores_encontrados:
            self.text_resultados.insert(tk.END, "⚙️ OPERADORES:\n", "header")
            for op, linea in self.scanner.operadores_encontrados:
                self.text_resultados.insert(tk.END, f"  • ", "operator")
                self.text_resultados.insert(tk.END, f"'{op}'", "operator")
                self.text_resultados.insert(tk.END, f" (línea {linea})\n", "line")
            self.text_resultados.insert(tk.END, "\n")
        
        # Orden de aparición
        self.text_resultados.insert(tk.END, "📋 ORDEN DE APARICIÓN:\n", "header")
        self.text_resultados.insert(tk.END, "─" * 50 + "\n", "line")
        
        for i, (tipo, valor, linea) in enumerate(self.scanner.tokens, 1):
            self.text_resultados.insert(tk.END, f"{i:3d}. ", "line")
            self.text_resultados.insert(tk.END, f"[{tipo}] ", "operator")
            
            tag = "operator"
            if tipo == "PALABRA_RESERVADA":
                tag = "keyword"
            elif tipo == "VARIABLE":
                tag = "variable"
            elif tipo in ["ENTERO", "REAL"]:
                tag = "number"
            
            self.text_resultados.insert(tk.END, f"'{valor}'", tag)
            self.text_resultados.insert(tk.END, f" (línea {linea})\n", "line")
    
    def limpiar(self):
        self.text_codigo.delete(1.0, tk.END)
        self.text_resultados.delete(1.0, tk.END)
        self.archivo_actual = None
        self.label_archivo.config(text="No hay archivo cargado", fg='#808080')
        self.btn_analizar.config(state=tk.DISABLED)
        
        for key in self.stats_labels:
            self.stats_labels[key].config(text="0")
        
        self.scanner.reset()


def main():
    root = tk.Tk()
    app = ScannerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()