def planner_agent(validated):
    plan = "Final Research Summary:\n\n"

    for item in validated:
        plan += f"- {item}\n"

    return plan