from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel, Field
from app.database import get_db
from app.models import Product, Category
from sqlalchemy.orm import Session

app = FastAPI()

class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt = 0)
    stock: int = Field(ge = 0)
    
    
class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    
    
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    



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
    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
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
        
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.stock = product.stock

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