import streamlit as st
import pandas as pd
import altair as alt


@st.cache_data
def load_fuel_categories():
    df_data = pd.read_csv("CEN0101J.csv")
    categories = df_data["Druh PHM"].unique()
    return categories.tolist()


@st.cache_data
def load_data():
    df_data = pd.read_csv("CEN0101J.csv")

    df_data.rename(columns={
        'Druh PHM': 'PalivoDruh',
        'CENPHM1': 'PalivoId',
        'Měsíce': 'RokMesicText',
        'CasM': 'RokMesicId',
        'Hodnota': 'Cena'},
        inplace=True)

    df_data = df_data[['PalivoDruh', 'PalivoId', 'RokMesicText', 'RokMesicId', 'Cena']]

    pd.to_datetime(df_data['RokMesicId'])

    df_data['Datum'] = pd.to_datetime(df_data['RokMesicId'])
    df_data['Rok'] = df_data['Datum'].dt.year
    df_data['Mesic'] = df_data['Datum'].dt.month

    df_data = df_data.groupby(['Rok', 'PalivoDruh'])['Cena'].mean().reset_index()

    return df_data[df_data['PalivoDruh'] == chosen_fuel]


# Web app deploy

# Title
st.set_page_config(layout="wide", page_title="Fuel prices", page_icon="Czech_flag.jpg")
st.title("Fuel prices overwiew")

# Inputs
name_input = st.text_input("Enter your name plese:")
if name_input:
    st.write(f"Hello {name_input}!")


# Let user choose fuel type
chosen_fuel = st.selectbox("Choose fuel", options=load_fuel_categories())
st.write(f"Chosen fuel: {chosen_fuel}")


# Table and Fig
st.divider()

tab_left, tab_right = st.tabs(["Fig", "Data"])

with tab_left:
    st.altair_chart(alt.Chart(load_data()).mark_line().encode(
        x='Rok:O',
        y='Cena:Q',
        color='PalivoDruh:N',
        tooltip=['Cena']).interactive()
        )

with tab_right:
    st.dataframe(load_data(), hide_index=True)
