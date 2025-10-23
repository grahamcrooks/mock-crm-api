from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# Mock customer database with Policy and Lifetime Health Cover fields
customers_db = {
    "45222608": {
        "member_number": "45222608",
        # Policy Section - Static data
        "first_name": "Toshiko",
        "middle_initial": "M",
        "last_name": "Kallik",
        "name": "Toshiko M Kallik",
        "sex": "M",
        "date_of_birth": "07/07/1949",
        "date_joined": "11/03/2022",
        "date_end": "01/05/2025",
        "email": "toshiko.kallik@example.com",
        "mobile": "",
        "address": "",
        # Lifetime Health Cover Section - Updated via API
        "lhc_person": None,
        "lhc_cae": None,
        "lhc_total_absent_days": None,
        "lhc_hospital_end_date": None,
        "lhc_paid_hospital_days": None,
        "lhc_updated": False,
        "lhc_update_date": None
    },
    "MEM001": {
        "member_number": "MEM001",
        "first_name": "John",
        "middle_initial": "",
        "last_name": "Smith",
        "name": "John Smith",
        "sex": "M",
        "date_of_birth": "01/15/1980",
        "date_joined": "01/01/2023",
        "date_end": "12/31/2024",
        "email": "john.smith@example.com",
        "mobile": "+1-555-0101",
        "address": "123 Main St, Springfield, IL 62701",
        "lhc_person": None,
        "lhc_cae": None,
        "lhc_total_absent_days": None,
        "lhc_hospital_end_date": None,
        "lhc_paid_hospital_days": None,
        "lhc_updated": False,
        "lhc_update_date": None
    },
    "MEM002": {
        "member_number": "MEM002",
        "first_name": "Sarah",
        "middle_initial": "",
        "last_name": "Johnson",
        "name": "Sarah Johnson",
        "sex": "F",
        "date_of_birth": "03/22/1985",
        "date_joined": "03/01/2023",
        "date_end": "02/28/2025",
        "email": "sarah.j@example.com",
        "mobile": "+1-555-0102",
        "address": "456 Oak Avenue, Chicago, IL 60601",
        "lhc_person": None,
        "lhc_cae": None,
        "lhc_total_absent_days": None,
        "lhc_hospital_end_date": None,
        "lhc_paid_hospital_days": None,
        "lhc_updated": False,
        "lhc_update_date": None
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

@app.route('/api/customers/<member_number>/lifetime-health-cover', methods=['PUT'])
def update_lifetime_health_cover(member_number):
    """Update Lifetime Health Cover data for a customer"""
    customer = customers_db.get(member_number)
    
    if not customer:
        return jsonify({
            "success": False,
            "error": "Customer not found"
        }), 404
    
    data = request.json
    
    # Update Lifetime Health Cover fields
    customer['lhc_updated'] = True
    customer['lhc_update_date'] = datetime.now().isoformat()
    
    # Update provided fields
    if 'person' in data:
        customer['lhc_person'] = data['person']
    if 'cae' in data:
        customer['lhc_cae'] = data['cae']
    if 'total_absent_days' in data:
        customer['lhc_total_absent_days'] = data['total_absent_days']
    if 'hospital_end_date' in data:
        customer['lhc_hospital_end_date'] = data['hospital_end_date']
    if 'paid_hospital_days' in data:
        customer['lhc_paid_hospital_days'] = data['paid_hospital_days']
    
    return jsonify({
        "success": True,
        "message": f"Lifetime Health Cover data updated for member {member_number}",
        "customer": customer
    })

@app.route('/api/customers/<member_number>/lifetime-health-cover', methods=['DELETE'])
def clear_lifetime_health_cover(member_number):
    """Clear Lifetime Health Cover data for a customer (for testing)"""
    customer = customers_db.get(member_number)
    
    if not customer:
        return jsonify({
            "success": False,
            "error": "Customer not found"
        }), 404
    
    # Clear all LHC fields
    customer['lhc_person'] = None
    customer['lhc_cae'] = None
    customer['lhc_total_absent_days'] = None
    customer['lhc_hospital_end_date'] = None
    customer['lhc_paid_hospital_days'] = None
    customer['lhc_updated'] = False
    customer['lhc_update_date'] = None
    
    return jsonify({
        "success": True,
        "message": f"Lifetime Health Cover data cleared for member {member_number}",
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
    
    # Create new customer with default LHC fields
    first_name = data.get('first_name', '')
    middle_initial = data.get('middle_initial', '')
    last_name = data.get('last_name', '')
    full_name = data.get('name', f"{first_name} {middle_initial} {last_name}".strip())
    
    new_customer = {
        "member_number": member_number,
        "first_name": first_name,
        "middle_initial": middle_initial,
        "last_name": last_name,
        "name": full_name,
        "sex": data.get('sex', ''),
        "date_of_birth": data.get('date_of_birth', ''),
        "date_joined": data.get('date_joined', ''),
        "date_end": data.get('date_end', ''),
        "email": data.get('email', ''),
        "mobile": data.get('mobile', ''),
        "address": data.get('address', ''),
        "lhc_person": None,
        "lhc_cae": None,
        "lhc_total_absent_days": None,
        "lhc_hospital_end_date": None,
        "lhc_paid_hospital_days": None,
        "lhc_updated": False,
        "lhc_update_date": None
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
