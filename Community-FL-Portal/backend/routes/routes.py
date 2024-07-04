import time
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from models.Model import User, Client, Reservation
from auth.oauth import get_current_user
from controller.Controller import *
from typing import List, Dict, Any

user = APIRouter(prefix='/user')
infra = APIRouter(prefix='')
clients: Dict[str, Dict[str, Any]] = {}

@user.get("/")
async def read_root(current_user: User = Depends(get_current_user)):
    """
    Endpoint to return a welcome message. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: dict: A dictionary containing a welcome message.
    """
    return {"data": "Hello World"}

@user.post('/register')
async def create_user(request: User):
    """
    Endpoint to register a new user.
    Args: request (User): The user data for registration.
    Returns: dict: A dictionary indicating user creation status.
    Exception: HTTP Exception in case of errors.
    """
    try:
        uid = await create_user_logic(request)
        return {"res": "created", "uid": uid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint to log in a user and return a JWT access token.
    Args: request (OAuth2PasswordRequestForm): The login form data containing username and password.
    Returns: dict: A dictionary containing the access token and token type.
    Exception: HTTPException: If the username or password is invalid.
    """
    try:
        access_token = await authenticate_user(request.username, request.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/all", response_model=List[User])
async def get_users(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of all users.
    """
    try:
        return await get_all_users()
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.get("/data_scientists", response_model=List[User])
async def get_data_scientists(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all 'Data Scientists'. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of rehistered 'Data Scientists'.
    """
    try:
        return await get_users_by_type("Data Scientist")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/data_providers", response_model=List[User])
async def get_data_providers(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users of type 'Data Provider'. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of users with type 'Data Provider'.
    """
    try:
        return await get_users_by_type("Data Provider")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/model_providers", response_model=List[User])
async def get_model_providers(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users of type 'Model Provider'. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of users with type 'Model Provider'.
    """
    try:
        return await get_users_by_type("Model Provider")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/infra_providers", response_model=List[User])
async def get_infra_providers(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users of type 'Infrastructure Providers'. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of users with type 'Infrastructure Providers'.
    """
    try:
        return await get_users_by_type("Infrastructure Provider")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.get("/infra_with_data_providers", response_model=List[User])
async def get_infra_with_data_providers(current_user: User = Depends(get_current_user)):
    """
    Endpoint to retrieve all users of type 'Infrastructure with Data Providers'. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: List[User]: A list of users with type 'Infrastructure with Data Providers'.
    """
    try:
        return await get_users_by_type("Infrastructure with Data Provider")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.delete("/{user_id}")
async def remove_user(user_id: str, current_user: User = Depends(get_current_user)):
    """
    Endpoint to delete a user. Requires user authentication.
    Args: user_id: User ID for deletetion, current_user (User): The current authenticated user.
    Returns: Status of deletion request
    """
    try:
        result = await delete_user(user_id, current_user)
        return {"res": result}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@user.get("/uid")
async def get_uid(current_user: User = Depends(get_current_user)):
    """
    Endpoint to get uid of the user. Requires user authentication.
    Args: current_user (User): The current authenticated user.
    Returns: uid of the current user
    """
    try:
        uid =  await get_user_data(current_user, "uid")
        return {"uid": uid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@infra.post("/register")
async def register_service(request: Request):
    """
    Endpoint for client nodes to register with community portal.
    Args: request (Request): The request containing the client data.
    Returns: str: A success message.
    """
    try:
        data = await request.json()
        data['last_seen'] = int(time.time())
        clients[data['uid']] = data
        return {"message": "Service registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while registering service: {str(e)}")

@user.get("/discover_clients")
async def discover_clients(current_user: User = Depends(get_current_user)):
    """
    Endpoint to discover available nodes.
    Returns: list: A list of available nodes.
    """
    try:
        current_time = int(time.time())
        available_clients = [item for item in clients.values() if (current_time - item['last_seen']) <= 10]
        infra_data = await update_and_return_infra_data(available_clients)
        return infra_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while discovering services: {str(e)}")

@user.post("/reserve_clients")
async def reserve_clients(clients: List[Client] , current_user: User = Depends(get_current_user)):
    """
    Endpoint to reserve available nodes.
    Args: A list of Username and client IP
    Returns: list: A success message.
    """
    try:
        return await reserve(current_user, clients)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while reserving clients: {str(e)}")
    
@user.get("/reserved_clients")
async def reserved_clients(current_user: User = Depends(get_current_user)):
    """
    Endpoint to get list of reserved clients for the current user.
    Args: Current user
    Returns: list: A list of reserved clients.
    """
    try:
        reservation = await allocate_clients()
        return await get_reserved_clients(current_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while unreserving clients: {str(e)}")

@user.post("/unreserve_clients")
async def unreserve_clients(clients: List[Client] , current_user: User = Depends(get_current_user)):
    """
    Endpoint to unreserve available nodes.
    Args: A list of Username and client IP
    Returns: list: A success message.
    """
    try:
        return await unreserve(current_user, clients)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while unreserving clients: {str(e)}")
    
@user.post('/advance_reservation')
async def advance_reservation(reservation: Reservation, current_user: User = Depends(get_current_user)):
    """
    Endpoint to place a reservation.
    Args: Reservarion data inlcudes user, no.of.clients and duration
    Returns: Reservation request status
    """
    try:
        reservation.username = current_user
        reservation_id = await create_reservation(reservation)
        return {"reservation": "accepted", "reservation_id": reservation_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@user.get("/get_reservartion_status")
async def get_reservartion_status(current_user: User = Depends(get_current_user)):
    """
    Endpoint to get reservation status.
    Returns: list: Client allocation list.
    """
    try:
        reservation = await allocate_clients()
        return reservation
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while discovering services: {str(e)}")