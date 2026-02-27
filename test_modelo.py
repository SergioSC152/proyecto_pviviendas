"""
Script de prueba para verificar que el modelo carga y predice correctamente.
Ejecutar: python test_modelo.py
"""

import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    
    from backend.model import cargar_modelo, predecir_precio
    print("✅ Módulos cargados correctamente")
    
    
    print("\n📝 Ejecutando predicción de prueba...")
    print("   Calidad: 7/10")
    print("   Área: 1500 sq ft")
    print("   Habitaciones: 3")
    print("   Baños: 2")
    print("   Garajes: 2")
    
    precio = predecir_precio(7, 1500.0, 3, 2, 2)
    print(f"\n💰 Precio estimado: ${precio:,.2f}")
    
    
    if 50000 <= precio <= 500000:
        print("✅ Precio dentro de rango esperado")
    else:
        print("⚠️ Precio fuera de rango - revisar modelo")
        
except FileNotFoundError:
    print("❌ Error: No se encontró el archivo del modelo")
    print("   Asegúrate de que exista: models/modelo_regression.pkl")
    
except ImportError as e:
    print(f"❌ Error importando: {e}")
    print("   Verifica que backend/model.py exista y tenga las funciones")
    
except Exception as e:
    print(f"❌ Error inesperado: {e}")

input("\nPresiona Enter para salir...")