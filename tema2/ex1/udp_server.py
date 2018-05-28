# UDP Server
import socket
import logging

logging.basicConfig(format = u'[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.NOTSET)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 10000
adresa = '172.111.0.14'
server_address = (adresa, port)
sock.bind(server_address)
logging.info("Serverul a pornit pe %s si portnul portul %d", adresa, port)

received_numbers = []
max_number = 6

# Sliding window
window_size = 3
window_start = 1
window_end = window_start+window_size-1


while True:
    logging.info('Asteptam mesaje...')
    data, address = sock.recvfrom(4096)

    logging.info("Am primit %s octeti de la %s", len(data), address)
    logging.info('Content primit: "%s"', data)
    

    print("Received numbers:")
    print received_numbers


    if data:
        number = int(data.replace("hello ", ""));
        print "number:" + str(number)
        print "window start:" + str(window_start)
        print "window_end" + str(window_end)

        if not number in received_numbers and number >= window_start and number <= window_end and number <= max_number:
            if(number == 1 or number == received_numbers[len(received_numbers)-1] + 1):
                received_numbers.append(number)
            
                # if number not in received_numbers:
                #     received_numbers.append(number)        

                while(number in received_numbers and number==window_start):
                  window_end = window_end + 1
                  window_start = window_start + 1
                  number = number + 1


                sent = sock.sendto(data, address)
                logging.info('Am trimis %d octeti inapoi la %s', sent, address)

        if(number in received_numbers):
            sent = sock.sendto(data, address)
            logging.info('Am trimis %d octeti inapoi la %s', sent, address)
                

        if len(received_numbers) == max_number:
            break
print("Received numbers:")
print received_numbers
          