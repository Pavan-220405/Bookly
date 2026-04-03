from asyncpg import Connection
from uuid import UUID
from pydantic import EmailStr

from myapp.users.schemas import UserCreate
from myapp.auth.utils import hash_password

async def crud_create_user(conn : Connection, new_user_data : UserCreate):
    create_user_query = """
                        INSERT INTO users (user_name,first_name,last_name,email,hashed_password)
                        VALUES ($1,$2,$3,$4,$5)
                        RETURNING *;
                    """ 
    row = await conn.fetchrow(
        create_user_query,
        new_user_data.user_name,
        new_user_data.first_name,
        new_user_data.last_name,
        new_user_data.email,
        hash_password(new_user_data.password)
    )
    return dict(row) if row else None



async def crud_get_user_by_email(conn : Connection, email : str):
    query = """
            SELECT * FROM users
            WHERE email = $1;
        """
    row = await conn.fetchrow(query,email)
    return dict(row) if row else None



async def crud_get_user_by_id(conn : Connection, id : UUID):
    query = """
            SELECT * FROM users
            WHERE id = $1;
        """
    row = await conn.fetchrow(query,id)
    return dict(row) if row else None



async def crud_delete_user_by_id(conn: Connection, id: UUID):
    query = """
        DELETE FROM users
        WHERE id = $1
        RETURNING *;
    """
    row = await conn.fetchrow(query, id)
    return dict(row) if row else None


async def crud_make_user_admin(conn : Connection, user_email : EmailStr):
    query = """
            UPDATE users
            SET role = 'admin'
            WHERE email = $1
            RETURNING *;
        """
    row = await conn.fetchrow(query,user_email)
    return dict(row) if row else None
    