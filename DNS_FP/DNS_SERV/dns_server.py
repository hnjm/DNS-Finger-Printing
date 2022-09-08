#!/usr/bin/python

import socket

from scapy.layers.dns import *
from scapy.all import *

#from DNS_FP_runner import *

# dns_names = {"mpapp.nobies.in" : "172.16.45.84"}
#
# def resolve(name):
#     global dns_names
#     if name in dns_names:
#         return dns_names[name]
#     else :
#         # you ought to add some basic checking of name here
#         dns_names[name] = socket.gethostbyname(name)
#         return dns_names[name]
#
# host = ''
# port = 50000
# backlog = 5
# size = 1024
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind((host,port))
# s.listen(backlog)
# while 1:
#     client, address = s.accept()
#     data = client.recv(size).decode()
#     if data:
#         bits = data.split(":")
#         if bits[0] == 'h':
#             client.send(resolve(bits[1]).encode())
#     client.close()

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    # finally:
    #     globals()[package] = importlib.import_module(package)

import alive_progress
install_and_import('alive_progress')
INTERVAL_WAIT_SEC = 5



def wait_bar(interval_wait_sec: int = INTERVAL_WAIT_SEC):
    sec_time = interval_wait_sec if (interval_wait_sec > 0) else INTERVAL_WAIT_SEC
    with alive_progress.alive_bar(sec_time, title=f'Wait now {sec_time} seconds', theme='classic') as bar:
        for i in range(sec_time):
            time.sleep(1)
            bar()

wait_bar()
#
# src_port = random.randint(49152, 65535)
# dns_req = IP(dst='88.80.64.8') / UDP(sport=src_port, dport=53) / DNS(rd=0, qd=DNSQR(qname='lexico.com'))#, qtype='A'))
# answer = sr1(dns_req, timeout=5)
# answer.show()
# print('rd flag is:', answer[DNS].rd)
#
#
# from time import gmtime, strftime, localtime
#
# print('ttl is:', answer[DNS].ttl)
# print('got ', answer[DNS].ancount, 'answers')
# print('answer time:', answer.time)
# print(strftime("%a, %d %b %Y %H:%M:%S +0000", localtime(answer.time)),'\n')
# print('pkt time:', dns_req.sent_time)
# print(strftime("%a, %d %b %Y %H:%M:%S +0000", localtime(dns_req.sent_time)),'\n')
# print()
#
# for x in range(answer[DNS].ancount):
#     print(answer[DNSRR][x].ttl)
#
# def sub_date(t: str, sep : str = ', '):
#     try:
#         return t.split(sep)[1]
#     except:
#         return ''
#
# # print(sub_date("sdfsd , sds", sep=', '))
# # with open('me.txt', 'r') as f:
# #     print(*f.readlines(), sep='\n')
