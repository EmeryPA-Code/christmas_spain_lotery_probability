import random
import sys

# Forzar UTF-8 en salida estándar si es posible, sino, evitar caracteres especiales
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass # Versiones viejas de python o entornos raros

def main():
    print("=== ESTADISTICAS LOTERIA DE NAVIDAD 2025 ===")
    print("------------------------------------------")
    print("Este programa te ayuda a entender las probabilidades de ganar")
    print("diferentes premios basado en la cantidad de decimos que juegas.")
    print("Nota: Asumimos que juegas numeros DISTINTOS (que es lo logico para aumentar probabilidad).\n")

    # 1. Definicion de Datos (Basado en el texto proporcionado)
    TOTAL_NUMEROS = 100_000  # Del 00000 al 99999
    
    # Estructura de premios: (Nombre, Cantidad de numeros ganadores, Premio por decimo)
    premios = [
        {"nombre": "El Gordo (1er Premio)", "cantidad": 1, "premio": 400_000},
        {"nombre": "Segundo Premio", "cantidad": 1, "premio": 125_000},
        {"nombre": "Tercer Premio", "cantidad": 1, "premio": 50_000},
        {"nombre": "Cuartos Premios", "cantidad": 2, "premio": 20_000},
        {"nombre": "Quintos Premios", "cantidad": 8, "premio": 6_000},
        {"nombre": "La Pedrea", "cantidad": 1_794, "premio": 100},
        {"nombre": "Aproximaciones Gordo", "cantidad": 2, "premio": 2_000}, # Anterior y posterior
    ]

    # Total de numeros que tienen alguno de estos premios directos (sin contar solapamientos complejos o reintegros por ahora)
    # Nota: Las aproximaciones son numeros especificos distintos a los premios principales, 
    # pero tecnicamente un numero de pedrea podria ser una aproximacion? 
    # En la realidad, las normas son complejas (generalmente premios no acumulables excepto con reintegro),
    # pero para este ejercicio de estadistica basica, sumaremos las "oportunidades" como casos favorables.
    
    total_premios_listados = sum(p["cantidad"] for p in premios)
    
    # El Reintegro es un caso especial interesante para estadistica: 10% de probabilidad (ultima cifra)
    CANTIDAD_REINTEGROS = 9_999 # 10,000 terminaciones menos el Gordo (que ya cobra el Gordo) => Aprox 10%

    try:
        cantidad_decimos = int(input("Cuantos decimos con numeros DISTINTOS tienes?: "))
        if cantidad_decimos < 1:
            print("Necesitas al menos un decimo para jugar!")
            return
        if cantidad_decimos > TOTAL_NUMEROS:
            print("No puedes tener mas decimos que numeros posibles!")
            return
    except ValueError:
        print("Por favor, introduce un numero valido.")
        return

    print(f"\n ANALISIS PARA {cantidad_decimos} DECIMO(S):")
    print("-" * 50)

    # Calculo de Probabilidades usando la Regla de Laplace y Probabilidad Complementaria
    # Probabilidad de que ocurra al menos una vez = 1 - P(no ocurra nunca)
    
    def calcular_probabilidad_al_menos_uno(casos_favorables, mis_intentos, total_casos):
        """
        Calcula la probabilidad de ganar al menos UN premio de la categoria dada.
        Usa la logica: 1 - (Probabilidad de PERDER todos los intentos)
        """
        casos_perdedores = total_casos - casos_favorables
        
        # Si mis intentos son mayores que los casos perdedores, seguro gano algo (probabilidad 100%)
        if mis_intentos > casos_perdedores:
            return 1.0
            
        probabilidad = (casos_favorables / total_casos) * mis_intentos
        return probabilidad

    total_inversion = cantidad_decimos * 20 # 20 euros por decimo estandar
    print(f"Inversion estimada: {total_inversion} EUR\n")

    print(f"{'PREMIO':<25} | {'PREMIO/DECIMO':<15} | {'CANTIDAD':<10} | {'PROBABILIDAD (Aprox)':<20}")
    print("-" * 80)

    for p in premios:
        prob = calcular_probabilidad_al_menos_uno(p["cantidad"], cantidad_decimos, TOTAL_NUMEROS)
        porcentaje = prob * 100
        # Formato amigable: 1 entre X
        uno_entre = int(1/prob) if prob > 0 else 0
        
        premio_fmt = f"{p['premio']:,} EUR".replace(",", ".")
        print(f"{p['nombre']:<25} | {premio_fmt:<15} | {p['cantidad']:<10} | {porcentaje:.5f}%  (1 entre {uno_entre})")

    print("-" * 80)
    
    # Probabilidad de ganar "Algo" (Cualquiera de los listados arriba)
    prob_algo = calcular_probabilidad_al_menos_uno(total_premios_listados, cantidad_decimos, TOTAL_NUMEROS)
    print(f"\n Probabilidad de ganar ALGUNO de los premios principales (inc. Pedrea): {prob_algo*100:.4f}%")
    print(f"   (Aproximadamente 1 entre {int(1/prob_algo)})")

    # Reintegro
    prob_reintegro = calcular_probabilidad_al_menos_uno(10_000, cantidad_decimos, TOTAL_NUMEROS)
    print(f"\n Probabilidad de recuperar lo jugado (Reintegro - 10%): {prob_reintegro*100:.2f}%")
    
    print("\n\n--- EXPLICACION PARA ESTUDIANTE ---")
    print("La probabilidad basica se calcula como: Casos Favorables / Casos Posibles.")
    print(f"Por ejemplo, para El Gordo hay 1 caso favorable entre {TOTAL_NUMEROS} posibles.")
    print(f"Si tienes {cantidad_decimos} decimos, tienes {cantidad_decimos} oportunidades.")
    print("Por eso la probabilidad aproximada es simplemente: (1/100000) * tus_decimos.")
    print("Mucha suerte!")

if __name__ == "__main__":
    main()
