from model import predecir_precio 

print(" SISTEMA DE PREDICCIÓN DE VIVIENDAS\n")

calidad = int(input("Ingresa la calidad (1 - 5): "))
area = int(input("Ingresa el área (m²): "))
habitaciones = int(input("Número de habitaciones: "))
banos = int(input("Número de baños: "))
garaje = int(input("Número de garajes: "))
anio = int(input("Año de construcción: "))  

precio = predecir_precio(calidad, area, habitaciones, banos, garaje, anio)

print("\nPrecio estimado:", precio)