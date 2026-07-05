# jkbmsr-releases

Public release repository for JKBMSR distributable artifacts.

JKBMSR means **JK Battery Management System Remote**.

This repository is public by design. It is for release binaries, checksums, signed OTA metadata, release notes, and public download documentation.

Public artifact host:

- `https://cdn.jkbmsr.com`

Authenticated OTA delivery remains separate and continues through the JKBMSR cloud API. This repository and domain are for public manual downloads and verification material.

## Scope

This repository may contain:

- ESP32 firmware release binaries
- SHA-256 checksum files
- Signed OTA metadata
- Public OTA verification keys
- Release notes and changelogs
- Public download instructions
- Future Android APK release artifacts

This repository must not contain:

- Firmware source code
- Mobile source code
- Cloud or dashboard source code
- Private signing keys
- GitHub, Cloudflare, or API secrets
- Internal-only architecture material

## Current Published Artifacts

- Firmware target: `esp32dev`
- Current published firmware: `v0.1.2`
- OTA signing key ID: `jkbmsr-ota-p256-20260705`
- OTA signature algorithm: `ecdsa-p256-sha256`

## Repository Layout

```text
firmware/
  esp32dev/
    v0.1.2/
      firmware.bin
      firmware.sha256
      firmware-metadata.json
      release.json
      RELEASE_NOTES.md
  latest.json
mobile/
  android/
    README.md
ota/
  latest.json
  keys/
    public/
      jkbmsr-ota-p256-20260705.pem
docs/
  VERIFY_FIRMWARE.md
  OTA_SECURITY.md
  DOWNLOADS.md
CHANGELOG.md
README.md
```

## Related Repositories

- `jkbmsr-firmware`: private source repository for ESP32 firmware
- `jkbmsr-cloud`: private backend/API repository
- `jkbmsr-web`: private dashboard repository
- `jkbmsr-mobile`: private mobile app planning and future source repository

## Rules

- Publish only artifacts intended for customer or installer consumption.
- Keep release metadata aligned with the production OTA release.
- Never publish private signing material.
- Keep version 1 limited to JK-BMS support only.

## Deployment

- Cloudflare Pages project: `jkbmsr-releases`
- Public custom domain: `cdn.jkbmsr.com`
- Source branch: `main`
- Deployment workflow: `.github/workflows/pages.yml`

The Cloudflare Pages deployment should publish this repository as a static artifact mirror only. Do not place authenticated APIs, upload handlers, or private operational tooling behind this domain.

## Publishing Model

- `cdn.jkbmsr.com` is the canonical anonymous host for manual downloads.
- `api.jkbmsr.com` remains the authenticated OTA channel for managed devices.
- `jkbmsr-firmware` is the private source of truth for firmware source, release generation, and OTA signing.
- Public artifacts mirrored here must match the release metadata published by the production OTA flow.

## Maintainer Checklist

Before merging public artifact updates:

1. Confirm the firmware binary, checksum, and public metadata all describe the same version.
2. Confirm `firmware/latest.json` points at the current public version and target.
3. Confirm `ota/latest.json` exposes only public verification material.
4. Confirm no private keys, Cloudflare tokens, or internal-only files were added.
5. Confirm links on `index.html` and docs still resolve under `https://cdn.jkbmsr.com`.
