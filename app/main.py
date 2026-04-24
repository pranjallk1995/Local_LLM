import time
import streamlit as st

st.title("Llama3 Chat")

with st.expander(":material/warning: Disclaimer"):
  st.write(
    """
    It is a smaller model running locally on GPU.

    It Cannot keep context for more than one response.

    Hence the UI has no history of messages.
    """
  )
st.divider()

prompt = st.chat_input("Type something")
if prompt:
    st.subheader(":green[:material/face:] :")
    st.write(f"{prompt}")

import asyncio
from ollama import AsyncClient

client = AsyncClient(
  host='http://ollama-serve:11434',
  headers={'x-some-header': 'some-value'}
)

def text_stream(response):
  for data in response['message']['content']:
     yield data
     time.sleep(0.01)

start_time = time.time()
async def chat():
  message = {'role': 'user', 'content': prompt}
  response = await client.chat(model='llama3', messages=[message])
  st.subheader(":blue[:material/smart_toy:] :")
  st.write_stream(text_stream(response))

asyncio.run(chat())

st.divider()
st.write(f":material/timer: response time: :red[{round(time.time() - start_time, 2)}s]")
