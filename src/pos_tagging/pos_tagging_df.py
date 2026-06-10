import spacy
from collections import Counter

def pos_tagging_df(nombre, textos_con_rating):
    contadores = {
        "VERB": Counter(),
        "NOUN": Counter(),
        "ADJ": Counter(),
        "ADV": Counter(),
        "DET": Counter(),
        "PRON": Counter(),
        "ADP": Counter(),
        "CCONJ": Counter(),
    }
    entidades = Counter()
    ratings_por_lema = {}
    ratings_por_ent = {}

    nlp = spacy.load("es_core_news_md")

    for texto, rating in textos_con_rating:
        doc = nlp(texto)

        for ent in doc.ents:
            key = (ent.text, ent.label_)
            entidades[key] += 1
            ratings_por_ent.setdefault(key, Counter())[rating] += 1

        for token in doc:
            if token.is_punct or token.is_space:
                continue

            lema = token.lemma_.lower()
            if token.pos_ in contadores:
                contadores[token.pos_][lema] += 1
                ratings_por_lema.setdefault((token.pos_, lema), Counter())[rating] += 1

    registros = []
    etiquetas = list(contadores.keys())

    for pos in etiquetas:
        top = contadores[pos].most_common()
        for lema, frec in top:
            registro = {
                "lugar": nombre,
                "tipo": "POS",
                "categoria": pos,
                "elemento": lema,
                "frecuencia": frec,
            }
            registro.update({
                f"rating_{r}": c
                for r, c in ratings_por_lema[(pos, lema)].items()
            })
            registros.append(registro)

    for (ent_texto, ent_label), frec in entidades.most_common():
        registro = {
            "lugar": nombre,
            "tipo": "NER",
            "categoria": ent_label,
            "elemento": ent_texto,
            "frecuencia": frec,
        }
        registro.update({
            f"rating_{r}": c
            for r, c in ratings_por_ent[(ent_texto, ent_label)].items()
        })
        registros.append(registro)

    return registros