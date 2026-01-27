import logging
import os

from openai import OpenAI

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class MinutesGenerator:
  def __init__(self, max_tokens:int) -> None:
    self.system_prompt = os.getenv("SYSTEM_PROMPT", "You are a professional meeting minutes generator. Extract key points, action items, and decisions from the transcription.")
    self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
    self.model = 'gpt-4o'
    self.token_limit = max_tokens
    
  def generate(self, meeting_transcription:str):
    if not meeting_transcription:
      logging.error("Transcription is null or empty")
      return
    
    if os.path.exists(meeting_transcription):
      with open(meeting_transcription, 'r') as file:
        meeting_transcription = file.read()
      
    meeting_chunks = [meeting_transcription[i:i + self.token_limit] for i in range(0, len(meeting_transcription), self.token_limit)]
    logging.info("Generating meeting minutes")
    
    with open('minutes.txt', 'w') as file:
      for chunk in meeting_chunks:
        response = self.client.chat.completions.create(model=self.model,
          messages=[
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": chunk}
          ],
          max_tokens=self.token_limit,
          temperature=0.2,
          top_p=1
        )
        
        minutes_chunk = response.choices[0].message.content
        if not minutes_chunk:
          logging.error("Error generating minutes for chunk")
          return
        
        file.write(minutes_chunk)
    
    logging.info('Finished generating minutes')