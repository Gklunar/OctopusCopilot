import os
import unittest

from openai import RateLimitError
from retry import retry

from infrastructure.openai import llm_tool_query, llm_message_query
from tests.infrastructure.tools.build_test_tools import build_mock_test_tools


class MockRequests(unittest.TestCase):
    """
    Integration tests verifying calls to the OpenAI service.

    These tests should mostly be focused on ensuring tools are correctly matched to queries by having the correct
    function comments, and that the correct entities are extracted from the query.

    Tests can also submit mock data to verify the response. Be aware that LLMs are non-deterministic, so it can be hard
    to verify the response.

    Use the CopilotChatTest class to verify the function calls work against a real Octopus instance.
    """

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_no_match(self):
        """
        Tests that the llm responds appropriately when no function is a match
        """

        function = llm_tool_query("What is the size of the earth?", build_mock_test_tools)

        self.assertTrue(function.call_function().index("Sorry, I did not understand that request.") != -1)

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_project_question(self):
        """
        Tests that the llm correctly identifies the project name in the query
        """

        function = llm_tool_query("What does the project \"Deploy WebApp\" do?", build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Deploy WebApp" in body["project_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_project_group_question(self):
        """
        Tests that the llm correctly identifies the project group name in the query
        """

        function = llm_tool_query("What is the description of the \"Azure Apps\" project group?", build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Azure Apps" in body["projectgroup_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_runbook_question(self):
        """
        Tests that the llm correctly identifies the runbook name in the query
        """

        function = llm_tool_query(
            "What is the description of the \"Backup Database\" runbook defined in the \"Runbook Project\" project.",
            build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Backup Database" in body["runbook_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_tenant_question(self):
        """
        Tests that the llm correctly identifies the tenant name in the query
        """

        function = llm_tool_query("Describe the \"Team A\" tenant.", build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Team A" in body["tenant_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_feed_question(self):
        """
        Tests that the llm correctly identifies the feed name in the query
        """

        function = llm_tool_query("Does the \"Helm\" feed have a password?.", build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Helm" in body["feed_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_account_question(self):
        """
        Tests that the llm correctly identifies the feed name in the query
        """

        query = "What is the access key of the \"AWS Account\" account?."

        function = llm_tool_query(query, build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("AWS Account" in body["account_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_variable_set_question(self):
        """
        Tests that the llm correctly identifies the library variable set name in the query
        """

        function = llm_tool_query("List the variables belonging to the \"Database Settings\" library variable set.",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Database Settings" in body["library_variable_sets"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_worker_pool_question(self):
        """
        Tests that the llm correctly identifies the worker pool name in the query
        """

        function = llm_tool_query("What is the description of the \"Docker\" worker pool?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Docker" in body["workerpool_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_certificate_question(self):
        """
        Tests that the llm correctly identifies the certificate name in the query
        """

        function = llm_tool_query("What is the note of the \"Kind CA\" certificate?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Kind CA" in body["certificate_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_tagset_question(self):
        """
        Tests that the llm correctly identifies the tagset name in the query
        """

        function = llm_tool_query("List the tags associated with the \"region\" tag set?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("region" in body["tagset_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_lifecycle_question(self):
        """
        Tests that the llm correctly identifies the lifecycle name in the query
        """

        function = llm_tool_query("What environments are in the \"Simple\" lifecycle?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Simple" in body["lifecycle_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_git_creds_question(self):
        """
        Tests that the llm correctly identifies the git credentials name in the query
        """

        function = llm_tool_query("What is the username for the \"GitHub Credentials\" git credentials?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("GitHub Credentials" in body["gitcredential_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_machine_policy_question(self):
        """
        Tests that the llm correctly identifies the machine policy name in the query
        """

        function = llm_tool_query(
            "Show the powershell health check script for the \"Windows VM Policy\" machine policy.",
            build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Windows VM Policy" in body["machinepolicy_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_environment_question(self):
        """
        Tests that the llm correctly identifies the environment in the query
        """

        function = llm_tool_query(
            "List the variables scoped to the \"Development\" environment in the project \"Deploy WebApp\".",
            build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Development" in body["environment_names"], "body")
        self.assertTrue("Deploy WebApp" in body["project_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_unknown_arguments(self):
        """
        Sometimes unknown arguments are passed to functions. The query below has, in the past, passed an argument called
        "type" to the answer_general_query function. This behaviour is not consistent, but happens enough that any function
        should have an **kwargs argument to handle these cases. This test ensures that a query that has been shown to
        pass unknown arguments in the past does not break the function.
        """

        function = llm_tool_query(
            "Find steps in the \"Commercial Billing\" project with a type of \"Octopus.Manual\". Double check the type of each step to ensure it is \"Octopus.Manual\". Show the step name and type in a markdown table.",
            build_mock_test_tools)

        # Not raising an exception here is the test
        function.call_function()

        self.assertEqual(function.name, "answer_general_query")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_variable_question(self):
        """
        Tests that the llm responds appropriately when no function is a match
        """

        function = llm_tool_query("Where is the variable \"Database\" used in the project \"Project1\"?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Database" in body["variable_names"], "body")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_project_step_question(self):
        """
        Tests that the llm identifies the step name in the query
        """

        function = llm_tool_query("What do does the step \"Manual Intervention\" in the \"Project1\" do?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Manual Intervention" in body["step_names"])

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_date_question(self):
        """
        Tests that the llm identifies the step name in the query
        """

        function = llm_tool_query("Find deployments after \"1st Jan 2024\" and before \"2nd Mar 2024\"?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue(body["dates"][0] == '2024-01-01T00:00:00+00:00')
        self.assertTrue(body["dates"][1] == '2024-03-02T00:00:00+00:00')

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_machine_question(self):
        """
        Tests that the llm identifies the machine name in the query
        """

        function = llm_tool_query("Show the details of the machine \"Cloud Region target\"?",
                                  build_mock_test_tools)
        body = function.call_function()

        self.assertEqual(function.name, "answer_general_query")
        self.assertTrue("Cloud Region target" in body["target_names"], "body")

    def test_documentation_question(self):
        """
        Tests that the llm identifies queries answered by documentation
        """

        self.assertEqual(llm_tool_query("How do I enable Azure AD?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("How do I create a new azure target?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("How do I enable the ServiceNow integration?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("How do I setup a polling Tentacle?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("How do I add a Worker?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("How do I use Community Step templates?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("Where do I enable Config-as-code for a project?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("How do I use lifecycles",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("Where do I view the DORA metrics for my space?",
                                        build_mock_test_tools).name, "how_to_usage")
        self.assertEqual(llm_tool_query("Where can I see deployment frequency?",
                                        build_mock_test_tools).name, "how_to_usage")

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_general_prompt(self):
        """
        Tests that the llm responds some response to a general prompt
        """

        response = llm_message_query([
            ('system', 'You are a helpful agent.'),
            ('user', '{input}')
        ],
            {"input": 'What is the size of the earth?'})

        # Make sure we get some kind of response
        self.assertTrue(response)

    @retry((AssertionError, RateLimitError), tries=3, delay=2)
    def test_long_prompt(self):
        """
        Tests that the llm fails with the expected message when passed too much context
        """

        current_file_path = os.path.abspath(__file__)
        path_without_filename = os.path.dirname(current_file_path)

        with open(os.path.join(path_without_filename, 'large_example.tf'), 'r') as file:
            data = file.read()

        response = llm_message_query([
            ('system', 'You are a helpful agent.'),
            ('user', '{input}'),
            ('user', '###\n{hcl}\n###')
        ],
            {"input": 'What does this project do?', "hcl": data})

        # Make sure we get some kind of response
        self.assertTrue(response.index("reduce the length of the messages") != -1)


if __name__ == '__main__':
    unittest.main()
