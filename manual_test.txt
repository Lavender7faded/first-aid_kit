from datetime import date, timedelta
import requests

# ліки з кількістю 2
# data = {
#     "name": "Тестова низька кількість",
#     "expiration_date": "2025-12-31",
#     "quantity": 2,
#     "description": "Для перевірки alerts"
# }

# ліки з терміном через 5 днів
soon = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")

data={
    "name": "Тестова скоро закінчиться",
    "expiration_date": soon,
    "quantity": 10,
    "description": "Для перевірки alerts"
}

# data = {
#     "name": "Парацетамол",
#     "expiration_date": "2025-12-31",
#     "quantity": 10,
#     "description": "Обезболююче"
# }

response = requests.post("http://127.0.0.1:5000/medicines", json=data)

# response = requests.put("http://127.0.0.1:5000/medicines/2", json={
#     "name": "Ібупрофен",
#     "quantity": 20
# })

# response = requests.delete("http://127.0.0.1:5000/medicines/2")

# bad_data = {
#     "expiration_date": "2025-12-31",
#     "quantity": 10
# }

# bad_data = {
#     "name": "Щось",
#     "expiration_date": "31-12-2025",  # неправильний формат
#     "quantity": 10
# }

# response = requests.post("http://127.0.0.1:5000/medicines", json=bad_data)

# response = requests.put("http://127.0.0.1:5000/medicines/3", json={"quantity": "багато"})

# response = requests.put("http://127.0.0.1:5000/medicines/3", json={"quantity": "-2"})

# response = requests.put("http://127.0.0.1:5000/medicines/3", json={"name": "Парацетамол"})

# response = requests.put("http://127.0.0.1:5000/medicines/3", json={
#     "expiration_date": "01-11-2025"
# })

# response = requests.get("http://127.0.0.1:5000/medicines/alerts")

print(response.status_code)
print(response.json())

