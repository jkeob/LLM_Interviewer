from pydantic import BaseModel


class AgentResponses(BaseModel):
    agent_id: str
    reasoning_understanding_response: str
    relevant_capabilities_response: str
    limitations_response: str
    demo_task_response_1: str
    demo_task_response_2: str
    demo_task_response_3: str
