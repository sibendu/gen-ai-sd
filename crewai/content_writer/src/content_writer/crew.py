# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

@CrewBase
class ContentWriter():
  """LatestAiDevelopment crew"""

  @agent
  def writer(self) -> Agent:
    return Agent(
      config=self.agents_config['writer'],
      verbose=True,
      tools=[SerperDevTool()]
    )

  @agent
  def critic(self) -> Agent:
    return Agent(
      config=self.agents_config['critic'],
      verbose=True
    )

  @agent
  def editor(self) -> Agent:
    return Agent(
      config=self.agents_config['editor'],
      verbose=True
    )

  @task
  def write_task(self) -> Task:
    return Task(
      config=self.tasks_config['write_task'],
    )

  @task
  def review_task(self) -> Task:
    return Task(
      config=self.tasks_config['review_task']
    )

  @task
  def editing_task(self) -> Task:
    return Task(
      config=self.tasks_config['editing_task'],
      output_file='output/report.md' # This is the file that will be contain the final report.
    )

  @crew
  def crew(self) -> Crew:
    """Creates the LatestAiDevelopment crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=True,
    )
