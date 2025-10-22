# Mock CRM Application

A lightweight Flask-based mock CRM system with customer data management and certificate tracking capabilities.

## Features

- Customer data management (name, email, mobile, address, member number)
- Certificate data tracking (upload status, type, issuer, expiry date)
- RESTful API for integration with external applications
- Pre-populated with sample customer data

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the mock CRM server:

```bash
python mock_crm_app.py
```

The API will be available at `http://localhost:5000`

## API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Get All Customers
```
GET /api/customers
```

**Response:**
```json
{
  "success": true,
  "count": 5,
  "customers": [
    {
      "member_number": "MEM001",
      "name": "John Smith",
      "email": "john.smith@example.com",
      "mobile": "+1-555-0101",
      "address": "123 Main St, Springfield, IL 62701",
      "date_joined": "2023-01-15",
      "certificate_uploaded": false,
      "certificate_name": null,
      "certificate_upload_date": null,
      "certificate_expiry_date": null,
      "certificate_type": null,
      "certificate_issuer": null,
      "certificate_status": "pending"
    }
  ]
}
```

#### 2. Get Customer by Member Number
```
GET /api/customers/<member_number>
```

**Example:**
```
GET /api/customers/MEM001
```

**Response:**
```json
{
  "success": true,
  "customer": {
    "member_number": "MEM001",
    "name": "John Smith",
    ...
  }
}
```

#### 3. Update Certificate Data (PRIMARY ENDPOINT)
```
PUT /api/customers/<member_number>/certificate
```

**Request Body:**
```json
{
  "certificate_name": "insurance_cert_2024.pdf",
  "certificate_type": "Professional Indemnity Insurance",
  "certificate_issuer": "ABC Insurance Company",
  "certificate_expiry_date": "2025-10-22T00:00:00",
  "certificate_status": "verified"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Certificate data updated for member MEM001",
  "customer": {
    "member_number": "MEM001",
    "name": "John Smith",
    "certificate_uploaded": true,
    "certificate_name": "insurance_cert_2024.pdf",
    "certificate_type": "Professional Indemnity Insurance",
    ...
  }
}
```

#### 4. Add New Customer
```
POST /api/customers
```

**Request Body:**
```json
{
  "member_number": "MEM999",
  "name": "New Customer",
  "email": "new@example.com",
  "mobile": "+1-555-9999",
  "address": "123 Street, City, State 12345"
}
```

## Integration with Your Workflow Application

### Python Example

```python
import requests
from datetime import datetime

def update_crm_certificate(member_number, certificate_info):
    """
    Call this function from your workflow app after certificate upload
    """
    url = f"http://localhost:5000/api/customers/{member_number}/certificate"
    
    data = {
        "certificate_name": certificate_info['filename'],
        "certificate_type": certificate_info['type'],
        "certificate_issuer": certificate_info['issuer'],
        "certificate_expiry_date": certificate_info['expiry_date'],
        "certificate_status": "verified"
    }
    
    response = requests.put(url, json=data)
    return response.json()

# Usage in your workflow app
result = update_crm_certificate("MEM001", {
    'filename': 'cert.pdf',
    'type': 'Insurance',
    'issuer': 'ABC Corp',
    'expiry_date': '2025-12-31T00:00:00'
})

if result['success']:
    print("CRM updated successfully!")
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');

async function updateCRMCertificate(memberNumber, certificateInfo) {
    const url = `http://localhost:5000/api/customers/${memberNumber}/certificate`;
    
    const data = {
        certificate_name: certificateInfo.filename,
        certificate_type: certificateInfo.type,
        certificate_issuer: certificateInfo.issuer,
        certificate_expiry_date: certificateInfo.expiryDate,
        certificate_status: 'verified'
    };
    
    try {
        const response = await axios.put(url, data);
        return response.data;
    } catch (error) {
        console.error('Failed to update CRM:', error);
        throw error;
    }
}

// Usage
updateCRMCertificate('MEM001', {
    filename: 'cert.pdf',
    type: 'Insurance',
    issuer: 'ABC Corp',
    expiryDate: '2025-12-31T00:00:00'
}).then(result => {
    console.log('CRM updated:', result);
});
```

### cURL Example

```bash
curl -X PUT http://localhost:5000/api/customers/MEM001/certificate \
  -H "Content-Type: application/json" \
  -d '{
    "certificate_name": "insurance_cert.pdf",
    "certificate_type": "Professional Indemnity",
    "certificate_issuer": "ABC Insurance",
    "certificate_expiry_date": "2025-12-31T00:00:00",
    "certificate_status": "verified"
  }'
```

## Sample Customer Data

The application comes with 5 pre-populated customers:

| Member Number | Name | Email |
|---------------|------|-------|
| MEM001 | John Smith | john.smith@example.com |
| MEM002 | Sarah Johnson | sarah.j@example.com |
| MEM003 | Michael Chen | m.chen@example.com |
| MEM004 | Emily Davis | emily.davis@example.com |
| MEM005 | David Wilson | d.wilson@example.com |

## Certificate Fields

Each customer record includes the following certificate-related fields:

- `certificate_uploaded` (boolean): Whether a certificate has been uploaded
- `certificate_name` (string): Filename of the uploaded certificate
- `certificate_upload_date` (ISO datetime): When the certificate was uploaded
- `certificate_expiry_date` (ISO datetime): When the certificate expires
- `certificate_type` (string): Type/category of certificate
- `certificate_issuer` (string): Organization that issued the certificate
- `certificate_status` (string): Status (pending, verified, expired)

## Testing

Run the example client:

```bash
python api_client_example.py
```

This will demonstrate all API operations including:
1. Retrieving all customers
2. Getting a specific customer
3. Updating certificate data
4. Adding a new customer

## Error Handling

### Customer Not Found (404)
```json
{
  "success": false,
  "error": "Customer not found"
}
```

### Customer Already Exists (409)
```json
{
  "success": false,
  "error": "Customer with this member number already exists"
}
```

### Missing Required Field (400)
```json
{
  "success": false,
  "error": "member_number is required"
}
```

## CORS Support

The API includes CORS support, allowing requests from any origin. This is suitable for development but should be configured appropriately for production use.

## Notes

- This is a mock application for development/testing purposes
- Data is stored in memory and will be lost when the application restarts
- For production use, implement proper database storage
- Add authentication and authorization as needed
- Implement proper error logging and monitoring
