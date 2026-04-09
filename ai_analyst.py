import google.generativeai as genai

# Configure the API key
genai.configure(api_key="PASTE_YOUR_KEY_HERE")


def get_threat_explanation(vulnerability_count):
    if vulnerability_count == 0:
        return "No active threats. System is secure."

    # Initialize the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are an expert cybersecurity analyst. An automated scanner just found {vulnerability_count} high-severity vulnerabilities in a Node.js package.json file (including outdated versions of axios and lodash). 
    In exactly two short, punchy sentences, explain to a manager what could happen if a hacker exploits these outdated packages (e.g., Denial of Service, Prototype Pollution). Do not use markdown.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "AI Analysis unavailable at this time."
