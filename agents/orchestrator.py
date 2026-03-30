from agents.researcher import research_agent
from agents.analyst import analyst_agent
from agents.critic import critic_agent
from agents.planner import planner_agent


def orchestrator(query):

    # Step 1: Research
    data = research_agent(query)

    # Step 2: Reasoning loop
    for _ in range(2):
        analysis = analyst_agent(data)
        checked = critic_agent(analysis)

        if len(checked) > 0:
            break
        else:
            data = research_agent(query)

    # Step 3: Planning
    final_output = planner_agent(checked)

    return final_output