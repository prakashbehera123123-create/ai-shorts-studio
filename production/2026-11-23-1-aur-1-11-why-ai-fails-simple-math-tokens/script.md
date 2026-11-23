# Script: 1 aur 1 = 11? Why AI fails simple math: tokens

Language: English
Target duration: 42s
Voice: owner's cloned voice, English, energetic and plain; short sentences.

Central question: Why does an AI that writes code stumble on simple arithmetic and letter counting?
Payoff: The model reads chunks (tokens), not digits. Commas that force right-to-left grouping largely improved GPT-3.5/GPT-4 arithmetic, so write numbers with commas or hand exact math to a calculator or code tool.
Running example (ILLUSTRATIVE, not a real tokenizer dump): the number 8302447 chopped left to right as [830][244][7] versus 8,302,447 as [8][302][447].
Visual world: classroom chalkboard, robot student at a school desk, token tiles. Opening frame: board reads "8302447 + 2 = ?" and the robot is puzzled. Callback: same board rewritten 8,302,447 + 2 = 8,302,449 with a green tick.
Obstacle before fix: the chunks ignore place value (scenes 4-5) before the comma fix.

## Hook candidates
1. "AI writes code... but long sums?" | pattern: broken belief + on-screen "AI can code. Why can't it add?" | curiosity 5, specificity 4, honesty 5
2. "Why can an AI write code but not add?" | pattern: paradox question | curiosity 4, specificity 3, honesty 3 (implies it always fails)
3. "This AI cannot add two numbers." | pattern: bold claim | curiosity 5, specificity 3, honesty 1 (overclaims, rejected)
Chosen: 1, followed by the intro beat "They can still trip it up. Not the brain. The eyes."

## Beats
| beat | seconds | content |
|---|---|---|
| hook | 0-3 | board "8302447 + 2 = ?", puzzled robot; "AI writes code... but long sums?" |
| context (intro) | 3-6 | names the question; "not the brain, the eyes" (glasses metaphor) |
| explanation | 6-10 | text -> tokens -> model (motion-text B-roll, Lucide icons) |
| example (obstacle) | 10-21 | long number cut left to right in threes, chunks ignore place value; commas move the cut right to left |
| reveal | 21-30 | paper finding in words (GPT-3.5, GPT-4): commas largely improved accuracy; gap shrinks in bigger models |
| example | 30-34 | counting can suffer too (tokenization affects counting) (motion-text B-roll) |
| payoff | 34-40 | write numbers with commas, or use a calculator/code tool; board callback, green tick |
| cta | 40-43 | follow |

## Hook
AI writes code... but long sums?

## Narration
They can still trip it up. Not the brain. The eyes. Models don't read digits. They read tokens, small chunks of text. Picture a long number. Some models cut it left to right, up to three digits at a time. Those chunks ignore place value. Add commas, and the cut moves right to left. Researchers tested GPT-3.5 and GPT-4. Grouping digits right to left with commas largely improved accuracy. In bigger models, the gap shrinks. Counting can suffer too, since tokenization changes how well models count. So for exact math, write numbers with commas. Or ask it to use a calculator or code tool.

## On-screen text
- AI can code. Why can't it add?
- Not the brain. The eyes.
- text -> tokens -> model
- Illustrative: 8302447 -> [830][244][7]
- Commas: 8,302,447 -> [8][302][447]
- GPT-3.5 and GPT-4: commas largely improved accuracy
- The gap shrinks in bigger models
- Letters hide inside tokens (illustrative)
- Use commas, or a calculator / code tool
- Source: Singh and Strouse (2024); Zhang, Cao and You (2024)
- Follow for more AI concepts

## CTA
For more AI concepts like this, follow.

## Claim-to-source map
| id | claim | sources | type |
|---|---|---|---|
| C1 | Many AI models write code yet make arithmetic mistakes; the board sum is an illustrative prop, not a measured result | S1 | interpretation |
| C2 | The cause is how input is tokenized (the "eyes"), not general intelligence; "brain vs eyes" is a metaphor | S1, S2 | interpretation |
| C3 | Models process text as tokens (chunks), not individual digits | S1, S2 | fact |
| C4 | GPT-3.5 and GPT-4 have tokens for numbers of 1 to 3 digits, grouped left to right; the 8302447 split into [830][244][7] is illustrative, not a real tokenizer dump | S1 | fact |
| C5 | Such chunks do not line up with place value (interpretation of the left-to-right grouping) | S1 | interpretation |
| C6 | Commas force right-to-left tokenization; 8,302,447 into [8][302][447] is illustrative | S1 | fact |
| C7 | In GPT-3.5 and GPT-4, forcing right-to-left grouping with commas largely improved arithmetic accuracy; errors were stereotyped | S1 | fact |
| C8 | The gap shrinks with model scale (bigger models), so today's larger models do not always fail | S1 | fact |
| C9 | BPE tokenization causes substantial variation in LLM counting ability, so letter counting suffers too; the letter-tile picture is illustrative | S2 | fact |
| C10 | Practical tip: write numbers with commas (supported by C7); using a calculator or code tool is general practical advice, not a finding of the papers | S1 | interpretation |
| C11 | Robot, classroom board, tiles and glasses are a visual metaphor, labelled illustration | S1, S2 | interpretation |
