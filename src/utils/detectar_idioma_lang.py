import pandas as pd 
from langdetect import detect, DetectorFactory

def detectar_idioma_lang(texto):
    DetectorFactory.seed = 0
    if pd.isna(texto) or str(texto).strip() == "":
        return "unknown"
    
    try:
        return detect(str(texto))
    except:
        return "unknown"