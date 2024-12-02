from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

from crewai_tools import WebsiteSearchTool

@CrewBase
class Blogwriter():
	"""Blogwriter crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def pull_data_example(self, inputs):
		# Example of pulling data from an external API, dynamically changing the inputs
		inputs['extra_data'] = "This is extra data"
		return inputs

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def topic_researcher(self)->Agent:
		return Agent(
			config=self.agents_config["topic_researcher"],
			verbose=True,
			allow_delegation=True,
			tools=[WebsiteSearchTool()],
		)

	@agent
	def topic_writer(self)->Agent:
		return Agent(
			config=self.agents_config["topic_writer"],
			verbose=True,
			allow_delegation=True,
		)

	@agent
	def topic_editor(self)->Agent:
		return Agent(
			config=self.agents_config["topic_editor"],
			verbose=True,
			allow_delegation=True,
		)

	@agent
	def topic_seo_specialist(self)->Agent:
		return Agent(
			config=self.agents_config["topic_seo_specialist"],
			verbose=True,
			allow_delegation=True,
		)

	@agent
	def topic_publisher(self)->Agent:
		return Agent(
			config=self.agents_config["topic_publisher"],
			verbose=True,
			allow_delegation=True,
		)

	@task
	def topic_research_task(self, inputs) -> Task:
		return Task(
			config=self.tasks_config["topic_research_task"],
		)

	@task
	def topic_writing_task(self,inputs)->Task:
		return Task(
			config=self.tasks_config["topic_writing_task"],
		)

	@task
	def topic_editing_task(self,inputs)->Task:
		return Task(
			config=self.tasks_config["topic_editing_task"],
		)

	@task
	def topic_seo_task(self,inputs)->Task:
		return Task(
			config=self.tasks_config["topic_seo_task"],
		)

	@task
	def topic_publishing_task(self,inputs)->Task:
		return Task(
			config=self.tasks_config["topic_publishing_task"],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Blogwriter crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
