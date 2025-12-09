from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True)
    picture: Optional[str] = None
    is_setup: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    contacts: List["Contact"] = Relationship(back_populates="owner", sa_relationship_kwargs={"foreign_keys": "Contact.owner_id"})

class Contact(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    contact_user_id: int = Field(foreign_key="user.id")
    alias: Optional[str] = None

    owner: User = Relationship(back_populates="contacts", sa_relationship_kwargs={"foreign_keys": "Contact.owner_id"})
    # contact_user relation omitted for brevity, can be added if needed

class Group(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    admin_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GroupMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="group.id")
    user_id: int = Field(foreign_key="user.id")

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="user.id")
    recipient_id: Optional[int] = Field(foreign_key="user.id", nullable=True) # Valid for DM
    group_id: Optional[int] = Field(foreign_key="group.id", nullable=True) # Valid for Group
    
    # Encrypted content params
    content_blob: str # Base64 encoded encrypted string
    nonce: str # For ChaCha20 or IV for AES
    algorithm: str # "AES" or "ChaCha20"
    is_file: bool = False
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
