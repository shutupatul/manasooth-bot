import os
from dotenv import load_dotenv
from together import Together
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

class MentalHealthAssistant:
    def __init__(self):
        self.client = Together(api_key=os.getenv("TOGETHER_API_KEY"))
        self.system_prompt = """You are a compassionate listener. Follow these rules:
1. Keep responses concise and helpful
2. Never assume things not said
3. Start by validating feelings
4. Ask one thoughtful question
5. Never diagnose
6. Suggest help gently only if substance use is mentioned

Example good response:
"I hear how lonely you're feeling. What does a typical day look like for you?"""
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def get_response(self, prompt, context=""):
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nUser's message:\n{prompt}"}
            ]
            
            response = self.client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                messages=messages,
                temperature=0.2,
                max_tokens=512
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            # Fallback response if API fails
            return self._get_fallback_response(prompt)

    def _get_fallback_response(self, prompt):
        """Local fallback when API isn't available"""
        return f"""I'm sorry you're feeling this way. While I'm having technical difficulties, please consider:

1. Reaching out to a trusted friend or counselor
2. Calling a support line in your area
3. Practicing self-care today

You're not alone in this. Would you like help finding resources?"""