import re
from database import get_lead_info, create_task


# =========================================================
# CONFIRMATION WORDS
# =========================================================

YES = {
    "yes",
    "y",
    "confirm",
    "confirmed",
    "proceed",
    "do it",
    "okay",
    "ok",
}

NO = {
    "no",
    "n",
    "cancel",
    "stop",
    "don't",
    "do not",
}


# =========================================================
# FIND LEAD NAME FROM NORMAL QUESTIONS
# =========================================================

def find_lead_name(message):
    """
    Examples:

    Tell me about Sarah Johnson
    What do you know about Sarah Johnson?
    Show me Sarah Johnson
    Ask about Sarah Johnson
    """

    patterns = [
        r"(?:tell me about|what do you know about|show me|ask about)\s+(.+?)(?:\?|$)",
        r"(?:lead)\s+(.+?)(?:\?|$)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)

        if match:
            name = match.group(1).strip()

            name = re.sub(
                r"\s+(please|thanks|thank you)$",
                "",
                name,
                flags=re.IGNORECASE
            )

            return name.strip()

    return None


# =========================================================
# FORMAT LEAD INFORMATION
# =========================================================

def get_lead_response(name):

    lead = get_lead_info(name)

    if not lead:
        return {
            "reply": f"I couldn't find a lead named {name}.",
            "pending": None
        }

    return {
        "reply": (
            f"Here is the lead information:\n"
            f"Id: {lead.get('id')}\n"
            f"Name: {lead.get('name')}\n"
            f"Email: {lead.get('email')}\n"
            f"Company: {lead.get('company')}\n"
            f"Phone: {lead.get('phone')}\n"
            f"Status: {lead.get('status')}"
        ),
        "pending": None
    }


# =========================================================
# FIND KNOWN LEAD INSIDE TEXT
# =========================================================

def find_lead_in_text(text):
    """
    Searches the text for a lead.

    Example:

    Sarah
    Sarah Johnson
    call Sarah Johnson
    email Sarah Johnson tomorrow
    """

    words = text.split()

    # Try the longest possible combination first.
    for length in range(len(words), 0, -1):

        for start in range(0, len(words) - length + 1):

            candidate = " ".join(
                words[start:start + length]
            ).strip()

            # Remove punctuation
            candidate = candidate.strip(".,?!")

            if not candidate:
                continue

            lead = get_lead_info(candidate)

            if lead:
                return candidate, lead

    return None, None


# =========================================================
# CREATE TASK REQUEST
# =========================================================

def create_task_request(message):
    """
    Supports:

    Create a task for Sarah to call her

    Create a task for Sarah Johnson to call her tomorrow

    Create a task to call Sarah Johnson tomorrow

    Create a follow-up task for Sarah Johnson

    Add a task to email Sarah Johnson tomorrow
    """

    lower = message.lower()

    task_keywords = [
        "create a task",
        "create task",
        "make a task",
        "make task",
        "add a task",
        "add task",
        "follow-up task",
        "follow up task",
        "create a follow up",
        "create follow-up",
    ]

    if not any(keyword in lower for keyword in task_keywords):
        return None

    # -----------------------------------------------------
    # Extract due date
    # -----------------------------------------------------

    due_date = None

    if re.search(r"\btomorrow\b", lower):
        due_date = "tomorrow"

    elif re.search(r"\btoday\b", lower):
        due_date = "today"

    # -----------------------------------------------------
    # PATTERN 1
    #
    # Create a task for Sarah to call her
    # -----------------------------------------------------

    match = re.search(
        r"(?:create|make|add)\s+"
        r"(?:a\s+)?"
        r"(?:follow[- ]?up\s+)?"
        r"task\s+for\s+(.+)",
        message,
        re.IGNORECASE
    )

    if match:

        remaining = match.group(1).strip()

        # Remove due date from text
        remaining = re.sub(
            r"\s+(?:today|tomorrow)$",
            "",
            remaining,
            flags=re.IGNORECASE
        )

        remaining = remaining.rstrip(".?")

        # Try to find the lead in the text
        lead_name, lead = find_lead_in_text(remaining)

        if lead:

            # Find the text after the lead name
            lead_position = remaining.lower().find(
                lead_name.lower()
            )

            after_lead = remaining[
                lead_position + len(lead_name):
            ].strip()

            # Remove "to" from beginning
            if after_lead.lower().startswith("to "):
                after_lead = after_lead[3:].strip()

            task = after_lead

            if not task:
                task = "Follow up with lead"

            task = task.rstrip(".?")

            reply = (
                f"I can create a follow-up task for "
                f"{lead_name}: “{task}”"
            )

            if due_date:
                reply += f" for {due_date}"

            reply += ". Would you like me to proceed?"

            return {
                "reply": reply,
                "pending": {
                    "tool": "create_follow_up_task",
                    "args": {
                        "lead_name": lead_name,
                        "task": task,
                        "due_date": due_date
                    }
                }
            }

    # -----------------------------------------------------
    # PATTERN 2
    #
    # Create a task to call Sarah Johnson tomorrow
    # -----------------------------------------------------

    match = re.search(
        r"(?:create|make|add)\s+"
        r"(?:a\s+)?"
        r"(?:follow[- ]?up\s+)?"
        r"task\s+to\s+(.+)",
        message,
        re.IGNORECASE
    )

    if match:

        remaining = match.group(1).strip()

        # Remove today/tomorrow from end
        remaining = re.sub(
            r"\s+(?:today|tomorrow)$",
            "",
            remaining,
            flags=re.IGNORECASE
        )

        remaining = remaining.rstrip(".?")

        # Find the lead inside the sentence
        lead_name, lead = find_lead_in_text(remaining)

        if not lead:

            return {
                "reply": (
                    "I couldn't identify the lead. "
                    "Please provide the lead name, for example: "
                    "\"Create a task to call Sarah Johnson tomorrow.\""
                ),
                "pending": None
            }

        # -------------------------------------------------
        # Extract action
        # -------------------------------------------------

        task = remaining

        # Remove the lead name from the task if it appears
        task = re.sub(
            re.escape(lead_name),
            "",
            task,
            count=1,
            flags=re.IGNORECASE
        ).strip()

        # Clean up
        task = re.sub(
            r"\s+",
            " ",
            task
        ).strip()

        if not task:
            task = "Follow up with lead"

        task = task.rstrip(".?")

        reply = (
            f"I can create a follow-up task for "
            f"{lead_name}: “{task}”"
        )

        if due_date:
            reply += f" for {due_date}"

        reply += ". Would you like me to proceed?"

        return {
            "reply": reply,
            "pending": {
                "tool": "create_follow_up_task",
                "args": {
                    "lead_name": lead_name,
                    "task": task,
                    "due_date": due_date
                }
            }
        }

    # -----------------------------------------------------
    # Could not understand task
    # -----------------------------------------------------

    return {
        "reply": (
            "Sure. Please tell me the lead name "
            "and what the follow-up task should be."
        ),
        "pending": None
    }


# =========================================================
# EXECUTE CONFIRMED TASK
# =========================================================

def execute_pending(pending):

    if not pending:
        return None

    if pending.get("tool") != "create_follow_up_task":
        return None

    args = pending.get("args", {})

    lead_name = args.get("lead_name")
    task = args.get("task")
    due_date = args.get("due_date")

    if not lead_name or not task:
        return None

    # Verify lead still exists
    lead = get_lead_info(lead_name)

    if not lead:
        return None

    result = create_task(
        lead_name=lead_name,
        task=task,
        due_date=due_date
    )

    return result


# =========================================================
# MAIN CHAT FUNCTION
# =========================================================

def chat(message, history=None):

    message = (message or "").strip()

    if not message:
        return {
            "reply": "Please enter a message.",
            "pending": None
        }

    lower = message.lower()

    # -----------------------------------------------------
    # GREETINGS
    # -----------------------------------------------------

    greetings = {
        "hello",
        "hi",
        "hey",
        "hello!",
        "hi!",
        "hey!",
        "good morning",
        "good afternoon",
        "good evening",
    }

    if lower in greetings:
        return {
            "reply": (
                "Hello! I'm the ConneX AI Operator. "
                "I can look up leads and create follow-up tasks."
            ),
            "pending": None
        }

    # -----------------------------------------------------
    # HELP
    # -----------------------------------------------------

    if lower in {
        "help",
        "what can you do",
        "what can you do?",
        "commands",
    }:
        return {
            "reply": (
                "I can help with:\n\n"
                "• Look up a lead\n"
                "• Show lead information\n"
                "• Create a follow-up task\n\n"
                "Examples:\n"
                "Tell me about Sarah Johnson\n"
                "Create a task for Sarah to call her\n"
                "Create a task to call Sarah Johnson tomorrow"
            ),
            "pending": None
        }

    # -----------------------------------------------------
    # CREATE TASK
    # -----------------------------------------------------

    task_request = create_task_request(message)

    if task_request:
        return task_request

    # -----------------------------------------------------
    # LEAD LOOKUP
    # -----------------------------------------------------

    lead_name = find_lead_name(message)

    if lead_name:
        return get_lead_response(lead_name)

    # -----------------------------------------------------
    # DIRECT LEAD LOOKUP
    # -----------------------------------------------------

    direct_lead = get_lead_info(message)

    if direct_lead:
        return {
            "reply": (
                f"Here is the lead information:\n"
                f"Id: {direct_lead.get('id')}\n"
                f"Name: {direct_lead.get('name')}\n"
                f"Email: {direct_lead.get('email')}\n"
                f"Company: {direct_lead.get('company')}\n"
                f"Phone: {direct_lead.get('phone')}\n"
                f"Status: {direct_lead.get('status')}"
            ),
            "pending": None
        }

    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    return {
        "reply": (
            "I can look up leads or create follow-up tasks. "
            "Try: “Tell me about Sarah Johnson” or "
            "“Create a task for Sarah to call her”."
        ),
        "pending": None
    }