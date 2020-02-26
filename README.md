# NumbersCheckingServer

Пример запроса:
curl -H "Content-Type: application/json" -X POST http://node-13.hse/alexander/task --data '{"query":"123456"}'

Возможные ответы:
{"response":"123457"}
{"error":"Number has already been received"}

В output пишет "дата+время: <число> Number has already been received"
