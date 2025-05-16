import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import SessionLocal
from app.models.item import Item
from app.models.user import User
from app.utils.auth import get_password_hash

def create_demo_data():
    db = SessionLocal()
    
    admin_user = db.query(User).filter(User.username == "admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("adminpassword"),
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        print(f"Created admin user with ID: {admin_user.id}")
    
    demo_items = [
        {"name": "Laptop", "description": "High-performance laptop", "price": 1200.0, "tax": 120.0},
        {"name": "Smartphone", "description": "Latest smartphone model", "price": 800.0, "tax": 80.0},
        {"name": "Headphones", "description": "Noise-cancelling headphones", "price": 200.0, "tax": 20.0},
        {"name": "Monitor", "description": "4K Ultra HD monitor", "price": 350.0, "tax": 35.0},
        {"name": "Keyboard", "description": "Mechanical keyboard", "price": 100.0, "tax": 10.0}
    ]
    
    items_created = 0
    for item_data in demo_items:
        existing_item = db.query(Item).filter(
            Item.name == item_data["name"],
            Item.owner_id == admin_user.id
        ).first()
        
        if not existing_item:
            db_item = Item(
                name=item_data["name"],
                description=item_data["description"],
                price=item_data["price"],
                tax=item_data["tax"],
                owner_id=admin_user.id
            )
            db.add(db_item)
            items_created += 1
    
    db.commit()
    print(f"Demo data creation complete. {items_created} items created in SQLite database.")
    db.close()

if __name__ == "__main__":
    create_demo_data()
