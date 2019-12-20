import logging, threading, time

class myThread(threading.Thread):
    def __init__(self, threadID, list_numbers):
        logging.info("THREAD %d initialization", threadID)
        threading.Thread.__init__(self)
        self.__threadID = threadID
        self.__list_numbers = list_numbers
        self.__status = "Launched"
        self.__time_start = 0
        self.__time_finish = 0
        self.__list_sorted = []
    
    def get_info(self):
        logging.info('THREAD %d entered GET_THREAD_INFO()', self.__threadID)
        info = {"ID": self.__threadID, 
                "Numbers": len(self.__list_numbers),
                "Status": self.__status,
                "Start Time": self.__time_start,
                "Finished Time": self.__time_finish,
                "Total Time": self.__time_finish-self.__time_start}

        logging.info(info)
        return info

    def get_list_numbers(self):
        return self.__list_numbers
    
    def get_list_sorted(self):
        return self.__list_sorted

    def run(self):
        logging.info("THREAD %d entered RUN()", self.__threadID)
        self.__status = "Running"
        try:
            logging.info("THREAD %d launched QUICKSORT(data)", self.__threadID)
            self.__list_sorted = self.quicksort(self.__list_numbers)
            with open('thread-{}.txt'.format(str(self.__threadID)), 'w') as file:
                logging.info("OPENED file thread-%s.txt", str(self.__threadID))
                for number in self.__list_sorted:
                    file.write("%s\n" %str(number))
            self.__status = "Done"
            logging.info("THREAD %d finished QUICKSORT(data)", self.__threadID)
            #print(self.__list_sorted)

        except:
            logging.error("Error while sorting list from THREAD %s", self.__threadID)
            self.__status = "Error"

    
    def quicksort(self, remaining_data):
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
            return self.quicksort(less)+equal+self.quicksort(greater)
        else:
            return remaining_data