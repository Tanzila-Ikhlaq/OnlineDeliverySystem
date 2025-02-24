# Online Delivery System - Backend

## 📌 Project Overview
This is a **FastAPI-based backend** for an **Online Delivery System**, enabling users to order products, track deliveries, and make secure payments. The system supports multiple user roles (**Admin, Vendor, Customer, Delivery Personnel**) with role-based access control.

## 🛠️ Tech Stack
- **Backend Framework:** FastAPI (Python)
- **Database:** MySQL (Using MySQL Connector)
- **Authentication:** JWT (JSON Web Tokens)
- **Payment Integration:** Stripe
- **Notifications:** FastAPI-Mail (Emails), Twilio (SMS)

## ✨ Features
✔ **User Authentication & Role Management** (Admin, Vendor, Customer, Delivery Personnel)  
✔ **Product Management** (CRUD operations for vendors)  
✔ **Order Management** (Customers can place orders, order status tracking)  
✔ **Payment Integration** (Stripe API for secure transactions)  
✔ **Delivery Management** (Assign delivery personnel, update status)  
✔ **Email & SMS Notifications** (Order confirmation, delivery updates)  
✔ **Secure API Endpoints** (Role-based access & JWT authentication)  

## 🚀 Installation & Setup
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Tanzila-Ikhlaq/OnlineDeliverySystem.git
```

### **2️⃣ Create & Activate a Virtual Environment**
```bash
python -m venv venv  # Create virtual environment
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file in the project root and add the necessary environment variables.  
These include **database credentials, API keys (Stripe, Twilio), and email settings**.

### **5️⃣ Run the FastAPI Server**
```bash
uvicorn main:app --reload
```
FastAPI will start at **http://127.0.0.1:8000** 🎉


## 📌 API Endpoints
### **1️⃣ Authentication**
| Method | Endpoint            | Description          |
|--------|--------------------|----------------------|
| POST   | `/auth/register`   | Register a new user |
| POST   | `/auth/login`      | Login & get JWT     |
| GET    | `/auth/me`         | Get user details    |

### **2️⃣ Product Management** (Vendor Only)
| Method | Endpoint             | Description                |
|--------|----------------------|----------------------------|
| POST   | `/products/add`      | Add a new product         |
| GET    | `/products/list`     | List all products         |
| PUT    | `/products/update/{product_id}` | Update a product |
| DELETE | `/products/delete/{product_id}` | Delete a product |

### **3️⃣ Order Management** (Customer Only)
| Method | Endpoint                  | Description            |
|--------|---------------------------|------------------------|
| POST   | `/orders/place_order`     | Place a new order      |
| GET    | `/orders/order/{order_id}` | Get order details     |
| PUT    | `/orders/update_status`   | Update order status   |

### **4️⃣ Payment Integration**
| Method | Endpoint                          | Description                     |
|--------|----------------------------------|---------------------------------|
| POST   | `/payments/create-checkout-session` | Create a Stripe Checkout session |
| GET    | `/payments/verify-payment/{session_id}` | Verify payment status |

### **5️⃣ Delivery Management**
| Method | Endpoint                      | Description                   |
|--------|------------------------------|-------------------------------|
| POST   | `/deliveries/assign_delivery` | Assign delivery personnel    |
| PUT    | `/deliveries/update_delivery_status` | Update delivery status |
| GET    | `/deliveries/delivery/{order_id}` | Get delivery details |

### **6️⃣ Notifications (Email & SMS)**
- Order confirmation emails & SMS sent upon order placement.
- Delivery status updates sent via SMS.
