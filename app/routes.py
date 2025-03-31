from flask import request, jsonify
from app import app, db
from app.models import Medicine
from datetime import datetime
from app.utils.validation import validate_medicine_data

from flask import Response
import json
from flask import render_template, request, redirect, url_for

@app.route('/ui/medicines')
def list_medicines_ui():
    medicines = Medicine.query.all()
    return render_template('list_medicines.html', medicines=medicines)

@app.route('/ui/add', methods=['GET', 'POST'])
def add_medicine_ui():
    if request.method == 'POST':
        name = request.form.get('name')
        quantity = request.form.get('quantity')
        expiration_date = request.form.get('expiration_date')
        description = request.form.get('description')

        new_med = Medicine(
            name=name,
            quantity=int(quantity),
            expiration_date=datetime.strptime(expiration_date, '%Y-%m-%d'),
            description=description
        )
        db.session.add(new_med)
        db.session.commit()

        return redirect(url_for('list_medicines_ui'))

    return render_template('add_medicine.html')

# 📌 1. Отримати всі ліки
@app.route('/medicines', methods=['GET'])
def get_medicines():
    medicines = Medicine.query.all()
    result = [
        {
            "id": med.id,
            "name": med.name,
            "expiration_date": med.expiration_date.strftime('%Y-%m-%d'),
            "quantity": med.quantity,
            "description": med.description
        }
        for med in medicines
    ]
    response_json = json.dumps(result, ensure_ascii=False)
    return Response(response=response_json, status=200, mimetype='application/json; charset=utf-8')

# 📌 2. Отримати конкретний лікарський засіб за ID
@app.route('/medicines/<int:medicine_id>', methods=['GET'])
def get_medicine(medicine_id):
    medicine = db.session.get(Medicine, medicine_id)
    if medicine is None:
        return Response(
            response=json.dumps({"error": "Ліки не знайдено"}, ensure_ascii=False),
            status=404,
            mimetype='application/json; charset=utf-8'
        )

    result = {
        "id": medicine.id,
        "name": medicine.name,
        "expiration_date": medicine.expiration_date.strftime('%Y-%m-%d'),
        "quantity": medicine.quantity,
        "description": medicine.description
    }
    response_json = json.dumps(result, ensure_ascii=False)
    return Response(response=response_json, status=200, mimetype='application/json; charset=utf-8')

# 📌 3. Додати новий лікарський засіб
@app.route('/medicines', methods=['POST'])
def add_medicine():
    data = request.json
    errors = validate_medicine_data(data, for_update=False)
    if errors:
        return jsonify({"errors": errors}), 400

    new_medicine = Medicine(
        name=data['name'],
        expiration_date=datetime.strptime(data['expiration_date'], '%Y-%m-%d'),
        quantity=int(data['quantity']),
        description=data.get('description', '')
    )
    db.session.add(new_medicine)
    db.session.commit()

    return jsonify({"message": "Препарат успішно додано", "id": new_medicine.id}), 201

# 📌 4. Оновити лікарський засіб
@app.route('/medicines/<int:medicine_id>', methods=['PUT'])
def update_medicine(medicine_id):
    medicine = db.session.get(Medicine, medicine_id)
    if medicine is None:
        return jsonify({"error": "Ліки не знайдено"}), 404

    data = request.json
    errors = validate_medicine_data(data, for_update=True)
    if errors:
        return jsonify({"errors": errors}), 400

    if 'name' in data:
        medicine.name = data['name']
    if 'quantity' in data:
        medicine.quantity = int(data['quantity'])
    if 'expiration_date' in data:
        medicine.expiration_date = datetime.strptime(data['expiration_date'], '%Y-%m-%d')
    if 'description' in data:
        medicine.description = data['description']

    db.session.commit()
    return jsonify({"message": "Ліки успішно оновлено"}), 200
        

# 📌 5. Видалити лікарський засіб
@app.route('/medicines/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(medicine_id):
    medicine = db.session.get(Medicine, medicine_id)
    if medicine is None:
        return jsonify({"error": "Ліки не знайдено"}), 404

    db.session.delete(medicine)
    db.session.commit()

    return jsonify({"message": "Ліки видалено успішно"}), 200

from datetime import datetime, timedelta

# 📌 6. Отримати нагадування
@app.route('/medicines/alerts', methods=['GET'])
def get_medicine_alerts():
    today = datetime.today().date()
    near_expiry_date = today + timedelta(days=7)

    expiring = Medicine.query.filter(
        Medicine.expiration_date <= near_expiry_date,
        Medicine.expiration_date >= today
    ).all()

    low_quantity = Medicine.query.filter(
        Medicine.quantity <= 3
    ).all()

    result = {
        "expiring_soon": [
            {
                "id": m.id,
                "name": m.name,
                "expiration_date": m.expiration_date.strftime('%Y-%m-%d')
            }
            for m in expiring
        ],
        "low_quantity": [
            {
                "id": m.id,
                "name": m.name,
                "quantity": m.quantity
            }
            for m in low_quantity
        ]
    }

    return jsonify(result)