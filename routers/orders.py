from fastapi import APIRouter, HTTPException, Depends
from database import get_connection
from schemas import OrderCreate, OrderStatusUpdate
from mysql.connector import Error
from auth.auth import get_current_user
from auth.permission import check_role  
from routers.notifications import send_email,send_sms 

router = APIRouter()

ORDER_STATUSES = ["Placed", "Processing", "Shipped", "Out for Delivery", "Delivered", "Canceled"]

@router.post("/place_order")
async def place_order(order: OrderCreate, user: dict = Depends(get_current_user)):
    check_role(user, ["customer"])  

    conn = get_connection()
    cursor = conn.cursor()

    try:
        total_amount = 0
        product_prices = {}

        for item in order.products:
            cursor.execute("SELECT price FROM products WHERE id = %s", (item["product_id"],))
            product = cursor.fetchone()
            if not product:
                raise HTTPException(status_code=400, detail=f"Product ID {item['product_id']} does not exist")

            price = product[0]
            product_prices[item["product_id"]] = price
            total_amount += price * item["quantity"]

        cursor.execute(
            "INSERT INTO orders (customer_id, total_amount, status) VALUES (%s, %s, %s)",
            (user["user_id"], total_amount, "Placed")
        )
        order_id = cursor.lastrowid

        for item in order.products:
            subtotal = item["quantity"] * product_prices[item["product_id"]]
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
                (order_id, item["product_id"], item["quantity"], subtotal)
            )

        conn.commit()

        cursor.execute("SELECT phone_number FROM users WHERE id = %s", (user["user_id"],))
        phone_data = cursor.fetchone()
        customer_phone = phone_data[0] if phone_data else None

        email_body = f"Hello {user['username']},<br>Your order (ID: {order_id}) has been placed successfully! 🎉<br>Total: ${total_amount}"
        await send_email("Order Confirmation", user["email"], email_body)

        if customer_phone:
            sms_message = f"Hello {user['username']}, your order (ID: {order_id}) of ${total_amount} has been placed successfully! ✅"
            send_sms(customer_phone, sms_message)

        return {"message": "Order placed successfully", "order_id": order_id}

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()

# Get Order Details 
@router.get("/order/{order_id}")
def get_order(order_id: int, user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if user["role"] not in ["admin", "delivery"] and order["customer_id"] != user["user_id"]:
        raise HTTPException(status_code=403, detail="You are not authorized to view this order")

    cursor.execute("SELECT * FROM order_items WHERE order_id = %s", (order_id,))
    order["items"] = cursor.fetchall()

    cursor.close()
    conn.close()
    return order

# Update Order Status
@router.put("/update_status")
def update_order_status(order_update: OrderStatusUpdate, user: dict = Depends(get_current_user)):
    check_role(user, ["admin", "delivery"]) 

    if order_update.status not in ORDER_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid order status")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM orders WHERE id = %s", (order_update.order_id,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="Order not found")

        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (order_update.status, order_update.order_id))
        conn.commit()

        return {"message": f"Order {order_update.order_id} updated to {order_update.status}"}

    except Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()
