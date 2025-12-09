from sqlmodel import Session, select
import models
from models import User, Contact, Group, GroupMember

def get_user_by_email(session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def get_user_by_username(session: Session, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def add_contact(session: Session, owner_id: int, contact_username: str) -> Contact | None:
    contact_user = get_user_by_username(session, contact_username)
    if not contact_user:
        return None
    
    # Check if already exists
    statement = select(Contact).where(Contact.owner_id == owner_id).where(Contact.contact_user_id == contact_user.id)
    existing = session.exec(statement).first()
    if existing:
        return existing
        
    contact = Contact(owner_id=owner_id, contact_user_id=contact_user.id, alias=contact_user.username)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact

def get_contacts(session: Session, user_id: int) -> list[Contact]:
    statement = select(Contact).where(Contact.owner_id == user_id)
    return session.exec(statement).all()

def create_group(session: Session, admin_id: int, name: str, member_usernames: list[str]) -> Group:
    group = Group(name=name, admin_id=admin_id)
    session.add(group)
    session.commit()
    session.refresh(group)
    
    # Add admin
    session.add(GroupMember(group_id=group.id, user_id=admin_id))
    
    # Add members
    for username in member_usernames:
        user = get_user_by_username(session, username)
        if user:
            session.add(GroupMember(group_id=group.id, user_id=user.id))
            
    session.commit()
    return group

def get_user_groups(session: Session, user_id: int) -> list[Group]:
    # Join GroupMember to find groups
    statement = select(Group).join(GroupMember).where(GroupMember.user_id == user_id)
    return session.exec(statement).all()

def get_group_members(session: Session, group_id: int) -> list[int]:
    statement = select(GroupMember.user_id).where(GroupMember.group_id == group_id)
    return session.exec(statement).all()

def update_user_username(session: Session, user_id: int, new_username: str) -> User | None:
    user = session.get(User, user_id)
    if user:
        user.username = new_username
        user.is_setup = True
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

def get_active_chat_users(session: Session, user_id: int) -> list[User]:
    # Find all users who sent messages to me OR I sent messages to
    from models import Message
    
    # Received messages
    sub_received = select(Message.sender_id).where(Message.recipient_id == user_id)
    # Sent messages
    sub_sent = select(Message.recipient_id).where(Message.sender_id == user_id)
    
    # Combine (Raw SQL might be easier for UNION, but let's try python logic for simplicity in this filters or OR)
    # Actually, iterate and unique.
    
    sent_ids = session.exec(sub_sent).all()
    received_ids = session.exec(sub_received).all()
    
    related_ids = set(sent_ids + received_ids)
    
    # Also include Contacts (explicit adds)
    contacts = get_contacts(session, user_id)
    for c in contacts:
        related_ids.add(c.contact_user_id)
        
    if user_id in related_ids:
        related_ids.remove(user_id) # Remove self
        
    if not related_ids:
        return []
        
    statement = select(User).where(User.id.in_(related_ids))
    return session.exec(statement).all()

def create_message(session: Session, sender_id: int, target_type: str, target_id: int, content_blob: str, nonce: str, algorithm: str, is_file: bool = False) -> models.Message:
    msg = models.Message(
        sender_id=sender_id,
        recipient_id=target_id if target_type == 'user' else None,
        group_id=target_id if target_type == 'group' else None,
        content_blob=content_blob,
        nonce=nonce,
        algorithm=algorithm,
        is_file=is_file
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg
