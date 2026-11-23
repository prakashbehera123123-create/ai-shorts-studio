# Editorial QA: 2026-11-23 Hundreds of AI agents built a browser in a week (why locks failed)

Reviewer: video-reviewer (sonnet). Evidence: script.md, storyboard.json, sources.md, fact_check.md, render/captions.srt, qa_report.md, qa/technical.json, qa/contact_sheet.jpg, qa/frames/, plus ~1 frame per 2 s stills (21) and first frame extracted with ffmpeg. Audio judged from measurements and transcript recall only (-14.0 LUFS, TP -1.5, 92% recall, 0 SFX, pad bed); not heard by the reviewer.

Decision: PASS

## Rubric

| criterion | score | evidence |
|---|---|---|
| Hook strength | 4 | 0-2.9 s: 20 robots jammed at a big LOCK door, "Twenty AI agents worked like two or three." Paradox + number, visual on frame 0. Faithful to S1 ("two or three"). |
| Mechanism clarity | 4 | Lock file, then optimistic concurrency, then planner/workers/judge with travelling signal dots. Each step has a visual. Claim hedged ("Cursor says", "experiment"). |
| Visual-narration sync | 3 | Mostly matched (hook, lock, org chart, 1M lines). Mismatches: scene 4 counters read "20 working", "10 working", "4 working" while narration says "two or three"; scene 2 intro shows "Structure. ~1 week." with a "?" over the LOCK. |
| Visual variety | 4 | World-style 3D construction site (hard hats, yellow lanes, scaffolding) plus two dark 2D icon B-roll scenes (6, 9). Clearly different from the 11-22 office videos. Icon B-roll is thin (2 of 10 scenes). |
| Pacing | 4 | 41.5 s, a caption/visual change about every 1-2 s, longest static 1.0 s, no long silences. |
| Payoff usefulness | 4 | "Structure beats more agents" lands with a clear visual; outro has the door OPEN and exact phrase "For more AI concepts like this, follow." |
| Caption readability | 4 | Large lower-third captions, highlighted keywords, 0.5 s min cue, <=22 cps, contiguous; no caption/script errors found. Minor overlaps noted below. |

Average: 3.86 (all >= 3).

## Blockers
- none

## Blocker checks performed
- Facts: on-screen "20 agents ~ 2-3", "~1 week · 1M+ lines · ~1,000 files", "Experiment / kind of works" all match script.md claim map C1-C6 and S1/S2 in sources.md; fact_check.md has no unsupported claims. "Hundreds of agents" appears only in the title (supported by S1). "Structure beats more agents" is labelled as lesson/interpretation.
- Hook/title not misleading; "Illustration" tag and source chip present (disclosure ok).
- Captions: SRT matches narration; no typos.
- Text legibility: no unreadable or cropped-off-screen text in the sampled stills.
- Rights: all assets in manifest.csv with licence records (internally generated, own voice clone, generated pad).

## Warnings
- Owner requirement check: English only (pass); hook in 0-2 s (pass); outro phrase exact (pass); no transition SFX and soft bed only (pass by metadata: 0 SFX, pad.wav; not heard); 3D world + icons (pass); not the 11-22 office look (pass).
- Intro is weak: scene 2 starts "Then a clear team structure helped build a browser..." with no antecedent and does not pose the question; it also gives away the answer before the problem. Preferred: short question intro ("How do you run hundreds of agents without a pile-up?").
- Scene 4: "20 working / 10 working / 4 working" counters do not land on "2-3"; make the final count 2 or 3.
- Scene 7 (~31-33 s): "Workers" tag is clipped/overlapped by the "1M+ lines" chip; Planner/Judge tags sit on top of the robot row.
- Scene 3 (~11-12 s): "forgot to release" tag partly covers a robot head/face; "holds the lock" tag is near another.
- Scene 8: bottom robot row is cut off by the frame edge behind the caption (cosmetic).
- Scene 10: on-screen "Follow for more AI concepts" is lighter than the spoken outro; fine, but the chip at 38-40 s starts fading in while the scene 9 lesson caption is still running.
- Voice: scene 1 take still below 85% recall (render warning); human must listen for clone quality.
- T001 Segoe UI Bold font terms need confirming before publishing (known, non-blocking).

## Pass items
- Technical QA PASS: 1080x1920, H.264/AAC, 41.5 s, -14.0 LUFS, -1.5 dBFS TP, no silences.
- Hook visual present from frame 0, door motif pays off (LOCK to OPEN).
- Sourcing and attribution clear; on-screen source chip on every scene.
- Distinct world-style look; no transition SFX.

## Fix items (none require re-render; optional polish)
1. Scene 2: rewrite intro as a question and remove the "Structure. ~1 week." chip before the problem is shown.
2. Scene 4: end counter at "2-3 working".
3. Scene 7: move "Workers" tag so it is not overlapped by the "1M+ lines" chip.
4. Scene 3: nudge "forgot to release" tag off the robot face.
5. Scene 8: raise robot row or caption so the robots are not cut.
6. Add one more icon B-roll beat (e.g. scene 3 or 5) if time allows.
Status unchanged; final state remains READY_FOR_HUMAN_REVIEW (human approval required, never published).
