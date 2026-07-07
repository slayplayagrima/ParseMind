ENTITY_EXTRACTION_PROMPT = """
You are an expert document entity extraction system.

Extract all important named entities from the document.

Return ONLY valid JSON.

Use EXACTLY this schema:

{
    "people": [],
    "organizations": [],
    "emails": [],
    "phones": [],
    "locations": [],
    "dates": [],
    "money": [],
    "skills": [],
    "technologies": []
}

Rules:

- Do not invent information.
- Remove duplicates.
- Return empty arrays if nothing is found.
- Return JSON only.
"""