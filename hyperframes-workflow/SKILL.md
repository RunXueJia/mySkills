---
name: hyperframes-workflow
description: Repeatable workflow for creating, previewing, validating, rendering, and troubleshooting HyperFrames video projects. Use when the user asks to generate a HyperFrames video, follow a standard HyperFrames production process, render with Docker on Windows, or fix Docker render failures caused by Debian/Chromium/font package downloads on China network mirrors.
---

# HyperFrames Workflow

Use this skill as the operating checklist around the existing HyperFrames skills.

- Use `hyperframes` for composition authoring, captions, media timing, transitions, and video structure.
- Use `hyperframes-cli` for CLI commands such as `init`, `preview`, `lint`, `inspect`, `render`, `doctor`, and `browser`.
- Use `tailwind`, `gsap`, `css-animations`, `waapi`, `three`, `lottie`, or `animejs` only when the project actually uses those technologies.

## Standard Flow

For a new project:

```powershell
npx hyperframes init my-video --example blank --tailwind
cd my-video
npm install
```

When asking Codex to create the video, collect the practical spec first:

- Duration and resolution
- Visual style
- Scene list or content beats
- Required text, logo, images, video, music, and voiceover
- Whether Tailwind, GSAP, CSS animations, or plain JS should be used
- Expected output filename and quality

Put user-provided media under `assets/` and reference it from the composition with project-relative paths.

## Preview And Validation

Use preview for creative iteration before rendering:

```powershell
npx hyperframes preview
```

Check the preview for aspect ratio, text overflow, animation timing, media loading, audio sync, and total duration.

Before rendering, run:

```powershell
npx hyperframes lint
npx hyperframes inspect
```

Fix lint errors and serious inspect findings before rendering. Warnings such as `timeline_track_too_dense` do not block render unless `--strict` or `--strict-all` is used, but they are a signal to split coherent scene groups into sub-compositions when the timeline becomes hard to maintain.

## Rendering

Prefer Docker when reproducibility matters:

```powershell
npx hyperframes render --docker --output output.mp4
```

Use local rendering when Docker image build is blocked by network issues:

```powershell
npx hyperframes render --output output.mp4 --no-browser-gpu
```

For final high-quality Docker output:

```powershell
npx hyperframes render --docker --output output.mp4 --fps 60 --quality high
```

## Docker Build Troubleshooting

If `npx hyperframes render --docker` fails while building `hyperframes-renderer:<version>`, inspect the failing Docker step:

- Fails in `apt-get update` or `apt-get install`: treat it as Debian mirror/network trouble, not a HyperFrames composition failure.
- Fails on `Certificate verification failed` after switching to `https` mirrors: use `http` mirrors until `ca-certificates` is installed.
- Fails downloading large packages such as `chromium`, `fonts-noto-extra`, or `fonts-noto-cjk`: remove nonessential packages first and rely on `chrome-headless-shell` for rendering.
- Fails at `npx --yes @puppeteer/browsers install chrome-headless-shell@stable`: treat it as Chrome binary download/network trouble; adding an npm registry mirror only helps npm package metadata, not necessarily the Chrome binary URL.

For Windows/China network mirror failures, copy `assets/Dockerfile.hf` from this skill into the HyperFrames project directory and build the image manually:

```powershell
docker build --progress=plain --platform linux/amd64 -t hyperframes-renderer:0.5.7 -f Dockerfile.hf .
```

After a successful manual build, HyperFrames will detect the cached image and skip its own Docker image build:

```powershell
npx hyperframes render --docker --output output.mp4
```

Do not use `--no-cache` after the expensive apt layer succeeds unless the Dockerfile lines before or inside that layer changed. Without `--no-cache`, Docker can reuse completed layers and continue from the later failing step.

## Version Handling

The Docker image tag must match the HyperFrames version used by the CLI. Check the version when needed:

```powershell
npm view hyperframes version
```

If the current version is not `0.5.7`, update both:

- `ARG HYPERFRAMES_VERSION=<version>` in `Dockerfile.hf`
- `-t hyperframes-renderer:<version>` in the manual `docker build` command

## Continuing Existing Projects

For ongoing edits:

```powershell
cd my-video
npx hyperframes preview
npx hyperframes lint
npx hyperframes inspect
npx hyperframes render --docker --output output.mp4
```

Keep creative iteration in preview. Render only after the timeline and layout are stable.
