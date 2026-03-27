from backend.model import predecir_precio

print("=== Predicción de Precio de Vivienda ===")

try:
    calidad = int(input("Ingrese calidad (1-10): "))
    area = float(input("Ingrese área habitable: "))
    habitaciones = int(input("Ingrese número de habitaciones: "))
    banos = int(input("Ingrese número de baños: "))
    garaje = int(input("Ingrese número de garajes: "))

    datos = [calidad, area, habitaciones, banos, garaje]

    # Logs (seguimiento del proceso)
    print("Datos ingresados:", datos)
    print("Procesando predicción...")

    precio = predecir_precio(*datos)

    print("Resultado obtenido:", precio)
    print("\nPrecio estimado: $", precio)

except Exception as e:
    print("Error en los datos ingresados:", e)
