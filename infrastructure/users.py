from azure.data.tables import TableServiceClient


def save_users_details(username, octopus_url):
    user = {
        'PartitionKey': "github.com",
        'RowKey': username,
        'OctopusUrl': octopus_url
    }

    table_service_client = TableServiceClient.from_connection_string(conn_str="AzureWebJobsStorage")
    table_client = table_service_client.get_table_client(table_name="users")
    table_client.create_entity(user)


def get_users_details(username):
    table_service_client = TableServiceClient.from_connection_string(conn_str="AzureWebJobsStorage")
    table_client = table_service_client.get_table_client(table_name="users")
    return table_client.get_entity("github.com", username)
