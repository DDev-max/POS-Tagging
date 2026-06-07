import pandas as pd 
import fasttext

def detectar_espanol_fasttext(texto):
    if not isinstance(texto, str) or pd.isna(texto):
        return False
    
    model = fasttext.load_model(r'C:\Users\mecag\Desktop\TEXTOUS\src\utils\lid.176.ftz')
    prediccion = model.predict(texto, k=1)
    idioma = prediccion[0][0].replace("__label__", "")
    confianza = prediccion[1][0]
    
    return idioma == 'es' and confianza > 0.80