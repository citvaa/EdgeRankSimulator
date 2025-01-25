import csv
import datetime
import util
import pandas as pd
from collections import defaultdict
from trie import Trie


def edge_rank(korisnik):  # funkcija koja vraca listu objava sortiranu po ranku objave
    lista_statusa = []

    with open('dataset/dataset/test_statuses2.csv', 'r', encoding='utf-8') as f:
        statusi_reader = csv.reader(f)
        next(statusi_reader)
        for status in statusi_reader:
            status_id = status[0]
            rank = rank_statusa(korisnik, status_id)
            lista_statusa.append((status, rank))

    lista_statusa.sort(key=lambda x: x[1], reverse=True)

    return [status for status, rank in lista_statusa]


def rank_statusa(korisnik,
                 status_id):  # funkcija vraca rank statusa za korisnika, tj. koliko je status dobar za korisnika
    with open('dataset/dataset/test_statuses2.csv', 'r', encoding='utf-8') as f:
        statusi_reader = csv.reader(f)
        next(statusi_reader)
        for status in statusi_reader:
            if status[0] == status_id:
                autor_statusa = status[5]
                return korisnikova_sklonost(korisnik, autor_statusa) * popularnost(
                    status_id) * vremenski_baziran_parametar_raspada(status_id)


def korisnikova_sklonost(korisnik, autor_statusa):  # korisnikova sklonost ka autoru statusa
    jacina_akcije = {
        'reagovanje': 0.5,
        'komentarisanje': 1.0,
        'deljenje': 1.5,
        'prijateljstvo': 10.0
    }

    sklonost = 0

    korisnici = util.organizuj_korisnike_u_graf()
    prijatelji = set(korisnici.neighbors(korisnik))
    prijatelji_prijatelja = set()

    for prijatelj in prijatelji:
        for prijatelj_prijatelja in korisnici.neighbors(prijatelj):
            prijatelji_prijatelja.add(prijatelj_prijatelja)

    if autor_statusa in prijatelji:
        sklonost += jacina_akcije['prijateljstvo']

    df_statuses = pd.read_csv('dataset/dataset/test_statuses2.csv')
    autorovi_statusi = set(df_statuses[df_statuses['author'] == autor_statusa]['status_id'])

    trenutno_vreme = datetime.datetime.now()

    with open('dataset/dataset/test_reactions.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] in autorovi_statusi:
                vreme_akcije = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                faktor_vremena = 1 / (1 + (trenutno_vreme - vreme_akcije).total_seconds() / 86400)
                if row[2] == korisnik:
                    sklonost += jacina_akcije['reagovanje'] * faktor_vremena
                elif row[2] in prijatelji:
                    sklonost += jacina_akcije['reagovanje'] * faktor_vremena * 0.2
                elif row[2] in prijatelji_prijatelja:
                    sklonost += jacina_akcije['reagovanje'] * faktor_vremena * 0.05

    with open('dataset/dataset/test_shares.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] in autorovi_statusi:
                vreme_akcije = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
                faktor_vremena = 1 / (1 + (trenutno_vreme - vreme_akcije).total_seconds() / 86400)
                if row[2] == korisnik:
                    sklonost += jacina_akcije['deljenje'] * faktor_vremena
                elif row[2] in prijatelji:
                    sklonost += jacina_akcije['deljenje'] * faktor_vremena * 0.2
                elif row[2] in prijatelji_prijatelja:
                    sklonost += jacina_akcije['deljenje'] * faktor_vremena * 0.05

    with open('dataset/dataset/test_comments.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[1] in autorovi_statusi:
                vreme_akcije = datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                faktor_vremena = 1 / (1 + (trenutno_vreme - vreme_akcije).total_seconds() / 86400)
                if row[4] == korisnik:
                    sklonost += jacina_akcije['komentarisanje'] * faktor_vremena
                elif row[4] in prijatelji:
                    sklonost += jacina_akcije['komentarisanje'] * faktor_vremena * 0.2
                elif row[4] in prijatelji_prijatelja:
                    sklonost += jacina_akcije['komentarisanje'] * faktor_vremena * 0.05

    return sklonost


def popularnost(status_id):
    vrednost = 0

    with open('dataset/dataset/test_statuses2.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == status_id:
                vrednost += int(row[7]) * 10
                vrednost += int(row[8]) * 10
                vrednost += int(row[9]) * 10
                break

    return vrednost


def vremenski_baziran_parametar_raspada(status_id):
    with open('dataset/dataset/test_statuses2.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0] == status_id:
                status_vreme = row[4]

                trenutno_vreme = datetime.datetime.now()
                vreme_objave = datetime.datetime.strptime(status_vreme, '%Y-%m-%d %H:%M:%S')

                proslo_vreme = trenutno_vreme - vreme_objave
                proslo_dani = proslo_vreme.days
                proslo_sati = proslo_vreme.seconds // 3600
                proslo_minuti = (proslo_vreme.seconds % 3600) // 60

                ukupno_minuti = proslo_dani * 24 * 60 + proslo_sati * 60 + proslo_minuti

                vrednost = 1 / (1 + ukupno_minuti / 1440)  # 1440 minuta = 1 dan
                break

    return vrednost


if __name__ == '__main__':
    # print(edge_rank('Shirley Bell'))
