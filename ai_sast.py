import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_raw_code(file_path):
    """Reads raw JS files to hunt for zero-days and malicious obfuscation."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_code = file.read()

        # Protect the LLM context window
        if len(raw_code) > 15000:
            raw_code = raw_code[:15000] + "\n...[TRUNCATED]"

        prompt = f"""
        You are an advanced Static Application Security Testing (SAST) AI.
        Analyze this JavaScript code for zero-day vulnerabilities, malicious payloads, 
        obfuscated backdoors, Prototype Pollution, or unauthorized data exfiltration.

        Format strictly:
        VERDICT: [SAFE | SUSPICIOUS | MALICIOUS]
        RISK_SCORE: [1-100]
        THREATS_FOUND: [List threats]
        
        CODE TO ANALYZE:
        {raw_code}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strict, merciless code auditor. No fluff. Just the verdict.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.1,
        )

        result = response.choices[0].message.content

        if "VERDICT: MALICIOUS" in result or "VERDICT: SUSPICIOUS" in result:
            return False, result  # Block
        return True, result  # Safe

    except Exception as e:
        return False, "Error analyzing code."
