import spacy
from collections import Counter

def pos_tagging_df(nombre, textos):
    contadores = {
        "VERB": Counter(),
        "NOUN": Counter(),
        "ADJ": Counter(),
        "ADV": Counter(),
################################
        "DET": Counter(),
        "PRON": Counter(),
        "ADP": Counter(),
        "CCONJ": Counter(),
    }
    entidades = Counter()

    nlp = spacy.load("es_core_news_md")

    for texto in textos:
        doc = nlp(texto)

        for ent in doc.ents:
            entidades[(ent.text, ent.label_)] += 1

        for token in doc:
            if  token.is_punct or token.is_space:
                continue

            lema = token.lemma_.lower()
            if token.pos_ in contadores:
                contadores[token.pos_][lema] += 1

    registros = []
    etiquetas =  list(contadores.keys())

    for pos in etiquetas:
        top = contadores[pos].most_common()
        for lema, frec in top:
            registros.append(
                {
                    "lugar": nombre,
                    "tipo": "POS",
                    "categoria": pos,
                    "elemento": lema,
                    "frecuencia": frec,
                }
            )

    for (ent_texto, ent_label), frec in entidades.most_common():
        registros.append(
            {
                "lugar": nombre,
                "tipo": "NER",
                "categoria": ent_label,
                "elemento": ent_texto,
                "frecuencia": frec,
            }
        )

    return registros
