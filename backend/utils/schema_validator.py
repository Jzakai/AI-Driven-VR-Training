def validate_scenario_schema(scenario_json):
    if "events" not in scenario_json:
        raise ValueError("Invalid scenario format: missing events")
