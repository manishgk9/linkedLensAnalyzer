def prompt(resume_data):
    if not resume_data:
        return 'Please provide resume data.'

    return f"""
        You are a professional resume coach. Analyze the following resume data and respond ONLY with a VALID JSON object. Do NOT include explanations, markdown, or any extra characters.

        Format:
        {{
        "ats_score": <integer>,
        "summary": "<string>",
        "suggestions": ["<string>", ...],
        "strengths": ["<string>", ...],
        "weak_sections": ["<string>", ...],
        "missing_keywords": ["<string>", ...],
        "formatting_issues": ["<string>", ...],
        "section_scores": {{
            "education": <integer>,
            "experience": <integer>,
            "skills": <integer>,
            "projects": <integer>,
            "certifications": <integer>,
            "formatting": <integer>
        }}
        }}

        Rules:
        - Use only valid JSON (no markdown, no backticks, no \\n or \\" or escaped characters).
        - Use double quotes for all keys and string values.
        - Arrays should be proper JSON arrays.
        - Integers should not be in quotes.
        - Do not wrap the response in ```json or anything else.

        Resume data:
        {resume_data}
        """
