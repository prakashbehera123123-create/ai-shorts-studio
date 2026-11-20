---
name: voice-and-sound
description: Direct the voiceover (pace, emphasis, pauses, pronunciation) and design the audio bed (music, SFX, ducking, loudness) so audio carries the story.
---

# Voice and sound

## Purpose
Use after the storyboard exists and before rendering. Makes narration sound directed rather than read, and adds a
licensed music bed and sparse SFX. Standards: `docs/CREATIVE_PRODUCTION_STANDARD.md` §3 and §8.

## Inputs
- `script.md`, `storyboard.json` (schema v2 with `voice` per scene)
- `config/render.json` (TTS engine, voice, pronunciations, loudness)
- Optional `voiceover/voiceover.wav` (recorded) and licensed music/SFX files in `assets/audio/`

## Workflow
0. **Clean voice reference (one-time, or whenever the owner supplies a new recording):**
   `python -m studio voice prepare "<owner's recording>" --start 0 --seconds 13.8` → Demucs isolates the voice from any
   background music/noise, then high-pass 90 Hz + light spectral denoise, trimmed mono → `voice/reference_clean.wav`.
   Check the printed before/after `noise_profile` (2026-11-20: SNR 10.5 → 16.0 dB) and listen before cloning.
   The clone copies everything in the reference, so never clone from an uncleaned recording.
1. **Pronunciation pass:** list acronyms, version strings, product names; add each to `tts.pronunciations`; captions keep original spelling.
2. **Direction pass:** per scene set `voice.emphasis` (≤1 word per sentence) and `voice.pause_after_ms` (150–300 before reveals/steps, 0 in hook).
3. **Pace check:** target 165–180 wpm delivered; if the engine is slower, tighten the script before raising the rate.
4. **Voice source:** recorded voice if present; else the configured local TTS. SAPI = placeholder (disclose; flag in QA).
5. **Music bed (automatic, `config/render.json` → `sound`):** the render mixes a bed ducked under the voice
   (`bed_db` −4 on the generated bed ≈ 15 dB under the voice, measured 2026-11-20; sidechain ratio 3). Source order:
   owner-downloaded tracks in `assets/library/audio/music/` **with a row in `assets/library/audio/LICENSES.csv`**
   (YouTube Audio Library, Pixabay, Freesound CC0 only), else the self-generated pad. Manifest rows are written for you.
6. **SFX (automatic):** one cue max per scene start — the scene's `sfx` name if given (`whoosh`, `pop`, `tick`, `rise`,
   `knock`, or the stem of a licensed file in `sfx/`), else a default by transition (push/zoom/wipe → whoosh,
   match_cut → rise, crossfade → tick, new beat → pop); whoosh/rise lead the cut by 0.35 s; capped at 5 per 30 s.
   Set `sfx: ["none"]`-style names that do not exist to keep a scene silent. Never under a key spoken term.
7. **Mix (render step):** duck music ≥ 12 dB under voice (FFmpeg `sidechaincompress`), normalise to −14 LUFS, true peak ≤ −1.5 dBFS.
8. **Verify:** transcribe the final mix with whisper (`models/ggml-base.bin`, forced language) and compare to the spoken text.

## Tools
- **Cloned voice (default since 2026-11-20):** Chatterbox 0.1.7 (Resemble AI, MIT) in the isolated `.venv-voice`
  (Python 3.11, CPU PyTorch 2.6), worker `scripts/clone_tts.py`, integration `studio/clone_voice.py`, settings under
  `tts.clone` in `config/render.json`. Reference: `voice/reference_clean.wav` (Demucs-cleaned 13.8 s of the owner's own
  recording; git-ignored). Demucs 4.0.1 (MIT) is installed in `.venv-voice` (installed by the owner).
  Measured on this PC (CPU only): model load ~25–45 s, ~8–25 s compute per second of audio → ~10–15 min per 50 s video.
  Settings validated 2026-11-20: `exaggeration` 0.5 (0.6 garbled words), `cfg_weight` 0.3 (the owner speaks fast; 0.5
  rushed and dropped words). No rate control: runtime is fitted with ≤ 1.12× `atempo`.
  Per scene the pipeline: reuses a cached take when text/reference/settings match; denoises every take
  (`studio/audio_clean.py`: high-pass, 2× `afftdn`, soft gate — measured −49/−54 dB background, SNR 30–35 dB); checks
  whisper recall and re-clones takes below `min_recall` (85%) with a new seed up to `retakes` (2) times, keeping the
  best; writes `voiceover/takes.json`. Word timings are estimated from the audio (silence-aware).
- Windows SAPI: fallback placeholder (`tts.engine: "sapi"`), gives exact word boundaries.
- FFmpeg (`sidechaincompress`, `loudnorm`, `ebur128`, `whisper` for recall QA).
Emphasis/pauses: pauses are honoured via scene timing; per-word emphasis is not controllable in either engine.

## Decision rules
- Clone only the channel owner's own voice, from a recording they supplied for that purpose. Never clone anyone else
  (no songs, interviews or other creators). Disclose cloned narration as synthetic in metadata.
- The clone copies the reference's energy: to change delivery, record a new reference in the wanted style.
- Voice is the priority track; cut music before cutting intelligibility.
- No music with lyrics under narration. No copyrighted tracks without a licence record.
- Hinglish: the voice must handle both languages naturally; if not, record a human voice.

## Outputs
Updated `storyboard.json` (`voice`, `sfx`), `config/render.json` pronunciations, manifest rows for every audio asset,
mixed narration in `voiceover/`, loudness numbers in `qa/technical.json`.

## Quality checklist
- [ ] Every acronym has a pronunciation entry
- [ ] 165–180 wpm; pauses only where directed
- [ ] Music licence recorded; voice ≥ 12 dB above bed
- [ ] −14 LUFS ±1, true peak ≤ −1.5 dBFS
- [ ] Whisper transcript matches script (no missing/garbled terms)

## Failure handling
- Background noise or music audible in cloned audio → re-run `voice prepare` (check the reference's noise_profile);
  if the source recording itself is noisy, ask the owner for a 30–60 s recording in a quiet room.
- A scene stays below `min_recall` after retakes (listed in `voiceover/takes.json` and the render warnings) → rephrase
  that sentence (shorter words, fewer acronyms) or add a pronunciation entry, then re-render; cached scenes are reused.
- Demucs or the clone venv missing → `tts.engine: "sapi"` fallback, flagged as placeholder in QA.
- TTS mispronounces after mapping → respell phonetically or record that line.
- No licensed music available → ship voice-only and note it; never substitute an unlicensed track.
- Runtime too long at natural pace → shorten script (story-architecture), not faster speech beyond 195 wpm.
