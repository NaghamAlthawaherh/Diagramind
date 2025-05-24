<<<<<<< HEAD
import json
import datetime
from app.storage.memory import storage

def update_session(session_id, step, message, completed=False):
    """Update the analysis session status"""
    session = storage.get_analysis_session(session_id)
    if not session:
        return

    # Parse step progress JSON
    if isinstance(session["stepProgress"], str):
        step_progress = json.loads(session["stepProgress"])
    else:
        step_progress = session["stepProgress"]

    # Update the specific step
    if step in step_progress:
        step_progress[step]["status"] = "complete" if completed else "in_progress"
        step_progress[step]["message"] = message
        if completed:
            step_progress[step]["completedAt"] = datetime.datetime.now().isoformat()

    # Count completed steps
    completed_steps = sum(1 for s in step_progress.values() if s["status"] == "complete")

    # Determine next step
    current_step = get_next_step(step) if completed else step

    # Update session
    storage.update_analysis_session(session_id, {
        "currentStep": current_step,
        "completedSteps": completed_steps,
        "stepProgress": json.dumps(step_progress)
    })


def get_next_step(current_step):
    """Return the next step in the workflow"""
    steps = [
        "imageProcessing",
        "ocrExtraction",
        "requirementsAnalysis",
        "estimationCalculation",
        "reportGeneration"
    ]
    try:
        index = steps.index(current_step)
        if index < len(steps) - 1:
            return steps[index + 1]
    except ValueError:
        pass
    return "completed"
=======
import json
import datetime
from app.storage.memory import storage

def update_session(session_id, step, message, completed=False):
    """Update the analysis session status"""
    session = storage.get_analysis_session(session_id)
    if not session:
        return

    # Parse step progress JSON
    if isinstance(session["stepProgress"], str):
        step_progress = json.loads(session["stepProgress"])
    else:
        step_progress = session["stepProgress"]

    # Update the specific step
    if step in step_progress:
        step_progress[step]["status"] = "complete" if completed else "in_progress"
        step_progress[step]["message"] = message
        if completed:
            step_progress[step]["completedAt"] = datetime.datetime.now().isoformat()

    # Count completed steps
    completed_steps = sum(1 for s in step_progress.values() if s["status"] == "complete")

    # Determine next step
    current_step = get_next_step(step) if completed else step

    # Update session
    storage.update_analysis_session(session_id, {
        "currentStep": current_step,
        "completedSteps": completed_steps,
        "stepProgress": json.dumps(step_progress)
    })


def get_next_step(current_step):
    """Return the next step in the workflow"""
    steps = [
        "imageProcessing",
        "ocrExtraction",
        "requirementsAnalysis",
        "estimationCalculation",
        "reportGeneration"
    ]
    try:
        index = steps.index(current_step)
        if index < len(steps) - 1:
            return steps[index + 1]
    except ValueError:
        pass
    return "completed"
>>>>>>> 67ec19d3bb81bee2df6432acd2183c7468b661b9
