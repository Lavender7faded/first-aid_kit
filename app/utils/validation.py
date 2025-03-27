from datetime import datetime

def validate_medicine_data(data, for_update=False):
    errors = []

    required = ['name', 'expiration_date', 'quantity']
    if not for_update:
        for field in required:
            if field not in data:
                errors.append(f"Поле '{field}' обов’язкове")

    name = data.get('name')
    if name is not None:
        if not isinstance(name, str) or not name.strip():
            errors.append("Ім’я препарату має бути текстом")
        try:
            float(name)
            errors.append("Назва не може бути числом")
        except ValueError:
            pass

    quantity = data.get('quantity')
    if quantity is not None:
        try:
            q = int(quantity)
            if q == 0:
                errors.append("Кількість не може бути нульовою")
            elif q < 0:
                errors.append("Кількість не може бути від’ємною")
        except ValueError:
            errors.append("Кількість має бути числом")

    expiration = data.get('expiration_date')
    if expiration is not None:
        try:
            datetime.strptime(expiration, '%Y-%m-%d')
        except ValueError:
            errors.append("Невірний формат дати (очікується YYYY-MM-DD)")

    if 'description' in data and not isinstance(data['description'], str):
        errors.append("Опис має бути текстом")

    return errors
