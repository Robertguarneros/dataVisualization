import pandas as pd
import plotly.express as px

def get_data():
    url = 'https://analisi.transparenciacatalunya.cat/resource/rmgc-ncpb.json'
    offset = 0
    limit = 1000
    all_data = pd.DataFrame()

    while True:
        paginated_url = f"{url}?$offset={offset}&$limit={limit}"
        data = pd.read_json(paginated_url)
        if data.empty:
            break
        all_data = pd.concat([all_data, data], ignore_index=True)
        offset += limit

    return all_data


if __name__ == '__main__':
    #data = get_data()
    df = pd.read_csv('/Users/robertoguarneros/Documents/Uni/Cursos/dataVisualization/Project/Accidents_de_tr_nsit_amb_morts_o_ferits_greus_a_Catalunya.csv')
    #print(df.head())

    # Ejericicio 2: Proporción de accidentes por tipo de implicado
    #df = df_grouped = df.groupby('F_UNITATS_IMPLICADES').size().reset_index(name='counts')
    # Juntar mas de 2 implicados en un grupo
    #df.loc[df['F_UNITATS_IMPLICADES'] > 2, 'F_UNITATS_IMPLICADES'] = 'múltiples'

    # fig = px.pie(df, values='counts',names='F_UNITATS_IMPLICADES', title='Proporción de Accidentes por tipo de implicado')
    # fig.show()

    # Ejercicio 3: Número total de accidentes por tipo de colisión
    # Crear una nueva columna para las combinaciones de tipos de vehículos implicados con solo 2 implicados
    # Separar solo cuando hay 2 implicados
    df = df[df['F_UNITATS_IMPLICADES'] == 2]
    df = df.rename(columns={
        'F_CICLOMOTORS_IMPLICADES': 'Ciclomotor',
        'F_BICICLETES_IMPLICADES': 'Bicicleta',
        'F_MOTOCICLETES_IMPLICADES': 'Motocicleta',
        'F_VEH_LLEUGERS_IMPLICADES': 'Vehículo ligero',
        'F_VEH_PESANTS_IMPLICADES': 'Vehículo pesado'
    })
    vehicle_columns = [
        'Ciclomotor', 'Bicicleta', 'Motocicleta',
        'Vehículo ligero', 'Vehículo pesado'
    ]

    def get_vehicle_combinations(row):
        vehicles = []
        for col in vehicle_columns:
            if row[col] > 0:
                vehicles.append(col)
        return ', '.join(vehicles)

    df['Vehicle_Combination'] = df.apply(get_vehicle_combinations, axis=1)

    # Filtrar combinaciones no vacías
    df = df[df['Vehicle_Combination'] != '']

    # Agrupar por combinaciones de vehículos y contar el número de accidentes
    df_grouped = df.groupby('Vehicle_Combination').size().reset_index(name='Numero de accidentes')
    print(df_grouped.head())

    # Visualizar los resultados
    fig = px.bar(df_grouped, x='Vehicle_Combination', y='Numero de accidentes', title='Número de accidentes por combinación de vehículos')
    fig.update_traces(texttemplate='%{y}', textposition='outside')
    fig.show()


    # # Ejercicio 7: Número total de accidentes por año
    # df = df.groupby('Any').size().reset_index(name='counts')
    # print(df.info())
    # fig = px.bar(df, x='Any', y='counts', title='Número total de accidentes por año')
    # fig.show()

    # # Ejercicio 12: Consulta las carreteras con su número de accidentes
    # df = df.groupby('via').size().reset_index(name='Numero de accidentes')
    # print(df)

    # Ejercicio 17: Analiza si hay una correlación entre el límite de velocidad y la gravedad de los accidentes.
    # Mapear valores de la columna gravedad a valores numéricos
    # Mapear las categorías de D_GRAVETAT a valores numéricos
    # gravedad_mapping = {
    #     'Accident lleu': 1,
    #     'Accident greu': 2,
    #     'Accident mortal': 3
    # }
    # df['D_GRAVETAT'] = df['D_GRAVETAT'].map(gravedad_mapping)

    # # Convertir C_VELOCITAT_VIA a numérico
    # df['C_VELOCITAT_VIA'] = pd.to_numeric(df['C_VELOCITAT_VIA'], errors='coerce')

    # df_corr = df[['D_GRAVETAT', 'C_VELOCITAT_VIA']].dropna()
    # print(df_corr.head())
    # correlation_value = df_corr['D_GRAVETAT'].corr(df_corr['C_VELOCITAT_VIA'])
    # print(f"Correlación entre D_GRAVETAT y C_VELOCITAT_VIA: {correlation_value}")

    # # Ejercicio 22: Compara si hay más accidentes con condiciones de viento fuerte
    # # que con condiciones de viento débil

    # # Mapear las categorías de D_VENT a valores numéricos
    
    # df_vent = df.groupby('D_VENT').size().reset_index(name='Numero de accidentes')
    # print(df_vent)

    # # Acceder al número de accidentes con 'Vent fort'
    # vent_fort_accidents = df_vent.loc[df_vent['D_VENT'] == 'Vent fort', 'Numero de accidentes'].values[0]
    # print(f"Número de accidentes con Vent fort: {vent_fort_accidents}")

    # # Comparar con otras condiciones de viento
    # vent_debil_accidents = df_vent.loc[df_vent['D_VENT'] == 'Calma, vent molt suau', 'Numero de accidentes'].values[0]
    # print(f"Número de accidentes con Calma, vent molt suau: {vent_debil_accidents}")

    # if vent_fort_accidents > vent_debil_accidents:
    #     print('Hay más accidentes con viento fuerte')
    # else:
    #     print('Hay más accidentes con viento débil')