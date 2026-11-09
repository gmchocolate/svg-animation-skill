# Local motion taste library

The open-source Skill ships reusable grammar. Each user maintains a **private library of actual motion files** and personal notes in the environment where the CLI runs.

## Storage

Default: ~/.svg-animation-skill/
- index.json: IDs, user ratings, tags, use cases, liked_for and avoid_copying.
- media/: locally copied reference source files (content SHA-256 filenames).

Override with SVG_ANIMATION_HOME=/absolute/path or --home /absolute/path. This directory is intentionally outside the installed Skill and Git repository. No automatic syncing, retrieval or cloud uploads. File copies are kept in their original media format. **EXIF and other embedded metadata in GIF, images and videos are not stripped.** Do not store sensitive source files unless you are comfortable retaining the original metadata locally.

## Modes

~~~bash
# Only when the user explicitly agrees to persistent saving:
python scripts/motion_library.py add --file path/to/reference.webm \
  --title "Quiet onboarding transition" \
  --use-case onboarding --tag gentle \
  --like "first show relationship, then highlight" \
  --avoid "source brand mark" --rating 5

python scripts/motion_library.py list
python scripts/motion_library.py select --use-case onboarding --tag gentle --top 2
python scripts/motion_library.py prepare --use-case onboarding \
  --request "Create an original SaaS onboarding SVG"
python scripts/motion_library.py feedback --id ref-1234567890abcdef1234 \
  --like "one primary motion at a time" --rating 5
python scripts/motion_library.py remove --id ref-1234567890abcdef1234
~~~

Allowed formats: SVG, GIF, MP4, WebM, Lottie JSON, PNG, JPG/JPEG and WebP. SVG is parsed and rejected if it contains scripts, event handlers, foreignObject, DTD/entities or nonlocal resource URLs. This is only a basic safety boundary, not a complete sanitizer. Other binaries remain unexecuted local data. Lottie JSON is parsed and checked for basic format; it is never executed by the CLI.

A GIF/video reveals motion only when **actually played**; an SVG with SMIL or CSS may be animated when rendered in a browser. Lottie JSON needs a trusted renderer. A static image reveals only style and geometry.

## Selection vs. vision

The CLI scores matches using user-supplied use-case tags and ratings, not learned embeddings or visual similarity. `prepare` returns a JSON manifest containing real absolute paths. The agent must open/play the referenced media with host-supported tooling to claim visual analysis; text paths do not transfer media bytes to a cloud model.

## Permission

Reading for one task does not grant permission to save permanently. Only persist a reference or feedback if the user requests or approves that act. Local saving does NOT grant permission to redistribute, commit, transmit, or share source files. If an agent runs remotely with no access to the user's computer, it must explain this limitation; a temporary cloud workspace is not the user's local machine.
