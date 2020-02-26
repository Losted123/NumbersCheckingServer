# NumbersCheckingServer

Пример запроса:<br/>
curl -H "Content-Type: application/json" -X POST http://node-13.hse/alexander/task --data '{"query":"123456"}'<br/>
<br/>
Возможные ответы:<br/>
{"response":"123457"}<br/>
{"error":"Number has already been received"}<br/>
<br/>
В output пишет "дата+время: <число> Number has already been received"<br/>
