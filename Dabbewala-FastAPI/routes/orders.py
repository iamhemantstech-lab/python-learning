from fastapi import APIRouter, Depends, HTTPException, Query
from database import get_session
from models import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from sqlmodel import Session, select
from datetime import date, datetime

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.model_dump()) # ** means spreading our args into key value pair and model_dump convert out pydentic model into the dictionary
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

# multiple query paramters
@router.get("/", response_model=list[Order])
def list_orders(
    status: OrderStatus | None = Query(default=None, description="Filter by order status"),
    created_date: date | None = Query(default=None, description="Filter by creation date (YYYY-MM-DD)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: Session = Depends(get_session)
    ):

    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    if created_date:
        start = datetime.combine(created_date, datetime.min.time())
        end = datetime.combine(created_date, datetime.max.time())
        query = query.where(Order.created_at >= start, Order.created_at <= end)

    query = query.offset(skip).limit(limit)

    return session.exec(query).all()

@router.get("/{order_id}", response_model=Order)
def get_order_detail(order_id: int, session: Session = Depends(get_session)):
    """Fetch details for a single order by its ID."""
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
    
    return order

@router.patch("/{order_id}", response_model=Order)
def update_order(order_id: int, order_update: OrderUpdate, session: Session = Depends(get_session)):
    """Partially update an existing order's status or delivery address."""
    db_order = session.get(Order, order_id)

    if not db_order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

    old_status = db_order.status
    update_data = order_update.model_dump(exclude_unset=True) # Extract ONLY fields that the client sent

    db_order.sqlmodel_update(update_data) # Apply the changes to the database model
    db_order.updated_at = datetime.now() # Update the modified timestamp

    # If status changed, record an audit entry in StatusLog
    if order_update.status and order_update.status != old_status:
        log = StatusLog(
            order_id=db_order.id,
            old_status=old_status.value if hasattr(old_status, "value") else str(old_status),
            new_status=order_update.status.value if hasattr(order_update.status, "value") else str(order_update.status),
        )
        session.add(log)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    return db_order


@router.get("/{order_id}/timeline", response_model=list[StatusLog])
def get_order_timeline(order_id: int, session: Session = Depends(get_session)):
    """Fetch the delivery history timeline for an order."""
    db_order = session.get(Order, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

    query = select(StatusLog).where(StatusLog.order_id == order_id).order_by(StatusLog.changed_at)
    return session.exec(query).all()


@router.delete("/{order_id}")
def delete_order(order_id: int, session: Session = Depends(get_session)):
    """Cancel and delete an order and its associated status logs."""
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

    # Clean up associated child logs first to avoid orphaned records
    logs = session.exec(select(StatusLog).where(StatusLog.order_id == order_id)).all()
    for log in logs:
        session.delete(log)

    session.delete(order)
    session.commit()

    return {"message": f"Order with ID {order_id} deleted successfully"}
