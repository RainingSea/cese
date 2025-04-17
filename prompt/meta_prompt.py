META_PROMPT = """
---
I'm using an LLM to generate {role_output}, and this is part of the prompt I designed. 
My prompt is mainly divided into three parts: input, instruction, and output specification. 
The input describes what input the model will receive for this task; 
the output format or attention mainly defines the formatting requirements. They have already been defined and should not be changed.

Now, I want you to help me write the "instruction" section, which describes how the LLM should generate each output in the "format example."
Please consider how to design the instruction section (following the given formatting requirements), and then return only the content of the instruction section.
"""

META_PROMPT_OLD = """I am writing prompt to generate output based on one query.
A prompt includes 3 parts:
1. Describe the input to the LLM, this part introduces what content the LLM will receive, these content usually are key context needed.
I want you to write this part from my perspective (the user's perspective) to order LLM, not as a third-party observer.
You should wrap each role_input element (if there are more than one role_input element) with {{ and }}, 
which means this content is a placeholder and should be replaced by the actual content when I invoke the LLM.
such as, if I provide "document", then the prompt must include content like "the document is: {{document}} XXX", to let me replace it when I invoke LLM.

2. Describe the instrction to the LLM. This part will instruct the LLM what to generate and how to generate it.
Importantly, you should includes 1 or 2 helpful examples in this part to teach LLM how to generate good output.
Write this part in a tone that gives instructions to the LLM.

3. Describe the output format of the LLM. This part may not involve the logic of the output but focuses on the format of the output.
Again, write this part from my perspective.

Now, I am doing software development.
I will provide {role_input}, and I want the LLM to generate {role_output}.
Please generate a prompt for the LLM.

you could add more reasoning process, but the generated prompt should begin with [PROMPT] and end with another [PROMPT] within your output. I will use RegExp to extract generated prompt.

one particular attention:
in the input part, apart from analyzing the role_input to include them in the generated prompt, you should wrap each role_input element (if there are more than one role_input element) with {{ and }}, which means this content is placeholder and shoule be replaced by the actual content.

Only the specific elements provided as part of {role_input} should be enclosed with {{ and }}. 
Do not enclose any other text within {{ and }}, as doing so may lead to errors in generating the prompt.
"""
