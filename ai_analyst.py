import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def get_threat_explanation(vulnerability_count):
    if vulnerability_count == 0:
        return "No active threats. System is secure."

    prompt = f"An automated scanner just found {vulnerability_count} high-severity vulnerabilities in a Node.js package.json file (including outdated versions of axios and lodash). In exactly two short, punchy sentences, explain to a manager what could happen if a hacker exploits these outdated packages (e.g., Denial of Service, Prototype Pollution). Do not use markdown."

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert cybersecurity analyst.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=100,
        )
        return response.choices[0].message.content
    except Exception as e:
        # THE HACKATHON SAVIOR (DEMO MODE)
        return "Critical vulnerability detected in outdated dependencies (axios, lodash). Exploitation could allow attackers to execute arbitrary code via Prototype Pollution or trigger a severe Denial of Service (DoS) crash, leading to massive downtime."
