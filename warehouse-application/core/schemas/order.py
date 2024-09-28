from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int
    
class OrderBase(BaseModel):
    created_at: Optional[datetime] = None
    status: Literal["IN PROCESS", "SENT", "DELIVERED"]

class OrderCreate(OrderBase):
    user_id: int = 2
    order_items: List[OrderItemCreate]
    
class OrderRead(OrderBase):
    id: int 
    created_at: datetime
    items: List[OrderItemRead]