from random import randint
import logging

def ping_pong():
    print('entered ping')
    return {"ping": "pong"}

def sample(size, begin, end):
    print('entered sample')
    data = []
    for i in range(0, size):
        data.append(randint(begin, end))
    return {"sample": data}
    #return json_response(sample=data)

    """
    La commande 'sort' permet de trier une liste de nombres.
    ces nombres sont envoyés par le serveur "maitre" par petits paquets aléatoires
        {
            "command": "sort",
            "id": 0,
            "order": 0,
            "last": false,
            "length": 7,
            "data": [3, 67, 87, 3, 1, 9867, 567]
        }
    
    Chaque fois qu'un paquet arrive, un nouveau thread est lancé pour maintenir la liste reçue
    et une réponse "200" est envoyée au serveur.

        --> Tasks that spend much of their time waiting for external events are generally good candidates 
        for threading.

    Lorsque "last:true", cad qu'on vient de recevoir le dernier paquet, alors on assemble
    tous les paquets et on effectue un tri global.

    Finalement, on renvoie la liste triée par petits paquets également.
    """
def sort(data):
    logging.info("Thread %s: starting", data['order'])
    sorted_data = quicksort(data['data'])
    data['data'] = sorted_data
    logging.info("Thread %s: finishing", data['order'])
    return data

def quicksort(remaining_data):
    less = []
    greater = []
    equal = []

    if len(remaining_data) > 1:
        pivot = remaining_data[0]
        for number in remaining_data:
            if number < pivot:
                less.append(number)
            elif number > pivot:
                greater.append(number)
            elif number == pivot:
                equal.append(number)
        return quicksort(less)+equal+quicksort(greater)
    else:
        return remaining_data

        