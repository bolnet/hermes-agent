# DaVinci Resolve MCP Reference

Tested against DaVinci Resolve Studio **20.3.2** on macOS. All 26 MCP tools systematically tested (2026-03-21).

## Quick Start

```python
# The MCP server auto-launches Resolve if not running (up to 60s first call)
# All tools follow: action + params pattern
# Example: create project → import media → build timeline → grade → render
```

## Tool Index

| Tool | Category | Status |
|------|----------|--------|
| `resolve_control` | App Control | Full |
| `project_manager` | Projects | Full |
| `project_manager_database` | Projects | Full |
| `project_manager_folders` | Projects | Full |
| `project_settings` | Projects | Full |
| `media_storage` | Media | Full |
| `media_pool` | Media | Full |
| `folder` | Media | Full |
| `media_pool_item` | Media | Full |
| `timeline` | Timeline | Partial |
| `timeline_markers` | Timeline | Partial |
| `timeline_ai` | Timeline | Partial |
| `timeline_item` | Clip Editing | Partial |
| `timeline_item_markers` | Clip Editing | Full |
| `timeline_item_takes` | Clip Editing | Partial |
| `timeline_item_fusion` | Clip Editing | Partial |
| `timeline_item_color` | Color | Partial |
| `gallery_stills` | Color | Full |
| `gallery` | Color | Full |
| `fusion_comp` | Fusion | Partial |
| `render` | Delivery | Partial |
| `render_presets` | Delivery | Broken |
| `color_group` | Color | Full |

---

## 1. App Control & Project Management

### resolve_control

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_version` | — | Yes | Returns Resolve version string |
| `get_page` | — | Yes | Returns current page name (edit/color/fusion/deliver/etc.) |
| `open_page` | `page` | Yes | Switch between pages. Values: `edit`, `color`, `fusion`, `fairlight` |
| `get_keyframe_mode` | — | Yes | Returns current keyframe mode |

### project_manager

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_current` | — | Yes | Returns current project name + ID |
| `list` | — | Yes | All projects in current database |
| `save` | — | Yes | Save current project |

### project_manager_database / project_manager_folders

| Action | Works | Notes |
|--------|-------|-------|
| `get_current` (database) | Yes | Current database name |
| `list` (folders) | Yes | Project folders |

### project_settings

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_name` | — | Yes | Project name |
| `get_unique_id` | — | Yes | UUID |
| `get_presets` | — | Yes | All presets |
| `get_setting` | `name?` | Yes | All settings or specific setting. Massive dump when no name. |
| `get_color_groups` | — | Yes | List color groups |
| `add_color_group` | `name` | Yes | Create new group |

---

## 2. Media Storage & Media Pool

### media_storage

| Action | Works | Notes |
|--------|-------|-------|
| `get_volumes` | Yes | List mounted volumes |

### media_pool

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_root_folder` | — | Yes | Root bin |
| `get_current_folder` | — | Yes | Active bin |
| `add_subfolder` | `name` | Yes | Create bin |
| `import_media` | `paths` | Yes | Import files into current bin |
| `create_timeline_from_clips` | `clip_ids, name` | Yes | Build timeline from media pool items |

### folder

| Action | Works | Notes |
|--------|-------|-------|
| `get_clips` | Yes | List clips in folder with IDs |

### media_pool_item

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_clip_property` | `key?` | Yes | Massive metadata. Provide key for specific property. |

---

## 3. Timeline Operations

### timeline

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `list` | — | Yes | All timelines with name, ID, index |
| `get_current` | — | Yes | Active timeline |
| `set_current` | `index` | Yes | 1-based index |
| `get_name` / `set_name` | `name` | Yes | |
| `get_unique_id` | — | Yes | UUID |
| `get_start_timecode` / `set_start_timecode` | `timecode` | Yes | |
| `get_start_frame` / `get_end_frame` | — | Yes | |
| `get_track_count` | `track_type` | Yes | video, audio, subtitle |
| `get_track_name` / `set_track_name` | `track_type, index, name` | Yes | |
| `get_track_enabled` / `set_track_enable` | `track_type, index, enabled` | Yes | |
| `get_track_locked` / `set_track_lock` | `track_type, index, locked` | Yes | |
| `get_items` | `track_type, index` | Yes | Items with name, ID, start, end, duration |
| `set_clips_linked` | `clip_ids, linked` | Yes | Link/unlink clips |
| `duplicate` | `name?` | Yes | Duplicate timeline |
| `get_setting` | `name?` | Yes | All timeline settings |
| `set_mark_in_out` | `mark_in, mark_out` | Yes | |
| `get_mark_in_out` | — | Yes | Returns video + audio marks |
| `clear_mark_in_out` | — | Yes | |
| `insert_fusion_title` | `name` | Yes | Use `"Text+"` — this is the correct method for titles |
| `insert_generator` | `name` | Yes | Use `"Solid Color"` |
| `insert_fusion_composition` | — | Yes | |
| `add_track` | `track_type` | **Audio only** | Video and subtitle fail |
| `delete_track` | `track_type, index` | Yes (audio) | |
| `insert_title` | `name` | **No** | Use `insert_fusion_title` instead |
| `insert_fusion_generator` | `name` | **No** | |
| `export` | `path, type` | **No** | EDL, FCPXML all fail |

### timeline_markers

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `add` | `frame, color, name, note, duration, custom_data?` | Yes | |
| `get_all` | — | Yes | Dict keyed by frame number |
| `get_by_custom_data` | `custom_data` | Yes | |
| `get_custom_data` | `frame` | Yes | |
| `update_custom_data` | `frame, custom_data` | Yes | |
| `delete_at_frame` | `frame` | Yes | |
| `delete_by_color` | `color` | Yes | |
| `delete_by_custom_data` | `custom_data` | Yes | |
| `get_current_timecode` | — | Yes | |
| `set_current_timecode` | `timecode` | Yes | Moves playhead |
| `get_current_video_item` | — | Yes | Returns clip at playhead |
| `get_thumbnail` | — | **No** | Returns None |

### timeline_ai

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `grab_still` | — | Yes | Grabs still at playhead to gallery |
| `grab_all_stills` | `source?` | Yes | One per clip; returns count |
| `detect_scene_cuts` | — | Yes | |
| `create_subtitles` | `settings?` | **Conditional** | Fails if clips have no audio |

---

## 4. Timeline Item Manipulation

All actions default to `track_type="video"`, `track_index=1`, `item_index=0`.

### timeline_item

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_name` | — | Yes | |
| `get_duration` / `get_start` / `get_end` | — | Yes | Frame-based |
| `get_unique_id` | — | Yes | Timeline item UUID |
| `get_media_pool_item` | — | Yes | Returns pool item name + ID |
| `get_source_start_frame` / `get_source_end_frame` | — | Yes | |
| `get_left_offset` / `get_right_offset` | — | Yes | Trim handles |
| `get_property` | `key` | Yes | **Must provide key** — no-key returns null |
| `get_transform` | — | Yes | Pan, Tilt, ZoomX/Y, RotationAngle, AnchorPoint, Pitch, Yaw, Flip |
| `set_transform` | `Pan?, Tilt?, ZoomX?, ZoomY?, RotationAngle?...` | Yes | Per-field success reporting |
| `get_crop` / `set_crop` | `CropLeft?, CropRight?, CropTop?, CropBottom?...` | Yes | Values are 0-1 ratios |
| `get_composite` / `set_composite` | `Opacity?, CompositeMode?` | Yes | Opacity 0-100, Mode is int |
| `get_audio` / `set_audio` | `Volume?, Pan?` | Partial | Volume fails on clips without audio |
| `get_clip_enabled` / `set_clip_enabled` | `enabled` | Yes | |
| `get_retime` / `set_retime` | `process?, motion_estimation?` | Yes | process: nearest/frame_blend/optical_flow (0-3) |
| `add_keyframe` / `get_keyframes` / etc. | — | **No** | NoneType error — MCP bug |

### timeline_item_markers

| Action | Works | Notes |
|--------|-------|-------|
| `add`, `get_all`, `delete_at_frame`, `delete_by_color`, `delete_by_custom_data` | Yes | Same API as timeline markers |
| `set_clip_color` / `get_clip_color` / `clear_clip_color` | Yes | Colors: Orange, Blue, Green, Red, etc. |
| `add_flag` / `get_flags` / `clear_flags` | Yes | |

### timeline_item_takes

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_count` | — | Yes | |
| `add` | `clip_id` | Yes | Add media pool clip as alternate take |
| `get_selected_index` | — | Yes | |
| `get_by_index` | `index` | Partial | **1-based** — index 0 returns None |
| `select` | `index` | Partial | **1-based** — index 0 fails |
| `delete` | `index` | Yes | |

### timeline_item_fusion

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `add_comp` | — | Yes | |
| `get_comp_count` / `get_comp_names` | — | Yes | |
| `rename_comp` | `old_name, new_name` | Yes | |
| `load_comp` | `name` | Yes | Makes comp active for fusion_comp tool |
| `export_comp` | `path, index` | Yes | .setting format |
| `import_comp` | `path` | Yes | |
| `delete_comp` | `name` | **No** | |
| `set_cache` / `get_cache_enabled` | — | **No** | get returns -1, set fails |

---

## 5. Color Grading

### timeline_item_color

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `set_cdl` | `cdl: {NodeIndex, Slope, Offset, Power, Saturation}` | Yes | Slope/Offset/Power are [R,G,B] arrays |
| `get_node_graph` | — | Yes | Returns `available: true` |
| `add_version` | `name, type?` | Yes | type: 0=local, 1=remote |
| `get_current_version` | — | Yes | Returns name + type |
| `get_version_names` | `type?` | Yes | |
| `load_version` | `name, type?` | Yes | Switch active version |
| `rename_version` | `old_name, new_name, type?` | Yes | |
| `delete_version` | `name, type?` | Yes | **Cannot delete active version** — switch first |
| `copy_grades` | `target_ids` | Yes | Copy grade to clips by UUID |
| `get_color_group` / `assign_color_group` / `remove_from_color_group` | `group_name` | Yes | |
| `stabilize` | — | Yes | AI stabilization |
| `smart_reframe` | — | Yes | AI smart reframe |
| `create_magic_mask` | `mode` | **No** | Fails with F, B, BI modes |
| `export_lut` | `type, path` | **No** | |
| `get_color_cache` | — | Yes | Returns 0/1 |
| `set_color_cache` | `enabled` | **No** | |

### gallery_stills (requires Color page)

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_stills` | `album_index?` | Yes | Count of stills |
| `get_label` / `set_label` | `still_index, label` | Yes | |
| `export_stills` | `folder_path, prefix?, format?` | Yes | JPG/PNG/DPX + DRX grade. **Directory must exist.** |
| `grab_and_export` | `folder_path, prefix?, format?, delete_after?, cleanup?` | Yes | Grab + export in one call. **Use cleanup=true** — base64 inline is huge. |
| `import_stills` | `paths` | Yes | Import DRX to restore grades |
| `delete_stills` | `still_indices` | Yes | 0-based array |

---

## 6. Fusion Compositing

Operates on the currently active Fusion comp. Use `timeline_item_fusion.load_comp()` first.

### fusion_comp

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `add_tool` | `tool_type, x?, y?, name?` | Yes | See tool types below |
| `delete_tool` | `tool_name` | Yes | |
| `get_tool_list` | `type?` | Yes | All tools or filtered by type |
| `find_tool` | `name` | Yes | Returns type + full attrs |
| `connect` | `target_tool, input_name, source_tool, output_name?` | Yes | Wire nodes together |
| `disconnect` | `tool_name, input_name` | Yes | |
| `get_inputs` / `get_outputs` | `tool_name` | Yes | Full param list with connection status |
| `set_input` / `get_input` | `tool_name, input_name, value, time?` | Yes | Text, numeric, point values |
| `set_attrs` / `get_attrs` | `tool_name, attrs` | Yes | PassThrough, Locked, Visible, etc. |
| `get_comp_info` | — | Yes | Tool count, frame range, HiQ, etc. |
| `set_frame_range` | `start, end` | Yes | |
| `render` | — | Yes | Render the Fusion comp |
| `start_undo` / `end_undo` | `name?, keep?` | Yes | Batch operations atomically |
| `add_keyframe` | `tool_name, input_name, time, value` | **Partial** | Returns success but creates static value, not spline |
| `get_keyframes` | `tool_name, input_name` | **No** | Always returns empty |
| `delete_keyframe` | `tool_name, input_name, time` | **No** | NoneType error |

**Common tool_type values**: `Merge`, `Background`, `TextPlus`, `Transform`, `Blur`, `ColorCorrector`, `RectangleMask`, `EllipseMask`, `Tracker`, `MediaIn`, `MediaOut`, `Loader`, `Saver`, `Glow`, `FilmGrain`, `CornerPositioner`, `DeltaKeyer`, `UltraKeyer`

**Typical Fusion chain**:
```
MediaIn1 → ColorCorrector → Merge(Background) → Transform → MediaOut1
                              ↑ Foreground
                           TextPlus
```

---

## 7. Rendering & Delivery

### render

| Action | Params | Works | Notes |
|--------|--------|-------|-------|
| `get_formats` | — | Yes | 22 formats (MP4, MOV, MKV, MXF, AVI, EXR, PNG, JPG, GIF, WebP...) |
| `get_codecs` | `format` | Yes | e.g., MP4 → H264, H265, APVYUV422_10 |
| `get_format_and_codec` | — | Yes | Current setting |
| `set_format_and_codec` | `format, codec` | Yes | **Use IDs** like `mp4`/`H264`, not display names |
| `get_resolutions` | `format, codec` | Yes | May return empty (supports custom) |
| `get_mode` | — | Yes | Returns int |
| `set_settings` | `settings` | Yes | `{TargetDir, CustomName}` and more |
| `list_presets` | — | Yes | 35 built-in presets |
| `load_preset` | `name` | Yes | e.g., `"TikTok - 1080p"` |
| `save_preset` / `delete_preset` | `name` | Yes | Custom presets |
| `add_job` | — | Yes | Returns job_id |
| `list_jobs` | — | Yes | Rich metadata per job |
| `get_job_status` | `job_id` | Yes | JobStatus, CompletionPercentage, TimeTakenToRenderInMs, Error |
| `start` | `job_ids?, interactive?` | Yes | Start specific jobs or all |
| `is_rendering` | — | Yes | |
| `quick_export_presets` | — | Yes | 10 presets |
| `quick_export` | `preset` | **No** | Returns None |
| `stop` | — | **Post-render bug** | NoneType after render completes |
| `delete_job` / `delete_all_jobs` | `job_id` | **Post-render bug** | NoneType after render completes |
| `set_mode` | `mode` | **Post-render bug** | NoneType after render completes |

### render_presets

| Action | Works | Notes |
|--------|-------|-------|
| `import_render` / `export_render` | **No** | NoneType — unimplemented |
| `import_burnin` / `export_burnin` | **No** | NoneType — unimplemented |

**Render workflow**:
```
load_preset("TikTok - 1080p") → set_settings({TargetDir, CustomName}) → add_job() → start([job_id]) → poll get_job_status()
```

---

## Known Bugs Summary

| Bug | Affected Tools | Workaround |
|-----|---------------|------------|
| Keyframes broken | `timeline_item`, `fusion_comp` | Use Fusion comp `set_input` at different times (static values only) |
| render_presets unimplemented | `render_presets` | Use `render.list_presets` / `render.load_preset` instead |
| Post-render instability | `render` (delete, stop, set_mode) | Restart MCP connection or call operations before starting render |
| Timeline export fails | `timeline.export` | Export manually from Resolve UI |
| add_track limited | `timeline.add_track` | Only audio tracks can be added; video/subtitle must be added in UI |
| Magic Mask fails | `timeline_item_color` | Use Resolve UI for Magic Mask |
| LUT export fails | `timeline_item_color` | Export LUTs from Resolve UI |
| No Power Window API | `timeline_item_color` | Windows, Qualifiers, HSL Curves, Color/Chroma Warper, Tracker must be set up in Resolve UI. MCP can only set CDL values and copy grades. |

## Gotchas & Tips

- **insert_fusion_title** not `insert_title` for adding Text+ to timeline
- **set_format_and_codec** uses IDs (`mp4`, `H264`) not display names (`MP4`, `H.264`)
- **Takes are 1-based** — index 0 returns None/fails
- **gallery_stills.export** needs the directory to exist beforehand
- **grab_and_export** with `cleanup=false` returns multi-MB base64 inline — always use `cleanup=true`
- **delete_version** cannot delete the active version — load a different version first
- **get_property** on timeline items requires a key — no-key returns null
- **Fusion comp operations** require the comp to be loaded via `timeline_item_fusion.load_comp()`
