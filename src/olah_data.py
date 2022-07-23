#!/usr/bin/env python
# coding: utf-8

from typing import List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser(description='Make sigma plot')
parser.add_argument('--s1', type=str, required=True, help="spin component file 1")
parser.add_argument('--s2', type=str, required=True, help="spin component file 2")
parser.add_argument('--sigma', type=str, required=True, help="sigma x or y or z?", choices=["sigma_x", "sigma_y", "sigma_z"])

args = parser.parse_args()

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

def make_dataframe(clean_data: List[str]):
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
    return df

def sort_table(df: pd.DataFrame):
    return df.sort_values(by=['arc'])

def plot_data_table(df: pd.DataFrame, _color: str):
    plt.plot(df['arc'], df['sigma'], _color)

def main_plot(filename: str, sigma: str, _color : str):
    raw_data = read_raw(filename)
    clean_data = clean_raw(raw_data)
    df = make_dataframe(clean_data)
    x_array = compute_arctan(df)
    y_array = df[sigma].to_numpy()
    print("cek length :", len(x_array), len(y_array))
    df_plot = make_plot_table(x_array, y_array)
    plot_data_table(sort_table(df_plot), _color)
    return x_array, y_array

def main_code(fname1: str, fname2: str, sigma_name: str):
    x1, y1 = main_plot(fname1, sigma_name, 'r')
    x2, y2 = main_plot(fname2, sigma_name, 'b')
    all_x = np.array(np.append(x1, x2))
    custom_ticks = ["0", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
    x_range = [-np.pi, -np.pi/2.0, 0, np.pi/2.0, np.pi]
    print(x_range)
    if(sigma_name == 'sigma_x'):
        ylabel_name = r"$\sigma_x$"
    elif(sigma_name == 'sigma_y'):
        ylabel_name = r"$\sigma_y$"
    elif(sigma_name == 'sigma_z'):
        ylabel_name = r"$\sigma_z$"
    plt.xlabel(r"$\theta$", fontsize=18)
    plt.ylabel(ylabel_name, fontsize=18)
    plt.ylim(-1.0, 1.0)
    plt.xticks(x_range, custom_ticks)
    plt.tight_layout()
    plt.savefig(sigma_name + ".eps", format="eps")
    plt.show()

print(args)
main_code(args.s1, args.s2, args.sigma)

