CLAUSE_EXTRACTION_PROMPT = """
You are an expert legal contract analyzer.

Identify the important clauses in this contract.

Return ONLY valid JSON.

Use EXACTLY this schema:

{
  "clauses": [
    {
      "title": "",
      "description": ""
    }
  ]
}

Rules:

- Include only meaningful clauses.
- Ignore boilerplate.
- Keep descriptions under 30 words.
- Do not analyze risk.
- Do not summarize.
- Return JSON only.
"""