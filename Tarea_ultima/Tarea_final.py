"""
COMPILADOR C -> LINEALIZADO -> TERCETOS -> ASSEMBLER
Problema: Leer 6 numeros e imprimir el mayor y el menor
Curso: Lenguajes y Compiladores
Con soporte para: while, if, if-else, llaves {}
CORREGIDO: Usa comparaciones UNSIGNED (JB, JA, JBE, JAE), incluye espacio al imprimir y corrige saltos (ret).
"""

import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


CODIGO_FUENTE_C = """int a, b, c, d, e, f;
int mayor, menor, i;

cin >> a;
cin >> b;
cin >> c;
cin >> d;
cin >> e;
cin >> f;

mayor = a;
menor = a;
i = 1;

while (i < 6)
{
    if (i == 1)
    {
        if (b > mayor)
            mayor = b;
        if (b < menor)
            menor = b;
    }
    else
    {
        if (i == 2)
        {
            if (c > mayor)
                mayor = c;
            if (c < menor)
                menor = c;
        }
        else
        {
            if (i == 3)
            {
                if (d > mayor)
                    mayor = d;
                if (d < menor)
                    menor = d;
            }
            else
            {
                if (i == 4)
                {
                    if (e > mayor)
                        mayor = e;
                    if (e < menor)
                        menor = e;
                }
                else
                {
                    if (f > mayor)
                        mayor = f;
                    if (f < menor)
                        menor = f;
                }
            }
        }
    }
    i = i + 1;
}

cout << mayor;
cout << menor;"""


class Tokenizador:
    def __init__(self, codigo):
        self.codigo = codigo
        self.pos = 0
        self.tokens = []
        self.tokenizar()
    
    def tokenizar(self):
        patrones = [
            ('KEYWORD', r'\b(int|if|else|while|cin|cout)\b'),
            ('IDENT', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
            ('NUM', r'\b\d+\b'),
            ('OP', r'==|!=|<=|>=|>>|<<|\+\+|--|\+|-|\*|/|%|<|>|='),
            ('LBRACE', r'\{'),
            ('RBRACE', r'\}'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('SEMI', r';'),
            ('COMMA', r','),
            ('SKIP', r'[ \t\n]+'),
        ]
        patron_combinado = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in patrones)
        for match in re.finditer(patron_combinado, self.codigo):
            tipo = match.lastgroup
            valor = match.group()
            if tipo != 'SKIP':
                self.tokens.append((tipo, valor))
        self.tokens.append(('EOF', ''))
        self.pos = 0
    
    def actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')
    
    def consumir(self, tipo_esperado=None):
        token = self.actual()
        self.pos += 1
        return token


class Parser:
    def __init__(self, codigo):
        self.tokenizador = Tokenizador(codigo)
        self.etiqueta_counter = 1
        self.lineas = []
    
    def nueva_etiqueta(self):
        etiq = f"E{self.etiqueta_counter}"
        self.etiqueta_counter += 1
        return etiq
    
    def parsear(self):
        self.lineas = []
        while self.tokenizador.actual()[0] != 'EOF':
            self.parsear_statement()
        return '\n'.join(self.lineas)
    
    def parsear_statement(self):
        token = self.tokenizador.actual()
        if token[1] == 'int':
            self.parsear_declaracion()
        elif token[1] == 'cin':
            self.parsear_cin()
        elif token[1] == 'cout':
            self.parsear_cout()
        elif token[1] == 'if':
            self.parsear_if()
        elif token[1] == 'while':
            self.parsear_while()
        elif token[0] == 'IDENT':
            self.parsear_asignacion()
        elif token[0] == 'LBRACE':
            self.parsear_bloque()
        elif token[0] == 'SEMI':
            self.tokenizador.consumir()
        else:
            self.tokenizador.consumir()
    
    def parsear_declaracion(self):
        self.tokenizador.consumir()
        vars_decl = []
        while True:
            nombre = self.tokenizador.consumir()[1]
            if self.tokenizador.actual()[1] == '=':
                self.tokenizador.consumir()
                valor = self.tokenizador.consumir()[1]
                vars_decl.append(f"{nombre} = {valor}")
            else:
                vars_decl.append(nombre)
            if self.tokenizador.actual()[0] == 'COMMA':
                self.tokenizador.consumir()
            else:
                break
        self.tokenizador.consumir()
        self.lineas.append(f"int {', '.join([v.split('=')[0].strip() for v in vars_decl])};")
        for v in vars_decl:
            if '=' in v:
                self.lineas.append(f"{v};")
    
    def parsear_cin(self):
        self.tokenizador.consumir()
        self.tokenizador.consumir()
        var = self.tokenizador.consumir()[1]
        self.tokenizador.consumir()
        self.lineas.append(f"cin >> {var};")
    
    def parsear_cout(self):
        self.tokenizador.consumir()
        self.tokenizador.consumir()
        var = self.tokenizador.consumir()[1]
        self.tokenizador.consumir()
        self.lineas.append(f"cout << {var};")
    
    def parsear_asignacion(self):
        var = self.tokenizador.consumir()[1]
        self.tokenizador.consumir()
        expr_parts = []
        while self.tokenizador.actual()[0] != 'SEMI':
            expr_parts.append(self.tokenizador.consumir()[1])
        self.tokenizador.consumir()
        self.lineas.append(f"{var} = {' '.join(expr_parts)};")
    
    def parsear_condicion(self):
        self.tokenizador.consumir()
        cond_parts = []
        paren_count = 1
        while paren_count > 0:
            token = self.tokenizador.consumir()
            if token[0] == 'LPAREN':
                paren_count += 1
            elif token[0] == 'RPAREN':
                paren_count -= 1
                if paren_count == 0:
                    break
            cond_parts.append(token[1])
        return ' '.join(cond_parts)
    
    def negar_condicion(self, cond):
        cond = cond.strip()
        if '>=' in cond:
            return cond.replace('>=', '<')
        elif '<=' in cond:
            return cond.replace('<=', '>')
        elif '==' in cond:
            return cond.replace('==', '!=')
        elif '!=' in cond:
            return cond.replace('!=', '==')
        elif '>' in cond:
            return cond.replace('>', '<=')
        elif '<' in cond:
            return cond.replace('<', '>=')
        return f"!({cond})"
    
    def parsear_if(self):
        self.tokenizador.consumir()
        condicion = self.parsear_condicion()
        cond_negada = self.negar_condicion(condicion)
        etiq_else = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()
        self.lineas.append(f"if ({cond_negada}) goto {etiq_else};")
        self.parsear_cuerpo()
        if self.tokenizador.actual()[1] == 'else':
            self.tokenizador.consumir()
            self.lineas.append(f"goto {etiq_fin};")
            self.lineas.append(f"{etiq_else}:")
            self.parsear_cuerpo()
            self.lineas.append(f"{etiq_fin}:")
        else:
            self.lineas.append(f"{etiq_else}:")
    
    def parsear_while(self):
        self.tokenizador.consumir()
        condicion = self.parsear_condicion()
        cond_negada = self.negar_condicion(condicion)
        etiq_inicio = self.nueva_etiqueta()
        etiq_fin = self.nueva_etiqueta()
        self.lineas.append(f"{etiq_inicio}:")
        self.lineas.append(f"if ({cond_negada}) goto {etiq_fin};")
        self.parsear_cuerpo()
        self.lineas.append(f"goto {etiq_inicio};")
        self.lineas.append(f"{etiq_fin}:")
    
    def parsear_cuerpo(self):
        if self.tokenizador.actual()[0] == 'LBRACE':
            self.parsear_bloque()
        else:
            self.parsear_statement()
    
    def parsear_bloque(self):
        self.tokenizador.consumir()
        while self.tokenizador.actual()[0] != 'RBRACE':
            self.parsear_statement()
        self.tokenizador.consumir()


class GeneradorTercetos:
    def __init__(self):
        self.tercetos = []
        self.contador = 1
        self.etiquetas_linea = {}
    
    def reset(self):
        self.tercetos = []
        self.contador = 1
        self.etiquetas_linea = {}
    
    def agregar(self, op, arg1, arg2=""):
        self.tercetos.append((self.contador, op, arg1, arg2))
        self.contador += 1
        return self.contador - 1
    
    def generar(self, codigo_linealizado):
        self.reset()
        lineas = codigo_linealizado.strip().split('\n')
        
        # Primera pasada
        pos = 1
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith('int '):
                continue
            if linea.endswith(':') and not linea.startswith('if'):
                self.etiquetas_linea[linea[:-1]] = pos
                continue
            if linea.startswith('cin') or linea.startswith('cout'):
                pos += 1
            elif linea.startswith('if (') and 'goto' in linea:
                pos += 2
            elif linea.startswith('goto '):
                pos += 1
            elif '=' in linea:
                expr = linea.split('=')[1].replace(';', '').strip()
                pos += 2 if ('+' in expr or '-' in expr) else 1
        
        # Segunda pasada
        self.contador = 1
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith('int ') or (linea.endswith(':') and not linea.startswith('if')):
                continue
            
            if linea.startswith('cin >>'):
                self.agregar('cin', linea.replace('cin >>', '').replace(';', '').strip())
            elif linea.startswith('cout <<'):
                self.agregar('cout', linea.replace('cout <<', '').replace(';', '').strip())
            elif linea.startswith('goto '):
                etiq = linea.replace('goto ', '').replace(';', '').strip()
                self.agregar('B', self.etiquetas_linea.get(etiq, etiq))
            elif linea.startswith('if (') and 'goto' in linea:
                cond = linea[linea.index('(')+1:linea.index(')')].strip()
                etiq = linea[linea.index('goto')+5:].replace(';', '').strip()
                destino = self.etiquetas_linea.get(etiq, etiq)
                
                for op_str, op_code in [('<=','BBE'),('>=','BAE'),('!=','BNE'),('==','BE'),('<','BB'),('>','BA')]:
                    if op_str in cond:
                        partes = cond.split(op_str)
                        self.agregar('CMP', partes[0].strip(), partes[1].strip())
                        self.agregar(op_code, destino)
                        break
            elif '=' in linea:
                partes = linea.replace(';', '').split('=', 1)
                var, expr = partes[0].strip(), partes[1].strip()
                if ' + ' in expr:
                    ops = expr.split('+')
                    idx = self.agregar('+', ops[0].strip(), ops[1].strip())
                    self.agregar('=', var, f'({idx})')
                elif ' - ' in expr:
                    ops = expr.split('-')
                    idx = self.agregar('-', ops[0].strip(), ops[1].strip())
                    self.agregar('=', var, f'({idx})')
                else:
                    self.agregar('=', var, expr)
        return self.tercetos
    
    def to_string(self):
        return '\n'.join(f"({t[0]}) {t[1]}, {t[2]}, {t[3]}" if t[3] else f"({t[0]}) {t[1]}, {t[2]}," for t in self.tercetos)


class GeneradorASM:
    def __init__(self):
        self.codigo = []
        self.variables = set()
    
    def generar(self, tercetos):
        self.codigo = []
        self.variables = set()
        
        # Extraer variables
        for t in tercetos:
            _, op, arg1, arg2 = t
            if op in ['cin', 'cout']:
                self.variables.add(arg1)
            elif op == '=':
                self.variables.add(arg1)
                if arg2 and not arg2.startswith('(') and not arg2.isdigit():
                    self.variables.add(arg2)
            elif op in ['-', '+', 'CMP']:
                if arg1 and not arg1.isdigit():
                    self.variables.add(arg1)
                if arg2 and not arg2.isdigit():
                    self.variables.add(arg2)
        
        self.codigo.append("org 100h")
        self.codigo.append("")
        
        # Destinos de saltos
        destinos = set()
        for t in tercetos:
            if t[1] in ['BB', 'BA', 'BBE', 'BAE', 'BE', 'BNE', 'B']:
                try:
                    destinos.add(int(t[2]))
                except:
                    pass
        
        # Generar
        for t in tercetos:
            num, op, arg1, arg2 = t
            
            if num in destinos:
                self.codigo.append(f"L{num}:")
            
            if op == 'cin':
                self.codigo.append("    call lee_num")
                self.codigo.append(f"    mov [{arg1}], al")
            elif op == 'cout':
                self.codigo.append(f"    mov dl, [{arg1}]")
                self.codigo.append("    call imp_num")
            elif op == 'CMP':
                self.codigo.append(f"    mov al, [{arg1}]" if not arg1.isdigit() else f"    mov al, {arg1}")
                self.codigo.append(f"    cmp al, [{arg2}]" if not arg2.isdigit() else f"    cmp al, {arg2}")
            elif op == '+':
                self.codigo.append(f"    mov al, [{arg1}]" if not arg1.isdigit() else f"    mov al, {arg1}")
                self.codigo.append(f"    add al, [{arg2}]" if not arg2.isdigit() else f"    add al, {arg2}")
            elif op == '-':
                self.codigo.append(f"    mov al, [{arg1}]" if not arg1.isdigit() else f"    mov al, {arg1}")
                self.codigo.append(f"    sub al, [{arg2}]" if not arg2.isdigit() else f"    sub al, {arg2}")
            elif op == '=':
                if arg2.startswith('('):
                    self.codigo.append(f"    mov [{arg1}], al")
                elif arg2.isdigit():
                    self.codigo.append(f"    mov al, {arg2}")
                    self.codigo.append(f"    mov [{arg1}], al")
                else:
                    self.codigo.append(f"    mov al, [{arg2}]")
                    self.codigo.append(f"    mov [{arg1}], al")
            elif op == 'BB':
                self.codigo.append(f"    JB L{arg1}")
            elif op == 'BA':
                self.codigo.append(f"    JA L{arg1}")
            elif op == 'BBE':
                self.codigo.append(f"    JBE L{arg1}")
            elif op == 'BAE':
                self.codigo.append(f"    JAE L{arg1}")
            elif op == 'BE':
                self.codigo.append(f"    JE L{arg1}")
            elif op == 'BNE':
                self.codigo.append(f"    JNE L{arg1}")
            elif op == 'B':
                self.codigo.append(f"    JMP L{arg1}")
        
        # Cerrar el programa correctamente
        self.codigo.append("")
        self.codigo.append("    mov ax, 4C00h")
        self.codigo.append("    int 21h")
        self.codigo.append("")
        self.codigo.append("; === VARIABLES ===")
        for var in sorted(self.variables):
            self.codigo.append(f"{var} db 0")
        
        # Procedimientos
        self.codigo.append("")
        self.codigo.append("proc lee_num")
        self.codigo.append("    push bx")
        self.codigo.append("    push cx")
        self.codigo.append("    mov ah,01")
        self.codigo.append("    int 21h")
        self.codigo.append("    sub al,'0'")
        self.codigo.append("    mov bl,al")
        self.codigo.append("    mov ah,01")
        self.codigo.append("    int 21h")
        self.codigo.append("    sub al,'0'")
        self.codigo.append("    mov cx,10")
        self.codigo.append("F1:")
        self.codigo.append("    add al,bl")
        self.codigo.append("    loop F1")
        self.codigo.append("    pop cx")
        self.codigo.append("    pop bx")
        self.codigo.append("    ret")
        self.codigo.append("endp")
        self.codigo.append("")
        
        self.codigo.append("proc imp_num")
        self.codigo.append("    push ax")  # Guardamos registros para no ensuciarlos
        self.codigo.append("    push bx")
        self.codigo.append("    mov bl,dl")
        self.codigo.append("    mov dl,0")
        self.codigo.append("F2: cmp bl,9")
        self.codigo.append("    jle F3")
        self.codigo.append("    sub bl,10")
        self.codigo.append("    inc dl")
        self.codigo.append("    jmp F2")
        self.codigo.append("F3: add dl,'0'")
        self.codigo.append("    mov ah,02")
        self.codigo.append("    int 21h")
        self.codigo.append("    mov dl,bl")
        self.codigo.append("    add dl,'0'")
        self.codigo.append("    int 21h")
        
        # Imprimir un espacio despues del numero para que no se peguen
        self.codigo.append("    mov dl, ' '")
        self.codigo.append("    mov ah, 02h")
        self.codigo.append("    int 21h")
        
        self.codigo.append("    pop bx")
        self.codigo.append("    pop ax")
        self.codigo.append("    ret")  # <--- Este era el comando faltante crucial
        self.codigo.append("endp")
        
        return '\n'.join(self.codigo)


class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.parser = None
        self.gen_tercetos = GeneradorTercetos()
        self.gen_asm = GeneradorASM()
        
        self.title("Compilador C -> ASM | Lenguajes y Compiladores")
        self.geometry("1400x850")
        
        self.col_pink = "#FF2E63"
        self.col_bg = "#0D1117"
        self.col_sidebar = "#161B22"
        self.col_card = "#21262D"
        
        self.configure(fg_color=self.col_bg)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self._crear_sidebar()
        self._crear_area_principal()
    
    def _crear_sidebar(self):
        sb = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=self.col_sidebar)
        sb.grid(row=0, column=0, sticky="nsew")
        
        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.pack(pady=(35, 30))
        ctk.CTkLabel(logo, text="C", font=("Consolas", 44, "bold"), text_color=self.col_pink).pack(side="left", padx=6)
        ctk.CTkLabel(logo, text="COMPILADOR\nC -> ASM", font=("Consolas", 17, "bold"), text_color=self.col_pink).pack(side="left")
        
        info = ctk.CTkFrame(sb, fg_color=self.col_card, corner_radius=10)
        info.pack(pady=(0, 16), padx=18, fill="x")
        ctk.CTkLabel(info, text="Proceso:", font=("Segoe UI", 10, "bold"), text_color="#CCCCCC").pack(anchor="w", padx=10, pady=(10, 4))
        for paso in ["1. Codigo C", "2. Linealizado", "3. Tercetos", "4. ASM"]:
            ctk.CTkLabel(info, text=f"  {paso}", font=("Courier New", 10), text_color="#AAAAAA").pack(anchor="w", padx=14)
        ctk.CTkLabel(info, text="\nSoporta: while, if-else", font=("Courier New", 9), text_color="#98C379").pack(anchor="w", padx=10, pady=(4, 10))
        
        btn_kw = {"font": ("Segoe UI", 12, "bold"), "height": 46, "corner_radius": 8, "anchor": "w"}
        ctk.CTkButton(sb, text="  COMPILAR", command=self._compilar, fg_color=self.col_pink, hover_color="#D42650", **btn_kw).pack(pady=8, padx=18, fill="x")
        ctk.CTkButton(sb, text="  GUARDAR ASM", command=self._guardar_asm, fg_color="#2A2A2A", hover_color="#333333", **btn_kw).pack(pady=8, padx=18, fill="x")
        ctk.CTkButton(sb, text="  LIMPIAR", command=self._limpiar, fg_color="#2A2A2A", hover_color="#333333", **btn_kw).pack(pady=8, padx=18, fill="x")
        
        prob = ctk.CTkFrame(sb, fg_color=self.col_card, corner_radius=8)
        prob.pack(padx=18, fill="x", pady=(20, 0))
        ctk.CTkLabel(prob, text="Leer 6 numeros\nImprimir MAYOR y MENOR\nUsando WHILE e IF", font=("Consolas", 11), text_color="#61AFEF", justify="center").pack(pady=12)
    
    def _crear_area_principal(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=18, pady=18)
        main.columnconfigure((0, 1), weight=1)
        main.rowconfigure((0, 1), weight=1)
        
        for (r, c, titulo, color, attr) in [
            (0, 0, "CODIGO C", self.col_pink, "text_c"),
            (0, 1, "LINEALIZADO", "#E06C75", "text_lin"),
            (1, 0, "TERCETOS", "#98C379", "text_ter"),
            (1, 1, "ASSEMBLER", "#61AFEF", "text_asm")
        ]:
            panel = ctk.CTkFrame(main, fg_color=self.col_card, corner_radius=10)
            panel.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            ctk.CTkLabel(panel, text=titulo, font=("Consolas", 12, "bold"), text_color=color).pack(anchor="w", padx=12, pady=(12, 6))
            text = ctk.CTkTextbox(panel, font=("Consolas", 10), fg_color="#0F0F0F", text_color="#E6E6E6")
            text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
            setattr(self, attr, text)
        
        self.text_c.insert("1.0", CODIGO_FUENTE_C)
        for t in [self.text_lin, self.text_ter, self.text_asm]:
            t.insert("1.0", "Esperando...")
    
    def _compilar(self):
        try:
            codigo_c = self.text_c.get("1.0", tk.END).strip()
            self.parser = Parser(codigo_c)
            codigo_lin = self.parser.parsear()
            self.text_lin.delete("1.0", tk.END)
            self.text_lin.insert("1.0", codigo_lin)
            
            tercetos = self.gen_tercetos.generar(codigo_lin)
            self.text_ter.delete("1.0", tk.END)
            self.text_ter.insert("1.0", self.gen_tercetos.to_string())
            
            codigo_asm = self.gen_asm.generar(tercetos)
            self.text_asm.delete("1.0", tk.END)
            self.text_asm.insert("1.0", codigo_asm)
            
            messagebox.showinfo("OK", "Compilado correctamente.\nGuarda el ASM y pruebalo en emu8086.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _guardar_asm(self):
        codigo = self.text_asm.get("1.0", tk.END).strip()
        if "Esperando" in codigo:
            messagebox.showwarning("!", "Primero compila.")
            return
        with open("programa.asm", "w") as f:
            f.write(codigo)
        messagebox.showinfo("OK", "Guardado: programa.asm")
    
    def _limpiar(self):
        for t in [self.text_lin, self.text_ter, self.text_asm]:
            t.delete("1.0", tk.END)
            t.insert("1.0", "Esperando...")


if __name__ == "__main__":
    AppGUI().mainloop()