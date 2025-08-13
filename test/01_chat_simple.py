from openai import OpenAI
client = OpenAI()

result = client.chat.completions.create(
  model='gpt-5-nano', 
  messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'}, 
    {'role': 'user', 'content':'write a poem about tree structure in programming.'}
  ]
)

# print(result)
# print(results.choices[0].message)
print(result.choices[0].message.content)

"""
ChatCompletion(
  id='chatcmpl-C498A1zP4LtS9NajHi8OkLBqo0kdO', 
  choices=[
    Choice(finish_reason='stop', index=0, logprobs=None, 
      message=ChatCompletionMessage(
        content="In the realm of code where logic flows,  \nA mighty tree with branches grows,  \nIts roots are deep, its purpose clear,  \nA structured form that we hold dear.  \n  \nAt the base, the trunk so strong,  \nThe heart of logic, where we belong.  \nFrom node to node, we weave a tale,  \nA journey through the binary trail.  \n  \nBranches fork, decision made,  \nPaths diverge, and choices laid.  \nLeaf by leaf, with data crowned,  \nIn this tree, the answers found.  \n  \nBalanced trees with grace they stand,  \nTheir height controlled, their reach so grand.  \nRed and black, or AVL,  \nThey keep their order, serve us well.  \n  \nThe leaves of deepest depth reside,  \nIn search and sort, they are our guide.  \nTraversals in in-order, pre, and post,  \nNavigate this structure with utmost boast.  \n  \nBinary, n-ary, a forest grand,  \nWithin this world, all logic's planned.  \nIn every branch, a story spun,  \nA programmer's craft, forever young.  \n  \nSo here's to trees, in code they grow,  \nTheir mighty structures help us show,  \nThat in the language of machine,  \nA simple tree fulfills our dream.", refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)
        )
  ], 
  created=1755104446, 
  model='gpt-4o-2024-08-06', 
  object='chat.completion', 
  service_tier='default', 
  system_fingerprint='fp_07871e2ad8', 
  usage=CompletionUsage(
    completion_tokens=258, prompt_tokens=26, total_tokens=284, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)
  )
)
”“”