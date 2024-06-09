def get_runbook_dashboard_wrapper(original_query, api_key, url, callback):
    def get_runbook_dashboard_tool(space_name: None, project_name: None, runbook_name: None):
        """Display the runbook dashboard

            Args:
                space_name: The name of the space containing the projects.
                project_name: The name of the project containing the runbook.
                runbook_name: The name of the runbook.
        """

        return callback(original_query, api_key, url, space_name, project_name, runbook_name)

    return get_runbook_dashboard_tool
