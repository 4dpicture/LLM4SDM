# LLM4SDM


# Hallucination of Medical LLMs
Example of Meditron7b model hallunication on output is show in file "meditron_7b.130002_NL.txt", where the model generated score 3 for all items first; then score 0 for all items in the 2nd run. It also used the same justification for all OPTION12 items.

MedLlama also produced hallucination in the initial deployment when it generated score 1 for all OPTION12 items and even gave a mean score 10 very wrongly by averaging individual scores, as in file "medllama2_7b.110019_NL.txt". However, it did give different justifications and evidences across OPTION12 items.

# Two stages of development - Developing phase
We share the code of our prompting LLMs to do the SDM tasks
(we share this first, which we already have, for the development stage)

# Two stages of development - Deploying phase
We share our code of using LLM-judge to resolve disagreement of other OS-sLLMs.


