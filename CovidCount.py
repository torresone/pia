import matplotlib.pyplot as plt
import requests
import json
import openpyxl

# Función para obtener datos de la API
def obtener_datos():
    url = "https://disease.sh/v3/covid-19/historical/all?lastdays=all"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("La solicitud no fue exitosa; Estado:", response.status_code)
        return None

# Función para guardar datos en un archivo JSON
def guardar_datos_en_json(data, archivo):
    with open(archivo, "w") as file:
        json.dump(data, file)

# Función para cargar datos desde un archivo JSON
def cargar_datos_desde_json(archivo):
    try:
        with open(archivo, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("El archivo no existe.")
        return None

# Función para generar el gráfico
def generar_grafico(data):
    if data:
        dates = list(data['cases'].keys())
        cases = list(data['cases'].values())
        deaths = list(data['deaths'].values())
        recovered = list(data['recovered'].values())

        plt.figure(figsize=(12, 6))
        plt.plot(dates, cases, label='Casos', marker='o')
        plt.plot(dates, deaths, label='Muertes', marker='x')
        plt.plot(dates, recovered, label='Recuperados', marker='s')
        plt.xlabel('Fecha')
        plt.ylabel('Cantidad')
        plt.title('Evolución de casos, muertes y recuperados')
        plt.xticks(range(0, len(dates), 30), rotation=45)  # Mostrar una etiqueta por mes
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

# Función para guardar datos en un archivo Excel
def guardar_datos_en_excel(data, archivo):
    if data:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Fecha", "Casos", "Muertes", "Recuperados"])
        dates = list(data['cases'].keys())
        cases = list(data['cases'].values())
        deaths = list(data['deaths'].values())
        recovered = list(data['recovered'].values())
        for i in range(len(dates)):
            ws.append([dates[i], cases[i], deaths[i], recovered[i]])
        wb.save(archivo)

# Función para realizar cálculos estadísticos
def calcular_estadisticas(data):
    if data:
        cases = list(data['cases'].values())
        deaths = list(data['deaths'].values())
        recovered = list(data['recovered'].values())
        total_cases = sum(cases)
        total_deaths = sum(deaths)
        total_recovered = sum(recovered)
        max_cases = max(cases)
        max_deaths = max(deaths)
        max_recovered = max(recovered)
        min_cases = min(cases)
        min_deaths = min(deaths)
        min_recovered = min(recovered)
        promedio_cases = total_cases / len(cases)
        promedio_deaths = total_deaths / len(deaths)
        promedio_recovered = total_recovered / len(recovered)
        
        return {
            "Total de casos": total_cases,
            "Total de muertes": total_deaths,
            "Total de recuperados": total_recovered,
            "Máximo de casos en un día": max_cases,
            "Máximo de muertes en un día": max_deaths,
            "Máximo de recuperados en un día": max_recovered,
            "Mínimo de casos en un día": min_cases,
            "Mínimo de muertes en un día": min_deaths,
            "Mínimo de recuperados en un día": min_recovered,
            "Promedio de casos por día": promedio_cases,
            "Promedio de muertes por día": promedio_deaths,
            "Promedio de recuperados por día": promedio_recovered
        }
    else:
        return None

# Función para el menú
def menu():
    print("Menú:")
    print("1. Obtener datos de la API y guardarlos en un archivo JSON")
    print("2. Cargar datos desde un archivo JSON")
    print("3. Generar gráfico de datos")
    print("4. Guardar datos en un archivo Excel")
    print("5. Calcular estadísticas")
    print("6. Salir")

def main():
    data = None
    while True:
        menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            data = obtener_datos()
            if data:
                guardar_datos_en_json(data, "covid_data.json")  # Se puede cambiar el nombre de archivo
        elif opcion == "2":
            data = cargar_datos_desde_json("covid_data.json")  # Se puede cambiar el nombre de archivo
        elif opcion == "3":
            generar_grafico(data)
        elif opcion == "4":
            guardar_datos_en_excel(data, "covid_data.xlsx")  # Se puede cambiar el nombre de archivo
        elif opcion == "5":
            estadisticas = calcular_estadisticas(data)
            if estadisticas:
                for key, value in estadisticas.items():
                    print(f"{key}: {value}")
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()