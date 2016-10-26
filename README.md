# dyndns-metanet
This script updates a DNS A record for subdomain.
To run it in a regular basis - create a cron job

What you need to get it working:
1. Account for DNS hosting: Metanet DNS Cloud (up to 5 zones free of charge)
	https://www.metanet.ch/email-domains/dns-hosting
2. Update the script with you login data
	LOGIN_DATA = {
	  'action': 'login',
	  'username': 'Your-METANET-USERNAME',
	  'password': 'Your-METANET-PASSWORD'
	}
3. Define zone name and subdomain the ip address has to be update for:
	ZONE_NAME='bbb.com' <-- zone name set up on DNS Cloud
	SUBDOMAIN='abc.bbb.com' <-- subdomain set up on DNS Cloud for which ip address will be updated
4. The script will create a local file in the same directory where this script resides: lastip.txt . It contains last ip address was used to update the record. If the ip address didn't change since last update, the dns record update won't be triggered.


