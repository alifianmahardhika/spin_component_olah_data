from typing import List
import pandas as pd
import numpy as np

def read_raw(fname: str):
    raw_data = list()
    with open(fname) as f:
        raw_data = f.readlines()
    return raw_data

def clean_raw(raw_data: List[str]) -> List[str]:
    clean_data = list()
    for data in raw_data:
        clean_data.append(",".join(data.split()))
    return clean_data

def make_dataframe(clean_data: List[str]) -> pd.DataFrame:
    kx = list()
    ky = list()
    kz = list()
    sigma_x = list()
    sigma_y = list()
    sigma_z = list()
    for data in clean_data:
    #     print(data.split(","))
        split_data = data.split(",")
        kx.append(float(split_data[0]))
        ky.append(float(split_data[1]))
        kz.append(float(split_data[2]))
        sigma_x.append(float(split_data[3]))
        sigma_y.append(float(split_data[4]))
        sigma_z.append(float(split_data[5]))
    df = pd.DataFrame.from_dict({
    'kx': kx,
    'ky': ky,
    'kz': kz,
    'sigma_x': sigma_x,
    'sigma_y': sigma_y,
    'sigma_z': sigma_z
    })
    return df

def compute_arctan(df: pd.DataFrame):
    return np.arctan2(df['kz'].to_numpy(), df['ky'].to_numpy())

def make_plot_table(x_array, y_array):
    result = dict({
        'arc': x_array.tolist(),
        'sigma': y_array.tolist()
        })
    df = pd.DataFrame.from_dict(result)
    df.sort_values(by=['arc'], inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df