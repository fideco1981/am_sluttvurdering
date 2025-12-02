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

def date_agg_df(df, date_column, unit_column):
    df['Dato_Aggregering'] = df[date_column].dt.date
    new_df = df.groupby('Dato_Aggregering')[unit_column].sum().reset_index()
    new_df['Dato_Aggregering'] = pd.to_datetime(new_df['Dato_Aggregering'])
    return new_df





def main():
    df_traffic = pd.read_csv('lysakelysaker_tellinger.csv', sep=";", decimal=",")
    df_weather = pd.read_csv('lysaker_vær.csv', sep=";", decimal=",")
    df_traffic = df_traffic.drop(['Trafikkregistreringspunkt','Vegreferanse', 'Dato', 'Fra tidspunkt', 'Til tidspunkt','Felt'], axis=1)
    df_weather = df_weather.drop(['lokasjon', 'stasjon'], axis=1)
    df_traffic['Fra'] = pd.to_datetime(df_traffic['Fra'], utc=True, errors='coerce')
    df_traffic['Til'] = pd.to_datetime(df_traffic['Til'], utc=True, errors='coerce')
    df_weather['dato'] = pd.to_datetime(df_weather['dato'], utc=True, errors='coerce', format='%d.%m.%Y')

    df_traffic_cars = df_traffic[df_traffic['Navn'] == 'Maritim'].copy()
    df_traffic_bikes = df_traffic[df_traffic['Navn'] == 'Lysaker sykkel'].copy()

    df_dagsdata_sykkel = date_agg_df(df_traffic_bikes, 'Fra', unit_column='Trafikkmengde')
    df_dagsdata_biler = date_agg_df(df_traffic_cars, 'Fra', unit_column='Trafikkmengde')

    print(df_dagsdata_biler.describe())
    print(df_dagsdata_sykkel.describe())

    fig, ax1 = plt.subplots(figsize=(16, 13))  # Plot size
    ax2 = ax1.twinx()  # Constructing y2 axis
    ax1.set_xlabel('Måned', color='Black')
    ax1.grid(True, linestyle='--', color='gray', alpha=0.5)
    x = df_weather['dato']
    y = df_weather['temperatur_dogn']
    z = df_weather['nedbor_dogn']
    bikes = df_dagsdata_sykkel['Trafikkmengde']

    ax1.plot(x, y, color="lightblue", label='Temperatur')
    ax1.plot(x,z, color='lightgreen', label='Nedbor dogn')
    ax1.set_ylabel('Temperatur', color='Black')
    ax2.scatter(df_dagsdata_sykkel['Dato_Aggregering'], bikes, color="pink", label='Registrerte sykler')

    ax2.set_ylabel('Registrerte sykler', color='Black')

    fig.legend()
    fig.tight_layout()
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