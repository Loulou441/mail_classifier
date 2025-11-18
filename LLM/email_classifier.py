import time
import json
from typing import List, Dict
from groq import Groq, RateLimitError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# --- Exponential Backoff Retry Decorator ---
@retry(
    # Stop retrying after 5 attempts
    stop=stop_after_attempt(5),
    # Wait 2^x * 1 second between retries, up to 10 seconds
    wait=wait_exponential(multiplier=1, min=2, max=10),
    # Only retry if the exception is a RateLimitError
    retry=retry_if_exception_type(RateLimitError),
    # CORRECTED LINE: Access 'sleep' as an attribute, not a method
    before_sleep=lambda retry_state: print(
        f"Rate limit reached. Retrying in {retry_state.next_action.sleep}s... (Attempt {retry_state.attempt_number}/5)"
    )
)
def create_chat_completion_with_retry(client: Groq, model_name: str, messages: List[Dict], temperature: float):
    """A wrapper function to call the Groq API with automatic retries on RateLimitError."""
    return client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=temperature
    )

# ... The rest of your EmailClassifier class remains the same ...
# --- Email Classifier Class ---
class EmailClassifier:

    def __init__(self, api_key: str, model_name: str, verbose: bool = False):
        """
        Initialize Groq client.
        
        Args:
            api_key: Your Groq API key.
            model_name: The name of the model to use (e.g., "mixtral-8x7b-32768").
            verbose: If True, prints detailed information during processing. (New)
        """
        self.client = Groq(api_key=api_key)
        self.model_name = model_name
        self.verbose = verbose  # Store the verbose setting

    def classify_emails(self, emails: List[Dict[str, str]], prompt: str, rules: str) -> List[Dict[str, str]]:
        """
        Classify a list of emails based on prompt + rules.
        """
        results = []

        for i, email in enumerate(emails):
            if self.verbose:
                print(f"\n--- Processing Email {i+1}/{len(emails)}: '{email['subject']}' ---")

            full_instruction = f"""
{prompt}
Voici les règles de classification :
{rules}
E-mail à analyser :
Objet : {email['subject']}
Corps : {email['body']}

"""
            
            if self.verbose:
                print("--- Full Instruction Sent to Model ---")
                print(full_instruction)
                print("-------------------------------------")

            messages = [
                {"role": "system", "content": "You are an email classification assistant. You MUST return a JSON object."},
                {"role": "user", "content": full_instruction}
            ]

            response = None

            try:
                # response = create_chat_completion_with_retry(
                #     client=self.client,
                #     model_name=self.model_name,
                #     messages=messages,
                #     temperature=0.2
                # )
                
                response = self.client.chat.completions.create(
        model=self.model_name,
        messages=messages,
        temperature=0.2
    )
            except RateLimitError as e:
                if self.verbose:
                    print(f"FATAL: Rate limit exceeded after all retries for email: {email['subject']}")
                print(e)
            
            json_output = {}
            if response:
                content = response.choices[0].message.content
                
                if self.verbose:
                    print("--- Raw Model Response Content ---")
                    print(content)
                    print("---------------------------------")
                    
                try:
                    # Robust JSON parsing attempts
                    content = content.strip()
                    if content.startswith('```json'):
                        content = content.strip('```json').strip()
                    if content.startswith('```'):
                         content = content.strip('```').strip()

                    json_output = json.loads(content)
                    print(json_output)
                except json.JSONDecodeError:
                    if self.verbose:
                        print(f"JSON Decode Error for email: {email['subject']}")
                    json_output = {
                        "subject": email["subject"],
                        "priority_level": -1,
                        "summary": "ERROR: The model did not return valid JSON."
                    }
            else:
                json_output = {
                    "subject": email["subject"],
                    "priority_level": -2,
                    "summary": "CRITICAL ERROR: API call failed due to rate limiting or other issue after multiple retries."
                }

            results.append(json_output)

        return results