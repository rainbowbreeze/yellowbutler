Test structure
- https://github.com/ageitgey/face_recognition/blob/master/tests/test_face_recognition.py


Flask example
- https://github.com/atlassian/localstack/blob/master/localstack/dashboard/api.py


* Test right now *
logs at https://www.pythonanywhere.com/user/rainbowbreeze/files/var/log/rainbowbreeze.pythonanywhere.com.server.log

curl -v -X POST https://rainbowbreeze.pythonanywhere.com/yellowbutler/api/v1.0/message --data '{"value":3}' --header "Content-Type:application/json"
reply
2017-05-01 21:28:49 ***************************
2017-05-01 21:28:49 Accept: */*#015#012X-Forwarded-For: 151.65.133.109#015#012X-Real-Ip: 151.65.133.109#015#012User-Agent: curl/7.47.0#015#012Host: rainbowbreeze.pythonanywhere.com#015#012Connection: close#015#012Content-Type: application/json#015#012Content-Length: 11#015#012#015
2017-05-01 21:28:49 
2017-05-01 21:28:49 ***************************
2017-05-01 21:28:49 <Request 'https://rainbowbreeze.pythonanywhere.com/yellowbutler/api/v1.0/message' [POST]>
2017-05-01 21:28:49 ***************************
2017-05-01 21:28:49 {'value': 3}
2017-05-01 21:28:49 ***************************

from api.ai
https://docs.api.ai/docs/webhook
2017-05-01 21:36:26 ***************************
2017-05-01 21:36:26 Accept: */*#015#012X-Forwarded-For: 54.224.155.160#015#012X-Real-Ip: 54.224.155.160#015#012X-Auth: AAAA#015#012User-Agent: Java/1.8.0_112#015#012Host: rainbowbreeze.pythonanywhere.com#015#012Pragma: no-cache#015#012Connection: close#015#012Test-Alf: alf-header-custom#015#012Content-Type: application/json; charset=UTF-8#015#012Cache-Control: no-cache#015#012Content-Length: 587#015#012#015
2017-05-01 21:36:26 
2017-05-01 21:36:26 ***************************
2017-05-01 21:36:26 <Request 'https://rainbowbreeze.pythonanywhere.com/yellowbutler/api/v1.0/message' [POST]>
2017-05-01 21:36:26 ***************************
2017-05-01 21:36:26 {'sessionId': '30f2b63e-8ae2-4aee-9ab1-164025cfa5c5', 'id': '1e90684b-c03e-42a8-a426-75812666422c', 'timestamp': '2017-05-01T21:36:26.227Z', 'status': {'errorType': 'success', 'code': 200}, 'result': {'actionIncomplete': False, 'fulfillment': {'messages': [{'speech': '', 'type': 0}], 'speech': ''}, 'score': 0.31, 'action': 'repeat.message', 'source': 'agent', 'metadata': {'intentName': 'TestYellowButler', 'webhookUsed': 'true', 'webhookForSlotFillingUsed': 'false', 'intentId': '087adca3-ce2a-48c1-9d7a-214539f2c1cc'}, 'parameters': {'echomessage': ''}, 'speech': '', 'resolvedQuery': 'Repeat Ciao', 'contexts': []}, 'lang': 'it'}
2017-05-01 21:36:26 ***************************

2017-05-01 21:48:45 ***************************
2017-05-01 21:48:45 Accept: */*#015#012X-Forwarded-For: 54.224.155.160#015#012X-Real-Ip: 54.224.155.160#015#012X-Auth: AAAA#015#012User-Agent: Java/1.8.0_112#015#012Host: rainbowbreeze.pythonanywhere.com#015#012Pragma: no-cache#015#012Connection: close#015#012Test-Alf: alf-header-custom#015#012Content-Type: application/json; charset=UTF-8#015#012Cache-Control: no-cache#015#012Content-Length: 643#015#012#015
2017-05-01 21:48:45 
2017-05-01 21:48:45 ***************************
2017-05-01 21:48:45 <Request 'https://rainbowbreeze.pythonanywhere.com/yellowbutler/api/v1.0/message' [POST]>
2017-05-01 21:48:45 ***************************
2017-05-01 21:48:45 {'sessionId': '30f2b63e-8ae2-4aee-9ab1-164025cfa5c5', 'id': '38ac43c4-a2d0-4dd1-b0af-a0da4f7b989f', 'timestamp': '2017-05-01T21:48:45.762Z', 'status': {'errorType': 'success', 'code': 200}, 'result': {'actionIncomplete': False, 'fulfillment': {'messages': [{'speech': 'Ecco il tuo messaggio: ciao', 'type': 0}], 'speech': 'Ecco il tuo messaggio: ciao'}, 'score': 1.0, 'action': 'repeat.message', 'source': 'agent', 'metadata': {'intentName': 'TestYellowButler', 'webhookUsed': 'true', 'webhookForSlotFillingUsed': 'false', 'intentId': '087adca3-ce2a-48c1-9d7a-214539f2c1cc'}, 'parameters': {'echomessage': 'ciao'}, 'speech': '', 'resolvedQuery': 'Dimmi ciao', 'contexts': []}, 'lang': 'it'}
2017-05-01 21:48:45 ***************************
