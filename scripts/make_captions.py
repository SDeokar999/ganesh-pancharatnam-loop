from pathlib import Path

root = Path(__file__).resolve().parent.parent

verses = [
    "मुदाकरात्तमोदकं सदा विमुक्तिसाधकं\nकलाधरावतंसकं विलासिलोकरक्षकम् ।\n"
    "अनायकैकनायकं विनाशितेभदैत्यकं\nनताशुभाशुनाशकं नमामि तं विनायकम् ॥१॥",

    "नतेतरातिभीकरं नवोदितार्कभास्वरं\nनमत्सुरारिनिर्जरं नताधिकापदुद्धरम् ।\n"
    "सुरेश्वरं निधीश्वरं गजेश्वरं गणेश्वरं\nमहेश्वरं तमाश्रये परात्परं निरन्तरम् ॥२॥",

    "समस्तलोकशङ्करं निरस्तदैत्यकुञ्जरं\nदरेतरोदरं वरं वरेभवक्त्रमक्षरम् ।\n"
    "कृपाकरं क्षमाकरं मुदाकरं यशस्करं\nमनस्करं नमस्कृतां नमस्करोमि भास्वरम् ॥३॥",

    "अकिञ्चनार्तिमार्जनं चिरन्तनोक्तिभाजनं\nपुरारिपूर्वनन्दनं सुरारिगर्वचर्वणम् ।\n"
    "प्रपञ्चनाशभीषणं धनञ्जयादिभूषणं\nकपोलदानवारणं भजे पुराणवारणम् ॥४॥",

    "नितान्तकान्तदन्तकान्तिमन्तकान्तकात्मजं\nअचिन्त्यरूपमन्तहीनमन्तरायकृन्तनम् ।\n"
    "हृदन्तरे निरन्तरं वसन्तमेव योगिनां\nतमेकदन्तमेव तं विचिन्तयामि सन्ततम् ॥५॥",
]

# measured verse durations (seconds), from ffmpeg probe
durations = [15.10, 15.12, 14.86, 15.31, 15.36]
SILENCE = 1.5
CYCLES = 3


def srt_ts(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


blocks = []
idx = 1
t = 0.0
for _ in range(CYCLES):
    for verse, dur in zip(verses, durations):
        t += SILENCE
        start, end = t, t + dur
        blocks.append(f"{idx}\n{srt_ts(start)} --> {srt_ts(end)}\n{verse}\n")
        idx += 1
        t += dur
    t += SILENCE

out = root / "video" / "captions.srt"
out.write_text("\n".join(blocks), encoding="utf-8")
print(f"wrote {out} ({idx - 1} cues, total {t:.1f}s)")
