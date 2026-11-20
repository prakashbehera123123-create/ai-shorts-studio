"""Voice-clone TTS worker. Runs inside .venv-voice (Python 3.11 + CPU PyTorch + chatterbox-tts, MIT licence).

Usage: .venv-voice/Scripts/python.exe scripts/clone_tts.py <jobs.json>
jobs.json: {"reference": "voice/reference.wav", "language": "en", "exaggeration": 0.6, "cfg_weight": 0.5,
            "seed": 1234, "jobs": [{"text": "...", "out": "path.wav"}, ...]}
Loads the model once, synthesises every job with a fixed seed per job (repeatable output), prints one line per job.
Only the channel owner's own, consented voice may be used as the reference.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path


def main() -> int:
    spec = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    ref = Path(spec["reference"])
    if not ref.is_file():
        print(f"ERROR reference not found: {ref}", file=sys.stderr)
        return 2

    import torch
    import torchaudio as ta

    torch.set_num_threads(max(1, (torch.get_num_threads() or 4)))
    lang = spec.get("language", "en")
    t0 = time.time()
    if lang == "en":
        from chatterbox.tts import ChatterboxTTS
        model = ChatterboxTTS.from_pretrained(device="cpu")
        extra: dict = {}
    else:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        model = ChatterboxMultilingualTTS.from_pretrained(device=torch.device("cpu"))
        extra = {"language_id": lang}
    print(f"model loaded in {time.time() - t0:.0f}s", flush=True)

    for i, job in enumerate(spec["jobs"]):
        torch.manual_seed(int(job.get("seed", int(spec.get("seed", 1234)) + i)))  # per-job seed enables retakes
        t1 = time.time()
        wav = model.generate(job["text"], audio_prompt_path=str(ref),
                             exaggeration=float(spec.get("exaggeration", 0.5)),
                             cfg_weight=float(spec.get("cfg_weight", 0.5)), **extra)
        out = Path(job["out"])
        out.parent.mkdir(parents=True, exist_ok=True)
        ta.save(str(out), wav, model.sr)
        print(f"job {i + 1}/{len(spec['jobs'])}: {wav.shape[-1] / model.sr:.2f}s audio in {time.time() - t1:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
