from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import streamlit as st
import pandas as pd
import numpy as np
import os
from src.utils import (
    read_raw,
    clean_raw,
    make_dataframe,
    compute_arctan,
    make_plot_table,
)

st.set_page_config(
    layout="wide"
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

def make_figure(fp1: str, fp2: str, sigma_name: str) -> Figure:
    df_plot_1 = load_data(fp1, sigma_name)
    df_plot_2 = load_data(fp2, sigma_name)
    fig, ax = plt.subplots()
    ax.plot(df_plot_1["arc"], df_plot_1["sigma"], "r")
    ax.plot(df_plot_2["arc"], df_plot_2["sigma"], "b")
    return fig

def save_uploaded_file(uploadedfile):
    with open(os.path.join("data", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to data".format(uploadedfile.name))

def remove_file(fname: str):
    fpath = os.path.join("data", fname)
    if os.path.exists(fpath):
        os.remove(fpath)
    else:
        st.write("The file does not exist")

uploaded_files = st.file_uploader(
    "Upload Band Data",
    accept_multiple_files= True
    )

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    save_uploaded_file(uploaded_file)

data_list = os.listdir("data")

container_del = st.container()

remove_files = container_del.multiselect("Select Data to remove", data_list)

def on_remove_files(file_list):
    for r_file in file_list:
        remove_file(r_file)

container_del.button("Delete Selected File(s)",args=remove_files, on_click=on_remove_files)

sel_col_left, sel_col_right = st.columns(2)

sel_file1 = sel_col_left.selectbox("Select First Data", data_list)
sel_file2 = sel_col_right.selectbox("Select Second Data", data_list)

sig_x_col, sig_y_col, sig_z_col = st.columns(3)
path1 = os.path.join("data", sel_file1)
path2 = os.path.join("data", sel_file2)
sigma_list = ["sigma_x", "sigma_y", "sigma_z"]
figure_list = list()

for sigma_n in sigma_list:
    sig_fig = make_figure(path1, path2, sigma_n)
    figure_list.append(sig_fig)

with sig_x_col:
    st.header("Sigma X")
    st.pyplot(figure_list[0])

with sig_y_col:
    st.header("Sigma Y")
    st.pyplot(figure_list[1])

with sig_z_col:
    st.header("Sigma Z")
    st.pyplot(figure_list[2])