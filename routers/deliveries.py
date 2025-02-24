from fastapi import APIRouter, HTTPException, Depends
from database import get_connection
from schemas import DeliveryAssign, DeliveryStatusUpdate
from mysql.connector import Error
from auth.auth import get_current_user
from auth.permission import check_role  

router = APIRouter()

DELIVERY_STATUSES = ["Assigned", "Out for Delivery", "Delivered", "Failed"]

# Assign Delivery 
@router.post("/assign_delivery")
def assign_delivery(delivery: DeliveryAssign, user: dict = Depends(get_current_user)):
    check_role(user, ["admin"])  

    conn = get_connection()
    cursor = conn.cursor()

    try:
   
        cursor.execute("SELECT COUNT(*) FROM orders WHERE id = %s", (delivery.order_id,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="Order not found")

        
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = %s AND role = 'delivery'", (delivery.delivery_personnel_id,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=400, detail="Invalid delivery_personnel_id: Delivery personnel does not exist")

       
        cursor.execute("SELECT COUNT(*) FROM deliveries WHERE order_id = %s", (delivery.order_id,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="Delivery already assigned for this order")

       
        cursor.execute(
            "INSERT INTO deliveries (order_id, delivery_personnel_id, status) VALUES (%s, %s, %s)",
            (delivery.order_id, delivery.delivery_personnel_id, "Assigned")
        )
        conn.commit()
        return {"message": "Delivery assigned successfully", "order_id": delivery.order_id}

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()

# Update Delivery Status 
@router.put("/update_delivery_status")
def update_delivery_status(delivery_update: DeliveryStatusUpdate, user: dict = Depends(get_current_user)):
    check_role(user, ["delivery"])  

    if delivery_update.status not in DELIVERY_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid delivery status")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        
        cursor.execute("SELECT delivery_personnel_id FROM deliveries WHERE order_id = %s", (delivery_update.order_id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Delivery not found for this order")
        if result[0] != user["id"]:
            raise HTTPException(status_code=403, detail="You are not assigned to this delivery")

        
        cursor.execute("UPDATE deliveries SET status = %s WHERE order_id = %s", (delivery_update.status, delivery_update.order_id))
        conn.commit()

        return {"message": f"Delivery for Order {delivery_update.order_id} updated to {delivery_update.status}"}

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()

# Get Delivery Details 
@router.get("/delivery/{order_id}")
def get_delivery_details(order_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM deliveries WHERE order_id = %s", (order_id,))
    delivery = cursor.fetchone()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery details not found for this order")

    # Check if the user is authorized to view the order delivery details
    if user["role"] == "customer":
        cursor.execute("SELECT customer_id FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        if order["customer_id"] != user["id"]:
            raise HTTPException(status_code=403, detail="You are not authorized to view this delivery")

    cursor.close()
    conn.close()
    return delivery
