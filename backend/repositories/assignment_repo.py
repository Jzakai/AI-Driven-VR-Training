def insert_assignment(trainee_id, scenario_id):
    supabase.table("assigned_courses").insert({
        "trainee_id": trainee_id,
        "scenario_id": scenario_id
    }).execute()
