import numpy as np
import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
from funcoes import metodo_minimos_quadrados, polinomios, r_quadrado
import os

df = pd.read_excel(os.path.join("base_dados", "BaseDados.xlsx"), sheet_name=0, engine='openpyxl')

st.title("Sistema de recomendação para data de abate de lote de animais")

preco_carne = st.slider("Preço da carne animal (R$ / kg):", 3.0, 7.0, 5.3, 0.1)
preco_racao = st.slider("Preço da ração animal (R$ / kg):", 0.80, 1.50, 0.90, 0.1)

df["L"] = df["M"] * preco_carne - df["R"] * preco_racao
df = df.dropna(axis=0)

for g in range(2, 10):
  ts = []
  massas = []
  racoes = []
  coefs_massa = metodo_minimos_quadrados.mmq(entradas=np.array(df["t"]), saidas=np.array(df["M"]), g=g)
  coefs_racao = metodo_minimos_quadrados.mmq(entradas=np.array(df["t"]), saidas=np.array(df["R"]), g=g)
  coefs_lucro = metodo_minimos_quadrados.mmq(entradas=np.array(df["t"]), saidas=np.array(df["L"]), g=g)

  if coefs_lucro[0] < 0:
    for t in range(1, len(df) + 1):
        massas.append(polinomios.polinomio(coefs=coefs_massa, entrada=int(t)))
        racoes.append(polinomios.polinomio(coefs=coefs_racao, entrada=int(t)))
        ts.append(t)
    
    acerto_massas = r_quadrado.r_2(valores_exp=df["M"], valores_teo=massas)
    acerto_racoes = r_quadrado.r_2(valores_exp=df["R"], valores_teo=racoes)

    if acerto_massas > 0.99 and acerto_racoes > 0.99:
      break

if coefs_lucro[0] > 0:
  print(f"Coeficientes Lucro: \n{coefs_lucro}\n")
  st.warning("São necessários mais dados para definir a data de abate!!!")
  st.stop()

massas = np.array(massas)
racoes = np.array(racoes)
massas = list(np.round(massas, 2).reshape(len(massas)))
racoes = list(np.round(racoes, 2).reshape(len(racoes)))

t = 1
lucros = []
custos = []
ts_ate_negativo = []
virou = False
while True:
  lucros.append(polinomios.polinomio(coefs=coefs_lucro, entrada=int(t)))
  custos.append(preco_racao * polinomios.polinomio(coefs=coefs_racao, entrada=t))

  if len(lucros) > 1 and not virou:
    if lucros[-1] < lucros[-2]:
      t_ideal = t - 1
      lucro_maximo = float(lucros[-2])
      custo_total = np.sum(custos)
      virou = True

  if lucros[-1] < 0:
    ts_ate_negativo.append(t)
    break
  else:
    ts_ate_negativo.append(t)
    t += 1

lucros = np.array(lucros)
lucros = list(np.round(lucros, 2).reshape(len(lucros)))

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
      "data": lucros,
      "markPoint": {
        "data": [
          { "type": 'max', "name": 'Max' }
        ]
      }
    }
  ]
}

st_echarts(options=options)

col1, col2, col3 = st.columns(3)
col1.metric("Data para Abate:", "{}".format(t_ideal))
col2.metric("Lucro Maximo:", "R$ {:.2f}".format(lucro_maximo), "{:.0f}%".format(100 * lucro_maximo / custo_total))
col3.metric("Custo Total:", "R$ {:.2f}".format(custo_total))

st.title("Ração vs Engorda")

options = {
  "title": {
    "text": 'kg'
  },
  "tooltip": {
    "trigger": 'axis'
  },
  "legend": {
    "data": ["Massa Animal", "Massa de Ração"]
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
      "name": 'Massa Animal',
      "type": 'line',
      # "stack": 'Total',
      "data": list(df["M"])
    },
    {
      "name": 'Massa de Ração',
      "type": 'line',
      # "stack": 'Total',
      "data": list(df["R"])
    }
  ]
}

st_echarts(options=options)
