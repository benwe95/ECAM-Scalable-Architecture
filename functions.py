from random import randint
import logging, mythread
import tabulate
import requests
from flask import jsonify

NUMBERS = {}

def ping_pong():
    print('entered ping')
    return {"ping": "pong"}

def sample(size, begin, end):
    print('entered sample')
    data = []
    for i in range(0, size):
        data.append(randint(begin, end-1))
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
    
    Chaque fois qu'un paquet arrive, on stocke les nombres envoyés dans une liste globale et on renvoie immédiatemment
    une réponse "200" au serveur.

    Lorsque "last:true", cad qu'on vient de recevoir le dernier paquet, alors on peut lancer l'opération de tri
    de la liste entière en utilisant du multi-threading
    
        --> thread = Tasks that spend much of their time waiting for external events are generally good candidates 
        for threading.

    Finalement, on renvoie la liste triée par petits paquets également.
    """
def sort(data):
    logging.info("Entering SORT function")
    print(data)

    if(str(data['id']) not in NUMBERS.keys()): 
         NUMBERS[str(data['id'])] = data['data']
    else:
        NUMBERS[str(data['id'])].extend(data['data'])

    if not data['last']:
       return
    

    list_sequences = launch_threads(NUMBERS[str(data['id'])].copy(), 1)
    del NUMBERS[str(data['id'])][:]
    sorted_list = merge_sequences(list_sequences)
    prepare_response(sorted_list, 100, data['id'])
    '''
    for element in resp:
        requests.post('http://172.17.3.35:8000', json=element)
    '''

def launch_threads(list_numbers, number_threads):
    logging.info("Entered LAUNCH_THREADS function")
    jobs = []
    # Get all the numbers from the file.txt and store them as a list of integers
    '''
    with open(file, 'r') as file:
        list_numbers = file.readlines()
        list_numbers = [int(s.strip()) for s in list_numbers]
    '''

    total_numbers = len(list_numbers)   
    numbers_by_threads = total_numbers//number_threads
    logging.info("\nTotal numbers: %s\nNumbers by threads: %s\n", total_numbers, numbers_by_threads)

    for thread_num in range(0, number_threads):
        if len(list_numbers)<numbers_by_threads:
            numbers_by_threads = len(list_numbers)
        numbers = list_numbers[thread_num*numbers_by_threads:(thread_num+1)*numbers_by_threads]
        my_thread = mythread.myThread(thread_num, numbers)
        jobs.append(my_thread)
        my_thread.run()

    print_jobs(jobs)
    list_sequences = [job.get_list_sorted() for job in jobs]
    return list_sequences


''' Exemple:
    [
        [1, 5, 7, 12],
        [2, 3, 8, 10],
        [1, 6, 7, 11, 13]
    ]

    min_of_each_list = [1, 2, 1]
    minimum = 1
    index_min = 0
    sorted_list.append(1) -> [1]

    [
        [5, 7, 12],
        [2, 3, 8, 10],
        [1, 6, 7, 11, 13]
    ]

    min_of_each_list = [5, 2, 1]

'''
def merge_sequences(list_sequences):
    logging.info("Entered MERGE_SEQUENCES function")
    sorted_list = []
    # Cette liste permet de stocker le minimum de chaque liste çad le premier élément
    min_of_each_list = [element[0] for element in list_sequences]

    while (len(min_of_each_list)>0):
        ###print('----------------------------\nList of mins: {}'.format(min_of_each_list))
        # Take the minimum of the current minima...
        minimum = min(min_of_each_list)
        ###print('minimum: {}'.format(minimum))
        # ... and get the list ID corresponding (index stops when it finds a match)
        index_min = min_of_each_list.index(minimum)
        ###print('index_min: {}'.format(index_min))
        sorted_list.append(minimum)
        ###print('sorted list: {}'.format(sorted_list))
        if len(list_sequences[index_min]) == 1:
            ###print('if ok')
            del min_of_each_list[index_min]
            del list_sequences[index_min]
        else:
            ###print('else: {}'.format(list_sequences[index_min][0]))
            del list_sequences[index_min][0]
            # Replace the minimum by the 'new' minimum of the corresponding list
            min_of_each_list[index_min] = list_sequences[index_min][0]
        ###print('remaining: {}'.format(list_sequences))

    #print('Global sorted list: {}'.format(sorted_list))
    return sorted_list

def prepare_response(list_sorted_numbers, numbers_by_packets, id_packet):

    order_packet = 0
    end = False
    response = []

    while len(list_sorted_numbers)>0:
        if len(list_sorted_numbers)<numbers_by_packets:
            data = list_sorted_numbers[0:]
            end = True
            numbers_by_packets = len(list_sorted_numbers)
        else: 
            data = list_sorted_numbers[0:numbers_by_packets]

        res = {
	    "command": "sorted",
	    "data": data,
	    "id": id_packet,
	    "order": order_packet,
	    "last": end,
	    "length": numbers_by_packets
        }
        #print('----------------\nid: {}\norder_packer: {}\nlast: {}\nnumbers: {}'.format(
        #    id_packet, order_packet, end, numbers_by_packets))
        print(res)
        del list_sorted_numbers[0:numbers_by_packets]

        order_packet += 1
        requests.post('http://172.17.3.35:8000', json=res)
        response.append(res)
    return response

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

        
    #logging.info("Thread %s: starting", data['order'])
    #sorted_data = quicksort(data['data'])
    #data['data'] = sorted_data
    #logging.info("Thread %s: finishing", data['order'])
    #return data

def print_jobs(jobs):
    logging.info("FUNCTIONS Entered PRINT_JOBS()")
    jobs_info = [job.get_info() for job in jobs]
    headers = jobs_info[0].keys()
    rows = [x.values() for x in jobs_info]
    print (tabulate.tabulate(rows, headers, tablefmt="grid"))

if __name__ == '__main__':
    logging.info("FUNCTIONS file MAIN")
    list_sequences = [
        [1, 5, 7, 12],
        [2, 3, 8, 10],
        [1, 6, 7, 11, 13]
    ]

    merge_sequences(list_sequences)