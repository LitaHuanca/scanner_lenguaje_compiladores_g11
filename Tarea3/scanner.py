import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# Automata 

class AutomataAritmetico:

    OPERADORES        = set('+-*/%^')
    AGRUPADORES_ABRE  = {'(': ')', '[': ']'}
    AGRUPADORES_CIERRA = {')', ']'}

    def __init__(self):
        self.reset()

    def reset(self):
        self.pila      = []
        self.errores   = []
        self.historial = []
        self.snapshots = []

    def _push(self, abriente, linea):
        self.pila.append((abriente, linea))
        self.historial.append(
            f"Linea {linea}: PUSH '{abriente}' -> {[e[0] for e in self.pila]}"
        )
        self.snapshots.append({
            'op': 'PUSH', 'elem': abriente, 'linea': linea,
            'pila': [e[0] for e in self.pila]
        })

    def _pop(self, cierre_encontrado, linea):
        if not self.pila:
            self.errores.append(
                f"Linea {linea}: cierre '{cierre_encontrado}' sin apertura correspondiente"
            )
            return False

        abriente, linea_apertura = self.pila.pop()
        self.historial.append(
            f"Linea {linea}: POP '{abriente}' -> {[e[0] for e in self.pila]}"
        )
        self.snapshots.append({
            'op': 'POP', 'elem': abriente, 'linea': linea,
            'pila': [e[0] for e in self.pila]
        })

        cierre_esperado = self.AGRUPADORES_ABRE[abriente]
        if cierre_esperado != cierre_encontrado:
            self.errores.append(
                f"Linea {linea}: se esperaba '{cierre_esperado}' "
                f"para cerrar '{abriente}' (abierto en linea {linea_apertura}), "
                f"pero se encontro '{cierre_encontrado}'"
            )
            return False
        return True

    def analizar(self, expresion, numero_linea=1):
        tokens          = []
        operadores      = []
        numeros         = []
        errores_locales = []

        i           = 0
        longitud    = len(expresion)
        ultimo_tipo = None

        while i < longitud:
            c = expresion[i]

            if c in ' \t':
                i += 1
                continue

            # numero entero o real
            if c.isdigit() or (c == '.' and i+1 < longitud and expresion[i+1].isdigit()):
                inicio      = i
                tiene_punto = False
                if c == '.':
                    tiene_punto = True
                    i += 1
                while i < longitud and expresion[i].isdigit():
                    i += 1
                if i < longitud and expresion[i] == '.' and not tiene_punto:
                    tiene_punto = True
                    i += 1
                    while i < longitud and expresion[i].isdigit():
                        i += 1
                valor = expresion[inicio:i]
                tipo  = 'REAL' if tiene_punto else 'ENTERO'
                tokens.append((tipo, valor, numero_linea))
                numeros.append((valor, numero_linea))
                ultimo_tipo = 'NUMERO'
                continue

            # agrupador de apertura -> apilamos el ABRIENTE
            if c in self.AGRUPADORES_ABRE:
                self._push(c, numero_linea)
                tokens.append(('AGRUPADOR', c, numero_linea))
                ultimo_tipo = 'ABRE'
                i += 1
                continue

            # agrupador de cierre -> desapilamos y comparamos
            if c in self.AGRUPADORES_CIERRA:
                if not self.pila:
                    msg = f"Linea {numero_linea}: '{c}' sin apertura correspondiente"
                    errores_locales.append(msg)
                    self.errores.append(msg)
                else:
                    self._pop(c, numero_linea)
                tokens.append(('AGRUPADOR', c, numero_linea))
                ultimo_tipo = 'CIERRA'
                i += 1
                continue

            # operadores
            if c in self.OPERADORES:
                # signo unario al inicio, tras operador o tras apertura
                if c in '+-' and ultimo_tipo in (None, 'OPERADOR', 'ABRE'):
                    inicio = i
                    i += 1
                    while i < longitud and (expresion[i].isdigit() or expresion[i] == '.'):
                        i += 1
                    valor = expresion[inicio:i]
                    if valor in ('+', '-'):
                        msg = f"Linea {numero_linea}: operador unario '{c}' sin operando"
                        errores_locales.append(msg)
                        self.errores.append(msg)
                        tokens.append(('OPERADOR', c, numero_linea))
                        operadores.append((c, numero_linea))
                    else:
                        tipo = 'REAL' if '.' in valor else 'ENTERO'
                        tokens.append((tipo, valor, numero_linea))
                        numeros.append((valor, numero_linea))
                        ultimo_tipo = 'NUMERO'
                    continue

                if ultimo_tipo in ('OPERADOR', None, 'ABRE'):
                    msg = (f"Linea {numero_linea}: operador '{c}' inesperado "
                           f"(falta operando izquierdo)")
                    errores_locales.append(msg)
                    self.errores.append(msg)

                tokens.append(('OPERADOR', c, numero_linea))
                operadores.append((c, numero_linea))
                ultimo_tipo = 'OPERADOR'
                i += 1
                continue

            # caracter desconocido
            msg = f"Linea {numero_linea}: caracter no reconocido '{c}'"
            errores_locales.append(msg)
            self.errores.append(msg)
            i += 1

        # la expresion no puede terminar con operador o apertura sin cerrar
        if ultimo_tipo in ('OPERADOR', 'ABRE', None) and not errores_locales:
            msg = f"Linea {numero_linea}: la expresion termina de forma incorrecta"
            errores_locales.append(msg)
            self.errores.append(msg)

        # agrupadores sin cerrar al final de esta expresion
        for sym, ln in list(self.pila):
            msg = f"Linea {numero_linea}: '{sym}' abierto en linea {ln} nunca fue cerrado"
            errores_locales.append(msg)
            self.errores.append(msg)
        self.pila = []

        return tokens, operadores, numeros, errores_locales


# Logica central

class AnalizadorAritmetico:
    def __init__(self):
        self.reset()

    def reset(self):
        self.automata                 = AutomataAritmetico()
        self.expresiones              = []
        self.todos_tokens             = []
        self.todos_operadores         = []
        self.todos_numeros            = []
        self.resultados_por_expresion = []

    def agregar_expresion(self, expr):
        expr = expr.strip()
        if not expr:
            return False, ["La expresion esta vacia"]
        linea  = len(self.expresiones) + 1
        tokens, operadores, numeros, errores = self.automata.analizar(expr, linea)
        self.expresiones.append(expr)
        self.todos_tokens.extend(tokens)
        self.todos_operadores.extend(operadores)
        self.todos_numeros.extend(numeros)
        self.resultados_por_expresion.append((expr, tokens, operadores, numeros, errores))
        return len(errores) == 0, errores

    def total_expresiones(self): return len(self.expresiones)
    def total_operadores(self):  return len(self.todos_operadores)
    def total_numeros(self):     return len(self.todos_numeros)
    def total_errores(self):     return len(self.automata.errores)

    def conteo_por_operador(self):
        conteo = {}
        for op, _ in self.todos_operadores:
            conteo[op] = conteo.get(op, 0) + 1
        return conteo


# GUI 

class AppGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.analizador   = AnalizadorAritmetico()
        self.snapshot_idx = 0

        self.title("Analizador Sintactico - Expresiones Aritmeticas | Grupo 11")
        self.geometry("1500x900")

        self.col_pink    = "#FF2E63"
        self.col_bg      = "#0D1117"
        self.col_sidebar = "#161B22"
        self.col_card    = "#21262D"

        self.dash_colors = {
            "expresiones": "#FF2E63",
            "operadores":  "#E06C75",
            "numeros":     "#98C379",
            "errores":     "#FF6B6B",
            "tokens":      "#61AFEF",
        }

        self.configure(fg_color=self.col_bg)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._crear_sidebar()
        self._crear_area_principal()

    # Sidebar 

    def _crear_sidebar(self):
        sb = ctk.CTkFrame(self, width=260, corner_radius=0, fg_color=self.col_sidebar)
        sb.grid(row=0, column=0, sticky="nsew")

        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.pack(pady=(35, 30))
        ctk.CTkLabel(logo, text="∑", font=("Segoe UI", 44, "bold"),
                     text_color=self.col_pink).pack(side="left", padx=6)
        ctk.CTkLabel(logo, text="ANALIZADOR\nARITMETICO",
                     font=("Orbitron", 17, "bold"), text_color=self.col_pink).pack(side="left")

        info = ctk.CTkFrame(sb, fg_color=self.col_card, corner_radius=10)
        info.pack(pady=(0, 16), padx=18, fill="x")
        ctk.CTkLabel(info, text="Operadores soportados:",
                     font=("Segoe UI", 10, "bold"), text_color="#CCCCCC"
                     ).pack(anchor="w", padx=10, pady=(10, 4))
        for op in ["+ suma", "- resta", "* multiplicacion",
                   "/ division", "% modulo", "^ potencia"]:
            ctk.CTkLabel(info, text=f"  {op}",
                         font=("Courier New", 10), text_color="#AAAAAA"
                         ).pack(anchor="w", padx=14, pady=1)
        ctk.CTkLabel(info, text="Agrupadores: ( )  [ ]",
                     font=("Courier New", 10), text_color="#AAAAAA"
                     ).pack(anchor="w", padx=14, pady=(4, 10))

        btn_kw = {"font": ("Segoe UI", 12, "bold"), "height": 46,
                  "corner_radius": 8, "anchor": "w"}
        ctk.CTkButton(sb, text="  ▶   ANALIZAR", command=self._analizar,
                      fg_color=self.col_pink, hover_color="#D42650",
                      text_color="white", **btn_kw).pack(pady=8, padx=18, fill="x")
        ctk.CTkButton(sb, text="  🗑   LIMPIAR TODO", command=self._limpiar,
                      fg_color="#2A2A2A", hover_color="#333333",
                      **btn_kw).pack(pady=8, padx=18, fill="x")

        # visualizacion de pila
        ctk.CTkLabel(sb, text="Pila (agrupadores):",
                     font=("Segoe UI", 10, "bold"), text_color="#CCCCCC").pack(pady=(18, 4))

        self.lbl_op_sidebar = ctk.CTkLabel(
            sb, text="", font=("Courier New", 9, "bold"),
            text_color=self.col_pink, wraplength=210
        )
        self.lbl_op_sidebar.pack()

        self.canvas_pila = tk.Canvas(
            sb, width=218, height=190, bg="#0F0F0F",
            highlightthickness=1, highlightbackground="#333333"
        )
        self.canvas_pila.pack(padx=18, pady=4)

        ctrl = ctk.CTkFrame(sb, fg_color="transparent")
        ctrl.pack(pady=6)

        ctk.CTkButton(ctrl, text="◀", width=38, command=self._snap_prev,
                      fg_color=self.col_card, hover_color="#333333").pack(side="left", padx=2)

        self.lbl_snap = ctk.CTkLabel(ctrl, text="Paso: 0/0",
                                      font=("Courier New", 9), width=90)
        self.lbl_snap.pack(side="left", padx=8)

        ctk.CTkButton(ctrl, text="▶", width=38, command=self._snap_next,
                      fg_color=self.col_card, hover_color="#333333").pack(side="left", padx=2)


    def _crear_area_principal(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=18, pady=18)
        main.columnconfigure(0, weight=2)
        main.columnconfigure(1, weight=3)
        main.rowconfigure(0, weight=1)

        left = ctk.CTkFrame(main, fg_color="transparent")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        ctk.CTkLabel(left, text="✏  INGRESAR EXPRESIONES",
                     font=("Consolas", 13, "bold"), text_color=self.col_pink
                     ).pack(anchor="w", pady=(0, 6))

        entry_frame = ctk.CTkFrame(left, fg_color=self.col_card, corner_radius=10)
        entry_frame.pack(fill="x", pady=(0, 8))

        self.entry_expr = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Ej: 3 + (4 * 2) - [1 / 0.5]",
            font=("Consolas", 13), fg_color="#0F0F0F",
            border_width=0, height=42
        )
        self.entry_expr.pack(fill="x", padx=10, pady=8)
        self.entry_expr.bind("<Return>", lambda e: self._agregar_expr())

        ctk.CTkButton(
            entry_frame, text="+ Agregar expresion",
            command=self._agregar_expr,
            fg_color=self.col_pink, hover_color="#D42650",
            height=36, font=("Segoe UI", 11, "bold")
        ).pack(padx=10, pady=(0, 8), fill="x")

        ctk.CTkLabel(left, text="📋  EXPRESIONES INGRESADAS",
                     font=("Consolas", 11, "bold"), text_color="#CCCCCC"
                     ).pack(anchor="w", pady=(10, 4))

        self.lista_exprs = ctk.CTkTextbox(
            left, font=("Consolas", 12),
            fg_color="#0F0F0F", text_color="#E6E6E6",
            border_width=1, border_color="#333333"
        )
        self.lista_exprs.pack(fill="both", expand=True)
        self.lista_exprs.insert("1.0", "Aun no hay expresiones...\n")

        right = ctk.CTkFrame(main, fg_color="transparent")
        right.grid(row=0, column=1, sticky="nsew")

        self.tabview = ctk.CTkTabview(
            right,
            segmented_button_selected_color=self.col_pink,
            segmented_button_selected_hover_color="#D42650",
            height=40
        )
        self.tabview.pack(fill="both", expand=True)

        self.tab_dash = self.tabview.add("DASHBOARD")
        self.tab_det  = self.tabview.add("DETALLE TOKENS")
        self.tab_hist = self.tabview.add("HISTORIAL PILA")
        self.tab_err  = self.tabview.add("ERRORES")

        self._build_dashboard()
        self._build_detalle()
        self._build_historial()
        self._build_errores()

    # Tabs 

    def _build_dashboard(self):
        scroll = ctk.CTkScrollableFrame(self.tab_dash, fg_color="transparent")
        scroll.pack(fill="both", expand=True)
        scroll.columnconfigure((0, 1), weight=1)

        cards = [
            ("EXPRESIONES",  "📐", self.dash_colors["expresiones"], "expresiones"),
            ("OPERADORES",   "⚙",  self.dash_colors["operadores"],  "operadores"),
            ("NUMEROS",      "🔢", self.dash_colors["numeros"],      "numeros"),
            ("TOTAL TOKENS", "∑",  self.dash_colors["tokens"],       "tokens"),
            ("ERRORES",      "⚠",  self.dash_colors["errores"],      "errores"),
        ]

        self.dash_widgets = {}
        for i, (titulo, icono, color, key) in enumerate(cards):
            card = ctk.CTkFrame(scroll, fg_color=self.col_card, corner_radius=14,
                                border_width=1, border_color="#333333")
            card.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")

            hdr = ctk.CTkFrame(card, fg_color="transparent")
            hdr.pack(fill="x", padx=14, pady=(14, 4))
            ctk.CTkLabel(hdr, text=icono, font=("Segoe UI Emoji", 22)).pack(side="left")
            ctk.CTkLabel(hdr, text=f"  {titulo}", font=("Segoe UI", 11, "bold"),
                         text_color="#AAAAAA").pack(side="left")

            num = ctk.CTkLabel(card, text="0", font=("Segoe UI", 38, "bold"), text_color=color)
            num.pack(pady=(0, 14))
            self.dash_widgets[key] = num

        sep = ctk.CTkLabel(scroll, text="CONTEO POR OPERADOR",
                           font=("Segoe UI", 10, "bold"), text_color="#666666")
        sep.grid(row=3, column=0, columnspan=2, pady=(12, 4))

        self.tbl_operadores = ctk.CTkTextbox(
            scroll, height=80, fg_color=self.col_card,
            text_color="#DDDDDD", font=("Consolas", 11), corner_radius=10
        )
        self.tbl_operadores.grid(row=4, column=0, columnspan=2, padx=8, pady=4, sticky="ew")
        self.tbl_operadores.insert("1.0", "Pendiente de analisis...")

    def _build_detalle(self):
        self.text_detalle = ctk.CTkTextbox(
            self.tab_det, fg_color="#0D1117",
            text_color="#C9D1D9", font=("Consolas", 12)
        )
        self.text_detalle.pack(fill="both", expand=True)
        self.text_detalle.insert("1.0", "Esperando analisis...")

    def _build_historial(self):
        self.text_hist = ctk.CTkTextbox(
            self.tab_hist, fg_color="#0D1117",
            text_color="#C9D1D9", font=("Consolas", 11)
        )
        self.text_hist.pack(fill="both", expand=True)
        self.text_hist.insert("1.0", "Esperando analisis...")

    def _build_errores(self):
        self.text_errores = ctk.CTkTextbox(
            self.tab_err, fg_color="#0D1117",
            text_color="#FF6B6B", font=("Consolas", 12)
        )
        self.text_errores.pack(fill="both", expand=True)
        self.text_errores.insert("1.0", "Esperando analisis...")


    def _agregar_expr(self):
        texto = self.entry_expr.get().strip()
        if not texto:
            return
        ok, errores = self.analizador.agregar_expresion(texto)
        self.entry_expr.delete(0, tk.END)
        self._refrescar_lista()
        if not ok:
            messagebox.showwarning(
                "Expresion con errores",
                "Se agrego la expresion pero contiene errores:\n\n" + "\n".join(errores)
            )

    def _refrescar_lista(self):
        self.lista_exprs.delete("1.0", tk.END)
        for i, (expr, _, ops, nums, errs) in enumerate(
                self.analizador.resultados_por_expresion, 1):
            estado = "OK" if not errs else f"{len(errs)} error(es)"
            self.lista_exprs.insert(
                tk.END,
                f"[{i}] {expr}\n"
                f"     ops={len(ops)}  nums={len(nums)}  {estado}\n\n"
            )

    def _analizar(self):
        if not self.analizador.expresiones:
            messagebox.showinfo("Sin expresiones", "Agrega al menos una expresion primero.")
            return

        self._actualizar_dashboard()
        self._actualizar_detalle()
        self._actualizar_historial()
        self._actualizar_errores()

        self.snapshot_idx = 0
        snaps = self.analizador.automata.snapshots
        if snaps:
            s = snaps[0]
            self._dibujar_sidebar(s['pila'], s)
            self.lbl_snap.configure(text=f"Paso: 1/{len(snaps)}")
        else:
            self._dibujar_sidebar([], None)
            self.lbl_snap.configure(text="Sin datos")

        self.tabview.set("DASHBOARD")

        n_err = self.analizador.total_errores()
        if n_err == 0:
            messagebox.showinfo("Analisis listo",
                                "Todas las expresiones son sintacticamente correctas.")
        else:
            messagebox.showwarning("Errores detectados",
                                   f"Se encontraron {n_err} error(es).\n"
                                   f"Revisa la pestana ERRORES.")

    def _actualizar_dashboard(self):
        a = self.analizador
        self.dash_widgets["expresiones"].configure(text=str(a.total_expresiones()))
        self.dash_widgets["operadores"].configure(text=str(a.total_operadores()))
        self.dash_widgets["numeros"].configure(text=str(a.total_numeros()))
        self.dash_widgets["tokens"].configure(text=str(len(a.todos_tokens)))
        self.dash_widgets["errores"].configure(text=str(a.total_errores()))

        conteo = a.conteo_por_operador()
        self.tbl_operadores.delete("1.0", tk.END)
        if conteo:
            nombres = {'+': 'suma', '-': 'resta', '*': 'mult',
                       '/': 'div', '%': 'modulo', '^': 'potencia'}
            linea = "  ".join(
                f"{op}({nombres.get(op, op)}): {n}"
                for op, n in sorted(conteo.items())
            )
            self.tbl_operadores.insert("1.0", linea)
        else:
            self.tbl_operadores.insert("1.0", "No hay operadores")

    def _actualizar_detalle(self):
        self.text_detalle.delete("1.0", tk.END)
        cabecera = (f"{'EXPR':<5} {'TIPO':<12} {'VALOR':<20} {'LINEA':<5}\n"
                    + "-" * 50 + "\n")
        self.text_detalle.insert("1.0", cabecera)
        for i, (_, tokens, _, _, _) in enumerate(
                self.analizador.resultados_por_expresion, 1):
            for tipo, valor, linea in tokens:
                self.text_detalle.insert(
                    tk.END, f"[{i}]   {tipo:<12} {str(valor):<20} {linea}\n"
                )
            self.text_detalle.insert(tk.END, "\n")

    def _actualizar_historial(self):
        self.text_hist.delete("1.0", tk.END)
        hist = self.analizador.automata.historial
        if hist:
            self.text_hist.insert("1.0", "\n".join(hist))
        else:
            self.text_hist.insert(
                "1.0",
                "No hubo operaciones de pila.\n"
                "Ninguna expresion contiene agrupadores ( ) [ ]"
            )

    def _actualizar_errores(self):
        self.text_errores.delete("1.0", tk.END)
        errs = self.analizador.automata.errores
        if errs:
            for e in errs:
                self.text_errores.insert(tk.END, f"  {e}\n\n")
        else:
            self.text_errores.insert(
                "1.0",
                "Todas las expresiones son sintacticamente correctas.\n"
                "No se detectaron errores."
            )

    def _limpiar(self):
        self.analizador.reset()
        self.snapshot_idx = 0
        self.lista_exprs.delete("1.0", tk.END)
        self.lista_exprs.insert("1.0", "Aun no hay expresiones...\n")
        self.text_detalle.delete("1.0", tk.END)
        self.text_detalle.insert("1.0", "Esperando analisis...")
        self.text_hist.delete("1.0", tk.END)
        self.text_hist.insert("1.0", "Esperando analisis...")
        self.text_errores.delete("1.0", tk.END)
        self.text_errores.insert("1.0", "Esperando analisis...")
        self.tbl_operadores.delete("1.0", tk.END)
        self.tbl_operadores.insert("1.0", "Pendiente de analisis...")
        self.canvas_pila.delete("all")
        self.lbl_snap.configure(text="Paso: 0/0")
        self.lbl_op_sidebar.configure(text="")
        for w in self.dash_widgets.values():
            w.configure(text="0")

    # Visualizacion pila sidebar 

    def _dibujar_sidebar(self, pila_estado, snap_info):
        self.canvas_pila.delete("all")

        if not pila_estado:
            self.canvas_pila.create_text(
                109, 95, text="Pila vacia",
                fill="#555555", font=("Courier New", 11)
            )
            if snap_info is None:
                self.lbl_op_sidebar.configure(text="")
            return

        bw, bh, sx, sy = 178, 30, 15, 182
        colores = {'(': '#C678DD', '[': '#61AFEF'}

        for i, elem in enumerate(pila_estado):
            y       = sy - i * (bh + 5)
            es_tope = (i == len(pila_estado) - 1)
            color   = colores.get(elem, '#555555')
            borde   = "#FFFFFF" if es_tope else "#666666"
            grosor  = 2 if es_tope else 1

            self.canvas_pila.create_rectangle(
                sx, y - bh, sx + bw, y,
                fill=color, outline=borde, width=grosor
            )
            self.canvas_pila.create_text(
                sx + bw / 2, y - bh / 2,
                text=elem, fill="#FFFFFF", font=("Courier New", 14, "bold")
            )
            if es_tope:
                self.canvas_pila.create_text(
                    sx - 8, y - bh / 2,
                    text="▶", fill=self.col_pink,
                    font=("Arial", 10, "bold"), anchor="e"
                )

        if snap_info:
            col_op = "#4CAF50" if snap_info['op'] == 'PUSH' else "#F44336"
            sym    = "⬇" if snap_info['op'] == 'PUSH' else "⬆"
            self.lbl_op_sidebar.configure(
                text=f"{sym} L{snap_info['linea']}: {snap_info['op']} '{snap_info['elem']}'",
                text_color=col_op
            )

    def _snap_prev(self):
        snaps = self.analizador.automata.snapshots
        if self.snapshot_idx > 0:
            self.snapshot_idx -= 1
            s = snaps[self.snapshot_idx]
            self._dibujar_sidebar(s['pila'], s)
            self.lbl_snap.configure(text=f"Paso: {self.snapshot_idx + 1}/{len(snaps)}")

    def _snap_next(self):
        snaps = self.analizador.automata.snapshots
        if self.snapshot_idx < len(snaps) - 1:
            self.snapshot_idx += 1
            s = snaps[self.snapshot_idx]
            self._dibujar_sidebar(s['pila'], s)
            self.lbl_snap.configure(text=f"Paso: {self.snapshot_idx + 1}/{len(snaps)}")


def main():
    app = AppGUI()
    app.mainloop()


if __name__ == "__main__":
    main()