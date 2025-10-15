import random
import time
import os

class Floristeria:
    def __init__(self):
        self.descripciones = {
            1: {
                "titulo": "🏠 PARTE FRONTAL",
                "detalles": [
                    "Techo de tejas anaranjadas brillantes",
                    "Pared blanca impecable con detalles en madera",
                    "Pasto verde esmeralda bien cuidado",
                    "Árbol centenario de copa frondosa",
                    "3 macetas con: rosa roja, girasol amarillo y lirio morado"
                ]
            },
            2: {
                "titulo": "⬅️ PARTE LATERAL IZQUIERDA", 
                "detalles": [
                    "Pared blanca con ventana de marco café",
                    "Vidrio transparente con cortinas blancas",
                    "Pasto verde con camino de piedras",
                    "2 jardineras con: margarita blanca y tulipán naranja",
                    "Pequeño seto decorativo"
                ]
            },
            3: {
                "titulo": "➡️ PARTE LATERAL DERECHA",
                "detalles": [
                    "Pared blanca lisa sin ventanas",
                    "Puerta principal color rosado pastel",
                    "Pomo dorado brillante",
                    "Pasto verde con bordes floreados",
                    "Bienvenida escrita en madera sobre la puerta"
                ]
            },
            4: {
                "titulo": "🔙 PARTE POSTERIOR",
                "detalles": [
                    "Pared blanca con diseño geométrico",
                    "Techo triangular pintado de azul cielo",
                    "Pasto verde con diseño de espiral",
                    "4 flores en maceteros: orquídea, dalia, clavel y geranio",
                    "Pequeña fuente de agua en el centro"
                ]
            }
        }
    
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_parte(self, numero_parte):
        if numero_parte in self.descripciones:
            parte = self.descripciones[numero_parte]
            print(f"\n{parte['titulo']}")
            print("=" * 50)
            for detalle in parte['detalles']:
                print(f"• {detalle}")
                time.sleep(0.3)
            print("=" * 50)
    
    def mostrar_menu_principal(self):
        self.limpiar_pantalla()
        print("🌻 FLORISTERÍA 'CARLITOS' - TOUR VISUAL 🌻")
        print("=" * 55)
        opciones = [
            "1. Explorar Parte Frontal 🏠",
            "2. Explorar Parte Lateral Izquierda ⬅️", 
            "3. Explorar Parte Lateral Derecha ➡️",
            "4. Explorar Parte Posterior 🔙",
            "5. Salir del Tour 👋"
        ]
        for opcion in opciones:
            print(opcion)
            time.sleep(0.2)
        print("=" * 55)

def main():
    floristeria = Floristeria()
    
    while True:
        floristeria.mostrar_menu_principal()
        
        eleccion = input("\nSelecciona una opción (1-5): ").strip()
        
        if eleccion == "5":
            print("\n¡Gracias por visitar la Floristería Carlitos! 🌸")
            break
        elif eleccion in ["1", "2", "3", "4"]:
            floristeria.mostrar_parte(int(eleccion))
            input("\nPresiona Enter para continuar...")
        else:
            print("\n❌ Opción no válida. Por favor, selecciona 1-5.")
            time.sleep(1)

if __name__ == "__main__":
    main()