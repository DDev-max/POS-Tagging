# Análisis Morfosintáctico de Reseñas Turísticas de Costa Rica.
Claudio Poveda Sánchez - CUC - Mineria de textos - Proyecto 1.

Analisis morfosintáctico de reseñas turísticas **en español** de Costa Rica. Mediante POS Tagging (Part-of-Speech Tagging) con NLTK y spaCy.
Las reseñas turisticas fueron recolectadas mediante scraping de google maps. Incluyendo el Volcan Arenal, Kalambu Hot Springs, Las Ruinas de Cartago, Parque Nacional Manuel Antonio y el Museo de los niños.

Este proyecto compara ambas librerias en terminos de velocidad de ejecución y precision en la clasificacion. Se utiliza el modelo `cess_esp` para NLTK y el modelo `es_core_news_md` para spaCy.

## Estrutura del proyecto

```
.
├── dashboard
│   ├── app.py
│   ├── assets            # Imagenes de los lugares turisticos mostrados en el dashboard.
│   ├── data              # Reseñas en .csv. Deben ser importados antes de iniciar el proyecto
|   └── notebooks         # Notebooks que generan el .csv limpio. Comparacion de librerias
|   └── src               # Logica del proyecto
```

## Control de versiones
Se utilizaron las siguientes ramas de Git:

- `main`: Contiene el proyecto final
- `EDA`: Exploracion y limpieza de datos
- `pos_tagging`: Implementacion de POS Tagging con NLTK y spaCy
- `dashboard`: Implementacion del dashboard con plotly dash.

## Instalacion y ejecucion
Este proyecto utiliza python 3.11.9. Es necesario descargar el modelo [lid.176.ftz](https://fasttext.cc/docs/en/language-identification.html) para deteccion de idiomas. Puede cambiar la ruta al modelo en el archivo `src/utils/detectar_espanol_fasttext.py`

Para ejecutar el dashboard ejecute el siguiente comando en la raiz del proyecto:

```bash
python dashboard/app.py
```