import datetime
import util
from trie import Trie


def edge_rank(korisnici_graf, statusi, reakcije, komentari, deljenja, korisnik):  # funkcija koja vraca listu objava
    # sortiranu po ranku objave
    rezultat = []

    for status in statusi:
        status_id = status[0]
        rank = rank_statusa(korisnici_graf, statusi, reakcije, komentari, deljenja, korisnik, status_id)
        rezultat.append((status, rank))

    rezultat.sort(key=lambda x: x[1], reverse=True)

    return [status for status, rank in rezultat]


def rank_statusa(korisnici_graf, statusi, reakcije, komentari, deljenja, korisnik,
                 status_id):  # funkcija vraca rank statusa za korisnika, tj. koliko je status dobar za korisnika
    for status in statusi:
        if status[0] == status_id:
            autor_statusa = status[5]
            return korisnikova_sklonost(korisnici_graf, statusi, reakcije, komentari, deljenja, korisnik, autor_statusa) * popularnost(statusi, status_id) * vremenski_baziran_parametar_raspada(statusi, status_id)


def korisnikova_sklonost(korisnici_graf, statusi, reakcije, komentari, deljenja, korisnik,
                         autor_statusa):  # korisnikova sklonost ka autoru statusa
    jacina_akcije = {
        'reagovanje': 0.5,
        'komentarisanje': 1.0,
        'deljenje': 1.5,
        'prijateljstvo': 10.0
    }

    sklonost = 0

    #korisnici_graf = util.organizuj_korisnike_u_graf()
    prijatelji = set(korisnici_graf.neighbors(korisnik))
    prijatelji_prijatelja = set()

    for prijatelj in prijatelji:
        for prijatelj_prijatelja in korisnici_graf.neighbors(prijatelj):
            prijatelji_prijatelja.add(prijatelj_prijatelja)

    if autor_statusa in prijatelji:
        sklonost += jacina_akcije['prijateljstvo']

    autorovi_statusi = set()
    for status in statusi:
        if status[5] == autor_statusa:
            status_id = status[0]
            autorovi_statusi.add(status_id)

    trenutno_vreme = datetime.datetime.now()

    for reakcija in reakcije:
        if reakcija[0] in autorovi_statusi:
            vreme_akcije = datetime.datetime.strptime(reakcija[3], '%Y-%m-%d %H:%M:%S')
            faktor_vremena = 1 / (1 + (trenutno_vreme - vreme_akcije).total_seconds() / 86400)
            if reakcija[2] == korisnik:
                sklonost += jacina_akcije['reagovanje'] * faktor_vremena
            elif reakcija[2] in prijatelji:
                sklonost += jacina_akcije['reagovanje'] * faktor_vremena * 0.2
            elif reakcija[2] in prijatelji_prijatelja:
                sklonost += jacina_akcije['reagovanje'] * faktor_vremena * 0.05

    for deljenje in deljenja:
        if deljenje[0] in autorovi_statusi:
            vreme_akcije = datetime.datetime.strptime(deljenje[2], '%Y-%m-%d %H:%M:%S')
            faktor_vremena = 1 / (1 + (trenutno_vreme - vreme_akcije).total_seconds() / 86400)
            if deljenje[1] == korisnik:
                sklonost += jacina_akcije['deljenje'] * faktor_vremena
            elif deljenje[1] in prijatelji:
                sklonost += jacina_akcije['deljenje'] * faktor_vremena * 0.2
            elif deljenje[1] in prijatelji_prijatelja:
                sklonost += jacina_akcije['deljenje'] * faktor_vremena * 0.05

    for komentar in komentari:
        if komentar[1] in autorovi_statusi:
            vreme_akcije = datetime.datetime.strptime(komentar[5], '%Y-%m-%d %H:%M:%S')
            faktor_vremena = 1 / (1 + (trenutno_vreme - vreme_akcije).total_seconds() / 86400)
            if komentar[4] == korisnik:
                sklonost += jacina_akcije['komentarisanje'] * faktor_vremena
            elif komentar[4] in prijatelji:
                sklonost += jacina_akcije['komentarisanje'] * faktor_vremena * 0.2
            elif komentar[4] in prijatelji_prijatelja:
                sklonost += jacina_akcije['komentarisanje'] * faktor_vremena * 0.05

    return sklonost


def popularnost(statusi, status_id):
    vrednost = 0

    for status in statusi:
        if status[0] == status_id:
            vrednost += int(status[7]) * 5
            vrednost += int(status[8]) * 5
            vrednost += int(status[9]) * 5
            break

    return vrednost


def vremenski_baziran_parametar_raspada(statusi, status_id):
    vrednost = 1

    for status in statusi:
        if status[0] == status_id:
            status_vreme = status[4]

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


def pretraga_statusa(korisnici_graf, statusi, reakcije, deljenja, komentari, korisnik, unos_pretrage):
    rezultati = []
    rezultati_fraza = []
    if util.je_pod_navodnicima(unos_pretrage):
        fraza = True
        unos_pretrage = unos_pretrage[1:-1]
    else:
        fraza = False

    for status in statusi:
        if fraza and unos_pretrage.lower() in status[1].lower():
            rezultati_fraza.append(status)
        else:
            trie = Trie()
            words = status[1].split()
            for word in words:
                trie.insert(word.lower())

            rank = rank_statusa(korisnici_graf, statusi, reakcije, deljenja, komentari, korisnik, status[0])
            broj_reci = 0

            for rec in unos_pretrage.split():
                if trie.search(rec.lower()):
                    broj_reci += 1

            rezultati.append((status, broj_reci, rank))

    rezultati.sort(key=lambda x: (x[1], x[2]), reverse=True)
    pretraga = rezultati_fraza + rezultati
    prvih_10 = pretraga[:10]
    return prvih_10


if __name__ == '__main__':
    statusi = util.statusi_serijalizacija()
    reakcije = util.reakcije_serijalizacija()
    deljenja = util.deljenje_serijalizacija()
    komentari = util.komentari_serijalizacija()
    # print(edge_rank(statusi, reakcije, deljenja, komentari, 'Shirley Bell'))
    for status in pretraga_statusa(statusi, reakcije, deljenja, komentari, 'Shirley Bell', '"i love"'):
        print(status)
