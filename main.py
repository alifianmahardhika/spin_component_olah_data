
from zipfile import ZipFile
import io
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import streamlit as st
import pandas as pd
import os
import tempfile
from src.utils import (
    read_raw,
    clean_raw,
    make_dataframe,
    compute_arctan,
    make_plot_table,
)

# global setting
st.set_page_config(
    layout="wide",
    page_title="Spin component data analysis"
)

title_container = st.container()
title_container.title('Spin component data analysis')
title_container.markdown('Made by **Alifian Mahardhika Maulana**')
title_container.markdown('Connect with me : [Github](https://github.com/alifianmahardhika), [ResearchGate](https://www.researchgate.net/profile/Alifian-Maulana)')
# function
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
    ax.set_ylim((-1.0, 1.0))
    ax.plot(df_plot_1["arc"], df_plot_1["sigma"], "r")
    ax.plot(df_plot_2["arc"], df_plot_2["sigma"], "b")
    return fig

def save_uploaded_file(uploadedfile):
    with open(os.path.join("data", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("{} uploaded".format(uploadedfile.name))

def remove_file(fname: str):
    fpath = os.path.join("data", fname)
    if os.path.exists(fpath):
        os.remove(fpath)

def on_remove_files(file_list):
    for r_file in file_list:
        remove_file(r_file)

# upload section
upload_container = st.container()
upload_container.header("Upload Data")
uploaded_files = upload_container.file_uploader(
    "Browse data",
    accept_multiple_files= True
    )

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    save_uploaded_file(uploaded_file)

# select data section
select_container = st.container()
select_container.header("Select Data to Plot")
data_list = os.listdir("data")
sel_col_left, sel_col_right = select_container.columns(2)

sel_file1 = sel_col_left.selectbox("Select First Data", data_list)
sel_file2 = sel_col_right.selectbox("Select Second Data", data_list)

# plot sigma section
plot_sigma_container = st.container()
plot_sigma_container.header("Sigma Plot Result")
sig_x_col, sig_y_col, sig_z_col = plot_sigma_container.columns(3)
path1 = os.path.join("data", sel_file1)
path2 = os.path.join("data", sel_file2)
sigma_list = ["sigma_x", "sigma_y", "sigma_z"]
figure_list = list()

# make figure in memory
for sigma_n in sigma_list:
    sig_fig = make_figure(path1, path2, sigma_n)
    figure_list.append(sig_fig)

with sig_x_col:
    st.subheader("Sigma X")
    st.pyplot(figure_list[0])

with sig_y_col:
    st.subheader("Sigma Y")
    st.pyplot(figure_list[1])

with sig_z_col:
    st.subheader("Sigma Z")
    st.pyplot(figure_list[2])

# prepare for download
tempfile.tempdir = "tmp"
secure_temp_dir = tempfile.mkdtemp()

# save figure as png and add to zip
def save_to_zip(format_file: str):
    zip_fn = "sigma_plot_{}.zip".format(format_file)
    zip_fp = os.path.join(secure_temp_dir, zip_fn)
    zipObj = ZipFile(zip_fp, "w")
    for idx, sig_fig in enumerate(figure_list):
        fn = os.path.join(secure_temp_dir, "{}.{}").format(sigma_list[idx], format_file)
        sig_fig.savefig(fn, format=format_file)
        zipObj.write(fn)
    zipObj.close()
    return zip_fp, zip_fn

def remove_temp():
    try:
        for item in os.listdir(secure_temp_dir):
            os.remove(os.path.join(secure_temp_dir, item))
        os.removedirs(secure_temp_dir)
        print("Directory {} has been removed successfully".format(secure_temp_dir))
    except OSError as error:
        print(error)
        print("Directory {} can not be removed".format(secure_temp_dir))

# make png and eps zip
zip_fp_png, zip_fn_png = save_to_zip("png")
zip_fp_eps, zip_fn_eps = save_to_zip("eps")

png_col, eps_col, _, _ = plot_sigma_container.columns(4)

# download as PNG
with open(zip_fp_png, "rb") as fp:
    png_col.download_button(
        label="Download PNG",
        data=fp,
        file_name=zip_fn_png,
        mime="application/zip",
        on_click=remove_temp
    )

# Download as EPS
with open(zip_fp_eps, "rb") as fp:
    eps_col.download_button(
        label="Download EPS",
        data=fp,
        file_name=zip_fn_eps,
        mime="application/zip",
        on_click=remove_temp
    )

# Remove data section
container_del = st.container()
container_del.header("Remove Data")
remove_files = container_del.multiselect("Select Data to remove:", data_list)

def on_files_removed():
    container_del.success("Data removed")

if container_del.button("Delete", on_click=on_files_removed):
    try:
        on_remove_files(remove_files)
    except:
        container_del.write("Failed to remove")