import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor
from langchain_experimental.agents import create_pandas_dataframe_agent


_ = load_dotenv(find_dotenv())
api_key = os.getenv("ANTHROPIC_API_KEY")


class CsvAgent:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set in the environment variables."
            )
        self.llm = ChatAnthropic(
            model="claude-3-opus-20240229", temperature=0, api_key=self.api_key
        )

    def GetAgentExecutor(self, df: pd.DataFrame) -> AgentExecutor:
        agent_executor: AgentExecutor = create_pandas_dataframe_agent(
            self.llm,
            df,
            verbose=True,
            agent_type="tool-calling",  # Adjust the agent_type accordingly
            agent_executor_kwargs={"handle_parsing_errors": True},
            allow_dangerous_code=True,  # Ensure you have considered the security implications
        )
        return agent_executor
