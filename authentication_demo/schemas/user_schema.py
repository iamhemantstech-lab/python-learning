# Request and response validation
from pydantic import BaseModel, EmailStr, Field, ConfigDict

# 1. Request Schema: Validates incoming data during registration
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name of user")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, max_length=150, description="Plain text password")
    mobile_number: str | None = Field(default=None, max_length=20, description="Mobile number")
    city: str | None = Field(default=None, max_length=100, description="City")
    state: str | None = Field(default=None, max_length=100, description="State")
    country: str | None = Field(default=None, max_length=100, description="Country")

# Alias for backward compatibility
UserSchema = UserRegister

# 2. Response Schema for User: Never includes the password or password hash
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    mobile_number: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    is_active: bool

    # Pydantic v2: allows reading directly from SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)

# 3. Response Schema for Registration Endpoint
class RegisterResponse(BaseModel):
    message: str = "User registered successfully"
    user: UserResponse

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# 4. Response Schema for Login & Refresh Endpoints (JWT Tokens)
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# 5. Request Schema for Refresh Token Endpoint (Optional because it can also come from Cookie)
class RefreshTokenRequest(BaseModel):
    refresh_token: str | None = None

# 6. Request Schema for Updating User Details (All fields optional for partial updates)
class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100, description="Full name of user")
    mobile_number: str | None = Field(default=None, max_length=20, description="Mobile number")
    city: str | None = Field(default=None, max_length=100, description="City")
    state: str | None = Field(default=None, max_length=100, description="State")
    country: str | None = Field(default=None, max_length=100, description="Country")

