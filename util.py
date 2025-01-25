import csv
import networkx as nx
import pickle


def serialize_object(obj, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(obj, f)


def deserialize_object(file_path):
    with open(file_path, 'rb') as f:
        obj = pickle.load(f)
    return obj


def statusi_serijalizacija():
    return deserialize_object('statusi.pkl')


def reakcije_serijalizacija():
    return deserialize_object('reakcije.pkl')


def komentari_serijalizacija():
    return deserialize_object('komentari.pkl')


def deljenje_serijalizacija():
    return deserialize_object('deljenja.pkl')


def korisnici_serijalizacija():
    return deserialize_object('korisnici.pkl')


def organizuj_korisnike_u_graf():
    graf = nx.Graph()

    with open('dataset/dataset/friends.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            user = row[0]
            friends_list = row[2].split(',')

            graf.add_node(user)

            for friend in friends_list:
                graf.add_edge(user, friend)

    return graf


def je_pod_navodnicima(string):
    if string.startswith("'") and string.endswith("'"):
        return True
    elif string.startswith('"') and string.endswith('"'):
        return True
    else:
        return False


if __name__ == '__main__':
    grafikon = organizuj_korisnike_u_graf()

    print(grafikon.edges())
