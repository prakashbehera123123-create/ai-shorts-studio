# Fact check: GPT-6.2 Astra/Sol "what to check before you switch"

Audited 2026-11-20. Primary re-opened: OpenAI API changelog, Nov 17 entry (gpt-6.2-astra, gpt-6.2-sol; v1/responses, v1/chat/completions). GitHub changelog 2026-11-17 re-opened (availability only; not used by this script).

| claim | claim text | verdict | source | note |
|---|---|---|---|---|
| C1 | Switching to GPT-6.2 can change application behaviour | qualified | S2, S3 | Changelog: GPT-6.2 changes how the Responses API preserves reasoning on prefix edits and how it handles the top-level instructions field. The behaviour changes are scoped to the Responses API; the hook states it for any app. Add "if you use the Responses API" somewhere, or soften to "can change how some apps behave". |
| C2 | OpenAI released two variants, Astra and Sol | supported | S1 | Changelog names two models, gpt-6.2-astra and gpt-6.2-sol. "Variants" is our word, acceptable; "models" is closer to the source. No ranking present. |
| C3 | Both support the Responses API and Chat Completions | supported | S2 | Exact: "Both models support the Responses API and Chat Completions." |
| C4 | The changelog notes differences for GPT-6.2; picking three to test is our framing (revised) | supported | S2, S3 | Original claim (changelog lists three checks) was unsupported; revised wording labels the selection as ours. The three items appear verbatim in the Nov 17 entries. Re-verified by main session 2026-11-20. |
| C5 | Tool calling requires the Responses API | supported | S2 | Exact: "Tool calling requires the Responses API." |
| C6 | App that calls tools through Chat Completions must move to the Responses API | qualified | S2 | Source supports only "tool calling requires the Responses API" for these models. "Must move" is an inference and is only true if the app switches to GPT-6.2 and still needs tool calling. Source does not say the app must migrate or that it breaks. Reword conditionally. |
| C7 | GPT-6.2 changes how the Responses API preserves reasoning when you edit earlier messages | supported | S3 | Source: "when you edit a conversation's prefix". "Earlier messages" is a fair paraphrase. Narration omits "Responses API"; add it. Direction of change is not stated, so visuals must not show a specific mechanism. |
| C8 | GPT-6.2 changes how the Responses API handles the top-level instructions field | supported | S3 | Source says it changes how the API "handles the top-level instructions field". Nature of change not stated; "handled differently" is safe. |
| C9 | OpenAI points to a GPT-6.2 migration guide; testing the three first is our suggested workflow | supported | S3 | Changelog: "See the GPT-6.2 migration guide". Testing advice is our own and is framed as such. |
| C10 | Changelog describes behaviour changes; does not state anything breaks | qualified | S2, S3 | True: the word "breaking" does not appear. But check 1 is a requirement (not a "behaviour change"), and a reassuring "nothing breaks" tone clashes with scene 5 showing a failed call and "must move". Keep as absence-of-claim only; do not imply safety. |

## Unmapped statements
- "Both support the Responses API and Chat Completions" (scene 2): covered by C3; "both" refers to the two models.
- "Imagine an app that calls tools through Chat Completions" / "Imagine an app that rewrites chat history": illustrative framing, labelled illustrative on screen. OK.
- "So test those three before you switch" (scene 8): our advice, not sourced. Acceptable if worded as suggestion (C9). OK.
- "Which of these three would your app hit first? Comment below." CTA, no claim. OK.
- "One. / Two. / Three." enumeration: our structure (see C4).
- Hook framing: no "most people get this wrong" or invented audience claim. OK.
- "OpenAI's GPT-6.2 migration guide": the guide exists per changelog link; its contents are not described. OK.
- No Astra/Sol ranking or positioning appears in narration or on-screen. OK. (S1 vs S5 positioning conflict remains unused.)

## On-screen and chart values
| scene | item | verdict | note |
|---|---|---|---|
| 1 | "Same name, new behaviour" | unsupported | The model name changes (to GPT-6.2); "same name" is false. Visual "model-name tag" also implies a same-name swap. Replace, e.g. "New model, new behaviour" or "Check before you switch". |
| 2 | "Two variants, two APIs" | supported | Matches C2/C3. Source chip "OpenAI changelog, Nov 17 2026" correct. Cards must stay equal. |
| 3 | "3 checks first" | qualified | Count is ours; fine on screen if not attributed to OpenAI, but narration attributes it (C4). |
| 4 | "1: Tool calling"; dimmed Chat Completions lane with no tool-call arrow | supported | Consistent with C5. Dimming should not suggest Chat Completions is deprecated or worse; it is still supported. |
| 5 | "Illustrative app"; coral stalled dot vs mint reroute | qualified | Label present. Stalled coral dot depicts a failure the source does not state and contradicts "does not say anything breaks". Show "needs Responses API" without error styling. |
| 6 | "2: Edited history"; tag "shifts" when a block is edited | qualified | Source gives no mechanism. Show only an edit mark and a "changed handling" tag, not a specific shift. Label "illustrative" present. |
| 7 | "3: Instructions field" | supported | Matches C8. Generic UI, no vendor UI. |
| 8 | "Test 3, then read the guide"; ticked checks; migration guide node | supported | Advice framed as ours (C9). |
| 9 | "Changes, not breaks"; "breaks" struck out | qualified | Strike-out reads as a guarantee. Prefer "Sources: changes, no breakage stated" or drop the strike-through. |
| 10 | "Which one first?" | supported | CTA. |
No charts, benchmarks, prices, dates beyond Nov 17 2026, or numbers other than "3" and "two" are shown.

## Required corrections
1. C4 / scene 3: remove the attribution. Change "OpenAI's changelog lists three things to check before you switch" to something like "Here are three things worth checking before you switch." Keep "three" as our framing.
2. C6 / scene 5: replace "That app must move to the Responses API" with a conditional such as "To use tools with GPT-6.2, that app would need the Responses API." Match scene 5 on-screen/visual accordingly (no failed-call styling).
3. Scene 1 on-screen "Same name, new behaviour" and the model-name-tag visual: replace; the model name does change.
4. C1 / hook: scope the behaviour change to the Responses API, e.g. narration for check 2/3 says "the Responses API" explicitly (C7, C8); optionally soften hook to "can change how some apps behave".
5. C10 / scene 9: keep as "the changelog says behaviour changes; it does not say anything breaks", but remove the strike-through of "breaks" and avoid implying safety. Do not call check 1 a behaviour change.
6. Scene 6 visual: do not depict a specific reasoning-shift mechanism; source gives none.
7. Optional: say "two models" instead of "variants" (source wording).

## Corrections applied (main session, 2026-11-20)
- C4 (unsupported): the "three things" are now our pick ("We picked three worth testing"; on screen "3 checks (our pick)"), not a changelog list. C1 and C4 retyped as interpretation.
- C6: "must move" replaced by the conditional "if your app calls tools through Chat Completions, tools on GPT-6.2 need the Responses API"; coral failure styling removed.
- Scene 1: "Same name, new behaviour" and the model-name-tag visual replaced by "3 checks before GPT-6.2".
- C7/C8: narration now scopes both changes to the Responses API.
- Scene 9: struck-out "breaks" removed; now "1 requirement, 2 changes" (no safety implication).
- Scene 6: no reasoning mechanism drawn; neutral "changed in GPT-6.2" tag. "variants" changed to "models".
Revised claims re-verified by the main session against sources.md S1-S3 (OpenAI changelog text read verbatim in the browser pane on 2026-11-20).
