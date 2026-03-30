def critic_agent(insights):
    validated = []

    for insight in insights:
        if "AI" in insight or "learning" in insight:
            validated.append(insight)

    return validated