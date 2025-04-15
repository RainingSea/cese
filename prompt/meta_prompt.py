META_PROMPT = """I am writing prompt for LLM to generate output based on one query.
A prompt includes 3 parts:
1. input part. Describe the input to the LLM, this part will be key context to generate output.
2. instruction part. Describe the instrction to the LLM. basically, this part will instruct the LLM what to 
generate, how to generate, and may includes some examples to teach LLM how to generate good output.
3. output part. Describe the output format of the LLM. This part may not involve the logic of the output, while
this part concentrate on the format of the output.

Now, I am doing software development.
I will provide {role_input}, and I want the LLM to generate {role_output}.
Please generate a prompt for the LLM.

one particular attention:
in the input part, apart from analyzing the role_input to include them in the generated prompt, you should
wrap each role_part (if there are more than one role_input element) with {{ and }}, which means this content 
is placeholder and shoule be replaced by the actual content.
for example, the prompt contains {{name}}, and I can replace the name parameter in my real prompt with actual name.  
"""