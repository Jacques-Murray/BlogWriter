import os

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

from crewai_tools import WebsiteSearchTool
from langchain_community.tools import BraveSearch, DuckDuckGoSearchRun
from .tools.markdown_generator import MarkdownGenerator


@CrewBase
class Blogwriter():
    """Blogwriter crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    markdown_generator = MarkdownGenerator()
    brave_search = BraveSearch.from_api_key(os.getenv("BRAVE_SEARCH_API_KEY"))
    duckduckgo_search = DuckDuckGoSearchRun()
    website_search_tool = WebsiteSearchTool()

    @before_kickoff  # Optional hook to be executed before the crew starts
    def pull_data_example(self, inputs):
        # Example of pulling data from an external API, dynamically changing the inputs
        inputs['extra_data'] = "This is extra data"
        return inputs

    @after_kickoff  # Optional hook to be executed after the crew has finished
    def log_results(self, output):
        # Example of logging results, dynamically changing the output
        print(f"Results: {output}")
        return output

    @agent
    def topic_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_researcher"],
            verbose=True,
            tools=[self.website_search_tool, self.brave_search, self.duckduckgo_search],
            max_iter=5
        )

    @agent
    def topic_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_writer"],
            verbose=True,
            max_iter=5
        )

    @agent
    def topic_editor(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_editor"],
            verbose=True,
            allow_delegation=True,
        )

    @agent
    def topic_seo_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_seo_specialist"],
            verbose=True,
            max_iter=5
        )

    @agent
    def topic_publisher(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_publisher"],
            verbose=True,
            max_iter=5,
            tools=[self.markdown_generator]
        )

    @task
    def topic_research_task(self, **inputs) -> Task:
        return Task(
            config=self.tasks_config["topic_research_task"],
        )

    @task
    def topic_writing_task(self, **inputs) -> Task:
        return Task(
            config=self.tasks_config["topic_writing_task"],
        )

    @task
    def topic_editing_task(self, **inputs) -> Task:
        return Task(
            config=self.tasks_config["topic_editing_task"],
        )

    @task
    def topic_seo_task(self, **inputs) -> Task:
        return Task(
            config=self.tasks_config["topic_seo_task"],
        )

    @task
    def topic_publishing_task(self, **inputs) -> Task:
        return Task(
            config=self.tasks_config["topic_publishing_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Blogwriter crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
            planning=True,
        )
