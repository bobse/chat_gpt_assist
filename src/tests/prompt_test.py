import unittest
from exceptions.invalid_prompt import InvalidPromptException

from prompt.prompt import Prompt


class TestPrompt(unittest.TestCase):
    def test_valid_prompt(self):
        input_variables = {
            "answers": ["answer 1", "answer 2"],
            "string_variable": "this should be a text",
        }

        p = Prompt(
            "Question: {query}. Possible answers: {answers}, {string_variable}",
            input_variables,
        )

        question = "this is the question?"
        expected_answer = f"Question: {question}. Possible answers: answer 1\n answer 2, {input_variables['string_variable']}"

        self.assertEqual(expected_answer, p.generate(question))

    def test_reject_prompt_with_no_query_placeholder(self):
        with self.assertRaises(InvalidPromptException):
            Prompt("Question: Possible answers: {answers}, {string_variable}"),
