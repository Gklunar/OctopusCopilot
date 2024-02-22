import traceback
import uuid
from datetime import date, timedelta

from azure.core.exceptions import HttpResponseError
from azure.data.tables import TableServiceClient

from domain.logging.app_logging import configure_logging

logger = configure_logging(__name__)


def save_users_octopus_url(username, octopus_url, api_key, connection_string):
    logger.info("save_users_octopus_url - Enter")

    if not username or not isinstance(username, str) or not username.strip():
        raise ValueError("username must be the GitHub user's ID (save_users_octopus_url).")

    if not octopus_url or not isinstance(octopus_url, str) or not octopus_url.strip():
        raise ValueError("octopus_url must be an Octopus URL (save_users_octopus_url).")

    if not api_key or not isinstance(api_key, str) or not api_key.strip():
        raise ValueError("service_account_id must be a the ID of a service account (save_users_octopus_url).")

    if connection_string is None:
        raise ValueError('connection_string must be function returning the connection string (save_users_octopus_url).')

    user = {
        'PartitionKey': "github.com",
        'RowKey': username,
        'OctopusUrl': octopus_url,
        'OctopusApiKey': api_key
    }

    table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string())
    table_client = table_service_client.create_table_if_not_exists("users")
    table_client.upsert_entity(user)


def save_login_uuid(username, connection_string):
    logger.info("save_login_uuid - Enter")

    if not username or not isinstance(username, str) or not username.strip():
        raise ValueError("username must be the GitHub user's ID (save_users_id_token).")

    if connection_string is None:
        raise ValueError('connection_string must be function returning the connection string (save_users_id_token).')

    login_uuid = str(uuid.uuid4())

    user = {
        'PartitionKey': "github.com",
        'RowKey': login_uuid,
        'Username': username
    }

    table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string())
    table_client = table_service_client.create_table_if_not_exists("userlogin")
    table_client.upsert_entity(user)

    return login_uuid


def save_users_octopus_url_from_login(state, url, api, connection_string):
    logger.info("save_users_octopus_url_from_login - Enter")

    if not state or not isinstance(state, str) or not state.strip():
        raise ValueError("uuid must be the UUID used to link a login to a user (save_users_octopus_url_from_login).")

    if connection_string is None:
        raise ValueError(
            'connection_string must be function returning the connection string (save_users_octopus_url_from_login).')

    try:
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string())
        table_client = table_service_client.create_table_if_not_exists("userlogin")
        login = table_client.get_entity("github.com", state)

        username = login["Username"]

        save_users_octopus_url(username, url, api, connection_string)
    finally:
        # Clean up the linking record
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string())
        table_client = table_service_client.create_table_if_not_exists("userlogin")
        table_client.delete_entity(state)


def get_users_details(username, connection_string):
    logger.info("get_users_details - Enter")

    if not username or not isinstance(username, str) or not username.strip():
        raise ValueError("username must be the GitHub user's ID (get_users_details).")

    if connection_string is None:
        raise ValueError('connection_string must be function returning the connection string (get_users_details).')

    table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string())
    table_client = table_service_client.create_table_if_not_exists("users")
    return table_client.get_entity("github.com", username)


def delete_old_user_details(connection_string):
    logger.info("delete_old_user_details - Enter")

    if connection_string is None:
        raise ValueError('connection_string must be function returning the connection string (delete_login_details).')

    try:
        table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string())
        table_client = table_service_client.get_table_client(table_name="users")

        thirty_days_ago = (date.today() - timedelta(days=30)).strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ")

        rows = table_client.query_entities(f"Timestamp lt datetime'{thirty_days_ago}'")
        counter = 0
        for row in rows:
            counter = counter + 1
            table_client.delete_entity("github.com", row['RowKey'])

        logger.info(f"Cleaned up {counter} entries.")

    except HttpResponseError as e:
        error_message = getattr(e, 'message', repr(e))
        logger.error(error_message)
        logger.error(traceback.format_exc())
