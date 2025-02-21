
---

### **3. `ai_code_reviewer1.py`**
This is the main Python script for the AI Code Reviewer application.

```python
import streamlit as st
from dotenv import load_dotenv
import os
import openai

# Load API key from .env file
load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app
st.title("AI Code Reviewer")
st.write("Submit your Python code for review and receive feedback on potential bugs and fixes.")

# Input area for Python code
code = st.text_area("Enter your Python code here:", height=300)

# Function to review code using OpenAI
def review_code(code):
    prompt = f"""
    Review the following Python code and identify potential bugs, errors, or areas of improvement.
    Provide a detailed explanation of the issues and suggest fixes. Also, provide the corrected code snippet.

    Code:
    {code}
    """
    
    response = openai.Completion.create(
        engine="text-davinci-003",  # Use GPT-4 if available
        prompt=prompt,
        max_tokens=500,
        temperature=0.5,
    )
    
    review_text = response.choices[0].text.strip()
    
    # Parse the response to separate bugs and fixed code
    bugs = review_text.split("Fixed Code:")[0].strip()
    fixed_code = review_text.split("Fixed Code:")[1].strip() if "Fixed Code:" in review_text else ""
    
    return {
        "bugs": bugs,
        "fixed_code": fixed_code,
    }

# Button to submit code
if st.button("Review Code"):
    if code.strip() == "":
        st.error("Please enter some Python code to review.")
    else:
        review_results = review_code(code)
        
        # Display results
        st.subheader("Code Review Results")
        st.write("### Potential Bugs and Suggestions")
        st.write(review_results.get("bugs", "No bugs found."))
        
        st.write("### Fixed Code Snippet")
        st.code(review_results.get("fixed_code", "No fixes suggested."))
