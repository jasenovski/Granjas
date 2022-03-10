import numpy as np
import pandas as pd

def r_2(valores_exp: pd.core.series.Series, valores_teo: list):
    return ((valores_teo - valores_exp.mean()) ** 2).sum() / ((valores_exp - valores_exp.mean()) ** 2).sum()
