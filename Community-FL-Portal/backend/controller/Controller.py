import os
import uuid
from typing import List
from fastapi import HTTPException, status
from auth.hashing import Hash
from auth.jwttoken import create_access_token
from bson import ObjectId
from schemas.userSchemas import serializeDict, serializeList
from models.Model import User, Client, Reservation
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_url = os.getenv("MONGO_URL")
db_user = MongoClient(mongo_url)['communityFL']['users']
db_reservation = MongoClient(mongo_url)['communityFL']['reservation']

async def get_all_users() -> List[dict]:
    """
    Get all users from the database and serialize them into a list of dictionaries.
    Returns: List[dict]: A list of all user documents serialized as dictionaries.
    Exception: Incase of any errors.
    """
    try:
        users = db_user.find()
        return serializeList(users)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def create_user_logic(user_data) -> str:
    """
    Create a new user in the database with hashed password.
    Args: user_data: username, password, type, group, topology and email.
    Returns: str: The ID of the newly created user.
    Exception: Incase of any errors.
    """
    try:
        hashed_pass = Hash.bcrypt(user_data.password)
        user_object = dict(user_data)
        user_object["password"] = hashed_pass
        if not user_object["uid"]:
            user_object["uid"] = str(uuid.uuid4())
        user_id = db_user.insert_one(user_object).inserted_id
        return str(user_object["uid"])
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def authenticate_user(username, password) -> str:
    """
    Authenticate a user by verifying the username and password.
    Args: username and password.
    Returns: str: A JWT access token if authentication is successful.
    Exception: HTTPException: If the user is not found or if the password is incorrect.
    """
    try:
        user = db_user.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No user found with this {username} username')
        if not Hash.verify(user["password"], password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Wrong Username or password')
        access_token = create_access_token(data={"sub": user["username"]})
        return access_token
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_users_by_type(user_type: str) -> List[dict]:
    """
    Get users from the database based on their type and serialize them into a list of dictionaries.
    Args: user_type: "Data Provider" and "Data Scientist".
    Returns: List[dict]: A list of user documents of the specified type serialized as dictionaries.
    """
    try:
        users = db_user.find({"type": user_type})
        return serializeList(users)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_user(user_id: str, current_user: User) -> str:
    """
    Delete a user, Requires user authentication.
    Args: user_id: to delete, current_user (User): The current authenticated user.
    Returns: Status of deletion request
    """
    try:
        result = db_user.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return "User deleted successfully"
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def get_user_data(current_user, data: str) -> str:
    """
    Get required user data from the database.
    Args: data: field name.
    Returns: str: Requested data in string format.
    """
    try:
        user_data = db_user.find_one({"username": current_user}, {"_id": 0, data: 1})
        if data in user_data:
            return user_data[data]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{data} not found for user")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def update_and_return_infra_data(available_clients: list) -> list:
    """
    Update the infra status in the MongoDB and return the updated list to the endpoints.
    Args: data: list of available_clients.
    Returns: str: Requested data in list format.
    """
    try:
        # Updating the status of clients that have responded
        for client in available_clients:
            result = db_user.update_one(
                {"uid": client['uid']},
                {"$set": {"status": "Online",
                          "tags": client.get('tags', []),
                          "weights": client.get("weights", ""),
                          "client_ip": client.get("client_ip", ""),
                          "last_seen": client.get ("last_seen", 0)
                          }}
            )
        # Updating the status of clients that have not responded
        result = db_user.update_many(
            {"uid": {"$nin": [client['uid'] for client in available_clients]}, "status": "Online"},
            {"$set": {"status": "Offline",
                      "weights": "",
                      "client_ip": "",
                      "last_seen": ""
                      }}
        )

        infra_data = list(db_user.find({}, {"_id": 0, "uid": 0}))

        return infra_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def reserve(current_user: str, clients: list[Client]):
    """
    Update the reservation status in the MongoDB.
    Args: current_user and clients (list): A list of clients with client_ip and username.
    Returns: Success message.
    """
    try:
        for client in clients:
            result = db_user.update_one(
                {"username": client.username, "client_ip": client.client_ip},
                {"$set": {"reserved_by": current_user}}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client {client.username} with IP {client.client_ip} not found")

        return "Reservation status updated successfully."
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
async def unreserve(current_user: str, clients: list):
    """
    Unreserve the clients in the MongoDB.
    Args: clients (list): A list of clients with their username and client_ip.
    Returns: str: Success message.
    """
    try:
        for client in clients:
            result = db_user.update_one(
                {"username": client.username, "client_ip": client.client_ip, "reserved_by": current_user},
                {"$set": {"reserved_by": ""}}
            )
            if result.matched_count == 0:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Client {client.username} with IP {client.client_ip} not found")
        return "Unreservation status updated successfully."
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

async def get_reserved_clients(current_user: str):
    """
    Get the list of reserved clients by the current user.
    Args: current_user (str): The user who reserved the clients.
    Returns: A list of reserved clients with their username, email, group, client_ip, tags, and status.
    """
    try:
        reserved_clients = list(db_user.find(
            {"reserved_by": current_user},
            {"_id": 0, "username": 1, "email": 1, "group": 1, "client_ip": 1, "tags": 1,
              "status": 1,  "weights": 1, "last_seen": 1}
        ))
        return reserved_clients
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

async def create_reservation(reservation: Reservation):
    """
    Controller to place a reservation.
    Args: Reservarion data inlcudes user, no.of.clients and duration
    Returns: Reservation request status
    """
    try:
        reservation_id = db_reservation.insert_one(dict(reservation)).inserted_id
        return str(reservation_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def allocate_clients():
    """
    Controller to allocate clients based on reservation requests.
    Args: reservation (Reservation): The reservation request details.
    Returns: list: Client allocation list.
    Alogirthm: Greedy Algorithm, Most Beneficial First
    """
    try:
        reservations = list(db_reservation.find({"status": None}).sort([("no_of_clients", 1), ("duration", 1)]))
        available_clients = list(db_user.find({
            "$or": [{"reserved_by": ""}, {"reserved_by": None}]
        }).sort([("status", -1)]))
        allocation_results = []

        for res in reservations:
            required_clients = res["no_of_clients"]
            if len(available_clients) >= required_clients:
                allocated_clients = available_clients[:required_clients]
                available_clients = available_clients[required_clients:]

                for client in allocated_clients:
                    db_user.update_one(
                        {"uid": client["uid"]},
                        {"$set": {"reserved_by": res["username"]}}
                    )

                db_reservation.update_one(
                    {"_id": res["_id"]},
                    {"$set": {"status": "Completed"}}
                )

                allocation_results.append({
                    "reservation_id": str(res["_id"]),
                    "allocated_clients": allocated_clients
                })
            else:
                break

        return allocation_results

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))