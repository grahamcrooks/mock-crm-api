from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Mock customer database with certificate fields
customers_db = {
    "MEM001": {
        "member_number": "MEM001",
        "name": "John Smith",
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
        "name": "Sarah Johnson",
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
    },
    "MEM003": {
        "member_number": "MEM003",
        "name": "Michael Chen",
        "email": "m.chen@example.com",
        "mobile": "+1-555-0103",
        "address": "789 Pine Road, Boston, MA 02101",
        "date_joined": "2023-05-10",
        "certificate_uploaded": False,
        "certificate_name": None,
        "certificate_upload_date": None,
        "certificate_expiry_date": None,
        "certificate_type": None,
        "certificate_issuer": None,
        "certificate_status": "pending"
    },
    "MEM004": {
        "member_number": "MEM004",
        "name": "Emily Davis",
        "email": "emily.davis@example.com",
        "mobile": "+1-555-0104",
        "address": "321 Elm Street, Austin, TX 78701",
        "date_joined": "2023-07-18",
        "certificate_uploaded": False,
        "certificate_name": None,
        "certificate_upload_date": None,
        "certificate_expiry_date": None,
        "certificate_type": None,
        "certificate_issuer": None,
        "certificate_status": "pending"
    },
    "MEM005": {
        "member_number": "MEM005",
        "name": "David Wilson",
        "email": "d.wilson@example.com",
        "mobile": "+1-555-0105",
        "address": "654 Maple Drive, Seattle, WA 98101",
        "date_joined": "2023-09-05",
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
    new_customer = {
        "member_number": member_number,
        "name": data.get('name', ''),
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
