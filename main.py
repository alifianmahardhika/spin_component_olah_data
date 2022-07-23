from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from src.utils import (
    read_raw,
    clean_raw,
    make_dataframe,
    compute_arctan,
    make_plot_table,
)

st.title('Olah data spin component')

@st.cache
def load_data(filename: str, sigma: str) -> pd.DataFrame:
    raw_data = read_raw(filename)
    clean_data = clean_raw(raw_data)
    df = make_dataframe(clean_data)
    x_array = compute_arctan(df)
    y_array = df[sigma].to_numpy()
    print("cek length :", len(x_array), len(y_array))
    df_plot = make_plot_table(x_array, y_array)
    return df_plot

data_load_state = st.text('Loading data...')
df_plot_1 = load_data("data/vbm-FL.Pxyz_47", "sigma_x")
df_plot_2 = load_data("data/vbm-FL.Pxyz_48", "sigma_x")
data_load_state.text("Done! (using st.cache)")

left_col, right_col = st.columns(2)

left_col.header("vbm-FL.Pxyz_47")
left_col.dataframe(df_plot_1)

right_col.header("vbm-FL.Pxyz_48")
right_col.dataframe(df_plot_2)

fig, ax = plt.subplots()
ax.plot(df_plot_1["arc"], df_plot_1["sigma"], "r")
ax.plot(df_plot_2["arc"], df_plot_2["sigma"], "b")

st.pyplot(fig)