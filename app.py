# imports
import streamlit as st
import pandas as pd
import altair as alt

# functions
@st.cache_data
def load_data():
    df_data = pd.read_csv('CEN0101J.csv')

    df_data.rename(columns={
        'Druh PHM': 'PalivoDruh',
        'CENPHM1': 'PalivoId',
        'Měsíce': 'RokMesicText',
        'CasM': 'RokMesicId',
        'Hodnota': 'Cena'}
        , inplace=True)

    palivo_rename = {
        'Benzin automobilový bezolovnatý Natural 95 [Kč/l]': 'Natural 95 [Kč/l]',
        'Benzin automobilový bezolovnatý Super plus 98 [Kč/l]': 'Natural 98 [Kč/l]',
        'LPG [Kč/l]': 'LPG [Kč/l]',
        'Motorová nafta [Kč/l]': 'Nafta [Kč/l]',
        'Stlačený zemní plyn - CNG [Kč/kg]': 'CNG [Kč/kg]',
    }

    df_data['PalivoDruh'] = df_data['PalivoDruh'].replace(palivo_rename)

    df_data = df_data[['PalivoDruh', 'PalivoId', 'RokMesicText', 'RokMesicId', 'Cena']]

    df_data['Datum'] = pd.to_datetime(df_data['RokMesicId'])
    df_data['Rok'] = df_data['Datum'].dt.year
    df_data['Mesic'] = df_data['Datum'].dt.month

    return df_data


@st.cache_data
def load_categories(df_data: pd.DataFrame):
    categories = df_data['PalivoDruh'].unique()
    return categories.tolist()


@st.cache_data
def load_group_data(df_data: pd.DataFrame):
    return df_data.groupby(['Rok', 'PalivoDruh'])['Cena'].mean().reset_index()


def load_data_by_category(df_group_data, category):
    return df_group_data[df_group_data['PalivoDruh'] == category]


def load_min_price(df_group_data_by_category: pd.DataFrame):
    return df_group_data_by_category['Cena'].min()


def load_max_price(df_group_data_by_category: pd.DataFrame):
    return df_group_data_by_category['Cena'].max()


# def get_date(df_group_data_by_category: pd.DataFrame):
#     return df_group_data_by_category[df_group_data_by_category['Cena'] == load_min_price(df_group_data_by_category)]


# initial load data
data = load_data()
group_data = load_group_data(data)


# layout
st.title('Přehled cen pohonných hmot')
st.header('Ceny pohonných hmot podle typu paliva')

selected_type = st.selectbox('Vyberte typ paliva', load_categories(data))
data_by_category = load_data_by_category(group_data, selected_type)

category_chart = alt.Chart(data_by_category).mark_line().encode(x='Rok:O', y='Cena:Q')
st.altair_chart(category_chart)

# st.write(get_date(data_by_category)['Rok'])

st.metric("Min price:", value=load_min_price(data_by_category))
st.metric("Max price:", value=load_max_price(data_by_category))
