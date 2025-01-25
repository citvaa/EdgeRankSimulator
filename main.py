import edge_rank
import util


def meni():
    statusi = util.statusi_serijalizacija()
    reakcije = util.reakcije_serijalizacija()
    deljenja = util.deljenje_serijalizacija()
    komentari = util.komentari_serijalizacija()
    korisnici = util.korisnici_serijalizacija()
    korisnici_graf = util.organizuj_korisnike_u_graf()  # graf koji prikazuje prijateljstva
    while True:
        ulogovani_korisnik = input('Unesite ime korisnika: ')
        if any(ulogovani_korisnik == korisnik[0] for korisnik in korisnici):
            while True:
                print('1. Pregled objava')
                print('2. Pretraga objava')
                unos = int(input())
                if unos == 1:
                    print('Ucitavanje...')
                    for status in edge_rank.edge_rank(korisnici_graf, statusi, reakcije, deljenja, komentari,
                                                      ulogovani_korisnik):
                        print(status)
                elif unos == 2:
                    print('Ucitavanje...')
                    unos_pretrage = input('Pretrazite objave: ')
                    for status in edge_rank.pretraga_statusa(korisnici_graf, statusi, reakcije, deljenja, komentari, ulogovani_korisnik,
                                                             unos_pretrage):
                        print(status)
                else:
                    print('Nevazeci unos')
        else:
            print('Ne postoji izabrani korisnik')


if __name__ == '__main__':
    meni()
