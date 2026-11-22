REPORT_PARSE_PROMPT = """
You are an expert analyst who reads business, research and technical reports.

Extract the substance of the report.

Return ONLY valid JSON.

Use EXACTLY this schema:

{
  "title": null,
  "report_type": null,
  "authors": [],
  "organization": null,
  "publication_date": null,
  "purpose": null,

  "key_findings": [],

  "metrics": [
    {
      "name": "",
      "value": "",
      "context": null
    }
  ],

  "conclusions": [],
  "recommendations": [],
  "limitations": []
}

Rules:

- report_type is a short label, for example "Annual report", "Research paper",
  "Market analysis" or "Incident report".
- key_findings are the most important results, one sentence each, at most 8.
- metrics are numbers the report states, with the value exactly as written,
  for example "Revenue" / "$4.2M" / "FY2025, up 12% year on year".
- recommendations and limitations only if the report states them.
- Use null or [] for anything not in the report.
- Do not invent information.
- Do not summarize.
- Return JSON only.
"""
