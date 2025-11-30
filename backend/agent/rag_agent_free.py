import os
from textwrap import dedent

FREE_TESTING_MODE = True   # <<<<<< ENABLES FREE MODE

# ----------------------------
#  MOCK RESPONSES (NO COST)
# ----------------------------
MOCK_SCENARIO_RESPONSE = {
    "mission_narrative": "You are responding to a simulated battlefield in an urban zone. A soldier is injured during fire and requires immediate bleeding control.",
    "scenario_spec": {
        "environment": "urban-alley",
        "skill_category": "Care Under Fire",
        "skill": "Stop Major Bleeding",
        "difficulty": "Intermediate",
        "casualties": [
            {
                "id": "cas1",
                "injury": "Femoral artery bleeding",
                "consciousness": "responsive",
                "vitals": {
                    "pulse": "rapid",
                    "respiration": "shallow"
                }
            }
        ],
        "injects": [
            "Enemy fire approaching",
            "Dust interference reducing visibility"
        ],
        "objectives": [
            "Apply tourniquet",
            "Move casualty to cover"
        ],
        "expected_actions": [
            "Apply tourniquet within 60 seconds",
            "Move the casualty from direct fire"
        ],
        "evaluation_metrics": [
            "Tourniquet placement accuracy",
            "Reaction time"
        ]
    }
}


MOCK_MODIFIED_SCENARIO = {
    "updated_scenario": {
        "note": "This is a mock modified scenario (FREE MODE). No GPT used."
    }
}


# -----------------------------------------
#   MAIN FUNCTION: GENERATE SCENARIO (FREE)
# -----------------------------------------
def generate_scenario_from_agent(skill_category: str, skill: str, difficulty: str):
    if FREE_TESTING_MODE:
        print("⭐ Running in FREE TEST MODE — returning mock scenario")
        return MOCK_SCENARIO_RESPONSE

    # -----------------------------
    # (Your real agent code goes here)
    # -----------------------------
    raise NotImplementedError("Real AI mode disabled in free testing mode")


# -----------------------------------------
#   MODIFICATION FUNCTION (FREE)
# -----------------------------------------
def modify_scenario_with_agent(existing_json, edits):
    if FREE_TESTING_MODE:
        print("⭐ Running FREE TEST MODE — returning mock modified scenario")
        return MOCK_MODIFIED_SCENARIO

    # -----------------------------
    # (Your real agent code goes here)
    # -----------------------------
    raise NotImplementedError("Real AI mode disabled in free testing mode")
