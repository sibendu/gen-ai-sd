# Standard library imports
from datetime import datetime
import json
from threading import Thread
from uuid import uuid4

# Related third-party imports
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from dotenv import load_dotenv

# Local application/library specific imports
from crew import CompanyResearchCrew
from job_manager import append_event, jobs, jobs_lock, Event
from utils.logging import logger


load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def kickoff_crew(job_id, companies: list[str], positions: list[str]):
    logger.info(f"Crew for job {job_id} is starting")
    #print(f"Crew for job {job_id} is starting")

    results = None
    try:
        company_research_crew = CompanyResearchCrew(job_id)
        #print("Before setting input") 
        company_research_crew.setup_crew(
            companies, positions)
        #print("After setting input") 
        results = company_research_crew.kickoff()
        logger.info(f"Crew for job {job_id} is complete", results)	
        #print(f"Crew for job {job_id} is complete", results)
  
    except Exception as e:
        logger.error(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)

    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))


@app.route('/api/crew', methods=['POST'])
def run_crew():
    logger.info("Received request to run crew")
    #print("Received request to run crew")
    # Validation
    data = request.json
    if not data or 'companies' not in data or 'positions' not in data:
        abort(400, description="Invalid input data provided.")

    job_id = str(uuid4())
    companies = data['companies']
    positions = data['positions']

    thread = Thread(target=kickoff_crew, args=(
        job_id, companies, positions))
    thread.start()
    
    #print("Started job: "+job_id) 		
    return jsonify({"job_id": job_id}), 202


@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    #print("In get_status(): "+job_id)
    #print(jobs_lock)
    with jobs_lock:
        #print("here 1") 
        job = jobs.get(job_id)
        #print(job) 
        if job is None:
            print("job None") 
            abort(404, description="Job not found")

    # Parse the job.result string into a JSON object
    ''' 
    try:
        #print(job.result)	
        result_json = json.loads(job.result)    
        #print(result_json)
    except json.JSONDecodeError:
        # If parsing fails, set result_json to the original job.result string
        result_json = job.result
    '''
 	
    resp = jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": job.result,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })
    #print(resp)
    return resp  


if __name__ == '__main__':
    app.run(debug=True, port=3001)
