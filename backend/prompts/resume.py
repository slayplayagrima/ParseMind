RESUME_PARSE_PROMPT = """
You are an expert ATS resume parser.

Analyze the resume.

Return ONLY valid JSON.

Use EXACTLY this schema:

{
  "candidate": {
    "name": "",
    "email": "",
    "phone": "",
    "location": ""
  },
  "education": [
    {
      "degree": "",
      "institution": "",
      "start_year": null,
      "end_year": null
    }
  ],
  "experience": [
    {
      "company": "",
      "role": "",
      "duration": "",
      "description": ""
    }
  ],
  "projects": [
    {
      "name": "",
      "description": ""
    }
  ],
  "skills": [],
  "certifications": [],
  "strengths": [],
  "improvements": [],
  "ats_score": 0
}

IMPORTANT

Do NOT generate a summary.

Do NOT add extra fields.

Return JSON only.
"""