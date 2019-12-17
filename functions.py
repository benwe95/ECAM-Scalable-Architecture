from random import randint
import logging, mythread
import tabulate

FILE_NUMBERS = "numbers.txt"
JOBS = []

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
    with open (FILE_NUMBERS, "a") as file:
        logging.info("Opened file numbers.txt")
        for number in data['data']:
            file.write("%s\n" %str(number))

    if not data['last']:
       return {'response': 200}

    launch_threads(FILE_NUMBERS, 5)
    return {'response': 'last packet'}

def launch_threads(file, number_threads):
    logging.info("Entered LAUNCH_THREADS function")
    # Get all the numbers from the file.txt and store them as a list of integers
    with open(file, 'r') as file:
        list_numbers = file.readlines()
        list_numbers = [int(s.strip()) for s in list_numbers]

    total_numbers = len(list_numbers)   
    numbers_by_threads = total_numbers//number_threads
    logging.info("\nTotal numbers: %s\nNumbers by threads: %s\n", total_numbers, numbers_by_threads)

    for thread_num in range(0, number_threads):
        numbers = list_numbers[thread_num*numbers_by_threads:(thread_num+1)*numbers_by_threads]
        my_thread = mythread.myThread(thread_num, numbers)
        JOBS.append(my_thread.get_info())
        my_thread.run()
    print_jobs()
    return True

def thread_job(info_thread, list_numbers):
    info_thread['status'] = 'started'

    info_thread['status'] = 'done'
    return 

def merge_sequences():
    logging.info("Entered MERGE_SEQUENCES function")
    return False

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

def print_jobs():
    logging.info("FUNCTIONS Entered PRINT_JOBS()")
    headers = JOBS[0].keys()
    rows = [x.values() for x in JOBS]
    print (tabulate.tabulate(rows, headers, tablefmt="grid"))