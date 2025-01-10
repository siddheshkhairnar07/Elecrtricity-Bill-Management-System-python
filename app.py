from flask import Flask, request, jsonify
from models import create_tables, add_customer, get_customer_by_id, save_bill, get_bills_for_customer
from utilities import extract_text_from_image, extract_meter_reading, calculate_bill, get_today_date

app = Flask(__name__)

# Initialize database
create_tables()

@app.route('/register_customer', methods=['POST'])
def register_customer():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    previous_reading = data.get('previous_reading')

    if not name or not address or previous_reading is None:
        return jsonify({"error": "All fields are required!"}), 400
    
    add_customer(name, address, previous_reading)
    return jsonify({"message": "Customer registered successfully!"}), 201


@app.route('/calculate_bill', methods=['POST'])
def calculate_bill_for_customer():
    data = request.get_json()
    customer_id = data.get('customer_id')
    image_path = data.get('image_path')  # Path to the image file

    if not customer_id or not image_path:
        return jsonify({"error": "customer_id and image_path are required!"}), 400

    customer = get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"error": "Customer not found!"}), 404

    extracted_text = extract_text_from_image(image_path)
    current_reading = extract_meter_reading(extracted_text)

    if current_reading is None:
        return jsonify({"error": "Unable to extract meter reading from the image!"}), 400
    
    previous_reading = customer[3]  # Get previous reading from the customer record

    try:
        bill_amount = calculate_bill(previous_reading, current_reading)
        save_bill(customer_id, bill_amount, get_today_date())
        return jsonify({"bill_amount": bill_amount}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route('/get_bills/<int:customer_id>', methods=['GET'])
def get_bills(customer_id):
    bills = get_bills_for_customer(customer_id)
    if not bills:
        return jsonify({"message": "No bills found for this customer."}), 404
    
    bill_history = []
    for bill in bills:
        bill_history.append({
            "bill_amount": bill[1],
            "date": bill[2],
            "paid": bill[3]
        })

    return jsonify({"bill_history": bill_history}), 200


if __name__ == '__main__':
    app.run(debug=True)
