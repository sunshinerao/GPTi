# GPTI website content model

Version 1.0 · source for the first implementation

## Common fields

Every public content record has `id`, `type`, `status` (`draft|review|approved|published|archived`), `locale` (`en|zh`), `translation_group_id`, `title`, `summary`, `body`, `owner`, `reviewer`, `approved_at`, `published_at`, `updated_at`, `next_review_at`, `sources[]`, `rights[]`, `seo_title`, `seo_description` and `slug`. Draft content cannot be indexed or presented as active work.

## Entities

| Entity | Additional required fields | Integrity rule |
| --- | --- | --- |
| `ServiceLine` | `mission_link`, `audience`, `public_deliverables`, `operating_status` | Direction and active programme are distinct |
| `Project` | `lead_legal_entity`, `lifecycle`, `question`, `beneficiaries`, `geography`, `start_date?`, `end_date?`, `method`, `partner_roles[]`, `safeguarding?`, `outputs[]`, `outcome_claims[]`, `evidence_ids[]`, `limitations`, `cta?` | Candidate cannot appear as active |
| `Partner` | `legal_name`, `relationship_type`, `agreement_ref`, `name_use_permission`, `logo_use_permission`, `valid_from`, `valid_to?` | No partner brand without permission |
| `EvidenceRecord` | `claim`, `unit`, `numerator`, `denominator?`, `period_start`, `period_end`, `geography`, `population`, `method`, `source_ref`, `limitations`, `verification_owner`, `approved_at` | A number lacking scope or period stays unpublished |
| `Insight` | `kind` (`report|story|perspective|news`), `conclusion`, `author`, `publication_date`, `methodology?`, `file_type?`, `file_size?`, `media_credit?` | News and reports remain distinct |
| `Event` | `host`, `date_time`, `time_zone`, `format`, `location_or_online`, `theme`, `access`, `registration_state`, `source` | No calendar with fictitious events |
| `MediaAsset` | `alt`, `caption`, `credit`, `license_ref`, `consent_ref?`, `subject`, `desktop_crop`, `mobile_crop`, `expiry?` | Do not expose a minor without reviewed consent |

## Status and publication policy

- `Project.lifecycle`: `proposed|approved|active|paused|completed|archived`. Only `approved` and later may get a public project page; `proposed` can appear in internal planning, not public listings.
- `EvidenceRecord` supports `activity|output|outcome|impact`. Use “impact” only after method and contribution claim review.
- Partner approval and public wording are separate fields. A signed service contract does not automatically authorize a homepage logo.
- Legal status claims are editorially linked to `governance/status-register.md`; production implementation should use a maintained structured counterpart rather than copying claims into multiple components.
- Every multilingual record shares entity identity and independent publication review; fallback is visible, not silent.

## Example safe launch record

```json
{
  "id": "method-001",
  "type": "Insight",
  "kind": "perspective",
  "status": "draft",
  "locale": "en",
  "title": "How GPTI proposes to examine public outcomes",
  "summary": "A working method for separating activities, outputs and longer-term change.",
  "publication_date": null,
  "sources": ["research/source-register.md"],
  "approved_at": null
}
```

This example is explicitly a draft. It is not a claim that the organization or website is live.
