# Importerer nødvendige biblioteker
# pip install mysql-connector-python for å installere mysql-connector hvis det ikke er installert.
import matplotlib.pyplot as plt  # Bibliotek for å visualisere dataene
import numpy as np  # Bibliotek for numerisk beregning
import pandas as pd

def convert_datetime(df, field):
    df[field] = pd.to_datetime(df[field], utc=True, errors='coerce', format='%d.%m.%Y')

def filter_df(df, column, search):
    sok = search
    mask = df[column].str.strip().str.lower() == sok
    new_df = df[mask].copy()
    return new_df






def main():
    df_traffic = pd.read_csv('lysakelysaker_tellinger.csv', sep=";", decimal=",")
    df_weather = pd.read_csv('lysaker_vær.csv', sep=";", decimal=",")
    df_traffic = df_traffic.drop(['Trafikkregistreringspunkt','Vegreferanse', 'Dato', 'Fra tidspunkt', 'Til tidspunkt','Felt'], axis=1)
    df_weather = df_weather.drop(['lokasjon', 'stasjon'], axis=1)
    df_traffic['Fra'] = pd.to_datetime(df_traffic['Fra'], utc=True, errors='coerce')
    df_traffic['Til'] = pd.to_datetime(df_traffic['Til'], utc=True, errors='coerce')
    df_weather['dato'] = pd.to_datetime(df_weather['dato'], utc=True, errors='coerce', format='%d.%m.%Y')

    #convert_datetime(df_traffic, 'Fra')
    #convert_datetime(df_traffic, 'Til')
    #convert_datetime(df_weather, 'dato')
    print(df_traffic.head())
    print(df_traffic.tail())

    df_traffic_cars = df_traffic[df_traffic['Navn'] == 'Maritim'].copy()
    df_traffic_bikes = df_traffic[df_traffic['Navn'] == 'Lysaker sykkel'].copy()

    print(df_traffic_bikes)

    df_traffic_bikes['Dato_Aggregering'] = df_traffic_bikes['Fra'].dt.date
    df_dagsdata_sykkel = df_traffic_bikes.groupby('Dato_Aggregering')['Trafikkmengde'].sum().reset_index()
    df_dagsdata_sykkel['Dato_Aggregering'] = pd.to_datetime(df_dagsdata_sykkel['Dato_Aggregering'])
#    print(df_traffic.head(), df_traffic.describe(), df_traffic.dtypes)
#    print("*****")
#    print(df_weather.head(), df_weather.describe(), df_weather.dtypes)
    x = df_weather['dato']
    y = df_weather['temperatur_dogn']
    z = df_dagsdata_sykkel['Trafikkmengde']
    plt.plot(x, y, color="lightblue")
    plt.scatter(df_dagsdata_sykkel['Dato_Aggregering'], z, color="pink")


    plt.show()

if __name__ == '__main__':
    main()





'''
x=df['Temp'] # Sjekk navnet i første linje i temhum2.csv
y= df['Fukt']   # Sjekk navnet i første linje i temhum.csv

# Konverterer listene til numpy arrays for enklere bruk med lineær regresjon
temperatur = np.array(x)  # Numpy-array for temperaturdata
luftfuktigheit = np.array(y)  # Numpy-array for luftfuktigheitdata

# Utfører lineær regresjon ved hjelp av numpy sin polyfit-funksjon
regression = np.polyfit(temperatur, luftfuktigheit, 1)  # Utfører lineær regresjon og returnerer koeffisientene
poly = np.poly1d(regression)  # Lager en funksjon basert på koeffisientene for enkel plotting

# Leser inn given_temperatur fra tastaturet
given_temperatur = float(input("Skriv inn temperaturen for å forutsjå luftfuktigheita: "))

# Forutsier luftfuktigheita basert på den gitte temperaturverdien
predicted_luftfuktigheit = poly(given_temperatur)  # Forutsier luftfuktigheit for den gitte temperaturverdien

# Skriver ut den forutsette luftfuktigheitverdien
print(f"Forutsett luftfuktigheit for temperatur {given_temperatur} er: {predicted_luftfuktigheit}")

# Plotter dataene og regresjonslinjen ved hjelp av matplotlib
plt.scatter(temperatur, luftfuktigheit, color='b', label='Data')  # Plotter datapunktene i blå farge
plt.plot(temperatur, poly(temperatur), color='r', label='Linear Regression')  # Plotter regresjonslinjen i rød farge
plt.scatter(given_temperatur, predicted_luftfuktigheit, color='g', label='Forutsett luftfuktigheit', marker='x', s=200)  # Plotter prediksjonen i grønn farge som et kryss
plt.xlabel('Temperatur')  # Setter navnet på x-aksen
plt.ylabel('Luftfuktigheit')  # Setter navnet på y-aksen
plt.legend()  # Legger til en figurlegende
plt.show()  # Viser plottet'''