# UDP client
import socket
import logging
import sys
import timeit
import threading

timeout = 3
max_number = 6

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
        while True:
            number = 0;
            print("selfi: " + str(number));
            global window_start
            global window_end
            global confirmedNumbers


            logging.info('Asteptam un raspuns...')
            try:
                data, server = sock.recvfrom(4096)
                logging.info('Content primit: "%s"', data)
                number = int(data.replace("hello ", ""));
                print "SELFI:" + str(number)

                confirmedNumbers.append(number);

                # threadLock.acquire()
                print("selfi: " + str(number) + "   window_start:" + str(window_start))
                print("sent numbers:")
                print confirmedNumbers


                if(window_end >= max_number) and len(confirmedNumbers) == max_number:
                    logging.info('All numbers received:')
                    print confirmedNumbers
                    return


                # daca numarul a fost trimis deja, incrementez window_start si window_end
                while (window_start+1 in confirmedNumbers and window_end < max_number):
                    window_end = window_end + 1
                    window_start = window_start + 1

                if(window_end < max_number and number == window_start):
                        window_start = window_start+1;
                        window_end = window_end+1;
                        print ("send" + str(window_end))
                        sendNumber(window_end);
                    
                # threadLock.release()

              
            except:
                j = 1
                while j <= window_end:
                    if j not in confirmedNumbers:
                        break
                    j = j+1
                    print("j: " + str(j))
                if(j > max_number):
                    return
                number = j
                logging.info("timeout" + str(number))
                sendNumber(number)




threadLock = threading.Lock()
threads = []


# def sendNumber(i):
# sendNumber(i)
    # thread1 = waitForConfirmation()
    # thread1.start();
    # threads.append(thread1)


i=1;


initial_window_start = window_start
initial_window_end = window_end

for i in range(initial_window_start, initial_window_end+1):
    sendNumber(i)


thread1 = waitForConfirmation()
thread1.start();
threads.append(thread1)


# for i in range:

    # sendNumber(i);



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

# for t in threads:
thread1.join()

logging.info('window start:' + str(window_start))
logging.info('window end:' + str(window_end))
logging.info('closing socket')
sock.close()
