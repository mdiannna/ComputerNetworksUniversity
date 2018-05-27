# UDP client
import socket
import logging
import sys
import timeit
import threading

timeout = 3
max_number = 12

# Sliding window
window_size = 3
window_start = 1
window_end = window_start+window_size-1

port = 10000
adresa = '172.111.0.14'
server_address = (adresa, port)
# mesaj = sys.argv[0]



logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.settimeout(timeout);



confirmedNumbers = [];


def sendNumber(i):
    # logging.info("")
    try:
        mesaj = "hello " + str(i);
        logging.info('Trimitem mesajul "%d" catre %s', i, adresa)
        sent = sock.sendto(mesaj, server_address)
    except:
        logging.error("Send error")



class waitForConfirmation(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      # self.threadID = threadID
      # self.name = name
      # self.counter = counter
      # number = i

    def run(self):
        number = 0;
        print("selfi: " + str(number));
        global window_start
        global window_end
        global confirmedNumbers

        logging.info('Asteptam un raspuns...')
        try:
            data, server = sock.recvfrom(4096)
            logging.info('Content primit: "%s"', data)
            number = int(data.replace("Hello ", ""));
            print "SELFI:" + number

            confirmedNumbers.append(number);

            threadLock.acquire()
            print("selfi: " + str(number) + "   window_start:" + str(window_start))
            print("sent numbers:")
            print confirmedNumbers

            # daca numarul a fost trimis deja, incrementez window_start si window_end
            while (window_end+1 in confirmedNumbers and window_end < max_number):
                window_end = window_end + 1
                window_start = window_start + 1

            if(window_end < max_number and number == window_start and window_end < max_number):
                    window_start = window_start+1;
                    window_end = window_end+1;
                    print ("send" + str(window_end))
                    sendI(window_end);
                
            threadLock.release()

        except:
            logging.info("timeout" + str(number))
            sendI(number)




threadLock = threading.Lock()
threads = []


def sendI(i):
    sendNumber(i)
    thread1 = waitForConfirmation()
    thread1.start();
    threads.append(thread1)


i=1;

for i in range(window_start, window_end+1):
    sendNumber(i)

initial_window_start = window_start
initial_window_end = window_end

for i in range(initial_window_start, initial_window_end+1):
    thread1 = waitForConfirmation()
    thread1.start();
    threads.append(thread1)

    # sendI(i);



# sendNumber(6)
# # try:
# thread6 = waitForConfirmation(6)
# thread6.start();
# # thread1 = thread.start_new_thread( , (i,) )
# threads.append(thread6)
# # except:
 
# for i in range(1,5):
#     try:
#     except:

# finally:

for t in threads:
    t.join()

logging.info('window start:' + str(window_start))
logging.info('window end:' + str(window_end))
logging.info('closing socket')
sock.close()
