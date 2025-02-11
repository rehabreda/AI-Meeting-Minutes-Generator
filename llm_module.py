import ollama
import re 





def generate_meeting_minutes(transcription):
    system_message = """You are an expert assistant specializing in generating concise and actionable meeting minutes from audio transcripts. Your goal is to extract meaningful insights, key discussions, and actionable next steps from the provided text, even with potentially limited information."""

    user_prompt = f"""Generate meeting minutes from the following transcript. Focus on extracting:

    1. Key Discussion Points
    - Main topics discussed
    - Important insights
    - Significant conversations

    2. Takeaways
    - Core learnings
    - Critical insights
    - Strategic implications

    3. Action Items
    - Specific tasks or next steps
    - Prioritize clear, actionable items
    - Include any suggested responsibilities (if mentioned)

    Transcript:
    {transcription}


    Guidelines:
    - Be concise and precise
    - Extract value even from fragmented conversation
    - Prioritize actionable information
    - Use markdown formatting
    - If information is unclear or missing, note it appropriately
    - Include dates, locations, or names only if they are explicitly mentioned in the transcript """

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_prompt}
    ]
    MODEL='deepseek-r1'
    response = ollama.chat(model=MODEL, messages=messages)
    result=response['message']['content']
    meeting_minutes = re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)
    return meeting_minutes


# ## test 
# # Open the file in read mode
# with open('output1.txt', 'r') as file:
#     # Read the file content into a string
#     transcription = file.read()
# response=generate_meeting_minutes(transcription)
# # Now, file_content contains the text as a string
# print(response)