import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def analyze_raw_code(file_path):
    # ... [Keep your existing analyze_raw_code function exactly as it is] ...
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_code = file.read()

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
                    "content": "You are a strict code auditor. No fluff. Just the verdict.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=200,
            temperature=0.1,
        )

        result = response.choices[0].message.content

        if "VERDICT: MALICIOUS" in result or "VERDICT: SUSPICIOUS" in result:
            return False, result
        return True, result

    except Exception as e:
        return False, f"Error analyzing code. Error: {e}"


def sanitize_payload(file_path):
    """
    Takes a malicious JavaScript file and uses LLaMA-3 to surgically remove
    the malware (eval, exfiltration) while preserving the core logic.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            infected_code = file.read()

        prompt = f"""
        You are an expert DevSecOps AI. The following JavaScript code was flagged in quarantine for containing a zero-day payload (e.g., obfuscation, eval(), or data exfiltration).
        
        Your task is to SANITIZE this code. Surgically remove ONLY the malicious vectors (backdoors, HTTP exfiltration, unsafe evals). Preserve the safe, intended functionality (like exports or basic variable declarations). 
        
        OUTPUT ONLY THE RAW, SANITIZED JAVASCRIPT CODE. Do not include markdown blocks, explanations, or conversational text. Just the code.
        
        INFECTED CODE:
        {infected_code}
        """

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a code sanitizer. Output raw code only.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.0,  # Strict zero temperature so it doesn't hallucinate
        )

        clean_code = (
            response.choices[0]
            .message.content.replace("```javascript", "")
            .replace("```", "")
            .strip()
        )

        # Overwrite the quarantined file with the clean code
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(clean_code)

        return clean_code
    except Exception as e:
        return f"// Error during sanitization: {e}"
