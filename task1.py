# Importerer nødvendige biblioteker
import matplotlib.pyplot as plt  # Bibliotek for å visualisere dataene
import numpy as np  # Bibliotek for numerisk beregning
import pandas as pd

def date_agg_df(df, date_column, unit_column):
    """Slår sammen timebaserte data til en sum pr. døgn"""
    df['Dato_Aggregering'] = df[date_column].dt.date
    new_df = df.groupby('Dato_Aggregering')[unit_column].sum().reset_index()
    new_df['Dato_Aggregering'] = pd.to_datetime(new_df['Dato_Aggregering'])
    return new_df

def statistics(array, unit):
    """Skriver ut statistikken ved bruk av numpy."""
    print(f'Gjennomsnitt ({unit}): {np.mean(array)}')
    print(f'Standardavvik ({unit}): {np.std(array)}')
    print(f'Median ({unit}): {np.median(array)}')

def statistics_pd(array, unit):
    """Skriver ut statistikken ved bruk av pandas. Pandas standardavvik benytter Bessel's korreksjon som standard,
    noe som gir en litt høyere verdi enn numpy som ikke bruker denne"""
    print(f'Gjennomsnitt ({unit}): {array.mean()}')
    print(f'Standardavvik ({unit}): {array.std()}')
    print(f'Median ({unit}): {array.median()}\n')

def regression(df1, column1, df2, column2):
    x = df1[column1]
    y = df2[column2]

    # Konverterer listene til numpy arrays for enklere bruk med lineær regresjon
    xaxis = np.array(x)  # Numpy-array for temperaturdata
    yaxis = np.array(y)  # Numpy-array for luftfuktigheitdata

    # Utfører lineær regresjon ved hjelp av numpy sin polyfit-funksjon
    regression = np.polyfit(xaxis, yaxis, 1)  # Utfører lineær regresjon og returnerer koeffisientene
    poly = np.poly1d(regression)  # Lager en funksjon basert på koeffisientene for enkel plotting
    return poly, xaxis, yaxis


def main():
    # Leser inn data i to separate dataframes
    df_traffic = pd.read_csv('lysakelysaker_tellinger.csv', sep=";", decimal=",", header=0, skiprows=1)
    df_weather = pd.read_csv('lysaker_vær.csv', sep=";", decimal=",")

    #Fjerner kolonner vi ikke behøver
    df_traffic = df_traffic.drop(['Trafikkregistreringspunkt','Vegreferanse', 'Dato', 'Fra tidspunkt', 'Til tidspunkt','Felt'], axis=1)
    df_weather = df_weather.drop(['lokasjon', 'stasjon'], axis=1)

    #Gjør datokolonne om til standard dato/tidsformat for videre behandling
    df_traffic['Fra'] = pd.to_datetime(df_traffic['Fra'], utc=True, errors='coerce')
    df_traffic['Til'] = pd.to_datetime(df_traffic['Til'], utc=True, errors='coerce')
    df_weather['dato'] = pd.to_datetime(df_weather['dato'], utc=True, errors='coerce', format='%d.%m.%Y')

    #Filtrerer ut biler og sykler i to forskjellige dataframes
    df_traffic_cars = df_traffic[df_traffic['Navn'] == 'Maritim'].copy()
    df_traffic_bikes = df_traffic[df_traffic['Navn'] == 'Lysaker sykkel'].copy()

    #Summerer ut timesdata til døgnverdier
    df_dagsdata_sykkel = date_agg_df(df_traffic_bikes, 'Fra', unit_column='Trafikkmengde')
    df_dagsdata_biler = date_agg_df(df_traffic_cars, 'Fra', unit_column='Trafikkmengde')
    print(df_weather.describe())
    #Skriver ut gjennomsnitt, median og standardavvik
    statistics_pd(df_dagsdata_sykkel['Trafikkmengde'], 'Sykler')
    statistics_pd(df_dagsdata_biler['Trafikkmengde'], 'Biler')
    statistics_pd(df_weather['temperatur_dogn'], 'Temperatur')
    statistics_pd(df_weather['nedbor_dogn'], 'Nedbør')

    print(df_weather.describe())
    print(df_dagsdata_sykkel.describe())

    poly, xaxis, yaxis = regression(df_weather, 'temperatur_dogn', df_dagsdata_sykkel, 'Trafikkmengde')


    fig, ax = plt.subplots(2,1, figsize=(16, 13))  # Plot size
    ax1_0 = ax[0]
    #ax2_0 = ax1_0.twinx()

    p1 = ax1_0.scatter(df_dagsdata_sykkel['Trafikkmengde'], df_weather['temperatur_dogn'], color='red',alpha=0.4, label='Temperatur')
    ax1_0.set_xlabel('Dato', color='Black')
    ax1_0.set_ylabel('Temperatur (°C)', color='red')
    ax1_0.tick_params(axis='y', labelcolor='red')
    ax1_0.set_ylim(bottom=-15)  # Eksplisitt sett laveste temperatur

    #p2 = ax2_0.plot(df_dagsdata_sykkel['Dato_Aggregering'], df_dagsdata_sykkel['Trafikkmengde'], color='blue',  label='Sykkelpasseringer')
    #ax2_0.set_ylabel('Sykkelpasseringer', color='blue')
    #ax2_0.tick_params(axis='y', labelcolor='blue')
    #ax2_0.grid(False)
    #ax2_0.set_ylim(bottom=0)  # Eksplisitt sett laveste sykkelpasseringer til 0

    #lns1 = [p1[0]] + list(p2)
    #labs1 = ['Temperatur (°C)', 'Sykkelpasseringer']
    #ax1_0.legend(lns1, labs1, loc ='upper left')
    #ax1_0.set_title('Temperatur vs sykkelpasseringer')

    ax1_1 = ax[1]
    #ax2_1 = ax1_1.twinx()

    p3 = ax1_1.scatter(df_dagsdata_sykkel['Trafikkmengde'], df_weather['nedbor_dogn'], color='green', alpha=0.4, label='Nedbør (mm)')
    ax1_1.set_xlabel('Dato')
    ax1_1.set_ylabel('Nedbør (mm)', color='green')
    ax1_1.tick_params(axis='y', labelcolor='green')
    ax1_1.set_ylim(bottom=-5)

    #p4 = ax2_1.plot(df_dagsdata_sykkel['Dato_Aggregering'], df_dagsdata_sykkel['Trafikkmengde'], color='purple',  label='Sykkelpasseringer')
    #ax2_1.set_ylabel('Sykkelpasseringer', color='purple')
    #ax2_1.tick_params(axis='y', labelcolor='purple')
    #ax2_1.grid(False)
    #ax2_1.set_ylim(bottom=0)

    #lns2 = [p3[0]] + list(p4)
    #labs2 = ['Nedbør (mm)', 'Sykkelpasseringer']
    #ax1_1.legend(lns2, labs2, loc ='upper right')
    #ax1_1.set_title('Nedbør vs sykkelpasseringer')
    '''
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
    fig.tight_layout()'''
    plt.show()


    # Leser inn given_temperatur fra tastaturet
    given_temperature = float(input("Skriv inn temperaturen for å forutsjå antall syklister: "))

    # Forutsier luftfuktigheita basert på den gitte temperaturverdien
    predicted_trafikk = poly(given_temperature)  # Forutsier luftfuktigheit for den gitte temperaturverdien

    # Skriver ut den forutsette luftfuktigheitverdien
    print(f"Forutsett antall syklister for temperatur {given_temperature} er: {predicted_trafikk}")

    # Plotter dataene og regresjonslinjen ved hjelp av matplotlib
    plt.scatter(xaxis, yaxis, color='b', label='Data')  # Plotter datapunktene i blå farge
    plt.plot(xaxis, poly(xaxis), color='r', label='Linear Regression')  # Plotter regresjonslinjen i rød farge
    plt.scatter(given_temperature, predicted_trafikk, color='g', label='Forutsett trafikk', marker='x', s=200)  # Plotter prediksjonen i grønn farge som et kryss
    plt.xlabel('Temperatur')  # Setter navnet på x-aksen
    plt.ylabel('Trafikk')  # Setter navnet på y-aksen
    plt.legend()  # Legger til en figurlegende
    plt.show()  # Viser plottet'''



if __name__ == '__main__':
    main()





