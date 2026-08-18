# Video Production Capabilities

Complete inventory of asset generation, editing, and delivery tools available for video production. Use this to plan what assets to generate and how to assemble them.

## Architecture Overview

```
Topic/Script
    ↓
┌─────────────────────────────────────────────┐
│  ASSET GENERATION (parallel)                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ Images   │ │ Video    │ │ Audio    │    │
│  │ fal.ai   │ │ fal.ai   │ │ 11Labs   │    │
│  │ FLUX     │ │ Kling    │ │ fal.ai   │    │
│  │ Ideogram │ │ HeyGen   │ │ CassetteAI│   │
│  └──────────┘ └──────────┘ └──────────┘    │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  ASSEMBLY                                   │
│  ┌──────────────────────────────────────┐   │
│  │ DaVinci Resolve (MCP-controlled)    │   │
│  │ Timeline, Fairlight, Fusion, Color  │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────┐
│  DELIVERY                                   │
│  Platform fan-out → Upload-Post API         │
│  YouTube Shorts, Instagram Reels,           │
│  TikTok, LinkedIn                           │
└─────────────────────────────────────────────┘
```

---

## 1. Image Generation

### Models

| Model | Endpoint | Best For | Cost | Notes |
|-------|----------|----------|------|-------|
| **FLUX LoRA** | `fal-ai/flux-lora` | Character shots (Sofia/finance-ai) | ~$0.03 | Trigger: `sfvlr` (Sofia), `srndrs` (finance-ai). Scale 1.0, guidance 3.5, 28 steps |
| **FLUX Ultra** | `fal-ai/flux-pro/v1.1-ultra` | Objects, scenery, product shots | ~$0.06 | No LoRA needed for non-character shots |
| **FLUX Kontext Pro** | `fal-ai/flux-pro/kontext` | Character identity preservation, edits | ~$0.04 | Input image + text prompt for style transfer |
| **FLUX Kontext Max** | `fal-ai/flux-pro/kontext/max` | Complex multi-step edits | ~$0.08 | Higher quality Kontext |
| **Ideogram V3** | `fal-ai/ideogram/v3` | Thumbnails with text | ~$0.04 | Best text rendering of any model |
| **Recraft V4** | `fal-ai/recraft-v3` | Design-ready graphics | ~$0.04 | Clean vector-like output |
| **BiRefNet v2** | `fal-ai/birefnet/v2` | Background removal | ~$0.01 | |
| **Topaz Upscale** | `fal-ai/topaz` | Image upscaling | ~$0.02 | Up to 4x |

### Routing Logic (`generate_broll_keyframe()`)

```
Character in prompt? → FLUX LoRA (with profile trigger)
Object/scenery?      → FLUX Ultra (no LoRA)
Thumbnail with text? → Ideogram V3
```

### Code: `engine/media/generation/fal_image.py`, `fal_lora.py`

---

## 2. Video Generation

### Image-to-Video (I2V) — Primary Pipeline

Generate a keyframe image first, then animate it.

| Model | Endpoint | Best For | Cost/sec | Duration | Notes |
|-------|----------|----------|----------|----------|-------|
| **Kling 2.6 Pro** | `fal-ai/kling-video/v2/master/image-to-video` | Reliable B-roll, realistic humans | $0.07 | 5-10s | Best all-rounder |
| **Kling 3.0** | `fal-ai/kling-video/v3/image-to-video` | Expressive faces, character motion | $0.22 | 5-10s | Best for close-ups |
| **Kling O1** | `fal-ai/kling-video/v2.5/master/image-to-video` | Start+end frame transitions | $0.07 | 5s | Best for scene transitions |
| **Kling O3** | `fal-ai/kling-video/v3/master/image-to-video` | Premium start+end frame | $0.22 | 5s | |
| **MiniMax Hailuo** | `fal-ai/minimax/video-01` | Fast cheap B-roll | $0.017 | 6s | Budget option |
| **Wan 2.5** | `fal-ai/wan-ai/wan2.1/v2v` | Budget, artistic | $0.05 | 5s | |
| **Pika** | (via MCP) | Creative/stylized motion | varies | 4s | Good for abstract |

### Text-to-Video (T2V) — No keyframe needed

| Model | Endpoint | Cost/sec | Notes |
|-------|----------|----------|-------|
| **Kling 3.0 T2V** | `fal-ai/kling-video/v3/text-to-video` | $0.22 | |
| **LTX 2.3** | `fal-ai/ltx-video/v2.3` | $0.04 | Includes audio generation |
| **Sora 2** | (via API) | $0.50 | Hollywood quality |

### Avatar Video

| Model | Endpoint | Best For | Cost | Notes |
|-------|----------|----------|------|-------|
| **Kling Avatar Pro** | `fal-ai/kling-video/ai-avatar/v2/pro` | Sofia (full body motion) | ~$0.15/s | |
| **HeyGen Avatar IV** | `fal-ai/heygen/avatar4/image-to-video` | Finance-ai (talking head) | $0.10/s | Custom outfit per video via LoRA keyframe upload |

### Specialized

| Capability | Models | Notes |
|------------|--------|-------|
| **Lip Sync** | Kling Lipsync, Sync Lipsync Pro, PixVerse | Audio → lip-synced video |
| **Motion Control** | Kling v3/v2.6 motion control | Map reference motion to character |
| **Video Upscale** | Topaz, Kling upscale | Up to 4K |

### Model Selection Guide

```
Talking head (finance-ai)     → HeyGen Avatar IV (talking photo)
Talking head (Sofia)          → Kling Avatar Pro
B-roll (people, lifestyle)    → Kling 2.6 Pro or Kling 3.0
B-roll (objects, abstract)    → MiniMax Hailuo (cheap) or Kling 2.6 Pro
Scene transitions             → Kling O1/O3 (start+end frame)
Budget/fast                   → MiniMax Hailuo ($0.017/s)
Premium                       → Kling 3.0 ($0.22/s)
```

### Constraints

- **Veo 3.1**: Blocked for Sofia lifestyle/swimwear content. Do not use.
- **Seedance**: Audio may be Chinese — always strip audio from Seedance clips.
- **Avatar prompts**: Director-style physical choreography ("leans forward, holds up one finger") NOT abstract emotions.
- **LoRA identity**: Use LoRA keyframe as I2V input — video LoRA not needed for I2V pipeline.

### Code: `engine/media/generation/fal_video.py`, `heygen_client.py`

---

## 3. Audio Generation

### Voice / TTS

| Service | Best For | Notes |
|---------|----------|-------|
| **ElevenLabs** | Voiceover narration | 13 emotion presets per phrase. Sofia voice: `4tRn1lSkEn13EVTuqb0g`. Finance-ai voice: `Ch9eAOd5SabkaPfS9cIA` |
| **ElevenLabs Studio** | Podcasts (2-voice) | Host: `Ch9eAOd5SabkaPfS9cIA`, Guest: `kvQSb3naDTi3sgHwwBC1` |

### Music

| Service | Endpoint | Cost | Notes |
|---------|----------|------|-------|
| **CassetteAI** | via API | $0.02/min | Best for background music |
| **ElevenLabs Music** | via API | varies | |
| **Lyria2** | `fal-ai/lyria2` | varies | Google's music model |
| **Sonauto** | via API | varies | Full songs with lyrics |

### Sound Effects

| Service | Endpoint | Notes |
|---------|----------|-------|
| **MMAudio V2** | `fal-ai/mmaudio/v2` | Video-to-audio SFX |
| **CassetteAI SFX** | via API | Text-to-SFX |

### Auto-Captions

`fal_audio.add_captions()` — karaoke-style word-by-word highlights:
- Finance-ai: cyan highlights
- Sofia: pink highlights

### Code: `engine/media/generation/fal_audio.py`, `elevenlabs_client.py`, `audio_mixer.py`

---

## 4. Assembly — DaVinci Resolve (MCP-Controlled)

MCP-controlled professional editing via DaVinci Resolve Studio 20.3.

### What Works via MCP

| Category | Capabilities |
|----------|-------------|
| **Project Setup** | Create project, set resolution/fps/color science, import media, organize bins |
| **Timeline Building** | Create timeline from clips, insert generators, insert Fusion titles, link clips |
| **Clip Transforms** | Pan, Tilt, Zoom, Rotation, Crop, Opacity, Composite mode, Retime (optical flow) |
| **Color Grading** | CDL per node (Slope/Offset/Power/Saturation), color versions (add/load/rename/delete), copy grades between clips, color groups (assign/remove), grade management via stills (export DRX + reimport) |
| **Secondary Color** | Power Windows (shape masks), Qualifier (HSL color isolation), Outside Nodes (invert selection), Tracker (motion follow), HSL Curves (Hue vs Sat, Hue vs Hue, etc.), Color Warper (mesh-based hue+sat), Chroma Warper — all via Color page UI; MCP can set CDL on additional nodes but window/qualifier setup requires Resolve UI |
| **AI Features** | Stabilize, Smart Reframe, Scene Cut Detection, Grab Stills |
| **Fusion VFX** | Add tools (TextPlus, Merge, Background, Transform, Blur, ColorCorrector), connect node graph, set values, render comp |
| **Audio Tracks** | Add/delete audio tracks, name tracks, enable/disable, lock/unlock, set clip pan |
| **Gallery** | Export/import stills with DRX grades, label stills |
| **Rendering** | Set format/codec (22 formats, H.264/H.265), load presets (TikTok/YouTube/Vimeo), add render job, start render, monitor progress |
| **Vertical Timelines** | Duplicate timeline, static reframe via set_transform, Smart Reframe (AI) |

### What Does NOT Work via MCP

| Feature | Workaround |
|---------|------------|
| Keyframe animation | Use static transforms or Fusion `set_input` at specific times |
| Timeline export (EDL/FCPXML) | Export from Resolve UI |
| Add video/subtitle tracks | Add in Resolve UI first |
| Magic Mask | Use Resolve UI |
| Fairlight FX (EQ, Dynamics, Ducker, Dialogue Leveler) | Apply in Fairlight mixer UI |
| Audio clip volume | Pan works, volume fails on clips without audio |
| Subtitle generation from audio | `create_subtitles` fails — use Whisper via fal.ai |
| LUT export | Use Resolve UI |
| Quick Export | Use `add_job` + `start` instead |

### Typical MCP Workflow

```
1. open_page("edit")
2. media_pool.import_media([clip_paths])
3. media_pool.create_timeline_from_clips(clip_ids, "MyTimeline")
4. For each clip:
   - timeline_item.set_transform(ZoomX=1.1, ZoomY=1.1)  # Ken Burns
   - timeline_item.set_crop(...)                          # Reframe
5. open_page("color")
6. For each clip:
   - timeline_item_color.set_cdl({Slope, Offset, Power, Saturation})
   - timeline_item_color.stabilize()
7. open_page("fusion")
8. fusion_comp.add_tool("TextPlus") → set_input("StyledText", "Title")
9. render.load_preset("TikTok - 1080p")
10. render.set_settings({TargetDir, CustomName})
11. render.add_job() → render.start([job_id])
12. Poll render.get_job_status() until Complete
```

### Code: MCP tools via `mcp__davinci-resolve__*`, reference at `docs/davinci-resolve-mcp-reference.md`

---

## 6. Captions & Transcription

| Method | Tool | Notes |
|--------|------|-------|
| **Auto-subtitle** | `fal_audio.add_captions()` | Karaoke word highlights, profile-colored |
| **Whisper transcription** | `whisper_transcriber.transcribe_video()` | SRT/VTT export |
| **Caption burn** | `whisper_transcriber.burn_captions()` | Burn SRT into video |
| **Submagic** | Browser automation | AI captions with B-roll (external service) |
| **Resolve AI subtitles** | `timeline_ai.create_subtitles()` | Requires audio in clips |

---

## 7. Publishing & Delivery

### Platform Fan-out

| Platform | Format | Resolution | Max Duration | Notes |
|----------|--------|------------|-------------|-------|
| YouTube Shorts | MP4 H.264 | 1080x1920 | 60s | No custom thumbnail — append 2s thumbnail clip |
| Instagram Reels | MP4 H.264 | 1080x1920 | 90s | |
| TikTok | MP4 H.264 | 1080x1920 | 60s | |
| LinkedIn | — | — | — | **No video publishing** for finance-ai (text/image/carousel only) |

### Upload-Post API

All publishing goes through `engine/media/upload_post.py`:
- `post_video()` — video upload with scheduling
- `post_photo()` — image/carousel (supports scheduling)
- `post_document()` — PDF carousel (**no scheduling support**)
- Upload-Post usernames: `sofiavalerofit` (Sofia), `Surendra` (finance-ai)

---

## 8. Cost Estimates

### Per 60-Second Video

| Tier | Assets | Assembly | Total |
|------|--------|----------|-------|
| **Budget** | MiniMax B-roll ($1), CassetteAI music ($0.02), ElevenLabs voice ($0.30) | Resolve (free) | ~$2 |
| **Standard** | Kling 2.6 Pro B-roll ($4), HeyGen avatar ($6), ElevenLabs voice ($0.30), music ($0.50) | Resolve (free) | ~$11 |
| **Premium** | Kling 3.0 B-roll ($13), HeyGen avatar ($6), ElevenLabs voice ($0.30), music ($0.50) | Resolve (free) | ~$20 |

### Per Asset Type

| Asset | Budget | Standard | Premium |
|-------|--------|----------|---------|
| Keyframe image | $0.03 (FLUX LoRA) | $0.06 (FLUX Ultra) | $0.08 (Kontext Max) |
| 5s B-roll clip | $0.09 (MiniMax) | $0.35 (Kling 2.6) | $1.10 (Kling 3.0) |
| 10s avatar clip | $1.00 (Kling Avatar) | $1.00 (HeyGen AV4) | $1.50 (Kling Avatar Pro) |
| 60s voiceover | $0.30 (ElevenLabs) | $0.30 | $0.30 |
| Background music | $0.02 (CassetteAI) | $0.50 (Lyria2) | $1.00 (Sonauto) |
| Thumbnail | $0.04 (Ideogram) | $0.04 | $0.04 |

---

## 9. Decision Framework

### DaVinci Resolve Capabilities

| Feature | Tool | Notes |
|---------|------|-------|
| Timeline assembly | MCP `media_pool` + `timeline` | Clip import, sequencing, tracks |
| Color grading | Color page (manual) | CDL via MCP broken — grade in UI |
| VFX | Fusion node graph | TextPlus, Blur, CC, Merge |
| Audio mixing | Fairlight page | EQ, dynamics, bus routing, AI tools |
| Stabilization | AI stabilize + smart reframe | Per-clip via MCP |
| Text overlays | Fusion TextPlus | Animated, styled |
| Output | H.264, H.265, ProRes, IMF | Professional render queue |

### Asset Generation Decision Tree

```
Need character in shot?
├─ Yes → FLUX LoRA keyframe → Kling I2V (or HeyGen avatar if talking)
└─ No → FLUX Ultra keyframe → Kling 2.6 Pro I2V (or MiniMax for budget)

Need text in image?
├─ Yes → Ideogram V3
└─ No → FLUX Ultra or LoRA

Need talking head?
├─ Finance-ai → HeyGen Avatar IV (talking photo, portrait, no avatar)
└─ Sofia → Kling Avatar Pro (full body)

Need background music?
├─ Budget → CassetteAI ($0.02/min)
├─ Standard → Lyria2
└─ Premium → Sonauto (full song with lyrics)

Need captions?
├─ Auto-subtitle → fal_audio.add_captions() (karaoke style)
├─ Transcription → whisper_transcriber (SRT/VTT)
└─ Premium → Submagic (AI captions + B-roll)
```
