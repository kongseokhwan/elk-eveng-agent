# What is Kulcloud PRISM IPtables #
---


###### This documents how to use the kulcloud prims iptables application, which provides a compiling application from linux iptable's rules to openflow switch. Through this, user just install thia application on prism router and integrate with man iptables based application as like openstack neutron's firewall agent.


# Installation
---

###### Install git, iptables and pip tools. open a shell prompt and enter:

	$ git clone https://github.com/kongseokhwan/kulcloud-prism-iptable-agent.git
	$ cd kulcloud-prism-ipdup-agent
	$ sudo pip install -r requirement.txt

# Usage
---
###### Usage Run the application with the following command:
	$ sudo python prism_ipdup_agent.py 
	
* Mongo DB Database : iptable_database
* Mongo DB Collector : iptable_database


# Components
---

- Trigger URLs

- Watcher

- Action

	- python 기반의 action packaing 방법이랑 함께 컴파일 되어야 함

	- ELK

		- IP Duplication 에 관련해서는 완료

		- TODO : 추후 필요 item 발굴 필요

	- MAIL : 완료

	- MUL (Switch 관련)

	- SNS(Slack) : 완료. 현재 openwhisk 랑 연동 완료 되어 있음


- Policy : combination of Trigger / Action


Trigger URLS
---


| 왼쪽 정렬 | 가운데 정렬 | 오른쪽 정렬 |

| :--- | :---: | ---: |

| 내용 11 | 내용 12 | 내용 13 |


| 내용 21 | 내용 22 | 내용 23 |



