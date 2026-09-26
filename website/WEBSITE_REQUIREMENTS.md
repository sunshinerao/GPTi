# GPTI 官网产品与设计要求

Version 1.0 · 2026-09-26 · coding-agent implementation brief · **site has not been built or published**

## 0. Binding instructions

Use Website Design System v1.0 **Platform mode** at commit `4057223710d62398a4a6c543de2e0bc199c33eb7` of `sunshinerao/my-standards`. Before writing UI, read every web path listed in `standards.lock.md`. No token overrides are approved. This file defines GPTI's content, user journeys and acceptance criteria; the standard defines exact layout, palette, typography, motion and visual QA. Do not silently substitute a generic nonprofit template.

Read `AGENTS.md`, `strategy/mission-system.md`, `strategy/programme-business-model.md`, `brand/brand-system.md`, `governance/status-register.md` and `website/CONTENT_MODEL.md` first. Public copy states approved conclusions and verified facts, never these internal instructions or reasoning.

## 1. Product goal and audiences

The site establishes GPTI's purpose, makes active work understandable, exposes evidence and governance, and lets a visitor choose a concrete next step. A new visitor should answer within 30 seconds: What does GPTI do? For whom? What work is underway? How can I inspect or join it?

Priority audiences: (1) prospective funders and foundation programme staff; (2) universities, cities, community and implementation partners; (3) young people, parents and educators for relevant programmes; (4) researchers and journalists; (5) governance or compliance reviewers. Do not expose minors' personal data.

## 2. Information architecture

| Primary route | Purpose and minimum content | Status for MVP |
| --- | --- | --- |
| `/` | Institutional proposition, focus, work, evidence method, recent insight, participation | Required |
| `/about` | Mission, values, theory of change, governance, legal status as verified | Required |
| `/work` | Four service lines and project index with lifecycle state | Required |
| `/work/[slug]` | Problem, beneficiaries, location, partner roles, method, outputs, evidence, limitations, action | Required for a real approved project only |
| `/insights` | Reports and stories separated by type/date; source attribution | Required, may have sparse launch content |
| `/impact` | Evaluation approach, evidence register, honest results and limitations | Required; method first if no result yet |
| `/participate` | Propose collaboration, receive updates, eligible programme applications; consent | Required |

Footer routes: `/governance`, `/privacy`, `/accessibility`, `/contact`, `/terms` if relevant. Navigation target is 5–6 items: About, Our Work, Insights, Impact, Participate; Search and EN/中文 live in utility zone. At launch, omit empty pages instead of filling them with synthetic content.

## 3. Homepage composition

**Hero:** one institutional proposition: “Prosperity through responsible transition.” Supporting line grounded in the approved mission; primary action “Explore our work”; one secondary text link “How we work”. Use authentic documentary media only when licensed and relevant; otherwise use a disciplined editorial composition. Do not use a fake video or fabricated supporter logos.

**Why GPTI exists:** a short, specific explanation of opportunity, fairness and resilience in transition, plus the method `knowledge → learning → action → evidence` as text content, not decorative icons.

**Current priorities:** 3–4 editorial rows corresponding to actual approved work. If only one project has cleared approval, present one project and two service line directions clearly marked as planned. Never represent a candidate as live.

**Results/evidence:** show verified scope and period only. At founding launch, use an “How we measure change” editorial block instead of a metric band. Once records are approved, use `MetricField` with unit, time, scope and link to method.

**Stories:** 1–2 documentary human/place narratives only if consent and proof exist. If none, feature an evidence-backed research question or project method. Programme/event display is conditional on real events.

**Insights:** chronological records with document type, date, conclusion and source. **Participate:** tailored paths for partners, funders and learners. The footer carries governance, legal and privacy links with stable alignment.

## 4. Page level requirements

`/about`: Who we are, why we exist, vision and mission, principles, theory of change, governance and public status. Trustee biographies require approval. No claim of 501(c)(3) or UN standing without proof.

`/work`: Separate service lines from actual projects. Filter real projects by topic, geography, audience and lifecycle only when the number justifies filters. Every project card states its true status and lead entity.

`/work/[slug]`: Show a sourceable problem statement, stakeholders, project question, process, public deliverables, partner roles, resources, safeguarding/privacy as applicable, current evidence and limitations. A paused or completed project retains its archive and date.

`/insights`: Model `report`, `story`, `perspective` and `news` separately. Reports include methodology and downloadable file metadata; editorial opinion is labeled. Links and sources must work.

`/impact`: Explain activity, output, outcome and impact distinctions; include a public method, evidence records, scope, time and caveats. No counters with placeholders or exaggerated causal claims.

`/participate`: Multiple clear routes with lawful data handling. Do not open a Donate button until entity formation, payment ownership, tax wording and applicable fundraising registrations are verified.

## 5. Design and interaction

Follow the selected standard's shared 1320px content max and responsive gutter tokens; header, sections and footer align on one container. Use institutional blue/neutral Platform palette from the standard, predominantly white, with square or near-square geometry, flat rows and hairline borders. Layout is editorial, with alternating density, not repeated card walls. Body text remains at least 16px. Chinese and English hierarchy should be visually equivalent.

`SiteHeader`, `MegaMenu`, `PlatformHero`, `InstitutionStatement`, `PriorityStack`, `StoryRail`, `ReportFeature`, `NewsList`, `SiteFooter` should be reused where the content warrants them. Motion follows `web/platform/INTERACTION_SYSTEM.md`; keyboard, Esc, focus trap/restore and reduced motion are essential. Search, filters and views appear only when useful and backed by a real content model.

Media must show people, places, work or evidence; store photographer, rights, location, caption and consent. No generic green planet illustration or unlicensed partner mark. A persistent video needs pause, poster and captions.

## 6. Technical contract

**Suggested stack, subject to the repository's eventual implementation choice:** Next.js App Router + TypeScript; accessible semantic HTML; CSS tokens or Tailwind theme mapped once to pinned values; MDX/structured CMS content layer. The stack is a recommendation, not a reason to invent custom design tokens.

Internationalisation: `/en` and `/zh` route groups or an equivalent locale-aware routing strategy, canonical/hreflang pairs, localized metadata, dates, navigation and form errors. English and Chinese content share stable entity IDs and approval state. A language switch retains page identity when translation exists, otherwise offers a clear fallback.

Editorial pipeline: draft → factual review → partner/rights review → translation review → approved → published → archived. Preview unpublished content without exposing it to search. Each record has version, owner, approved_at, sources, image rights and next_review_at. See `CONTENT_MODEL.md`.

Accessibility target WCAG 2.2 AA; skip link, meaningful focus, 44×44px pointer targets, semantic headings, labels, adequate contrast, captions, alt text and functional content without animation. Verify 390, 768, 1024 and 1440px. Production performance targets follow global standard: LCP ≤2.5s, CLS ≤0.1 and INP ≤200ms in representative conditions; report test environment.

Privacy and security: collect only necessary contact fields, separate adult and minor flows, use explicit purpose-specific consent, document retention and processor roles, avoid exposing the API key or personal data. Before launch obtain approved privacy text and test form delivery and deletion process. Domain and email ownership must be verified.

## 7. Launch stages and acceptance

**MVP content gate:** verified legal wording, bilingual mission, four service line descriptions marked by status, one approved project or a transparent no-project state, one real insight/method, governance/contact/privacy basics and rights-cleared media. **Phase 2:** real event listings, richer results, report library, stakeholder newsletter. **Phase 3:** programme application and partner workspace only if operating processes are ready.

Acceptance tests for coding agent:

1. Header, every major section and footer use the exact same left/right anchors at all four breakpoints.
2. All primary and footer links resolve; page titles and locale switch lead to correct content.
3. No public page asserts an unverified legal/IRS/UN/partner status or placeholder impact figure.
4. Every metric has source, time range, scope and method; an empty evidence set displays an honest method block.
5. Every project has a visible actual lifecycle status and lead entity.
6. Keyboard-only visitor can open/close navigation, complete forms and reach every action; reduced motion works.
7. Images and videos pass rights, caption, cropping, alt and control checks.
8. Responsive layouts pass the standards QA 20-point checklist with ≥18/20 and all blocking content/accessibility/link failures resolved.

Implementation report format: `Mode: Platform; Page type: ...; QA score: .../20; Exceptions: none or approved reference.` Do not claim implementation QA for this requirements-only deliverable.
