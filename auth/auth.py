from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
import bcrypt
from database import get_connection
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Function to hash passwords
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

# Function to verify passwords
def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# User Registration Endpoint
@router.post("/register")
def register(username: str, email: str, password: str, role: str, phone_number: str):
    if role not in ["admin", "vendor", "delivery", "customer"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, email, password_hash, role, phone_number) VALUES (%s, %s, %s, %s, %s)",
            (username, email, hashed_password, role, phone_number),
        )
        conn.commit()
        return {"message": "User registered successfully"}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()


# User Login & Token Generation
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s", (form_data.username,))
        user = cursor.fetchone()

        if not user or not verify_password(form_data.password, user["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = create_access_token(
            data={"sub": user["username"], "user_id": user["id"], "role": user["role"]}
        )
        return {"access_token": access_token, "token_type": "bearer"}

    finally:
        cursor.close()
        conn.close()

# Get Current User (Decode JWT)
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        exp = payload.get("exp")
        if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
            raise HTTPException(status_code=401, detail="Token has expired")

        return payload 

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Role-Based Access Control
def check_role(user: dict, allowed_roles: list):
    if user["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="Unauthorized access")
