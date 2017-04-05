# What is Kulcloud PRISM IPtables #

###### This documents how to use the kulcloud prims iptables application, which provides a compiling application from linux iptable's rules to openflow switch. Through this, user just install thia application on prism router and integrate with man iptables based application as like openstack neutron's firewall agent.


# Installation
###### Install git, iptables and pip tools. open a shell prompt and enter:

	$ git clone https://github.com/kongseokhwan/kulcloud-prism-iptable-agent.git
	$ cd kulcloud-prism-ipdup-agent
	$ sudo pip install -r requirement.txt

# Usage
###### Usage Run the application with the following command:
	$ sudo python prism_ipdup_agent.py 
	
* Mongo DB Database : iptable_database
* Mongo DB Collector : iptable_database