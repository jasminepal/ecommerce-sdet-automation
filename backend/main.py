from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field, EmailStr
from app.database import get_db
from app.models import Product, Category, User
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

app = FastAPI()

password_hash = PasswordHash.recommended()

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt = 0)
    stock: int = Field(ge = 0)
    category_id: int
    
    
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category_id: int
    
    
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    category_id: int | None = None
    



class CategoryCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int 
    name: str
    description: str | None 


class CategoryUpdate(BaseModel):
    name: str = Field(min_length=1)
    description: str | None = None



class UserCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr 
    password: str = Field(min_length=8)
    
    
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    

class UserUpdate(BaseModel):
    name: str | None = Field(min_length=1, default=None)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    is_active: bool | None = None



@app.get("/")
def home():
    return {"message": "E-Commerce API is running"}


@app.get("/products", response_model= list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.post("/products", 
          response_model=ProductResponse, 
          status_code=status.HTTP_201_CREATED
          )
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    category = (db.query(Category).filter(Category.id == product.category_id).first())
    
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
    
    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock,
        category_id=product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product
    
    
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if product is None:
        raise HTTPException(
                status_code=404,
                detail="Product not found"
            )
    db.delete(product)
    db.commit()
    
    return {"message": "Product Deleted Successfully"} 


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):

    existing_product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )
    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product Not Found"
        )
        
    category = (db.query(Category).filter(Category.id == product.category_id).first())
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
        
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.stock = product.stock
    existing_product.category_id = product.category_id

    db.commit()
    db.refresh(existing_product)

    return existing_product
    
    
@app.patch(
    "/products/{product_id}",
    response_model=ProductResponse
)
def update_product_partial(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db)
):

    existing_product = (db.query(Product).filter(Product.id == product_id).first())
    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product.name is not None:
        existing_product.name = product.name
    if product.price is not None:
        existing_product.price = product.price
    if product.stock is not None:
        existing_product.stock = product.stock 
    if product.category_id is not None:
        category = (db.query(Category).filter(Category.id == product.category_id).first())
        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category Not Found"
            )
        if product.category_id is not None:
            existing_product.category_id = product.category_id

    db.commit()
    db.refresh(existing_product)

    return existing_product


## Category APIs
@app.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.post("/categories", 
          response_model=CategoryResponse,
          status_code=status.HTTP_201_CREATED
          )
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing_category = db.query(Category).filter(Category.name == category.name).first()
    
    if existing_category is not None:
        raise HTTPException(
            status_code=409,
            detail="Category Already Exists"
        )
        
    new_category = Category(
        name = category.name,
        description = category.description
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return new_category


@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
    
    return category


@app.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category Deleted Successfully"}


@app.put("/categories/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, category: CategoryCreate, db: Session = Depends(get_db)):
    
    existing_category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )
    
    if existing_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )
        
    existing_category.name = category.name
    existing_category.description = category.description

    db.commit()
    db.refresh(existing_category)

    return existing_category


@app.patch("/categories/{category_id}", response_model=CategoryResponse)
def update_category_partial(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    existing_category = (db.query(Category).filter(Category.id == category_id).first())

    if existing_category is None:
        raise HTTPException(
            status_code=404,
            detail="Category Not Found"
        )

    if category.name is not None:
        existing_category.name = category.name

    if category.description is not None:
        existing_category.description = category.description

    db.commit()
    db.refresh(existing_category)

    return existing_category


## User APIs
@app.post("/users", response_model=UserResponse, status_code=201)
def  create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (db.query(User).filter(User.email == user.email).first())
    
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User Already Registered")
        
    hashed_password = password_hash.hash(user.password)
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        is_active=True
    )

    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@app.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/users/{user_id}", response_model=UserResponse)
def get_all_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id == user_id).first())
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
        
    return user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = (db.query(User).filter(User.id == user_id).first())
    
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User Not Found"
        )
        
    db.delete(user)
    db.commit()
    
    return {"message": "User Deleted Successfully"}


# @app.put("/users/{user_id}")
# def update_user(user_id: int, db: Session = Depends(get_db)):
#     existing_user = (db.query(User).filter(User.id == user_id).first())
    
#     if existing_user is None:
#         raise HTTPException(
#             status_code=404,
#             detail="User Not Found"
#         )
        
#     user = (db.query(User).filter(User.id == user_id))