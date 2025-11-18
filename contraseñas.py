import tkinter as tk
from tkinter import ttk, messagebox
import re # Módulo para expresiones regulares
import math # Para la verificación de palíndromos

class PasswordGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Juego de la Contraseña (15 Reglas)")
        self.geometry("800x750")
        self.config(padx=20, pady=20)
        
        self.rules_status = {}
        self.rules_labels = []

        # 1. Definir las reglas PRIMERO
        self.define_rules()
        
        # 2. Luego, configurar la interfaz (que usa self.rules)
        self.setup_ui()
        
        
    def define_rules(self):
        """Define las 15 reglas como una lista de diccionarios y asegura que self.rules exista."""
        self.rules = [
            # Reglas del Equipo 1 (Fundamentos)
            {"id": 1, "text": "1. La contraseña debe tener al menos 15 caracteres de longitud.", "check": self.check_rule_1},
            {"id": 2, "text": "2. Debe contener al menos una mayúscula, una minúscula y un número.", "check": self.check_rule_2},
            {"id": 3, "text": "3. Debe incluir un carácter especial (e.g., !, @, #, $).", "check": self.check_rule_3},
            {"id": 4, "text": "4. El valor numérico del año actual (2025) debe aparecer en algún lugar.", "check": self.check_rule_4},
            {"id": 5, "text": "5. Debe incluir el nombre de uno de los patrocinadores: Pepsi, Starbucks, o Shell.", "check": self.check_rule_5},

            # Reglas del Equipo 2 (Absurdo y Matemáticas)
            {"id": 6, "text": "6. Debe contener un número que sea un múltiplo de 7 (sin incluir 7 o 14).", "check": self.check_rule_6},
            {"id": 7, "text": "7. Debe incluir un número romano cuya suma total sea 35 (I, V, X, L, C...).", "check": self.check_rule_7},
            {"id": 8, "text": "8. Debe contener el nombre de un continente escrito en mayúsculas y al revés.", "check": self.check_rule_8},
            {"id": 9, "text": "9. Ningún número adyacente puede sumar más de 9 (¡Regla Absurda!).", "check": self.check_rule_9},
            {"id": 10, "text": "10. El número total de vocales (a, e, i, o, u) debe ser un número primo.", "check": self.check_rule_10},

            # Reglas del Equipo 3 (Complejidad y Contexto)
            {"id": 11, "text": "11. Debe incluir una fracción (escrita como caracteres) que represente un tercio o un cuarto (ej: 1/3, 1/4).", "check": self.check_rule_11},
            {"id": 12, "text": "12. Debe aparecer el nombre de la ciudad sede de las últimas olimpiadas de verano antes de París 2024 (Tokio).", "check": self.check_rule_12},
            {"id": 13, "text": "13. Debe contener una palabra de 6 letras que sea un palíndromo (ej: somos, reconocer).", "check": self.check_rule_13},
            {"id": 14, "text": "14. La suma de los índices de los caracteres especiales (empezando en 0) debe ser un múltiplo de 5.", "check": self.check_rule_14},
            {"id": 15, "text": "15. El número de veces que aparece la letra 'a' debe ser exactamente igual al número de veces que aparece la letra 'e'.", "check": self.check_rule_15},
        ]
        
    def setup_ui(self):
        """Configura los elementos de la interfaz gráfica."""
        # --- Contraseña Input ---
        input_frame = ttk.LabelFrame(self, text="🔑 Contraseña")
        input_frame.pack(fill="x", pady=10)

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", lambda *args: self.update_rules()) # Llama a update_rules en cada cambio
        
        ttk.Label(input_frame, text="Ingrese la contraseña:").pack(side="left", padx=5, pady=5)
        self.entry_password = ttk.Entry(input_frame, textvariable=self.password_var, show="*", width=50)
        self.entry_password.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Botón para mostrar/ocultar
        self.show_hide_btn = ttk.Button(input_frame, text="👁️ Mostrar", command=self.toggle_visibility)
        self.show_hide_btn.pack(side="left", padx=5)

        # --- Reglas Display ---
        rules_frame = ttk.LabelFrame(self, text="📜 Reglas a Cumplir")
        rules_frame.pack(fill="both", expand=True, pady=10)

        self.canvas = tk.Canvas(rules_frame)
        self.scrollbar = ttk.Scrollbar(rules_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Inicializar las etiquetas de las reglas (AQUÍ se usa self.rules)
        for i, rule in enumerate(self.rules):
            label = ttk.Label(self.scrollable_frame, text=rule['text'], font=("Arial", 10))
            label.pack(fill="x", padx=5, pady=2, anchor="w")
            self.rules_labels.append(label)
            self.rules_status[rule['id']] = False # Inicializar estado

        # Inicializar al inicio
        self.update_rules()

    def toggle_visibility(self):
        """Alterna la visibilidad de la contraseña."""
        current_show = self.entry_password.cget("show")
        if current_show == "*":
            self.entry_password.config(show="")
            self.show_hide_btn.config(text="🙈 Ocultar")
        else:
            self.entry_password.config(show="*")
            self.show_hide_btn.config(text="👁️ Mostrar")

    def update_rules(self):
        """Verifica todas las reglas y actualiza la GUI."""
        password = self.password_var.get()
        all_passed = True

        for i, rule in enumerate(self.rules):
            is_passed = rule['check'](password)
            self.rules_status[rule['id']] = is_passed
            
            label = self.rules_labels[i]
            
            if is_passed:
                label.config(foreground="green", text=f"✅ {rule['text']}")
            else:
                label.config(foreground="red", text=f"❌ {rule['text']}")
                all_passed = False
                
        if all_passed:
            self.entry_password.config(foreground="green")
            if not hasattr(self, '_win_shown'):
                 messagebox.showinfo("¡VICTORIA!", "¡Felicidades! Has cumplido las 15 reglas.")
                 self._win_shown = True 
        else:
            self.entry_password.config(foreground="black")
            if hasattr(self, '_win_shown'):
                 del self._win_shown
        
        # Ajustar el scroll region después de actualizar el texto
        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    # --- Funciones de Verificación de Reglas (Checkers) ---

    def check_rule_1(self, p):
        """Regla 1: 15 caracteres de longitud."""
        return len(p) >= 15

    def check_rule_2(self, p):
        """Regla 2: Mayúscula, minúscula, número."""
        return bool(re.search(r'[A-Z]', p) and re.search(r'[a-z]', p) and re.search(r'\d', p))

    def check_rule_3(self, p):
        """Regla 3: Carácter especial."""
        return bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]', p))

    def check_rule_4(self, p):
        """Regla 4: Contiene 2025."""
        return "2025" in p

    def check_rule_5(self, p):
        """Regla 5: Contiene un patrocinador (Pepsi, Starbucks, Shell)."""
        return bool(re.search(r'pepsi|starbucks|shell', p, re.IGNORECASE))

    def check_rule_6(self, p):
        """Regla 6: Contiene un número que sea múltiplo de 7 (no 7 o 14)."""
        numbers = re.findall(r'\d+', p)
        for num_str in numbers:
            num = int(num_str)
            if num % 7 == 0 and num not in [7, 14, 0]:
                return True
        return False

    def check_rule_7(self, p):
        """Regla 7: Romanos suman 35."""
        
        roman_chars = re.findall(r'[IVXLCivxlc]', p)
        if not roman_chars:
            return False
            
        roman_string = "".join(roman_chars).upper()
        
        total_sum = 0
        for char in roman_string:
            if char == 'I': total_sum += 1
            elif char == 'V': total_sum += 5
            elif char == 'X': total_sum += 10
            elif char == 'L': total_sum += 50
            elif char == 'C': total_sum += 100

        return total_sum == 35


    def check_rule_8(self, p):
        """Regla 8: Continente al revés en mayúsculas."""
        continents = ["NORTEAMERICA", "SURAMERICA", "EUROPA", "ASIA", "AFRICA", "OCEANIA", "ANTARTIDA"]
        reversed_continents = [c[::-1] for c in continents]
        
        return bool(re.search('|'.join(reversed_continents), p))

    def check_rule_9(self, p):
        """Regla 9: Ningún número adyacente puede sumar más de 9."""
        digits = re.findall(r'\d', p)
        for i in range(len(digits) - 1):
            if int(digits[i]) + int(digits[i+1]) > 9:
                return False
        return True

    def check_rule_10(self, p):
        """Regla 10: Número total de vocales (a, e, i, o, u) es un número primo."""
        vowels_count = len(re.findall(r'[aeiou]', p, re.IGNORECASE))
        
        if vowels_count <= 1:
            return False
        
        # Verificar si es primo
        for i in range(2, vowels_count):
            if (vowels_count % i) == 0:
                return False
        return True

    def check_rule_11(self, p):
        """Regla 11: Incluye 1/3 o 1/4."""
        fractions = [r'1[/\\_]3', r'1[/\\_]4', r'un[_\s]tercio', r'un[_\s]cuarto']
        return bool(re.search('|'.join(fractions), p, re.IGNORECASE))

    def check_rule_12(self, p):
        """Regla 12: Contiene 'Tokio'."""
        return bool(re.search(r'tokio|tokyo', p, re.IGNORECASE))

    def check_rule_13(self, p):
        """Regla 13: Contiene un palíndromo de 6 letras."""
        words_6 = re.findall(r'[a-zA-Z]{6}', p)
        for word in words_6:
            if word.lower() == word[::-1].lower():
                return True
        return False

    def check_rule_14(self, p):
        """Regla 14: Suma de índices de caracteres especiales es múltiplo de 5."""
        special_char_pattern = r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?`~]'
        
        total_index_sum = 0
        found = False
        
        for i, char in enumerate(p):
            if re.match(special_char_pattern, char):
                total_index_sum += i
                found = True
        
        if not found:
            return False
            
        return total_index_sum % 5 == 0

    def check_rule_15(self, p):
        """Regla 15: Conteo de 'a' igual a conteo de 'e' (ignora mayúsculas)."""
        count_a = p.lower().count('a')
        count_e = p.lower().count('e')
        return count_a == count_e


if __name__ == "__main__":
    app = PasswordGame()
    app.mainloop()