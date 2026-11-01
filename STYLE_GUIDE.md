# Reel editing style (approved: reel2, final version)

Apply to every new video unless the user says otherwise.

**Format:** 1080x1920 (9:16), 30 fps, pure white background, built with the HyperFrames CLI (`reel2/` is the template: `tools/assemble.py` -> `tools/sound.py` -> `tools/build.py` -> `npx hyperframes render -q standard`).

**Characters / layout (y in px):** one character only (user's 3D hoodie character: pointL / pointR / think poses, bottom-anchored ~y985-1685, 700px tall, centred). App label y~215 (Poppins 700, 46px) above a 300px logo tile; two logos at x +-262 (scale 0.92), single logo centred (scale 1.18). Subtitle box top 700, Noto Sans Malayalam/Poppins 800, **52px, centred**, max 2 lines, one short chunk at a time. Black `@fyze.ai` watermark (38px, 70% opacity) centred at y~1722 under the character until the end card. Nothing in the top 168 px.

**Scene pattern per pair:** point-left pose "ഇത് X" (logo X pops left) -> point-right "ഇത് Y" (Y pops right) -> thinking pose "എന്താണ് വ്യത്യാസം?" -> X slides to centre while explained -> Y pops centre while explained.

**Voice:** ElevenLabs "Abhilash S - Fun, Encouraging Friend" (voice_id TyWXr0PTH6rgkJ5wKSZe), model eleven_v4, one clip per phrase, trimmed, **speed 1.25x for reel2 (kept as is). From the next video use 1.35x** (`REEL_SPEED=1.35`; user wants between 1.25 and 1.5), gaps 0.14/0.14/0.26/0.22/0.55 s. Free tier rate-limits (~10/min): send in small batches, wait 40-60 s.

**Volume:** voice was too quiet on phones. From the next video raise it ~+3 dB (`REEL_VOICE_GAIN=1.45`, soft-limited; peak must stay below 0 dBFS). Not much louder than that. reel2 itself stays unchanged.

**Sound:** voice + the user's uploaded mouse click only (`reel2/audio/click.wav`) on every app-name/logo appearance and when the end card appears. **No BGM, no booms/whooshes/pops.**

**Ending:** no spoken "follow" line. After the last explanation, show the user's "Follow fyze.ai" card (`reel2/assets/endcard.png`) full-frame for ~2.5 s with the click sound.

**Logos:** only the user's supplied logo files (never redrawn); crop to the icon, white margin ~6-10%; flatten transparent images onto white before cropping (black corners otherwise).

**Delivery:** send the MP4 to the user; push to GitHub when access is available (currently 403 until the Claude GitHub App is installed).

## Update (reel 5 request): "increase a little more speed and volume"
From reel 5 on: `REEL_SPEED=1.45` and `REEL_VOICE_GAIN=1.75` (was 1.35 / 1.45). Photo-based reels use 340x250 rounded photo tiles (`.logo.photo`) instead of 300px icon tiles.

## ElevenLabs free tier (important)
The free plan has 10,000 credits; by the end of reel 5 only 28 were left and the account then reported "Free Tier access disabled". Many "busy" refusals and later silent failures were this. Check `creative_get_flow_run_status` for `failed` generations (error_message) before assuming a line exists. Further voice needs a paid plan or a user-supplied voiceover.

## Clarification
Removing the repeated "Debit Card:/Credit Card:" prefixes and hiding photo labels applied ONLY to reel 5. For other reels keep the names in the scripted dialogue and show the labels, unless the user says otherwise per video.
