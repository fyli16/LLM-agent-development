from openai import OpenAI
client = OpenAI()

result = client.chat.completions.create(
  model='gpt-5-nano', 
  messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}, 
    # {'role': 'user', 'content':'write a poem about tree structure in programming.'}
    # {'role': 'user', 'content':'what is the capital of France'}
    {'role': 'user', 'content':'what is the weather like in Paris?'}
  ]
)

print(result)
print('')
print(result.choices[0].message)
print('')
print(result.choices[0].message.content)
print('')
print(result.choices[0].message.tool_calls)

"""
ChatCompletion(
  id='chatcmpl-C4DJz4z8Xg3Smipr9jiJURdUp6Zzu', 
  choices=[Choice(finish_reason='stop', index=0, logprobs=None, 
    message=ChatCompletionMessage(
      content='Paris. It is the capital and largest city of France.', 
      refusal=None, role='assistant', annotations=[], audio=None, 
      function_call=None, 
      tool_calls=None)
      )
  ], 
  created=1755120555, 
  model='gpt-5-nano-2025-08-07', 
  object='chat.completion', 
  service_tier='default', 
  system_fingerprint=None, 
  usage=CompletionUsage(
    completion_tokens=213, prompt_tokens=22, total_tokens=235, completion_tokens_details=CompletionTokensDetails(
      accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=192, rejected_prediction_tokens=0
    ), 
    prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)
  )
)

ChatCompletionMessage(content='Paris. It is the capital and largest city of France.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)

Paris. It is the capital and largest city of France.

None
"""

