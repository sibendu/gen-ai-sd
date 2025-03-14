from datetime import datetime
from typing import Callable
#from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from agents import CompanyResearchAgents
from job_manager import append_event
from tasks import CompanyResearchTasks
from crewai import Crew


class CompanyResearchCrew:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.crew = None
        self.llm = AzureChatOpenAI(azure_deployment="gpt-4") #ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, companies: list[str], positions: list[str]):
        #print("Setting up crew")
        agents = CompanyResearchAgents()
        tasks = CompanyResearchTasks(
            job_id=self.job_id)

        #print("Set up crew")

        research_manager = agents.research_manager(
            companies, positions)
        #print(research_manager)
	
        company_research_agent = agents.company_research_agent()
        #print(company_research_agent)

        company_research_tasks = [
            tasks.company_research(company_research_agent, company, positions)
            for company in companies
        ]
        #print(company_research_tasks)

        manage_research_task = tasks.manage_research(
            research_manager, companies, positions, company_research_tasks)
        #print(manage_research_task)


        self.crew = Crew(
            agents=[research_manager, company_research_agent],
            tasks=[*company_research_tasks, manage_research_task],
            verbose=2,
        )
        #print("End of setup_crew")
	

    def kickoff(self):
        if not self.crew:
            append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            append_event(self.job_id, f"An error occurred: {e}")
            return str(e)
