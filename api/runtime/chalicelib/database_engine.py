from abc import ABC
from abc import abstractmethod
from typing import Any, Dict, Optional

import boto3


class DatabaseEngineInterface(ABC):
    @abstractmethod
    def create_user(
        self, username: str, user_attributes: Dict[str, str]
    ) -> Dict[str, str]:
        pass

    @abstractmethod
    def update_user(self, username: str, user_attributes: Dict[str, str]) -> Any:
        pass

    @abstractmethod
    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_user(self, username: str) -> None:
        pass


class DynamoDBEngine(DatabaseEngineInterface):
    def __init__(self, table_name: str):
        dynamodb = boto3.resource("dynamodb")
        self._table = dynamodb.Table(table_name)

    def create_user(
        self, username: str, user_attributes: Dict[str, str]
    ) -> Dict[str, str]:
        user = {"username": username}
        user.update(user_attributes)
        self._table.put_item(Item=user)
        return user

    def update_user(self, username: str, user_attributes: Dict[str, str]) -> Any:
        update_expression_pairs = [f"#{key} = :{key}" for key in user_attributes]
        update_expression = "SET " + ", ".join(update_expression_pairs)
        expression_attribute_names = {f"#{key}": key for key in user_attributes}
        expression_attribute_values = {
            f":{key}": value for key, value in user_attributes.items()
        }

        updated_item = self._table.update_item(
            Key={"username": username},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="ALL_NEW",
        )
        return updated_item["Attributes"]

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        response = self._table.get_item(Key={"username": username})
        return response["Item"] if "Item" in response else None

    def delete_user(self, username: str) -> None:
        self._table.delete_item(Key={"username": username})
