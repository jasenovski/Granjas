import numpy as np
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
from funcoes import metodo_minimos_quadrados, polinomios
import json
import os

df = pd.read_excel(os.path.join("base_dados", "BaseDados.xlsx"), sheet_name=0, engine='openpyxl')

with open(os.path.join("configuracoes", "configs.json"), "r") as f:
  config = json.load(f)

df["L"] = df["M"] * config["valor_carne"] - df["R"] * config["preco_racao"]
df = df.dropna(axis=0)

coefs_massa = metodo_minimos_quadrados.mmq(entradas=np.array(df["t"]), saidas=np.array(df["M"]), g=3)
coefs_racao = metodo_minimos_quadrados.mmq(entradas=np.array(df["t"]), saidas=np.array(df["R"]), g=3)
coefs_lucro = metodo_minimos_quadrados.mmq(entradas=np.array(df["t"]), saidas=np.array(df["L"]), g=3)

ts = []
massas = []
racoes = []
for t in range(1, len(df) + 1):
    massas.append(polinomios.polinomio(coefs=coefs_massa, entrada=int(t)))
    racoes.append(polinomios.polinomio(coefs=coefs_racao, entrada=int(t)))
    ts.append(t)

massas = np.array(massas)
racoes = np.array(racoes)
massas = list(np.round(massas, 2).reshape(len(massas)))
racoes = list(np.round(racoes, 2).reshape(len(racoes)))

t = 1
lucros = []
ts_ate_negativo = []
virou = False
while True:
  lucros.append(polinomios.polinomio(coefs=coefs_lucro, entrada=int(t)))

  if len(lucros) > 1 and not virou:
    if lucros[-1] < lucros[-2]:
      t_ideal = t - 1
      virou = True

  if lucros[-1] < 0:
    ts_ate_negativo.append(t)
    break
  else:
    ts_ate_negativo.append(t)
    t += 1

lucros = np.array(lucros)
lucros = list(np.round(lucros, 2).reshape(len(lucros)))

st.title("Ração vs Engorda")

options = {
  "title": {
    "text": 'kg'
  },
  "tooltip": {
    "trigger": 'axis'
  },
  "legend": {
    "data": ["Massas", "Racoes"]
  },
  "grid": {
    "left": '3%',
    "right": '4%',
    "bottom": '3%',
    "containLabel": True
  },
  # "toolbox": {
  #   "feature": {
  #     "saveAsImage": {}
  #   }
  # },
  "xAxis": {
    "type": 'category',
    "boundaryGap": False,
    "data": ts
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "name": 'Massas',
      "type": 'line',
      "stack": 'Total',
      "data": massas
    },
    {
      "name": 'Racoes',
      "type": 'line',
      "stack": 'Total',
      "data": racoes
    }
  ]
}

st_echarts(options=options)

st.title("Lucro")

options = {
  "title": {
    "text": 'R$'
  },
  "tooltip": {
    "trigger": 'axis'
  },
  # "legend": {
  #   "data": ["lucros"]
  # },
  "grid": {
    "left": '3%',
    "right": '4%',
    "bottom": '3%',
    "containLabel": True
  },
  # "toolbox": {
  #   "feature": {
  #     "saveAsImage": {}
  #   }
  # },
  "xAxis": {
    "type": 'category',
    "boundaryGap": False,
    "data": ts_ate_negativo
  },
  "yAxis": {
    "type": 'value'
  },
  "series": [
    {
      "name": 'Lucros',
      "type": 'line',
      "stack": 'Total',
      "data": lucros
    }
  ]
}

st_echarts(options=options)

st.write("A data recomendada para abate do rebanho é: {}".format(t_ideal))
