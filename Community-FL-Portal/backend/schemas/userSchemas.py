from typing import List, Dict, Any
from bson import ObjectId

"""
Provides serialization functions to facilitate the data exchange between the 
API service and MongoDB. It includes two functions: serializeDict, which 
converts MongoDB documents to dictionaries with appropriate type handling for 
object IDs and datetime objects.
serializeList, which applies this serialization to a list of documents.
The UserToken class models the response structure for authentication routes.
"""

def serializeDict(item: Dict) -> Dict[str, Any]:
    """
    Serialize MongoDB documents to a dictionary, handling object IDs and datetime objects.
    """
    return {key: str(value) if isinstance(value, ObjectId) else value for key, value in item.items()}

def serializeList(items: List[Dict]) -> List[Dict[str, Any]]:
    """
    Serialize a list of MongoDB documents using serializeDict.
    """
    return [serializeDict(item) for item in items]
