import stripe
from fastapi import APIRouter, HTTPException
from database import get_connection
from config import STRIPE_SECRET_KEY

router = APIRouter()

stripe.api_key = STRIPE_SECRET_KEY  

@router.post("/create-checkout-session")
def create_checkout_session(order_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT total_amount FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        total_amount = int(order["total_amount"] * 100)  

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Order {order_id}"},
                        "unit_amount": total_amount,
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/payment-success",
            cancel_url="http://localhost:8000/payment-cancel",
        )

        return {"session_id": session.id,"checkout_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()

@router.get("/verify-payment/{session_id}")
def verify_payment(session_id: str):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {"status": session.payment_status}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
