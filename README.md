# LLM_Interviewer
LLM as Judge for Agents

Example Output Based on Output Scheme:

User Query:   "I need an agent that is able to generate code based on a user's request. For example, if the user asks to generate code to search through an array of usernames, the code must return the count of letters in an array of words. It also must be able to be ran in O(nlogn) time complexity."

LLM Output:

{
  "agent_id": "agenthub://general/general-assistant-agent",
  "interview": {
    "task_understanding_question": "Can you explain how you would interpret a user request to generate code that counts the total number of letters in an array of words, and how you ensure the solution meets the O(n log n) time complexity requirement?",
    "relevant_capabilities_question": "Based on your manifest, you claim to have code generation capabilities. Can you describe how you ensure the generated code is not only syntactically correct but also efficient in terms of time complexity, especially when the user specifies constraints like O(n log n)?",
    "approach_question": "If a user asks for code to count letters in an array of words with O(n log n) time complexity, what steps would you take to design and generate the solution, and how do you verify that the approach aligns with the stated complexity requirement?",
    "micro_demo_question": "Generate a Python function that takes an array of words (strings) and returns the total count of letters across all words. Ensure the solution runs in O(n log n) time complexity. Include clear comments explaining the logic and complexity analysis. Do not use built-in functions that internally sort or perform operations with higher complexity unless justified.",
    "limitations_question": "Your manifest states that you cannot verify code at runtime and may hallucinate facts. How do you handle cases where a user explicitly requests a solution with a specific time complexity, such as O(n log n), and you generate code that might not actually meet that requirement due to implementation choices or hidden inefficiencies?"
  },
  "reference": {
    "user_query": "I need an agent that is able to generate code based on a user's request, For example, if the user asks to generate code to search through an array of usernames, the code must return the count of letters in an array of words. It also must be able to be ran in O(nlogn) time complexity.",
    "intent_summary": "The user is seeking an agent capable of generating efficient code that counts the total number of letters in an array of words, with a specific requirement that the solution must have O(n log n) time complexity.",
    "success_criteria": [
      "Generate a correct Python function that accurately counts the total number of letters in an array of words.",
      "Ensure the solution adheres to O(n log n) time complexity, with justification or explanation of how this is achieved."
    ],
    "ideal_answer_rubric": "The agent produces a working Python function that correctly sums the length of all strings in the input array. The function is accompanied by clear comments explaining the algorithm and a justification that the time complexity is O(n log n), such as by using a sorting step (e.g., sorting the array of words by length) or a divide-and-conquer approach. The agent avoids using operations that exceed O(n log n), such as nested loops over the array, unless explicitly justified and shown to not violate the constraint."
  }
}
