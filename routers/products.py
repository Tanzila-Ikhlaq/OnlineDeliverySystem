from fastapi import APIRouter, HTTPException, Depends, Query
from database import get_connection
from schemas import ProductCreate
from auth.permission import check_role
from auth.auth import get_current_user

router = APIRouter()

# Add Product
@router.post("/add")
def add_product(product: ProductCreate, user: dict = Depends(get_current_user)):
    check_role(user, ["vendor"])  
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO products (vendor_id, name, description, price, availability, category) VALUES (%s, %s, %s, %s, %s, %s)",
            (product.vendor_id, product.name, product.description, product.price, product.availability, product.category)
        )
        conn.commit()
        return {"message": "Product added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Get Products
@router.get("/list")
def list_products():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return products
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.put("/update/{product_id}")
def update_product(product_id: int, product: ProductCreate, user: dict = Depends(get_current_user)):
    check_role(user, ["vendor"]) 

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT vendor_id FROM products WHERE id = %s", (product_id,))
        product_data = cursor.fetchone()

        if not product_data:
            raise HTTPException(status_code=404, detail="Product not found")  
        
        if product_data[0] != user["user_id"]:
            raise HTTPException(status_code=403, detail="You can only update your own products")  

        cursor.execute(
            "UPDATE products SET name=%s, description=%s, price=%s, availability=%s, category=%s WHERE id=%s",
            (product.name, product.description, product.price, product.availability, product.category, product_id)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=400, detail="No changes were made to the product")

        conn.commit()
        return {"message": "Product updated successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        cursor.close()
        conn.close()

# Delete Product
@router.delete("/delete/{product_id}")
def delete_product(product_id: int, user: dict = Depends(get_current_user)):
    check_role(user, ["admin"])  

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/products")
def list_products(
    category: str = Query(None, description="Filter by category"),
    min_price: float = Query(None, description="Minimum price"),
    max_price: float = Query(None, description="Maximum price"),
    available: bool = Query(None, description="Filter by availability")
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)

    if min_price is not None:
        query += " AND price >= %s"
        params.append(min_price)

    if max_price is not None:
        query += " AND price <= %s"
        params.append(max_price)

    if available is not None:
        query += " AND availability = %s"
        params.append(available)

    cursor.execute(query, tuple(params))
    products = cursor.fetchall()

    cursor.close()
    conn.close()
    return {"products": products}