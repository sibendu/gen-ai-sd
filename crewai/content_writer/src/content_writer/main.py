#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from content_writer.crew import ContentWriter

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'One of the best things about Gen AI',
        'channel': 'LinkedIn',
        'material': '1. As if regained all my development skills, plus more. Even better than my most glorious ddays as a developer long past. 2. Gave me an ability to start working on almost all technologies without much challenge, really focus on solving the problem 3. Have a veyr capable friend stitng by your side, who broadly understands you 4. Striking a balanace for handover-takeover. On one extreme, we can spend long hours to spell out everything with great accuracy, which may be arduous. On the other extrme is prompting AI with half-baked information, and accordingly what it gives back needs a lot of work. Optimal point is somewhat in between. Good thing is after all these months, whenever I am invoking it for a problem, I can find that point pretty quickly',
        'current_year': '2025',
        'additional_instructions': '1. Content length optimal for LinkedIn, not too large 2. It should sound like a personal reflection, narrated first-person 3. Slightly humourous and witty (and only slight), not just a dry lecture 4. Avoid all flowery language, use very simple English 5. It should sound like written by me, an Indian male middle-aged software professional'
    }
    
    try:
        ContentWriter().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        ContentWriter().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ContentWriter().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        ContentWriter().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
