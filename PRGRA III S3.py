import tkinter as tk
from tkinter import messagebox, filedialog


class TextAnalyzer:
    def __init__(self, text):
        self.original_text = text
        self.normalized_text = ""
        self.tokens = []
        self.counts = {}

    def normalize_text(self):
        text = self.original_text.lower()

        punctuation = ".,;:!?()[]{}\"'"

        for char in punctuation:
            text = text.replace(char, "")

        text = " ".join(text.split())

        self.normalized_text = text

        return text

    def tokenize(self):
        self.tokens = self.normalized_text.split()
        return self.tokens

    def analyze(self):
        self.normalize_text()
        self.tokenize()

        self.counts = {}

        for token in self.tokens:
            self.counts[token] = self.counts.get(token, 0) + 1

    def generate_report(self):
        if not self.tokens:
            return "No hay datos para analizar."

        total_tokens = len(self.tokens)
        unique_tokens = len(set(self.tokens))

        report = "===== REPORTE =====\n\n"
        report += f"Total de palabras: {total_tokens}\n"
        report += f"Palabras únicas: {unique_tokens}\n\n"

        report += "Top 10 palabras más frecuentes:\n"

        top = sorted(
            self.counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        for word, count in top:
            report += f"{word}: {count}\n"

        lengths = [len(word) for word in self.tokens]

        avg_length = sum(lengths) / len(lengths)

        report += f"\nLongitud promedio: {avg_length:.2f}\n"

        max_len = max(lengths)
        min_len = min(lengths)

        longest = sorted(
            set(word for word in self.tokens if len(word) == max_len)
        )

        shortest = sorted(
            set(word for word in self.tokens if len(word) == min_len)
        )

        report += "\nPalabra(s) más larga(s):\n"
        report += ", ".join(longest)

        report += "\n\nPalabra(s) más corta(s):\n"
        report += ", ".join(shortest)

        return report

    def query(self, word):
        word = word.lower()

        freq = self.counts.get(word, 0)

        if freq == 0:
            return "La palabra no aparece en el texto."

        percentage = (freq / len(self.tokens)) * 100

        result = f"Frecuencia: {freq}\n"
        result += f"Porcentaje: {percentage:.2f}%\n"

        if freq == 1:
            result += "Clasificación: Rara"
        elif freq >= 5:
            result += "Clasificación: Común"
        else:
            result += "Clasificación: Normal"

        return result


def cargar_archivo():
    ruta = filedialog.askopenfilename(
        filetypes=[("Archivos de texto", "*.txt")]
    )

    if not ruta:
        return

    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()

        if not contenido.strip():
            raise ValueError("El archivo está vacío.")

        texto.delete("1.0", tk.END)
        texto.insert(tk.END, contenido)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def analizar_texto():
    global analyzer

    contenido = texto.get("1.0", tk.END).strip()

    if not contenido:
        messagebox.showerror(
            "Error",
            "Debe ingresar un texto."
        )
        return

    try:
        analyzer = TextAnalyzer(contenido)

        analyzer.analyze()

        reporte.delete("1.0", tk.END)

        reporte.insert(
            tk.END,
            analyzer.generate_report()
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )


def consultar_palabra():
    if analyzer is None:
        messagebox.showerror(
            "Error",
            "Primero analice un texto."
        )
        return

    palabra = entrada_palabra.get().strip()

    if not palabra:
        messagebox.showerror(
            "Error",
            "Ingrese una palabra."
        )
        return

    resultado = analyzer.query(palabra)

    resultado_consulta.config(
        text=resultado
    )


def run_tests():
    prueba = TextAnalyzer(
        "Hola, Mundo!! Python 3."
    )

    assert (
        prueba.normalize_text()
        == "hola mundo python 3"
    )

    prueba = TextAnalyzer(
        "hola hola mundo"
    )

    prueba.analyze()

    assert prueba.counts["hola"] == 2
    assert prueba.counts["mundo"] == 1

    print("Pruebas ejecutadas correctamente.")


run_tests()

analyzer = None

ventana = tk.Tk()
ventana.title("Analizador de Texto")
ventana.geometry("850x700")

titulo = tk.Label(
    ventana,
    text="Analizador de Texto",
    font=("Arial", 18, "bold")
)

titulo.pack(pady=10)

btn_archivo = tk.Button(
    ventana,
    text="Cargar Archivo TXT",
    command=cargar_archivo
)

btn_archivo.pack(pady=5)

texto = tk.Text(
    ventana,
    width=90,
    height=12
)

texto.pack(pady=10)

btn_analizar = tk.Button(
    ventana,
    text="Analizar Texto",
    command=analizar_texto
)

btn_analizar.pack(pady=5)

reporte = tk.Text(
    ventana,
    width=90,
    height=15
)

reporte.pack(pady=10)

tk.Label(
    ventana,
    text="Consultar palabra:"
).pack()

entrada_palabra = tk.Entry(
    ventana,
    width=30
)

entrada_palabra.pack(pady=5)

btn_consultar = tk.Button(
    ventana,
    text="Buscar",
    command=consultar_palabra
)

btn_consultar.pack(pady=5)

resultado_consulta = tk.Label(
    ventana,
    text="",
    justify="left",
    font=("Arial", 11)
)

resultado_consulta.pack(pady=10)

ventana.mainloop()