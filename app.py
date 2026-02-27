from backend.model import predecir_precio

print("=== Predicción de Precio de Vivienda ===")

calidad = int(input("Ingrese calidad (1-10): "))
area = float(input("Ingrese área habitable: "))
habitaciones = int(input("Ingrese número de habitaciones: "))
banos = int(input("Ingrese número de baños: "))
garaje = int(input("Ingrese número de garajes "))

precio = predecir_precio(calidad, area, habitaciones, banos, garaje)

print("\nPrecio estimado: $", precio)