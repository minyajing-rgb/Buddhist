---
name: product-acceptance
description: Independently review every product page, state, feature and flow after implementation and actual live versions after authorized release; fix and retest before owner review.
metadata:
  standard_version: 1.0.0
---
Read product-definition and complete approved PRD/UI/flow/architecture. Bind each review to exact source/build/environment/URL/browser/device/viewport/locale. All required concrete pages/branches/tabs/modals/states form the denominator. PASS/FAIL/BLOCKED/NA_WITH_REASON; untested cannot pass.
Open ACTUAL desktop/mobile screenshots against mockups; inspect hierarchy/layout/type/spacing/colors/contrast/original imagery/readability/controls/clipping/overlap/zoom/focus/reduced motion. DOM-only tests and builder claims are not visual acceptance. Exercise every CTA and success/error/empty/loading/timeout/permissions/cancel/back/refresh/deeplink/storage-denied/repeat path. Verify real outcomes and applicable auth/RLS/data/API/model/forms/payment safely; no unauthorized side effects or weakened security.
Defects need severity, reproduction, expected/actual, evidence, fixing commit and retest. Fix and rerun regressions. No internal acceptance with incomplete coverage, missing visual inspection, open P0/P1 or unaccepted P2. Check actual visitor value, architecture/privacy/language/SEO/performance.
Separate build, preview, internal acceptance, owner review, deployed and live-verified. After authorized deployment inspect real live version/hash, every route and critical flow, not stale preview. Preserve old site when requested. No repeated backup diversion or repeated requests for owner to ask for review. Hand off only self-checked candidate; unfinished remains NOT_READY.
Pinned full standard/templates: minyajing-rgb/GGC-AI-Spirituality-Research @ b50cc78567641341419c45a5759811b70f9d0456, .agents/skills/product-acceptance/SKILL.md and skills/product-delivery/.
