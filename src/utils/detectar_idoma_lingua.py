import pandas as pd
from lingua import Language, LanguageDetectorBuilder

def detectar_idoma_lingua(texto):
    if pd.isna(texto) or str(texto).strip() == "":
        return None
    
    idiomas = [Language.SPANISH, Language.ENGLISH, Language.GERMAN, Language.FRENCH, Language.PORTUGUESE]
    detector = LanguageDetectorBuilder.from_languages(*idiomas).build()
    resultado = detector.detect_language_of(str(texto))
    return resultado.iso_code_639_1.name.lower() if resultado else "unknown"