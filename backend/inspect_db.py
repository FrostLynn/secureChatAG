from database import engine
from sqlmodel import Session, select
from models import Message, User

def inspect_messages():
    output_file = "db_export.txt"
    with open(output_file, "w") as f:
        with Session(engine) as session:
            messages = session.exec(select(Message)).all()
            
            print(f"\n{'='*60}", file=f)
            print(f" SERVER DATABASE DUMP", file=f)
            print(f"{'='*60}\n", file=f)
            
            if not messages:
                print("No messages found in database yet.", file=f)
                return
    
            for msg in messages:
                sender = session.get(User, msg.sender_id)
                sender_name = sender.username if sender else "Unknown"
                
                print(f"From: {sender_name} (ID: {msg.sender_id})", file=f)
                target = f"User {msg.recipient_id}" if msg.recipient_id else f"Group {msg.group_id}"
                print(f"To: {target}", file=f)
                print(f"Algorithm: {msg.algorithm}", file=f)
                print("-" * 30, file=f)
                print(f"{msg.content_blob}", file=f) 
                print("-" * 30, file=f)
    
    print(f"Dump saved to {output_file}")

if __name__ == "__main__":
    inspect_messages()
