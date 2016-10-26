#!/usr/bin/python

from requests import session
from bs4 import BeautifulSoup as BS
import os.path
import re
############# DATA TO CHANGE ##############
# DNS Cloud login data
LOGIN_DATA = {
    'action': 'login',
    'username': '<METANET-USERNAME>',
    'password': '<METANET-PASSWORD>'
}
#NEW_IP='2.10.10.10'
ZONE_NAME='bbb.com' # DNS zone, which contains subdomain record to be updated
SUBDOMAIN='dyn-ip.bbb.com' # Subdomain record to update the ip address for

########## END DATA TO CHANGE ############

SUB_SHORT=SUBDOMAIN[0:SUBDOMAIN.find(ZONE_NAME)-1]
DOMAIN_ID_REGEX='.*domain_id=([0-9]+).+rr_id=([0-9]+).*(vpn\.domain\.com).*'
SUBDOMAIN_ID_REGEX='.*<a\shref=content\.php\?screen=zone\/zone_edit&domain_id=([0-9]+)&.?rr_id=([0-9]+).*Click\sto\sdisabled\sit\..+(vpn\.digisec\.ch)\.<\/td>'

LOGIN_URL='https://dns.sui-inter.net/login_up.php'
LIST_ZONES='https://dns.sui-inter.net/content.php'
VIEW_DOMAIN='https://dns.sui-inter.net/content.php?screen=zone/zone_edit&domain_id='

zone_data=dict()


def findZoneID(response):
    if response != '': 
        # search for doamin_id only
        soup=BS(response.text,'html.parser')
        elements_tr=soup.find('form',{'id':'dns_form'}).findAll('tr',{'class':'Row'})
        for i in elements_tr:
            if ZONE_NAME in str(i):
                domain_id=re.findall(r'.*domain_id=([0-9]+).*Manage\sDNS\szone">'+ZONE_NAME+'\.</a>.*',str(i))
#                print(domain_id)
        zone_data['domain_id']=''.join(domain_id)

def findSubdomainID(domain_id,response):
    if response != '': 
        # search for doamin_id only
        soup=BS(response.text,'html.parser')
        elements_tr=soup.find('form',{'id':'dns_records_form'}).find('table',{'id':'dns_records_table'}).findAll('tr',{'class':'Row'})

        for i in elements_tr:
            if SUBDOMAIN in str(i):
                subdomain_id=re.findall(r'.*domain_id=[0-9]+.+rr_id=([0-9]+).*'+SUBDOMAIN+'.*',str(i))
#                print(subdomain_id)
        zone_data['subdomain_id']=''.join(subdomain_id)

def update_dns_entry(domain_id,subdomain_id,ip):
    UPDATE_DNS_RECORD='https://dns.sui-inter.net/content.php?screen=zone/zone_record_edit&id='+subdomain_id+'&dns_record_type=A&domain_id='+domain_id
    new_entry = {'dns_template_record_form_cmd' : '1', 'dns_entry_type' : 'A', 'prev_record_type' : 'A', 'host_hidden' : SUB_SHORT, 'base_value' : ip, 'opt' : '', 'last_mask' : '0', 'id' : subdomain_id, 'status' : '1', 'host' : SUB_SHORT, 'entry_value' : ip
}
#    print(UPDATE_DNS_RECORD)
#    print(new_entry)
    with session() as c:
        c.post(LOGIN_URL, data=LOGIN_DATA)
        c.post(UPDATE_DNS_RECORD,new_entry)
    #    response = c.get(VIEW_DOMAIN)
    #    response = c.get(LIST_ZONES)
    #    print(response.headers)
        #print(response.text)
    #    rex=re.findall(DOMAIN_ID_REGEX, response.text)

def main():
    with session() as c:
        CURRENT_IP=c.get('http://icanhazip.com').text.strip('\n')
        c.post(LOGIN_URL, data=LOGIN_DATA)
        response = c.get(LIST_ZONES)
        findZoneID(response)
        response = c.get(VIEW_DOMAIN+zone_data.get('domain_id'))
        findSubdomainID(zone_data.get('domain_id'),response)
        mode = 'r' if os.path.exists('lastip.txt') else 'w'
#        print(zone_data)
        with open('lastip.txt',mode) as fip:
            if mode == 'r' and CURRENT_IP not in fip.read():
#                update_dns_entry(zone_data.get('domain_id'),zone_data.get('subdomain_id'),NEW_IP)
                update_dns_entry(zone_data.get('domain_id'),zone_data.get('subdomain_id'),CURRENT_IP)
                fip=open('lastip.txt',mode='w').write(CURRENT_IP)
            elif mode=='w':
#                update_dns_entry(zone_data.get('domain_id'),zone_data.get('subdomain_id'),NEW_IP)
                update_dns_entry(zone_data.get('domain_id'),zone_data.get('subdomain_id'),CURRENT_IP)
                fip=open('lastip.txt',mode).write(CURRENT_IP)

if __name__=='__main__':
    main()
