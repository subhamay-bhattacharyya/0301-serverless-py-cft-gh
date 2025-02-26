""" Module providing a library of utility functions """

from __future__ import annotations
from typing import Any

import botocore.exception
from botocore.dynamodb.types import TypeSerializer, TypeDeserializer


def deserialize_dynamodb_item(item: dict[str, Any]) -> dict[str, Any]:
    """Deserialize a DynamoDB item into a Python dictionary"""
    if not isinstance(item, dict):
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message="Item must be a dictionary",
        )

    if len(item) == 0:
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message="Item must not be empty",
        )

    try:
        deserializer = TypeDeserializer()
        return {k: deserializer.deserialize(v) for k, v in item.items()}
    except botocore.exception.ClientError as e:
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message=f"Failed to deserialize item: {e}",
        ) from e


def serialize_dynamodb_item(item: dict[str, Any]) -> dict[str, Any]:
    """Serialize a Python dictionary into a DynamoDB item"""
    if not isinstance(item, dict):
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message="Item must be a dictionary",
        )

    if len(item) == 0:
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message="Item must not be empty",
        )

    try:
        serializer = TypeSerializer()
        return {k: serializer.serialize(v) for k, v in item.items()}

    except botocore.exception.ClientError as e:
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message=f"Failed to serialize item: {e}",
        ) from e


def get_dynamodb_item(
    table_name: str,
    key: dict[str, Any],
    dynamodb_client: botocore.client.BaseClient,
) -> dict[str, Any]:
    """Get a DynamoDB item from a table"""
    try:
        response = dynamodb_client.get_item(
            TableName=table_name,
            Key=serialize_dynamodb_item(key),
        )
        return deserialize_dynamodb_item(response["Item"])
    except botocore.exception.ClientError as e:
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message=f"Failed to get item from table {table_name}: {e}",
        ) from e


def put_dynamodb_item(
    table_name: str,
    item: dict[str, Any],
    dynamodb_client: botocore.client.BaseClient,
) -> None:
    """Put a DynamoDB item into a table"""
    try:
        dynamodb_client.put_item(
            TableName=table_name,
            Item=serialize_dynamodb_item(item),
        )
    except botocore.exception.ClientError as e:
        raise botocore.exception.ClientError(
            error_type="ClientError",
            error_message=f"Failed to put item into table {table_name}: {e}",
        ) from e
