# combination of semantic and conversation type memory

import re


def extract_facts(user_input: str) -> dict[str, str]:
    facts = {}

    # this would be later semanticised using LLM to extract the facts

    # in this example, we're assuming that the user's name is the first thing they say
    match = re.search(r"my name is (.+)", user_input, re.IGNORECASE)
    if match:
        facts["name"] = match.group(1).strip()

    # in this example, we're assuming that the user's favorite language is the second-thing they say
    match = re.search(
        r"my favorite language is (.+)",
        user_input,
        re.IGNORECASE,
    )
    if match:
        facts["favorite_language"] = match.group(1).strip()

    return facts  # this return value would be stored in the semantic-memory
