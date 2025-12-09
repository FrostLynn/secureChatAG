from database import engine
from sqlmodel import Session, select
from models import Message, User

def inspect_messages():
    with Session(engine) as session:
        messages = session.exec(select(Message)).all()
        
        print(f"\n{'='*60}")
        print(f" SERVER DATABASE DUMP")
        print(f"{'='*60}\n")
        
        if not messages:
            print("No messages found in database yet.")
            return

        for msg in messages:
            sender = session.get(User, msg.sender_id)
            sender_name = sender.username if sender else "Unknown"
            
            print(f"From: {sender_name} (ID: {msg.sender_id})")
            target = f"User {msg.recipient_id}" if msg.recipient_id else f"Group {msg.group_id}"
            print(f"To: {target}")
            print(f"Algorithm: {msg.algorithm}")
            print("-" * 30)
            print(f"{msg.content_blob}") 
            print("-" * 30)

if __name__ == "__main__":
    inspect_messages()
