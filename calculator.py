import tkinter as tk
from tkinter import ttk, messagebox
import math

# Calculator functions
def calculate_expression(expr):
    try:
        expr = expr.replace('×', '*').replace('÷', '/').replace('^', '**')
        expr = expr.replace('√', 'math.sqrt')
        expr = expr.replace('sin', 'math.sin(math.radians')
        expr = expr.replace('cos', 'math.cos(math.radians')
        expr = expr.replace('tan', 'math.tan(math.radians')
        expr = expr.replace('log', 'math.log10')
        expr = expr.replace(')', '))') if any(f in expr for f in ['sin(', 'cos(', 'tan(']) else expr
        result = eval(expr, {"math": math, "__builtins__": {}})
        return str(result)
    except Exception:
        return "Error"

# Color palette for buttons
BTN_COLORS = [
    "#FFB347", "#FF6961", "#77DD77", "#AEC6CF",
    "#CBAACB", "#B39EB5", "#779ECB", "#966FD6",
    "#F49AC2", "#FFB347", "#FF6961", "#77DD77",
    "#AEC6CF", "#CBAACB", "#B39EB5", "#779ECB",
    "#966FD6", "#F49AC2", "#FFB347", "#FF6961",
    "#77DD77", "#AEC6CF", "#CBAACB", "#B39EB5",
    "#779ECB", "#966FD6", "#F49AC2"
]

class AnimatedLabel(ttk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.colors = ["#fff", "#f8ffae", "#43c6ac", "#191654"]
        self.idx = 0
        self.animate()

    def animate(self):
        self.configure(foreground=self.colors[self.idx])
        self.idx = (self.idx + 1) % len(self.colors)
        self.after(400, self.animate)

class CalculatorUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("340x500")
        self.resizable(False, False)
        self.configure(bg="#222")

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TButton', font=('Segoe UI', 16), padding=8, background="#444", foreground="#fff")
        style.map('TButton',
                  background=[('active', '#333')],
                  foreground=[('active', '#f8ffae')])
        style.configure('Display.TLabel', font=('Segoe UI', 28), background="#222", foreground="#fff")

        self.expression = ""
        self.create_widgets()

    def create_widgets(self):
        # Animated Display
        self.display_var = tk.StringVar(value="")
        display = AnimatedLabel(self, textvariable=self.display_var, anchor='e', style='Display.TLabel', background="#222")
        display.pack(fill='x', padx=10, pady=(20, 10), ipady=10)

        # Button layout
        btns = [
            ['C', '√', '^', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '(', ')'],
            ['sin', 'cos', 'tan', 'log'],
            ['=']
        ]
        btn_frame = ttk.Frame(self)
        btn_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.btn_widgets = []
        color_idx = 0
        for r, row in enumerate(btns):
            for c, char in enumerate(row):
                btn = tk.Button(
                    btn_frame, text=char, font=('Segoe UI', 16, 'bold'),
                    bg=BTN_COLORS[color_idx % len(BTN_COLORS)],
                    fg="#222", activebackground="#fff", activeforeground="#222",
                    bd=0, relief='ridge',
                    command=lambda ch=char: self.on_button_click(ch)
                )
                btn.grid(row=r, column=c, sticky='nsew', padx=3, pady=3)
                self.btn_widgets.append(btn)
                color_idx += 1
        # Make buttons expand equally
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(len(btns)):
            btn_frame.rowconfigure(i, weight=1)

        self.animate_buttons()

    def animate_buttons(self):
        # Animate button background colors in a wave
        for idx, btn in enumerate(self.btn_widgets):
            orig_color = BTN_COLORS[idx % len(BTN_COLORS)]
            def make_anim(b, color1, color2):
                def anim(step=0):
                    b.configure(bg=color1 if step % 2 == 0 else color2)
                    b.after(800 + (idx % 4) * 100, lambda: anim(step+1))
                return anim
            make_anim(btn, orig_color, "#fff")()
        # No need to call after here, each anim schedules itself

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            result = calculate_expression(self.expression)
            # Flash display if error
            if result == "Error":
                self.flash_display()
            self.expression = result
        else:
            if char in ['sin', 'cos', 'tan', 'log', '√']:
                if char == '√':
                    self.expression += '√('
                else:
                    self.expression += f"{char}("
            else:
                self.expression += char
        self.display_var.set(self.expression)

    def flash_display(self):
        # Flash the display background to red on error
        display_widget = self.winfo_children()[0]
        orig_bg = display_widget.cget("background")
        def flash(count=0):
            if count < 4:
                display_widget.configure(background="#ff6961" if count % 2 == 0 else orig_bg)
                self.after(100, lambda: flash(count+1))
            else:
                display_widget.configure(background=orig_bg)
        flash()

if __name__ == "__main__":
    app = CalculatorUI()
    app.mainloop()
