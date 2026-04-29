import tkinter as tk
from tkinter import messagebox
from programa import ArbolDiagnostico

class AplicacionGUI(tk.Tk):
    def __init__(self, json_file):
        super().__init__()
        self.title("Diagnóstico de Vehículos con IA")
        self.geometry("600x500")
        
        self.arbol = ArbolDiagnostico(json_file)
        
        if self.arbol.raiz is None:
            messagebox.showerror("Error", "No se pudo cargar la base de conocimientos JSON.")
            self.destroy()
            return
            
        self.crear_widgets()
        self.actualizar_vista()

    def crear_widgets(self):
        # Marco para el título y pregunta actual
        self.frame_top = tk.Frame(self, pady=20)
        self.frame_top.pack(fill=tk.X)
        
        self.lbl_pregunta = tk.Label(self.frame_top, text="", font=("Arial", 14, "bold"), wraplength=550)
        self.lbl_pregunta.pack()

        # Marco para los botones de opciones
        self.frame_opciones = tk.Frame(self, pady=10)
        self.frame_opciones.pack(fill=tk.BOTH, expand=True)

        # Marco para el texto de resultado IA
        self.frame_resultado = tk.Frame(self, pady=10)
        
        self.lbl_resultado_titulo = tk.Label(self.frame_resultado, text="Soluciones Generadas por la IA:", font=("Arial", 12, "bold"))
        self.lbl_resultado_titulo.pack(anchor=tk.W)
        
        self.text_resultado = tk.Text(self.frame_resultado, height=10, width=70, wrap=tk.WORD, font=("Arial", 11))
        self.text_resultado.pack(pady=5)
        self.text_resultado.config(state=tk.DISABLED)
        
        self.btn_reiniciar = tk.Button(self.frame_resultado, text="Empezar de nuevo", font=("Arial", 12), command=self.reiniciar, bg="#d4edda")
        self.btn_reiniciar.pack(pady=10)

    def actualizar_vista(self):
        # Limpiar opciones actuales
        for widget in self.frame_opciones.winfo_children():
            widget.destroy()
            
        self.frame_resultado.pack_forget()

        nodo_actual = self.arbol.nodo_actual

        if nodo_actual is None:
            return

        # Si llegamos a una hoja o es un diagnóstico
        if not nodo_actual.hijos or nodo_actual.es_diagnostico:
            self.lbl_pregunta.config(text=f"Diagnóstico encontrado:\n{nodo_actual.valor}")
            self.frame_opciones.pack_forget()
            self.frame_resultado.pack(fill=tk.BOTH, expand=True)
            
            # Consultar IA
            self.text_resultado.config(state=tk.NORMAL)
            self.text_resultado.delete("1.0", tk.END)
            self.text_resultado.insert(tk.END, "Consultando a la IA, por favor espere...\n")
            self.update_idletasks()
            
            respuesta_ia = self.arbol.generar_soluciones_ia(nodo_actual.valor)
            
            self.text_resultado.delete("1.0", tk.END)
            self.text_resultado.insert(tk.END, respuesta_ia)
            self.text_resultado.config(state=tk.DISABLED)
        else:
            self.lbl_pregunta.config(text=nodo_actual.valor)
            self.frame_opciones.pack(fill=tk.BOTH, expand=True)
            
            for i, hijo in enumerate(nodo_actual.hijos):
                btn = tk.Button(
                    self.frame_opciones, 
                    text=hijo.valor, 
                    font=("Arial", 12), 
                    command=lambda i=i: self.seleccionar(i),
                    wraplength=450,
                    pady=5
                )
                btn.pack(pady=5, fill=tk.X, padx=50)

    def seleccionar(self, indice):
        if self.arbol.seleccionar_opcion(indice):
            self.actualizar_vista()

    def reiniciar(self):
        self.arbol.reiniciar()
        self.frame_resultado.pack_forget()
        self.actualizar_vista()

if __name__ == "__main__":
    app = AplicacionGUI("vehiculos.json")
    app.mainloop()