# fal.ai Video Production Toolkit

Complete reference of all fal.ai models available for video production.
The video agent should dynamically select tools based on the topic and shot requirements.

> **Registry swept live 2026-08-04** — i2v (83 endpoints), t2v (60), 3D (39) sections below carry
> per-model ✅/🚫 verdicts. The rule behind every verdict: prefer the **newest full tier** in each
> family, skip speed tiers (`fast`/`turbo`/`lite`/`mini`/`distilled`) because they trade the
> detail this brand's look depends on, and skip superseded siblings.
>
> Re-sweep before any new pipeline — the catalog moves monthly and stale model choices are the
> most common silent quality loss:
> ```bash
> curl -s "https://fal.ai/api/models?keywords=image-to-video" | jq -r '.items[].id'
> ```
> ⚠️ Pricing is **not** in the API and model pages 429 under WebFetch — $/s figures come from the
> pricing page and go stale independently of the endpoint list.

## VIDEO GENERATION

### Image-to-Video (I2V) — Animate keyframes

⭐ **Full registry sweep 2026-08-04: 83 live i2v endpoints.** Below is the whole surface with a
verdict for the **standard shot job** — a slow camera push on an already-styled still, 9:16, 3-5s,
no faces, no articulated motion, no physics, no audio. Detail preservation is the only real demand.

⚠️ **Style comes from the STILL, motion from i2v — never from text-to-video.** Wan fed a text
prompt goes photoreal and ignores the brief; the same model fed a styled plate holds the look
exactly. This is why the whole table is i2v.

#### ✅ USE — current generation, full tier
| Model | Endpoint | Why |
|-------|----------|-----|
| **Kling v3 4K** | `fal-ai/kling-video/v3/4k/image-to-video` | Highest raster available; render 4K → downscale keeps maximum gloss/specular detail |
| ⭐ **Kling v3 Pro** | `fal-ai/kling-video/v3/pro/image-to-video` | **Verified working**, $0.22/s. Toolkit's own pick for product/object detail |
| **Kling O3 Pro** | `fal-ai/kling-video/o3/pro/image-to-video` | Newest O-series; start+end frame = precise A→B moves |
| **Kling 2.6 Pro** | `fal-ai/kling-video/v2.6/pro/image-to-video` | **$0.07/s — the cost candidate.** 68% cheaper; a slow push may not need v3 |
| ⭐ **Seedance 2.0** | `bytedance/seedance-2.0/image-to-video` | SOTA family; strongest reference-conditioning |
| **Veo 3.1** | `fal-ai/veo3.1/image-to-video` | Premium cinematic — but $0.40/s and an **8s hard cap** |
| **LTX-2.3 Quality** | `fal-ai/ltx-2.3-quality/image-to-video` | Quality tier of the newest LTX |
| **LTX-2.3 22B** | `fal-ai/ltx-2.3-22b/image-to-video` | Largest LTX param count |
| **Wan 2.7** | `fal-ai/wan/v2.7/image-to-video` | Newest Wan |
| **Wan 2.6** | `wan/v2.6/image-to-video` | Newer than the 2.5-preview we had listed |
| **MiniMax H3** | `minimax/h3/image-to-video` | Newest MiniMax generation |
| **Hailuo 2.3 Pro** | `fal-ai/minimax/hailuo-2.3/pro/image-to-video` | **~$0.02/s — cheapest credible.** Guide routes "doesn't need realism" work here, which fits a slow push |
| **Luma Ray 3.2** | `luma/agent/ray/v3.2/image-to-video` | Newest Ray |
| **PixVerse V6** | `fal-ai/pixverse/v6/image-to-video` | Newest PixVerse |
| **Vidu Q3** | `fal-ai/vidu/q3/image-to-video` | Newest Vidu full tier |
| **Grok Imagine 1.5** | `xai/grok-imagine-video/v1.5/image-to-video` | Newest xAI, untested |
| ⭐ **Happy Horse 1.1** | `alibaba/happy-horse/v1.1/image-to-video` | **Won the 9-model t2v bake-off on look** (1920×1080). Its i2v is untested and overdue |

#### 🚫 SKIP — and why
| Group | Endpoints | Reason |
|-------|-----------|--------|
| **Superseded Kling** | `o1`, `v3/standard`, `o3/standard`, `v2.5-turbo/*`, `v2.1/{master,pro,standard}`, `v2/master`, `v1.6/standard` | Older gen or sub-pro tier of a family whose current version we already use |
| **Turbo/fast/lite/mini/distilled** | `v3/turbo/*`, `seedance-2.0/{fast,mini}`, `veo3.1/{fast,lite}`, `ltx*/distilled`, `ltx-2.3/image-to-video/fast`, `hailuo-*-fast/*`, `hailuo-02*`, `pika/v2/turbo`, `pixverse/*/fast`, `vidu/*/turbo`, `wan/*/turbo`, `wan/v2.6/*/flash`, `gemini-omni-flash` | Speed tiers trade the detail this look depends on — excluded by the standing top-tier preference |
| **Superseded Seedance/LTX/Wan/Vidu/PixVerse/Luma** | `seedance/v1{,.5}/pro`, `ltx-2-19b*`, `ltx-video-13b-distilled`, `ltx-2.3/image-to-video`, `wan-25-preview`, `wan-pro`, `wan/v2.2-*`, `vidu/{,q1,q2}*`, `pixverse/{c1,v3.5,v4,v4.5,v5,v5.5,v5.6}`, `luma-dream-machine/ray-2*` | Newer sibling exists in the same family |
| **Wrong purpose** | `minimax/video-01-{director,live}`, `*/lora` | Character/director control and LoRA conditioning we don't use |
| **Stylisation-first** | `pika/v2.1`, `pika/v2.2` | Tuned for creative/stylised motion; our look is photoreal gloss |

❌ **LTX distilled measurably failed** a like-for-like quality test — flat sky, crude figures,
ignored the prompt. Treat every `distilled` tag as a quality-class drop, not a tuning knob.

⚠️ **Pricing is NOT in the fal API** (`pricing`/`pricingInfoOverride` → n/a) and model pages 429
under WebFetch. The $/s figures here come from the pricing page and need periodic re-checking.

### Text-to-Video (T2V) — Generate from prompt only

**Full sweep 2026-08-04: 60 live t2v endpoints.**

🚫 **T2V IS THE WRONG TOOL FOR STYLED BRAND WORK — measured, not assumed.** Given the same brief,
Wan 2.2 t2v produced the right *content* in the wrong *look*: photoreal, underexposed, murky,
where the styled-still→i2v route held the art direction exactly. **Style originates in the still.**
Reach for t2v only when no plate exists and the look is disposable.

⭐ The one t2v capability i2v cannot match is **native multishot** — several cuts inside a single
generation, with free intra-generation coherence (same set, lighting, grade across cuts).

#### ✅ USE
| Model | Endpoint | Why |
|-------|----------|-----|
| ⭐ **Seedance 2.0** | `bytedance/seedance-2.0/text-to-video` | **Multishots from plain prose** with no special param — 6 cuts @1.43s measured. Up to 30s, 30-image referencing |
| ⭐ **Happy Horse 1.1** | `alibaba/happy-horse/v1.1/text-to-video` | **Best look in the 9-model bake-off**, 1920×1080. Timecoded `Shot N (framing, 0-1.4s):` prompts give exact shot counts |
| **Kling v3 4K / O3 4K** | `fal-ai/kling-video/{v3,o3}/4k/text-to-video` | Highest raster t2v available |
| **Kling v3 Pro** | `fal-ai/kling-video/v3/pro/text-to-video` | `multi_prompt` array = explicit per-shot control (Kling-family only) |
| **Kling O3 Pro** | `fal-ai/kling-video/o3/pro/text-to-video` | Newest O-series |
| **Sora 2 Pro** | `fal-ai/sora-2/text-to-video/pro` | Top-end cinematic + native audio, ~$0.50/s |
| **Veo 3.1** | `fal-ai/veo3.1` | Premium + audio, ⚠️ **4/6/8s hard cap — cannot do 10s blocks** |
| **LTX-2.3 Quality / 22B** | `fal-ai/ltx-2.3-{quality,22b}/text-to-video` | Cheapest credible tier, open weights |
| **Wan 2.7 / 2.6** | `fal-ai/wan/v2.7/text-to-video`, `wan/v2.6/text-to-video` | Newest Wan; ⚠️ needs a styled anchor or goes photoreal |
| **MiniMax H3** | `minimax/h3/text-to-video` | Newest MiniMax |
| **Hunyuan Video 1.5** | `fal-ai/hunyuan-video-v1.5/text-to-video` | Open source, runs on consumer GPUs if self-hosting |
| **Luma Ray 3.2** | `luma/agent/ray/v3.2/text-to-video` | Newest Ray |
| **PixVerse V6 · Vidu Q3 · Grok 1.5** | `pixverse/v6`, `vidu/q3`, `xai/grok-imagine-video/v1.5` | Newest in family, untested |
| **Bernini-R** | `fal-ai/bernini-r/text-to-video` | Unknown/new — untested, worth a probe |

#### 🚫 SKIP
| Group | Reason |
|-------|--------|
| `seedance-2.0/{fast,mini}`, `seedance/v1{,.5}/*`, `*/turbo/*`, `*/fast`, `*/standard`, `hailuo-02*`, `pika/v2/turbo`, `vidu/q3/*/turbo`, `wan/v2.2-*/turbo` | Speed/sub tiers, or superseded by a newer sibling |
| `kling-video/{v1.6,v2.1,v2.5-turbo,v2.6}/*` | Superseded by v3/O3 |
| `pixverse/{c1,v3.5,v4,v4.5,v5,v5.5,v5.6}`, `vidu/{q1,q2}`, `pika/v2.1`, `wan-25-preview`, `wan/v2.2-5b` | Older sibling exists |
| ❌ `ltx-2.3/text-to-video/fast`, all `distilled` | **Measurably failed** a like-for-like test: flat orange sky, crude figures, ignored the prompt, 0 cuts |

### Image-to-3D / Text-to-3D — 39 endpoints

Relevant to Nordyl only for **molecular or product hero objects**. ⚠️ For peptides prefer the real
computed structure via Mol\* (`molstar-render`) — a generated mesh of a molecule is exactly the
"AI-imagined blob" the brand exists to correct.

#### ✅ USE
| Model | Endpoint | Why |
|-------|----------|-----|
| **Hunyuan3D v3.1 Pro** | `fal-ai/hunyuan-3d/v3.1/pro/image-to-3d` (+ `/text-to-3d`) | Newest Hunyuan, pro tier |
| **Hunyuan3D 3.1 Part / Smart-Topology** | `fal-ai/hunyuan-3d/v3.1/{part,smart-topology}` | Part segmentation + retopology — clean meshes for animation |
| **Tripo H3.1** | `tripo3d/h3.1/{image,text,multiview}-to-3d` | Newest Tripo; multiview = most faithful reconstruction |
| **Meshy V6** | `fal-ai/meshy/v6/{image,text,multi-image}-to-3d` | Newest Meshy full tier |
| **Rodin v2.5** | `fal-ai/hyper3d/rodin/v2.5` (+ `/text-to-3d`) | Hyper3D newest; strong on hard-surface product |
| **SAM 3 3D** | `fal-ai/sam-3/{3d-objects,3d-body,3d-align}` | Segment-then-reconstruct from a real photo |
| **TripoSplat** | `tripo3d/triposplat` | Gaussian splat rather than mesh — better for volumetric looks |

#### 🚫 SKIP
`hunyuan3d/v2*` (superseded by v3/v3.1) · `hunyuan3d-v3/*` (superseded by v3.1) ·
`*/rapid/*`, `*/fast`, `*/turbo`, `*/mini` (speed tiers) · `meshy/v6-preview` (preview, v6 is out) ·
`meshy/v5/*`, `tripo3d/{p1,tripo/v2.5}/*`, `hyper3d/rodin{,/v2}` (older siblings) ·
`hunyuan3d-v3/sketch-to-3d` (wrong input) · `fal-ai/pixal3d` (unknown, unprobed)

### Start+End Frame (Transitions)
| Model | Endpoint | Best For |
|-------|----------|----------|
| **Veo 3.1 First/Last** | `fal-ai/veo3.1/first-last-frame-to-video` | Premium transitions between two keyframes |
| **Kling O3 Pro** | `fal-ai/kling-video/o3/pro/image-to-video` | Precise A-to-B transitions |
| **Kling O1** | `fal-ai/kling-video/o1/image-to-video` | Budget start/end frame |

### Motion Control & Character Animation
| Model | Endpoint | Best For |
|-------|----------|----------|
| **Kling v3 Motion Control** | `fal-ai/kling-video/v3/pro/motion-control` | Transfer dance/fitness from reference video |
| **Kling v2.6 Motion Control** | `fal-ai/kling-video/v2.6/pro/motion-control` | Budget motion transfer |
| **Wan Animate Move** | `fal-ai/wan/v2.2-14b/animate/move` | Replicate expressions/movements from reference |
| **Wan Animate Replace** | `fal-ai/wan/v2.2-14b/animate/replace` | Replace character in video keeping scene |

### Reference-to-Video (Identity Preservation)
| Model | Endpoint | Best For |
|-------|----------|----------|
| **Kling O3 Reference** | `fal-ai/kling-video/o3/pro/reference-to-video` | Consistent character identity across shots |
| **Veo 3.1 Reference** | `fal-ai/veo3.1/reference-to-video` | Premium reference-guided video |
| **Kling O1 Reference** | `fal-ai/kling-video/o1/reference-to-video` | Budget reference video |

### Video-to-Video (Edit existing)
| Model | Endpoint | Best For |
|-------|----------|----------|
| **Kling O3 Edit** | `fal-ai/kling-video/o3/pro/video-to-video/edit` | Edit videos with natural language |
| **Kling O1 Edit** | `fal-ai/kling-video/o1/video-to-video/edit` | Budget video editing |
| **Kling O3 Reference V2V** | `fal-ai/kling-video/o3/pro/video-to-video/reference` | Restyle preserving motion/camera |

### Avatar / Talking Head / Lip Sync
| Model | Endpoint | Best For | Cost |
|-------|----------|----------|------|
| **HeyGen Avatar4** | `fal-ai/heygen/avatar4/image-to-video` | Photo → talking head | $0.10/s |
| **Kling Avatar Pro** | `fal-ai/kling-video/ai-avatar/v2/pro` | Premium avatar with gestures | $0.10/s |
| **Kling Avatar Std** | `fal-ai/kling-video/ai-avatar/v2/standard` | Budget avatar | $0.05/s |
| **OmniHuman v1.5** | `fal-ai/bytedance/omnihuman/v1.5` | Audio-driven human animation | ~$0.10/s |
| **Creatify Aurora** | `fal-ai/creatify/aurora` | Studio-quality talking/singing | ~$0.10/s |
| **VEED Fabric 1.0** | `veed/fabric-1.0` | Image → talking video | ~$0.10/s |
| **Sync Lipsync Pro** | `fal-ai/sync-lipsync/v2/pro` | Realistic lip sync overlay | ~$0.05/s |
| **Kling LipSync** | `fal-ai/kling-video/lipsync/audio-to-video` | Kling-native lip sync | ~$0.05/s |
| **PixVerse LipSync** | `fal-ai/pixverse/lipsync` | Alternative lip sync | ~$0.05/s |
| **VEED LipSync** | `veed/lipsync` | Alternative lip sync | ~$0.05/s |

### Video Post-Production
| Model | Endpoint | Best For |
|-------|----------|----------|
| **Topaz Upscale** | `fal-ai/topaz/upscale/video` | Professional video upscaling |
| **SeedVR2 Upscale** | `fal-ai/seedvr/upscale/video` | Temporal-consistent upscaling |
| **Bytedance Upscaler** | `fal-ai/bytedance-upscaler/upscale/video` | Budget upscaling |
| **Auto-Subtitle** | `fal-ai/workflow-utilities/auto-subtitle` | Karaoke-style animated captions |
| **MMAudio V2** | `fal-ai/mmaudio-v2` | Add SFX/ambient audio to video |
| **FFmpeg Merge** | `fal-ai/ffmpeg-api/merge-videos` | Concatenate videos |
| **FFmpeg Compose** | `fal-ai/ffmpeg-api/compose` | Compose from multiple sources |
| **FFmpeg Merge Audio** | `fal-ai/ffmpeg-api/merge-audio-video` | Merge audio into video |
| **FFmpeg Extract Frame** | `fal-ai/ffmpeg-api/extract-frame` | Extract frames from video |

## IMAGE GENERATION

### Text-to-Image
| Model | Endpoint | Best For | Cost |
|-------|----------|----------|------|
| **Ideogram V3** | `fal-ai/ideogram/v3` | Text rendering, thumbnails, logos | $0.03-$0.09 |
| **Ideogram Character** | `fal-ai/ideogram/character` | Consistent character across images | ~$0.06 |
| **FLUX Ultra** | `fal-ai/flux-pro/v1.1-ultra` | Professional photos, up to 2K | ~$0.06 |
| **FLUX LoRA** | `fal-ai/flux-lora` | Identity-locked with custom LoRA | ~$0.04 |
| **FLUX 2 Pro** | `fal-ai/flux-2-pro` | Latest FLUX, best quality | ~$0.06 |
| **FLUX 2 Max** | `fal-ai/flux-2-max` | Maximum FLUX quality | ~$0.10 |
| **Imagen 4** | `fal-ai/imagen4/preview` | Google's highest quality | ~$0.08 |
| **Nano Banana Pro** | `fal-ai/nano-banana-pro` | Fast Google image gen + editing | ~$0.03 |
| **Recraft V4** | `fal-ai/recraft/v4/text-to-image` | Design-ready, brand systems | ~$0.04 |
| **Recraft V3** | `fal-ai/recraft/v3/text-to-image` | Vector art, long text, brand style | ~$0.04 |
| **GPT Image 1.5** | `fal-ai/gpt-image-1.5` | High-fidelity, strong prompt adherence | ~$0.08 |
| **Qwen Image 2** | `fal-ai/qwen-image-2/pro/text-to-image` | Text editing, fine textures | ~$0.04 |
| **Seedream v4.5** | `fal-ai/bytedance/seedream/v4.5/text-to-image` | Bilingual, unified gen+edit | ~$0.04 |
| **Kling Image V3** | `fal-ai/kling-image/v3/text-to-image` | Kling-native image gen | ~$0.04 |
| **SDXL** | `fal-ai/fast-sdxl` | Fast, free-tier friendly | ~$0.01 |

### Image Editing
| Model | Endpoint | Best For |
|-------|----------|----------|
| **FLUX Kontext Pro** | `fal-ai/flux-pro/kontext` | Character editing preserving identity |
| **FLUX Kontext Max** | `fal-ai/flux-pro/kontext/max` | Premium consistency editing |
| **FLUX 2 Pro Edit** | `fal-ai/flux-2-pro/edit` | Style transfer, sequential edits |
| **Nano Banana Edit** | `fal-ai/nano-banana-pro/edit` | Fast Google editing |
| **Ideogram Reframe** | `fal-ai/ideogram/v3/reframe` | Extend/crop images with context |
| **Ideogram Character Edit** | `fal-ai/ideogram/character/edit` | Edit character preserving identity |
| **Seedream v4.5 Edit** | `fal-ai/bytedance/seedream/v4.5/edit` | Unified editing |
| **FASHN Try-On** | `fal-ai/fashn/tryon/v1.6` | Virtual clothing try-on |

### Image Utilities
| Model | Endpoint | Best For |
|-------|----------|----------|
| **BiRefNet v2** | `fal-ai/birefnet/v2` | Background removal (best) |
| **Bria RMBG 2.0** | `fal-ai/bria/background/remove` | Background removal (commercial) |
| **Bria Expand** | `fal-ai/bria/expand` | Outpainting / image expansion |
| **Topaz Upscale** | `fal-ai/topaz/upscale/image` | Professional image upscaling |
| **SeedVR2 Upscale** | `fal-ai/seedvr/upscale/image` | AI image upscaling |
| **Recraft Crisp Upscale** | `fal-ai/recraft/upscale/crisp` | Detail-focused upscaling |
| **Recraft Vectorize** | `fal-ai/recraft/vectorize` | Raster to SVG conversion |
| **VecGlypher** | `fal-ai/vecglypher/image-to-svg` | Custom font/glyph SVG generation |
| **SAM 3** | `fal-ai/sam-3/image` | Segment anything (text/visual prompt) |
| **Qwen Layered** | `fal-ai/qwen-image-layered` | Decompose image into RGBA layers |

## AUDIO GENERATION

### Music
| Model | Endpoint | Best For | Cost |
|-------|----------|----------|------|
| **CassetteAI Music** | `cassetteai/music-generator` | Fast custom music from text | $0.02/min |
| **ElevenLabs Music** | `fal-ai/elevenlabs/music` | High-quality music gen | ~$0.05/min |
| **Lyria2** | `fal-ai/lyria2` | Google's music gen | ~$0.03/min |
| **MiniMax Music v2** | `fal-ai/minimax-music/v2` | Diverse musical styles | ~$0.03/min |
| **Sonauto V2** | `sonauto/v2/text-to-music` | Full songs with lyrics | ~$0.05/song |
| **ACE-Step** | `fal-ai/ace-step` | Music with lyrics from text | ~$0.03/min |
| **Stable Audio 2.5** | `fal-ai/stable-audio-25/text-to-audio` | Open source audio gen | ~$0.02/min |
| **Beatoven** | `beatoven/music-generation` | Royalty-free instrumental | ~$0.03/min |

### Sound Effects
| Model | Endpoint | Best For | Cost |
|-------|----------|----------|------|
| **CassetteAI SFX** | `cassetteai/sound-effects-generator` | Fast custom SFX | $0.01/gen |
| **MMAudio V2 T2A** | `fal-ai/mmaudio-v2/text-to-audio` | Text-to-sound effects | ~$0.01/gen |
| **ElevenLabs SFX** | `fal-ai/elevenlabs/sound-effects/v2` | Premium sound effects | ~$0.02/gen |
| **Beatoven SFX** | `beatoven/sound-effect-generation` | Professional SFX | ~$0.02/gen |

### Text-to-Speech
| Model | Endpoint | Best For |
|-------|----------|----------|
| **ElevenLabs v3** | `fal-ai/elevenlabs/tts/eleven-v3` | Premium TTS |
| **ElevenLabs Turbo** | `fal-ai/elevenlabs/tts/turbo-v2.5` | Fast TTS |
| **MiniMax Speech HD** | `fal-ai/minimax/speech-02-hd` | High quality speech |
| **Chatterbox** | `fal-ai/chatterbox/text-to-speech` | Expressive/meme TTS |
| **Dia TTS** | `fal-ai/dia-tts` | Dialogue with nonverbals |

### Audio Utilities
| Model | Endpoint | Best For |
|-------|----------|----------|
| **Whisper** | `fal-ai/whisper` | Speech transcription |
| **ElevenLabs STT** | `fal-ai/elevenlabs/speech-to-text` | Premium transcription |
| **Demucs** | `fal-ai/demucs` | Stem separation (voice/drums/bass) |
| **SAM Audio** | `fal-ai/sam-audio/separate` | Isolate any sound by text |
| **ElevenLabs Isolation** | `fal-ai/elevenlabs/audio-isolation` | Voice isolation |
| **DeepFilterNet 3** | `fal-ai/deepfilternet3` | Noise removal + upsampling |
| **FFmpeg Merge Audios** | `fal-ai/ffmpeg-api/merge-audios` | Combine audio tracks |

## DYNAMIC SHOT SELECTION GUIDE

When planning B-roll, choose models based on the shot's purpose:

| Shot Type | Recommended Models | Why |
|-----------|-------------------|-----|
| **Hero establishing shot** | Veo 3.1, Sora 2 | Maximum cinematic quality |
| **Character close-up** | Kling 2.6 Pro (I2V from LoRA) | Best human realism |
| **Data visualization / UI** | MiniMax Hailuo (cheap, fast) | Doesn't need realism |
| **Product/object showcase** | Kling 3.0 Pro | Detail preservation |
| **Scene transition** | Kling O3 / Veo 3.1 first-last-frame | Smooth A→B morph |
| **Dance/fitness replication** | Kling v3 Motion Control | Transfer motion from reference |
| **3D rotating object** | Kling O3 Reference | Consistent multi-angle |
| **News footage feel** | Veo 3.1 with native audio | Realistic ambient sound |
| **Abstract/artistic** | Pika v2.2, PixVerse v5.5 | Creative stylization |
| **Budget filler** | Wan 2.5, LTX 2.3 | Good enough at lowest cost |
| **Talking head hook** | HeyGen Avatar4 (expressive, 1080p) | Best lip sync quality |
| **Full body avatar** | Kling Avatar Pro | Gesture + lip sync |
| **Thumbnail with text** | Ideogram V3 (QUALITY) | Best text rendering |
| **Character-consistent image** | FLUX LoRA + Ideogram Character | Identity preservation |
