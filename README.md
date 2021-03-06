## Openwhisk 
---
####1. Installation

	git clone --depth=1 https://github.com/openwhisk/openwhisk.git

	cd openwhisk/tools/vagrant

	./hello

	cd ../../

	./gradlew distDocker

	cd ansible
	
	ansible-playbook -i environments/local couchdb.yml
	
	ansible-playbook -i environments/local initdb.yml
	
	ansible-playbook -i environments/local wipe.yml
	
	ansible-playbook -i environments/local apigateway.yml
	
	ansible-playbook -i environments/local openwhisk.yml
	
	ansible-playbook -i environments/local postdeploy.yml


- API host (name or IP address) for the OpenWhisk deployment you want to use.

	./bin/wsk property set --apihost 172.17.0.1


- Authorization key (username and password) which grants you access to the OpenWhisk API.
The API host can be acquired from the edge.host property in whisk.properties file, which is generated during deployment of OpenWhisk. Run the following command from your openwhisk directory to set the API host:

	./bin/wsk property set --auth `cat ansible/files/auth.guest`


#### 2. Use

	

	./bin/wsk -i action create hello hello.js

	./bin/wsk -i list

	./bin/wsk -i action invoke --blocking hello


- Openwhisk API list : https://github.com/openwhisk/openwhisk/blob/master/docs/rest_api.md

- GUI 에서 이것들을 사용하게 될 계획임


#### 3. CLI Usage

(1) Packages 관련 CLI 정리
	
	wsk package list /whisk.system

	wsk package get --summary /whisk.system/cloudant

	wsk action get --summary /whisk.system/cloudant/read



(2) actions sequence 만들기

	wsk action create sequenceAction --sequence /whisk.system/utils/split,/whisk.system/utils/sort


(3) action invoke 시, json 파라미터로 넘기기 

	$ wsk action invoke --blocking --result hello --param-file parameters.json
 

(4) Rule 만들기 (trigger + action)
	
	$ wsk trigger update locationUpdate

	$ wsk action update hello hello.js

	$ wsk rule create myRule locationUpdate hello

	$ wsk trigger fire locationUpdate --param name Donald --param place "Washington, D.C."

	$ wsk rule create recordLocation locationUpdate /whisk.system/utils/echo

	$ wsk action create recordLocationAndHello --sequence /whisk.system/utils/echo,hello

	$ wsk rule create anotherRule locationUpdate recordLocationAndHello
	
	$ wsk activation list --limit 1 hello
	
	$ wsk activation result 9c98a083b924426d8b26b5f41c5ebc0d{Activation_id}
	

#### 4. REST Usage

(1) Rest API 로 trigger Call 하기

- **참조** https://github.com/openwhisk/openwhisk/blob/master/docs/rest_api.md

Fire the trigger event 

- curl -u $AUTH https://openwhisk.ng.bluemix.net/api/v1/namespaces/_/triggers/$EVENT_NAME -X POST -H "Content-Type: application/json" -d '{"temperature":60}' 
	

		curl -u $AUTH https://openwhisk.ng.bluemix.net/api/v1/namespaces/_/triggers/events -X POST -H "Content-Type: application/json" -d '{"temperature":60}'
		
		curl https://172.17.0.1/api/v1/namespaces/_/triggers/kulcloud_hello -X POST -H "Content-Type: application/json" -d '{"name":"kong", "place":"seoul"}' 
		

- 오늘할 것 : 간단한 Rule 만들고, REST API 로 Trigger 할 것

(2) 인증 정보 추출 하기

	./bin/wsk -i property get --auth

	output : 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP

	23bc46b1-71f6-4ed5-8c54-816aa4f8c502 ==> USERNAME

	123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP ==> PASSWORD

	export USERNAME=23bc46b1-71f6-4ed5-8c54-816aa4f8c502

	export PASSWORD=123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP


(3) X.509 인증 bypass 시키기

	curl -u $USERNAME:$PASSWORD http://172.17.0.1:10001/api/v1/namespaces/whisk.system/packages

(4) 예제

REST API REQUEST

	curl -u $USERNAME:$PASSWORD http://172.17.0.1:10001/api/v1/namespaces/_/triggers/kulcloud_hello -X POST -H "Content-Type: application/json" -d '{"name":"kong", "place":"seoul"}'
	
RESPONSE

	{ "activationId": "1805a0ef4dcd469db42c22aca095a09f" }

RESULT CHECK

	./bin/wsk -i activation result 1805a0ef4dcd469db42c22aca095a09f
	
	{    "name": "kong",    "place": "seoul"    }
	

#### 5. 3rd-pary : NodeJS 모듈 연동

#### (1) Install first all dependencies locally

	npm install
	
#### (2) Create a .zip archive containing all files (including all dependencies):

	$ zip -r action.zip *

#### (3) Create the action

	$ wsk action create packageAction --kind nodejs:6 action.zip

#### (4) You can invoke the action like any other

	$ wsk action invoke --result packageAction --param lines "[\"and now\", \"for something completely\", \"different\" ]"


#### 6. 3rd-party : Python 모듈 연동

#### (1) __main__.py

	import sys
	from slackclient import SlackClient

	def slack(params):     	
		slack_token = params['token']
    		sc = SlackClient(slack_token)
    		sc.api_call(
	    		"chat.postMessage",	    
	    		channel=params['channel'],	    
	    		text=params['message']
    		)
    		return {"message": params['message']}


#### (2) requirements.txt

	slackclient
	pyOpenSSL 
	ndg-httpsclient 
	pyasn1
    

#### (4) Docker 기반 build

	docker run --rm -v "$PWD:/tmp" openwhisk/python2action sh -c "cd tmp; virtualenv virtualenv; source virtualenv/bin/activate; pip install -r requirements.txt;"


#### (5) Docker 기반 Packaging

	zip -r slack.zip virtualenv __main__.py 

#### (6) Action 생성

	wsk action create slack --kind python:2 --main slack slack.zip	

	wsk action invoke slack --blocking --result --param token "xoxb-172489925216-UdxsbjxZzade8dePFQIdbTLB" --param channel "#alert" --param message "ddos attack detection"

#### 7. NaaCS Test 시험 검증 스크립트

	import sys
	wsk -i action create DdosAttackActionList --sequence naacsmail,naacsslack

	wsk -i rule create DdosAttackRule DdosAttackDetection DdosAttackActionList

	wsk -i rule create SwitchErrorRule SwitchErrorDetection naacsmail

	wsk -i trigger fire DdosAttackDetection --param user_mail " kongseokhwan@gmail.com" --param message "ddos attack detection" --param token "xoxb-172489925216-BNFydvGBHzqkzMsDfrGgvwiJ" --param channel "#alert"

	wsk -i trigger fire SwitchErrorDetection --param user_mail " kongseokhwan@gmail.com" --param message "ddos attack detection" --param token "xoxb-172489925216-BNFydvGBHzqkzMsDfrGgvwiJ" --param channel "#alert"

#### FAQs

(1) X.509 인증 문제 in CLI

Problems

	error: Unable to invoke action 'hello': Post https://172.17.0.1/api/v1/namespaces/_/actions/hello?blocking=true&result=true: x509: cannot validate certificate for 172.17.0.1 because it doesn't contain any IP SANs
	
Solution

	./bin/wsk -i action invoke --result hello --param-file parameters.json
	
	-i 옵션을 주어서 인증을 바이패스 시킬 수 있음
	
(2) X.509 인증 문제 in REST API

http://172.17.0.1:10001 의 HTTP API Host 사용 가능

	curl -u $USERNAME:$PASSWORD http://172.17.0.1:10001/api/v1/namespaces/whisk.system/paages



(3) Action 사용시 3rd Party Libraray dependency 는 어떻게 해결

- $OPENWHISK_HOME/core 폴더에 해당 라이브러리들이 있는 것으로 판단됨

- Packaging an action as a Node.js module

Package.json

	{
 		
 		"name": "my-action",
 		
		"main": "index.js",

		"dependencies" : {
		
		    "left-pad" : "1.1.3"
  		
  		}
	
	}
	
 - **중요** 하지만 packaging 이 동작이 잘 안됨. 한번은 되는 듯 하나 구후로 제대로 되지를 않음. shell command 로 프로세스를 콜하는 것을 생각할 필요 있음.
 
 





























