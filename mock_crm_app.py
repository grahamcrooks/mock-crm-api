from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Mock customer database with certificate fields
customers_db = {
    "45222608": {
        "member_number": "45222608",
        "first_name": "TOSHIKO",
        "last_name": "GALLIK",
        "name": "TOSHIKO GALLIK",
        "sex": "M",
        "date_of_birth": "05/07/1949",
        "email": "toshiko.gallik@example.com",
        "mobile": "",
        "address": "",
        "date_joined": "2025-10-22",
        "certificate_uploaded": False,
        "certificate_name": None,
        "certificate_upload_date": None,
        "certificate_expiry_date": None,
        "certificate_type": None,
        "certificate_issuer": None,
        "certificate_status": "pending"
    },
    "MEM001": {
        "member_number": "MEM001",
        "first_name": "John",
        "last_name": "Smith",
        "name": "John Smith",
        "sex": "M",
        "date_of_birth": "01/15/1980",
        "email": "john.smith@example.com",
        "mobile": "+1-555-0101",
        "address": "123 Main St, Springfield, IL 62701",
        "date_joined": "2023-01-15",
        "certificate_uploaded": False,
        "certificate_name": None,
        "certificate_upload_date": None,
        "certificate_expiry_date": None,
        "certificate_type": None,
        "certificate_issuer": None,
        "certificate_status": "pending"
    },
    "MEM002": {
        "member_number": "MEM002",
        "first_name": "Sarah",
        "last_name": "Johnson",
        "name": "Sarah Johnson",
        "sex": "F",
        "date_of_birth": "03/22/1985",
        "email": "sarah.j@example.com",
        "mobile": "+1-555-0102",
        "address": "456 Oak Avenue, Chicago, IL 60601",
        "date_joined": "2023-03-22",
        "certificate_uploaded": False,
        "certificate_name": None,
        "certificate_upload_date": None,
        "certificate_expiry_date": None,
        "certificate_type": None,
        "certificate_issuer": None,
        "certificate_status": "pending"
    }
}

@app.route('/')
def home():
    return jsonify({
        "message": "Mock CRM API",
        "version": "1.0",
        "endpoints": {
            "GET /api/customers": "Get all customers",
            "GET /api/customers/<member_number>": "Get customer by member number",
            "PUT /api/customers/<member_number>/certificate": "Update certificate data for a customer",
            "POST /api/customers": "Add a new customer"
        }
    })

@app.route('/api/customers', methods=['GET'])
def get_all_customers():
    """Get all customers"""
    return jsonify({
        "success": True,
        "count": len(customers_db),
        "customers": list(customers_db.values())
    })

@app.route('/api/customers/<member_number>', methods=['GET'])
def get_customer(member_number):
    """Get a specific customer by member number"""
    customer = customers_db.get(member_number)
    
    if customer:
        return jsonify({
            "success": True,
            "customer": customer
        })
    else:
        return jsonify({
            "success": False,
            "error": "Customer not found"
        }), 404

@app.route('/api/customers/<member_number>/certificate', methods=['PUT'])
def update_certificate(member_number):
    """Update certificate data for a customer"""
    customer = customers_db.get(member_number)
    
    if not customer:
        return jsonify({
            "success": False,
            "error": "Customer not found"
        }), 404
    
    data = request.json
    
    # Update certificate fields
    customer['certificate_uploaded'] = True
    customer['certificate_upload_date'] = data.get('certificate_upload_date', datetime.now().isoformat())
    
    # Optional fields
    if 'certificate_name' in data:
        customer['certificate_name'] = data['certificate_name']
    if 'certificate_expiry_date' in data:
        customer['certificate_expiry_date'] = data['certificate_expiry_date']
    if 'certificate_type' in data:
        customer['certificate_type'] = data['certificate_type']
    if 'certificate_issuer' in data:
        customer['certificate_issuer'] = data['certificate_issuer']
    if 'certificate_status' in data:
        customer['certificate_status'] = data['certificate_status']
    else:
        customer['certificate_status'] = 'verified'
    
    return jsonify({
        "success": True,
        "message": f"Certificate data updated for member {member_number}",
        "customer": customer
    })

@app.route('/api/customers', methods=['POST'])
def add_customer():
    """Add a new customer"""
    data = request.json
    
    member_number = data.get('member_number')
    
    if not member_number:
        return jsonify({
            "success": False,
            "error": "member_number is required"
        }), 400
    
    if member_number in customers_db:
        return jsonify({
            "success": False,
            "error": "Customer with this member number already exists"
        }), 409
    
    # Create new customer with default certificate fields
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    full_name = data.get('name', f"{first_name} {last_name}".strip())
    
    new_customer = {
        "member_number": member_number,
        "first_name": first_name,
        "last_name": last_name,
        "name": full_name,
        "sex": data.get('sex', ''),
        "date_of_birth": data.get('date_of_birth', ''),
        "email": data.get('email', ''),
        "mobile": data.get('mobile', ''),
        "address": data.get('address', ''),
        "date_joined": data.get('date_joined', datetime.now().isoformat()),
        "certificate_uploaded": False,
        "certificate_name": None,
        "certificate_upload_date": None,
        "certificate_expiry_date": None,
        "certificate_type": None,
        "certificate_issuer": None,
        "certificate_status": "pending"
    }
    
    customers_db[member_number] = new_customer
    
    return jsonify({
        "success": True,
        "message": "Customer added successfully",
        "customer": new_customer
    }), 201

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "="*60)
    print("Mock CRM Application Starting...")
    print("="*60)
    print("\nAPI Endpoints:")
    print("  - GET    http://localhost:{}/api/customers".format(port))
    print("  - GET    http://localhost:{}/api/customers/<member_number>".format(port))
    print("  - PUT    http://localhost:{}/api/customers/<member_number>/certificate".format(port))
    print("  - POST   http://localhost:{}/api/customers".format(port))
    print("\n" + "="*60 + "\n")
    
    app.run(debug=False, host='0.0.0.0', port=port)
