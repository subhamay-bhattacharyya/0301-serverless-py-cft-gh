""" Module providing a library of utility functions related to AWS Systems Manager"""

from __future__ import annotations
from typing import Any

from botocore.exceptions import ClientError
from botocore.client import BaseClient as Client


def get_ssm_parameter(
    ssm_client: Client, name: str, logger: Any = None, tracer: Any = None
) -> str:
    """
    Retrieve a parameter value from AWS Systems Manager Parameter Store.

    Args:
        name (str): The name of the parameter to retrieve.

    Returns:
        str: The decrypted value of the parameter.

    Raises:
        botocore.exceptions.ClientError: If there is an error retrieving the parameter.
    """
    try:
        response = ssm_client.get_parameter(Name=name, WithDecryption=True)
        return response["Parameter"]["Value"]
    except ClientError as e:
        error_message = f"Failed to get parameter: {e}"
        if logger:
            logger.error(error_message)
        if tracer:
            tracer.capture_exception(e)
        raise ClientError(error_message)
