import numpy as np
import pandas as pd
import streamlit as st
import pydeck as pdk
import time
from datetime import date, datetime, timedelta

from urllib.error import URLError

data_path = "./covid_korean_cleaned.csv"

@st.cache
def from_data_file(data_path):
    # load static pre-processed datafile
    return pd.read_csv(data_path)[["deceased_date", "released_date", "confirmed_date", "age_class", "sex", "lat", "lon"]]

df_covid = from_data_file(data_path)
try:
    st.title("South Korean COVID-19 Analysis")
    left_column, right_column = st.columns(2)
    pressed = left_column.button('Any Questions?')
    if pressed:
      right_column.write("Contact me at *yukunj@cs.cmu.edu* at anytime!")
    st.write("Mankind has been fighting Covid-19 Virus for almost two years. Major attention has been put on the Europe, North America and China in the East. In this project, therefore, we will focus on a less noticed country - **South Korea**.")
    st.write("We have collected around **4000** infection cases from **Jan 2020** to **Jun 2020** in South Korea. The [dataset](https://www.kaggle.com/kimjihoo/coronavirusdataset) is released on Kaggle. We will analyze it in 2 dimensions: **spatially** and **temporally**")
    st.write("+ **Spatial**: infection case distribution by province, gender and age")
    st.write("+ **Temporal**: Time Series Trending and Aggregation")
    st.write("")
    st.write("")
    
    #==============================Spatial Analysis======================#
    st.write("### Spatial Analysis")
    st.write("In the spatial analysis, by comparing the four different groups **[Male/Female] * [Young/Elder]**, we could have the following observations:")
    st.write("+ Generally, infections occur more often in big cities with a larger population, like `Gyeongsangbuk`, `Gyeonggi`, `Seoul` (The 3 red-colored hills on the map).")
    st.write("+ In term of **Age**, we observe that there are more young people infection cases in the cities of `Busan` and `Geoje-si`. Partially we coudl attribute this to the fact that these cities are modern, fast-paced and attractive to young people.")
    st.write("+ In term of **Gender**, in total it's `60%` female and `40%` male. But in geographical distribution, it's rather uniform.")
    st.write("You may use the map layer filter on the left-side menu to confirm the above observations.")
    # all layers' definitions here
    ALL_LAYERS = {
    "Young Male" : pdk.Layer(
        'HexagonLayer',
        data = df_covid[(df_covid["sex"] == "male") & (df_covid["age_class"] == "Young")], # 1079 people
        get_position=['lon', 'lat'],
        radius=400,
        opacity=0.8,
        auto_highlight=True,
        elevation_scale=40,
        elevation_range=[0, 1500],
        color=[180, 0, 200],
        extruded=True,
        coverage=3),
        
    "Young Female" : pdk.Layer(
        'HexagonLayer',
        data = df_covid[(df_covid["sex"] == "female") & (df_covid["age_class"] == "Young")], # 1102
        get_position=['lon', 'lat'],
        radius=400,
        opacity=0.8,
        auto_highlight=True,
        elevation_scale=40,
        elevation_range=[0, 1500],
        extruded=True,
        coverage=3),
    
     "Elder Male" : pdk.Layer(
        'HexagonLayer',
        data = df_covid[(df_covid["sex"] == "male") & (df_covid["age_class"] == "Old")], # 635
        get_position=['lon', 'lat'],
        radius=400,
        opacity=0.8,
        auto_highlight=True,
        elevation_scale=40,
        elevation_range=[0, 1500],
        extruded=True,
        coverage=3),
    
    "Elder Female" : pdk.Layer(
        'HexagonLayer',
        data = df_covid[(df_covid["sex"] == "female") & (df_covid["age_class"] == "Old")], # 966
        get_position=['lon', 'lat'],
        radius=400,
        opacity=0.8,
        auto_highlight=True,
        elevation_scale=40,
        elevation_range=[0, 1500],
        extruded=True,
        coverage=4),
    }
    
    st.sidebar.markdown("## Map Layers")
    selected_layers = [
        layer for layer_name, layer in ALL_LAYERS.items()
        if st.sidebar.checkbox(layer_name, True)]
    if selected_layers:
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/outdoors-v11",
            initial_view_state={"latitude" : 36,
                                "longitude" : 128,
                                "zoom" : 6.7,
                                "min_zoom" : 3,
                                "max_zoom" : 10,
                                "pitch" : 45},
            layers=selected_layers
            ))
    else:
        st.error("Please select at least one layer visualization above")

    #==============================Temporal Analysis======================#
    st.write("### Temporal Analysis")
    st.write("In the temporal analysis, we are interested in how severe is the situation of covid-19 infection as time goes. In specific, we will look at 3 time series trend since **day1 (Jan 22 2020)** to **day160 (Jun 28 2020)**:")
    st.write("1) the total number of **confirmed cases**")
    st.write("2) the total number of **deceased cases**")
    st.write("3) the number of people **in hospital** at a given day")
    st.write("We have the following observations that:")
    st.write("+ from February(day30) to April(day70), the total confirmed cases **increased rapidly**, with a lot of people being in hospitalization.")
    st.write("+ Starting from May, the infection trend **alleviated** and hospital was no longer super crowded.")
    st.write("+ South Korea's deceased cases were kept at **a low number** all the time, showing its medical superiority to a certain degree.")
    
    # dynamic plotting data preparation
    start_date = date.fromisoformat('2020-01-22').strftime("%Y-%m-%d")
    end_date = date.fromisoformat('2020-06-29').strftime("%Y-%m-%d")
    total_confirmed = []
    total_deceased = []
    total_hospital = []
    for i in range(160):
        curr_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
        confirmed = len(df_covid[(start_date <= df_covid["confirmed_date"]) & \
                                       (df_covid["confirmed_date"] <= curr_date)])
        deceased = len(df_covid[(start_date <= df_covid["deceased_date"]) & \
                                       (df_covid["deceased_date"] <= curr_date)])
        hospital = len(df_covid[(start_date <= df_covid["confirmed_date"]) &\
                            (df_covid["confirmed_date"] <= curr_date) &\
                            (curr_date<=df_covid["released_date"])])
        total_confirmed.append(confirmed)
        total_deceased.append(deceased)
        total_hospital.append(hospital)

    df = pd.DataFrame(np.column_stack([total_confirmed, total_hospital, total_deceased]),
                         columns=["total_confirmed", "now_in_hospital", "total_deceased"],
                         )
    df.rename_axis('day')
    progress_bar = st.sidebar.progress(0.0)
    status_text = st.sidebar.empty()
    last_row = df[0:1]
    chart = st.line_chart(last_row)
    for i in range(1, 160):
        new_row = df[i:i+1]
        status_text.text("%i%% Complete" % int(100*i/160))
        chart.add_rows(new_row)
        progress_bar.progress(i/160)
        time.sleep(0.1)
    
    progress_bar.empty()
    st.write("Click the **Re-run** bottom below to see the statistical evolution of infection trend.")
    st.write("After it finishes, you can check the **exact number** of putting mouse on a specific line")
    st.button("Re-run")
    
except URLError as e:
    st.error("""
        **This demo requires internet access.**

        Connection error: %s
    """ % e.reason)
