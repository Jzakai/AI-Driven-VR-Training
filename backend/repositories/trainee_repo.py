

def get_trainee_by_id(trainee_id):
    result = supabase.table("trainees").select("*").eq("id", trainee_id).execute()
    return result.data[0] if result.data else None
