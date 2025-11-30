

def save_scenario(scenario_json, skill, skill_category, difficulty, version):
    result = supabase.table("scenarios").insert({
        "scenario_json": scenario_json,
        "skill": skill,
        "skill_category": skill_category,
        "difficulty": difficulty,
        "version": version
    }).execute()

    return result.data[0]["id"]


def get_scenario_by_id(scenario_id):
    result = supabase.table("scenarios").select("*").eq("id", scenario_id).execute()
    return result.data[0] if result.data else None
