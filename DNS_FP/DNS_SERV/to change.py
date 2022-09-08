# import logging
# import atexit
# # https://blog.apnic.net/2021/06/22/cache-me-outside-dns-cache-probing/
# # https://publicdnsserver.com/
#
# from scapy.layers.dns import DNSRR
#
# from main_app import pic_of_plot
#
# # logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
#
# from scapy.all import *
# import time
# from random import sample
# import json
# from alive_progress import alive_bar
# from dns_data_db import *
#
#
#
# INTERVAL_WAIT_SEC = 10
#
# class DNS_FP_runner:
#     def __init__(self, DNS_address, list_names, json_file_name: str = JSON_FILE_NAME_DEFAULT):
#         self.FREE_PORTS = range(49152, 65535) #(1024, 65536)
#         self.mutex = Lock()
#         self.JSON_FILE = json_file_name if json_file_name.endswith('.json') else JSON_FILE_NAME_DEFAULT
#         self.json_dict_total = {}
#         self.dns_dict = {}
#         self.DNS_address = DNS_address
#         self.list_names = list_names
#         self.reset_rd_illegal_count()
#         self.dns_db = dns_data_db(self.JSON_FILE)
#
#
#     def save_data(self):
#         self.dns_db.save_and_update_db()
#
#     def reset_rd_illegal_count(self):
#         self.rd_counter = 0
#         self.pkt_counter = 0
#
#     def is_recursive_DNS(self):
#         if self.pkt_counter == 0:
#             return 0
#         return (self.rd_counter / self.pkt_counter) > 0.7
#
#     # primary data of dns requests
#
#     def send_DNS_request(self, dns_server: str, name_domain: str, src_port: int, bar, is_recusive: bool = False, sec_timeout: int = MAX_WAIT):
#         rd_flag = 1 if is_recusive else 0
#         answer = None
#         i = 0
#         dns_req = IP()
#
#         while answer is None and i < 4:
#             dns_req = IP(dst=dns_server) / UDP(sport=src_port, dport=53) / DNS(rd=rd_flag, qd=DNSQR(qname=name_domain))#, qtype='A'))
#             answer = sr1(dns_req, verbose=0, timeout=sec_timeout)
#             src_port = random.randint(49152, 65535)
#
#         bar()
#
#         if (answer is not None) and (not is_recusive):
#             self.rd_counter += answer[DNS].rd
#             self.pkt_counter += 1
#
#         self.dns_dict[name_domain] = {'pkt_recv': answer, 'pkt_sent': dns_req}
#
#
#     def get_data_from_pkts(self, pkt_dict : dict):
#         dns_addr = 'No answer received...'
#         dns_ttl = 0
#         dns_time = MAX_WAIT
#         if 'pkt_recv' not in pkt_dict or 'pkt_sent' not in pkt_dict:
#                 return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': 0, 'recv_time': 0}
#
#         answer = pkt_dict['pkt_recv']
#         dns_req = pkt_dict['pkt_sent']
#         sent_time = dns_req.sent_time
#         recv_time = sent_time + MAX_WAIT if answer is None else answer.time
#         if answer is not None:
#             dns_addr = str(answer[DNS].summary()).replace('DNS Ans ', '').replace('"', '').replace(' ', '')
#             dns_addr = dns_addr if len(dns_addr) > 0 else '--'
#             dns_time = answer.time - dns_req.sent_time #end - start
#             dns_ttl = 0
#             RR_ans = answer[DNS].ancount
#             if RR_ans > 0:  # if requests came
#                 for i in range(RR_ans):
#                     dns_ttl += answer[DNSRR][i].ttl
#                 dns_ttl = round(dns_ttl / RR_ans) # get average
#
#             return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': sent_time, 'recv_time': recv_time}
#
#     def gen_port_names(self, add_names):
#         ports = sample(self.FREE_PORTS, len(add_names))
#         dict_names_ports = {}
#         i = 0
#         for name in add_names:
#             dict_names_ports[name] = ports[i]
#             i += 1
#         return dict_names_ports
#
#     def run_names_with_dns(self, is_recusive: bool = False, title: str = ''):
#
#         return self.__run_names_with_dns(self.DNS_address, self.list_names, is_recusive, title)
#
#     def __run_names_with_dns(self, dns_main_ip, names, is_recusive: bool = False, title: str = '', label: str):
#         th_list = []
#         dict_names_ports = self.gen_port_names(names)
#         # curr_time = str(time.time())
#         now = datetime.now()  # current date and time
#         curr_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#         self.dns_dict = {}
#         with alive_bar(len(names), title=title, theme='classic') as bar:  ## for something nice
#             for name in dict_names_ports:
#                 port = dict_names_ports[name]
#                 self.send_DNS_request(dns_main_ip, name, port, bar, is_recusive=is_recusive)
#
#         return self.dns_db.add_data_to_db(dns_main_ip, now, self.dns_dict)
#
#     def get_dict_times_of_dns(self, dns_ip: str, time_str: str):
#         try:
#             return self.json_dict_total[dns_ip][time_str], time_str
#         except:
#             return None, None
#
#     def reset_rd_illegal_count(self):
#         self.rd_counter = 0
#         self.pkt_counter = 0
#
# #python DNS_FP_runner.py
# def wait_bar(interval_wait_sec: int = INTERVAL_WAIT_SEC):
#     sec_time = interval_wait_sec if (interval_wait_sec > 0) else INTERVAL_WAIT_SEC
#     with alive_bar(sec_time, title=f'Wait now {sec_time} seconds', theme='classic') as bar:
#         for i in range(sec_time):
#             time.sleep(1)
#             bar()
#
# def main(DNS_address, list_names, repeats: int = 8, col_per_page:int = 1, interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True, to_show_results: bool = True):
#
#     #list_names = ['xinshipu.com']
#
#     dns_fp_run = DNS_FP_runner(DNS_address, list_names)
#     label_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
#     list_ans_vals = []
#     for i in range(repeats):
#         is_rec = (i == 0) and is_first_rec
#         str_title = f'round %d out ouf %d' % (i + 1, repeats)
#         list_ans_vals += [dns_fp_run.run_names_with_dns(is_recusive=is_rec, title=str_title)]
#
#         if i == repeats - 1:
#             continue
#
#         wait_bar(interval_wait_sec)
#
#     # dict_1, time_1 = dns_fp_run.get_dict_times_of_dns(DNS_address, '09/04/2022, 16:49:10')
#     # dict_2, time_2 = dns_fp_run.get_dict_times_of_dns(DNS_address, '09/04/2022, 16:50:13')
#     dns_fp_run.save_data()
#
#     #print(print_list)
#     print()
#     ans_rec = 'IS' if dns_fp_run.is_recursive_DNS() else 'is NOT'
#     print(f'the DNS server {DNS_address} : {ans_rec} an auto-recoesive dns')
#     if to_show_results:
#         app = pic_of_plot(DNS_address, list_names, list_ans_vals, cols_in_plot=col_per_page)
#         app.runner()
#
#
# def get_app_by_time(DNS_address, list_names, col_per_page = 1):
#
#     # list_names = ['xinshipu.com']
#
#     dns_fp_run = DNS_FP_runner(DNS_address, list_names)
#
#     list_ans_vals = []
#     list_times = [*dns_fp_run.json_dict_total[DNS_address]][-8*3:]
#     for time_str in list_times:
#         list_ans_vals += [dns_fp_run.get_dict_times_of_dns(DNS_address, time_str)]
#
#
#     app = pic_of_plot(DNS_address, list_names, list_ans_vals, cols_in_plot=col_per_page)
#     app.runner()
#
#     # fig.tight_layout()
#     #
#     # plt.show()
#
# #python DNS_FP_runner.py
#
# if __name__ == "__main__":
#     try:
#         # 94.153.241.134 - intresting
#         # 88.80.64.8 - good dns for check
#         DNS_address = '94.153.241.134'  # '88.80.64.8' # <--- GOODONE #'62.219.128.128'
#         list_domain_names = ['wikipedia.org', 'china.org.cn', 'fdgdhghfhfghfjfdhdh.com', 'cnbc.com', 'lexico.com',
#                       'tr-ex.me', 'tvtropes.org', 'tandfonline.com', 'amazon.in', 'archive.org', 'amitdvir.com',
#                       'nihonsport.com', 'aeon-ryukyu.jp', '4stringsjp.com']
#
#         # with open('list_of_domain_names.txt', 'w') as f:
#         #     f.write('\n'.join(list_names))
#         # main(DNS_address, list_domain_names, repeats=4, interval_wait_sec=10, is_first_rec=True, to_show_results=False)
#         laps = 5
#         for i in range(laps):
#             main(DNS_address, list_domain_names, repeats=6, interval_wait_sec=10, is_first_rec=True, to_show_results=False)
#             if i < laps - 1:
#                 wait_bar(10)
#
#         #get_app_by_time(DNS_address, list_domain_names)
#     except KeyboardInterrupt:
#         print('Interrupted')
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)