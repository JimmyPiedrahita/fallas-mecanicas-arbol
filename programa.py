import json
from dotenv import load_dotenv
from groq import Groq

class Nodo:
    def __init__(self, valor, es_diagnostico=False):
        self.valor = valor
        self.es_diagnostico = es_diagnostico
        self.hijos = []

    def agregar_hijo(self, nodo):
        self.hijos.append(nodo)

class ArbolDiagnostico:
    def __init__(self, json_file):
        load_dotenv()
        self.client = Groq()
        self.raiz = self.cargar_arbol(json_file)
        self.nodo_actual = self.raiz
        self.camino = []

    def cargar_arbol(self, json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self._construir_nodo(data)
        except Exception as e:
            print(f"Error al cargar el archivo JSON: {e}")
            return None

    def _construir_nodo(self, data):
        es_diag = data.get("es_diagnostico", False)
        nodo = Nodo(data["valor"], es_diag)
        if "hijos" in data:
            for hijo_data in data["hijos"]:
                nodo.agregar_hijo(self._construir_nodo(hijo_data))
        return nodo

    def seleccionar_opcion(self, indice):
        if self.nodo_actual and 0 <= indice < len(self.nodo_actual.hijos):
            self.camino.append(self.nodo_actual.valor)
            self.nodo_actual = self.nodo_actual.hijos[indice]
            return True
        return False

    def reiniciar(self):
        self.nodo_actual = self.raiz
        self.camino = []

    def generar_soluciones_ia(self, diagnostico):
        historial = " -> ".join(self.camino)
        prompt = f"El usuario reporta los siguientes síntomas: {historial}. El diagnóstico preliminar es: '{diagnostico}'. Por favor, genera posibles soluciones muy resumidas para este problema."
        print(f"\n[GROQ] Generando soluciones con el siguiente prompt:\n{prompt}")
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un mecánico experto que da respuestas prácticas y directas para problemas de vehículos."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Hubo un error al contactar a la IA: {e}"