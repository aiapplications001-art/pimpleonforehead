# MyMirror GA4 Analytics Tracking Guide

Last updated: 2026-05-24
GA4 property stream used in code: `G-QR2SPD4MZM`

This document explains the Google Analytics logging now implemented across the MyMirror static SEO pages, the Face3LayerScanner frontend funnel, and the scanner backend. It is intended for an analytics/reporting owner who needs to build GA4 explorations, funnels, and dashboards.

## Executive Summary

| Area | Pages / surfaces | Custom GA event names | Standard GA events |
|---|---:|---:|---|
| Static SEO pages in parent repo | 63 HTML pages | 7 | `page_view` from GA config |
| Face3LayerScanner frontend SPA | 1 scanner page / multi-step app | 26 | `page_view` from GA config |
| Face3LayerScanner backend | `/analyze-face` API | 2 | None |
| **Total custom event names** | **64 page surfaces + backend API** | **35** | `page_view` also present |

The end-to-end funnel to analyze is:

`seo_page_view` → `seo_scan_cta_click` → `scanner_home_view` → `start_scan_click` → `camera_permission_result` → `scan_started` → `scan_completed` → `regions_confirmed` → `analysis_completed` / `backend_analysis_completed` → `results_viewed` → `action_plan_seen` → `report_share_success` or `report_download_click`

## Implementation Locations

| Repo area | File | Purpose |
|---|---|---|
| Parent repo | `assets/site-analytics.js` | Shared GA4 loader and static SEO page tracker |
| Parent repo | 63 tracked `.html` files | Each loads `/assets/site-analytics.js` with `defer` |
| Scanner repo | `face3layerscanner/src/index.html` | GA4 base tag for scanner |
| Scanner repo | `face3layerscanner/src/script.js` | Scanner frontend funnel and interaction events |
| Scanner repo | `face3layerscanner/src/services/analyticsService.js` | Backend Measurement Protocol helper |
| Scanner repo | `face3layerscanner/src/controllers/analyzeController.js` | Backend analysis success/failure event calls |

## Privacy Guardrails

GA receives aggregate product analytics only.

Do not send or register these in GA:

- Raw face images, base64 crops, scan files, or screenshots
- Raw Gemini responses, prompts, reasoning text, diagnosis-like prose, or clinical scratchpad
- Full stack traces or unrestricted error bodies
- Unique scan log filenames or user identifiers as custom dimensions
- Any future user email, phone number, or health identifier

The current implementation sends buckets, stages, counts, scores, durations, and safe labels.

## Static SEO Page Tracking

All 63 parent-repo HTML pages outside `face3layerscanner` load:

```html
<script defer src="/assets/site-analytics.js"></script>
```

The script loads GA4, sends a custom SEO page event, tracks scroll/engagement, classifies link clicks, and adds attribution parameters to `/scan` CTA clicks.

### SEO Event Count

There are 7 custom SEO event names.

| Event | When it fires | Key use |
|---|---|---|
| `seo_page_view` | On page load after tracker init | SEO landing/page traffic analysis |
| `seo_scroll_depth` | At 25%, 50%, 75%, 90% scroll depth | Content engagement depth |
| `seo_page_engaged` | After 15 seconds on page | Engaged reader quality |
| `seo_cta_click` | Any CTA-like click | CTA performance by page/location |
| `seo_scan_cta_click` | CTA click to `/scan` or scanner host | SEO to scanner funnel handoff |
| `seo_face_map_click` | Click to Face Map pages/experiments | Intermediate diagnostic-page intent |
| `seo_toc_click` / `seo_link_click` | TOC/internal/outbound guide links | Content navigation behavior |

### SEO Common Parameters

These are attached to SEO events where applicable:

| Parameter | Example | Notes |
|---|---|---|
| `app_area` | `seo_pages` | Constant for static pages |
| `page_slug` | `acne_forehead-acne` | Safe page-level dimension |
| `content_group` | `seo_acne`, `seo_home`, `seo_face_map_experiment` | Recommended dimension |
| `canonical_path` | `/acne/forehead-acne/` | Useful for page reports |
| `device_category` | `mobile`, `tablet`, `desktop` | Script-computed |
| `engagement_time_msec` | `15432` | Required for useful GA engagement sessioning |
| `page_title` | Page title | On `seo_page_view` |
| `referrer_domain` | `google.com`, `direct` | On `seo_page_view` |
| `scroll_percent` | `25`, `50`, `75`, `90` | On `seo_scroll_depth` |
| `engaged_seconds` | `15` | On `seo_page_engaged` |
| `link_type` | `scanner`, `face_map`, `internal`, `outbound`, `anchor` | Click classification |
| `link_url` | `/scan?...` | High-cardinality; use carefully |
| `link_domain` | `mymirror.fit` | Useful for outbound/internal split |
| `link_text` | `Start your free skin analysis now` | High-cardinality; use in explorations carefully |
| `cta_location` | `hero`, `nav`, `sidebar`, `footer`, section id, `body` | Recommended dimension |
| `cta_class` | `face-ai-btn`, `nav-cta` | Debug/QA parameter |
| `cta_type` | `scanner`, `face_map`, `internal` | On `seo_cta_click` |

### SEO to Scanner Attribution

When a user clicks a scanner CTA, the tracker appends attribution to the destination URL:

| Query parameter | Example |
|---|---|
| `utm_source` | `seo` |
| `utm_medium` | `site_cta` |
| `utm_campaign` | `skin_scan` |
| `utm_content` | `<page_slug>` |
| `source` | `seo_<page_slug>` |
| `entry_page` | `<page_slug>` |
| `cta_location` | `hero`, `nav`, `sidebar`, etc. |

This lets GA acquisition and scanner-side reporting connect discovery pages to scanner funnel behavior.

## Static Page Coverage

Each page below has the shared SEO tracker and therefore supports the 7 SEO custom events listed above.

| # | Page path | Event set |
|---:|---|---|
| 1 | `index.html` | SEO common event set |
| 2 | `MyMirror_Progress_Summary_Beautified.html` | SEO common event set |
| 3 | `face-map-experiment.html` | SEO common event set |
| 4 | `face-map-experiment-v1.html` | SEO common event set |
| 5 | `acne/index.html` | SEO common event set |
| 6 | `acne/face-map.html` | SEO common event set |
| 7 | `acne/face-map/index.html` | SEO common event set |
| 8 | `acne/types-of-acne/index.html` | SEO common event set |
| 9 | `acne/blackheads-whiteheads/index.html` | SEO common event set |
| 10 | `acne/pimple-zit/index.html` | SEO common event set |
| 11 | `acne/nodule-cyst/index.html` | SEO common event set |
| 12 | `acne/chin-acne/index.html` | SEO common event set |
| 13 | `acne/chin-acne-meaning/index.html` | SEO common event set |
| 14 | `acne/cystic-chin-pimple/index.html` | SEO common event set |
| 15 | `acne/lower-face-treatment/index.html` | SEO common event set |
| 16 | `acne/nose-acne-treatment/index.html` | SEO common event set |
| 17 | `acne/nose-pimple-treatments-home-remedies-clinical-cures/index.html` | SEO common event set |
| 18 | `acne/forehead-acne/index.html` | SEO common event set |
| 19 | `acne/forehead-acne-cheat-sheet/index.html` | SEO common event set |
| 20 | `acne/forehead-acne-dandruff/index.html` | SEO common event set |
| 21 | `acne/forehead-acne-organ-connection/index.html` | SEO common event set |
| 22 | `acne/forehead-acne/fast-treatment/index.html` | SEO common event set |
| 23 | `acne/forehead-acne/home-remedies/index.html` | SEO common event set |
| 24 | `acne/forehead-acne/meaning/index.html` | SEO common event set |
| 25 | `acne/pimple-on-forehead-hindi/index.html` | SEO common event set |
| 26 | `acne/back-acne/index.html` | SEO common event set |
| 27 | `acne/back-acne-apple/index.html` | SEO common event set |
| 28 | `acne/back-acne-faq/index.html` | SEO common event set |
| 29 | `acne/back-acne-faq-hindi/index.html` | SEO common event set |
| 30 | `acne/back-acne-natural-remedies/index.html` | SEO common event set |
| 31 | `acne/back-acne-women/index.html` | SEO common event set |
| 32 | `acne/back-acne-women-30s/index.html` | SEO common event set |
| 33 | `acne/acne-back-cure-cheat-sheet/index.html` | SEO common event set |
| 34 | `acne/why-men-get-acne/index.html` | SEO common event set |
| 35 | `acne/men-acne-faq/index.html` | SEO common event set |
| 36 | `acne/small-pimples-forehead-men/index.html` | SEO common event set |
| 37 | `acne/why-teenagers-get-acne/index.html` | SEO common event set |
| 38 | `acne/pregnancy-forehead-acne/index.html` | SEO common event set |
| 39 | `acne/adult-acne-worsening/index.html` | SEO common event set |
| 40 | `acne/acne-pcos-treatment-indian-skin/index.html` | SEO common event set |
| 41 | `acne/hormonal-acne-vs-oily-skin/index.html` | SEO common event set |
| 42 | `acne/acne-diet-india/index.html` | SEO common event set |
| 43 | `acne/indian-acne-diet-guide/index.html` | SEO common event set |
| 44 | `acne/indian-acne-diet-guide/checklist.html` | SEO common event set |
| 45 | `acne/science-of-clear-skin/index.html` | SEO common event set |
| 46 | `acne/best-acne-homemade-face-pack/index.html` | SEO common event set |
| 47 | `acne/minimalist-acne-routine/index.html` | SEO common event set |
| 48 | `acne/skincare-layering-guide/index.html` | SEO common event set |
| 49 | `acne/best-mens-face-wash-pimples-dark-spots/index.html` | SEO common event set |
| 50 | `acne/best-benzoyl-peroxide-face-wash-india/index.html` | SEO common event set |
| 51 | `acne/best-salicylic-acid-face-wash-india/index.html` | SEO common event set |
| 52 | `acne/best-salicylic-acid-products-india/index.html` | SEO common event set |
| 53 | `acne/best-non-comedogenic-moisturizer-india/index.html` | SEO common event set |
| 54 | `acne/best-pimple-patch-india/index.html` | SEO common event set |
| 55 | `acne/niacinamide-serums-india/index.html` | SEO common event set |
| 56 | `acne/1-vs-2-percent-salicylic-acid/index.html` | SEO common event set |
| 57 | `acne/salicylic-acid-for-beginners/index.html` | SEO common event set |
| 58 | `acne/salicylic-acid-face-wash-vs-serum/index.html` | SEO common event set |
| 59 | `acne/mixing-salicylic-acid-with-retinol-adapalene/index.html` | SEO common event set |
| 60 | `acne/adapalene-before-after-results/index.html` | SEO common event set |
| 61 | `acne/adapalene-benzoyl-peroxide-gel/index.html` | SEO common event set |
| 62 | `acne/adapalene-clindamycin-phosphate-gel/index.html` | SEO common event set |
| 63 | `acne/adapalene-differin-adaferin-gel-comparison-india/index.html` | SEO common event set |

## Scanner Frontend Tracking

The scanner is a single-page app. It emits virtual stage events instead of relying only on standard `page_view`.

### Scanner Frontend Event Count

There are 26 custom frontend scanner event names.

| Event | Stage | When it fires | Useful dimensions/metrics |
|---|---|---|---|
| `scanner_home_view` | home | Scanner page loads | `session_stage`, device params |
| `start_scan_click` | home | User taps start | Start conversion |
| `camera_start_requested` | camera | Camera flow begins | `session_stage` |
| `camera_permission_result` | camera | Permission granted or denied/error | `permission_result`, `startup_ms`, `error_type` |
| `camera_first_frame` | camera | First video frame arrives | `startup_ms`, `video_resolution` |
| `camera_start_failed` | camera | Camera startup fails | `error_type`, `startup_ms` |
| `face_detected` | camera | First face landmarks found | `startup_ms`, `video_resolution` |
| `scan_started` | scan | Stabilization completes | `startup_ms`, `lighting_warning`, `shine_advisory` |
| `scan_quality_warning` | scan | Face lost or capture gate blocked | `warning_type`, `warning_stage` |
| `region_locked` | scan | Region crop reaches verified quality | `region`, `lock_time_ms`, `quality_score`, `quality_bucket`, `locked_region_count` |
| `scan_completed` | scan | Scan collection completes | `scan_duration_ms`, `locked_region_count`, `unlocked_region_count`, `result_status` |
| `region_review_view` | review | Region confirmation screen appears | `locked_region_count`, `unlocked_region_count` |
| `regions_confirmed` | review | User confirms region crops | `selected_region_count` |
| `analysis_requested` | analysis | Frontend sends `/analyze-face` | `selected_region_count`, `payload_region_count` |
| `analysis_completed` | analysis | Frontend receives successful response | `analysis_duration_ms`, `confidence_score`, `confidence_bucket`, `marker_count`, `marker_count_bucket` |
| `analysis_failed` | analysis | Frontend request or response fails | `error_stage`, `error_type`, `analysis_duration_ms` |
| `results_viewed` | results | Results render | `overall_score`, `overall_score_bucket`, `confidence_score`, `top_focus_region`, `top_focus_pillar`, `marker_count_bucket` |
| `score_card_expand` | results | User expands score/pillar card | `card_type`, `pillar_name` |
| `image_review_toggle` | results | User opens/hides crop review | `toggle_state`, `highlighted_region_count`, `marker_count_bucket` |
| `action_plan_seen` | results | Action plan area enters viewport | `top_focus_region`, `top_focus_pillar`, `severity` |
| `report_share_click` | results | User taps share scorecard | `report_type`, `share_supported` |
| `report_share_success` | results | Native share completes | `report_type` |
| `report_download_click` | results | Download fallback triggers | `report_type`, `download_reason` |
| `report_share_failed` | results | Share/report generation fails | `error_type` |
| `retake_scan_click` | results/review | User chooses new scan | `button_location` |
| `frontend_error` | any | Runtime error/unhandled promise rejection | `error_stage`, `error_type` |

### Scanner Common Parameters

Most frontend scanner events include:

| Parameter | Example |
|---|---|
| `app_area` | `face_scanner` |
| `source_page` | `scan` |
| `ui_version` | `2026_05_24` |
| `session_stage` | `home`, `camera`, `scan`, `review`, `analysis`, `results` |
| `device_category` | `mobile`, `tablet`, `desktop` |
| `viewport_bucket` | `xs`, `mobile`, `tablet_desktop`, `wide` |
| `camera_supported` | `yes`, `no` |
| `engagement_time_msec` | GA engagement timing |

## Backend Tracking

Backend events are sent through GA4 Measurement Protocol from `/analyze-face`.

Render environment variables required:

| Env var | Required | Notes |
|---|---|---|
| `GA_API_SECRET` | Yes for backend events | Never commit this value |
| `GA_MEASUREMENT_ID` | Optional | Defaults to `G-QR2SPD4MZM` if absent |
| `GA_REGION` | Optional | Set `eu` only if Measurement Protocol should use `region1.google-analytics.com` |

### Backend Event Count

There are 2 custom backend event names.

| Event | When it fires | Useful dimensions/metrics |
|---|---|---|
| `backend_analysis_completed` | Backend returns successful analysis | `backend_ms`, `gemini_ms`, `confidence_score`, `confidence_bucket`, `marker_count`, `marker_count_bucket`, `model_family`, `result_status` |
| `backend_analysis_failed` | Backend catches analysis failure | `backend_ms`, `error_stage`, `error_type`, `result_status` |

Backend events rely on frontend-passed `client_id` and `session_id` so they can attach to the same GA session when available.

## Recommended GA4 Custom Dimensions

Register these event-scoped dimensions first:

| Dimension | Why |
|---|---|
| `app_area` | Separate SEO pages, scanner, backend |
| `page_slug` | SEO page reporting |
| `content_group` | Group SEO page types |
| `canonical_path` | Page-level table reporting |
| `session_stage` | Scanner funnel stage analysis |
| `device_category` | Device split |
| `cta_location` | CTA placement performance |
| `cta_type` | Scanner vs face-map vs internal CTAs |
| `link_type` | Internal/outbound/anchor/scanner links |
| `permission_result` | Camera permission analysis |
| `error_stage` | Failure location |
| `error_type` | Aggregated error class |
| `warning_type` | Scan quality issue analysis |
| `warning_stage` | Stabilization vs active scan |
| `region` | Region lock behavior |
| `quality_bucket` | Region quality bucket |
| `confidence_bucket` | Result confidence bucket |
| `marker_count_bucket` | Results marker bucket |
| `overall_score_bucket` | Overall score distribution |
| `top_focus_region` | Personalized focus region |
| `top_focus_pillar` | Personalized focus pillar |
| `card_type` | Overall / skin age / pillar expansion |
| `pillar_name` | Pillar interaction analysis |
| `toggle_state` | Crop section view/hide |
| `share_supported` | Native share availability |
| `report_type` | Report format |
| `button_location` | Retake source |
| `model_family` | Backend model source |
| `result_status` | Success/partial/failed |

Use `link_text`, `link_url`, and `cta_class` mainly for ad hoc explorations. They can become high-cardinality dimensions if registered broadly.

## Recommended GA4 Custom Metrics

Register these event-scoped metrics:

| Metric | Unit | Used by |
|---|---|---|
| `scroll_percent` | Number | SEO scroll depth |
| `engaged_seconds` | Seconds | SEO engagement |
| `startup_ms` | Milliseconds | Camera startup |
| `scan_duration_ms` | Milliseconds | Scan completion |
| `lock_time_ms` | Milliseconds | Region lock timing |
| `quality_score` | Number | Region lock quality |
| `locked_region_count` | Count | Scan completeness |
| `unlocked_region_count` | Count | Scan quality risk |
| `selected_region_count` | Count | Region confirmation |
| `payload_region_count` | Count | Analysis payload completeness |
| `analysis_duration_ms` | Milliseconds | Frontend analysis latency |
| `backend_ms` | Milliseconds | Backend total latency |
| `gemini_ms` | Milliseconds | Gemini latency |
| `confidence_score` | Number | Analysis confidence |
| `marker_count` | Count | Region marker richness |
| `overall_score` | Number | Result distribution |

## Recommended Key Events

Mark these as key events in GA4:

| Event | Reason |
|---|---|
| `seo_scan_cta_click` | SEO page conversion to scanner |
| `start_scan_click` | Scanner start intent |
| `camera_permission_result` | Critical camera gate |
| `scan_completed` | Successful scan capture |
| `regions_confirmed` | User accepted crops |
| `analysis_completed` | Frontend got analysis |
| `backend_analysis_completed` | Backend succeeded |
| `results_viewed` | Core product value delivered |
| `action_plan_seen` | Final recommendation consumed |
| `report_share_success` | Viral/share conversion |
| `report_download_click` | Report export conversion |

## Suggested GA Reports

### 1. SEO to Scanner Funnel

Use events:

`seo_page_view` → `seo_scan_cta_click` → `scanner_home_view` → `start_scan_click` → `results_viewed`

Breakdowns:

- `page_slug`
- `content_group`
- `cta_location`
- `device_category`
- `utm_content`

### 2. Scanner Completion Funnel

Use events:

`scanner_home_view` → `start_scan_click` → `camera_permission_result` with `permission_result=granted` → `scan_started` → `scan_completed` → `regions_confirmed` → `analysis_completed` → `results_viewed`

Breakdowns:

- `device_category`
- `viewport_bucket`
- `permission_result`
- `warning_type`
- `locked_region_count`

### 3. Camera and Scan Health

Use events:

- `camera_permission_result`
- `camera_first_frame`
- `camera_start_failed`
- `scan_quality_warning`
- `region_locked`
- `scan_completed`

Metrics:

- `startup_ms`
- `lock_time_ms`
- `quality_score`
- `locked_region_count`
- `scan_duration_ms`

### 4. Backend and Gemini Latency

Use events:

- `backend_analysis_completed`
- `backend_analysis_failed`

Metrics:

- `backend_ms`
- `gemini_ms`

Breakdowns:

- `model_family`
- `confidence_bucket`
- `marker_count_bucket`
- `error_type`

### 5. Results Engagement

Use events:

- `results_viewed`
- `score_card_expand`
- `image_review_toggle`
- `action_plan_seen`
- `report_share_click`
- `report_share_success`
- `report_download_click`

Breakdowns:

- `overall_score_bucket`
- `top_focus_region`
- `top_focus_pillar`
- `card_type`
- `pillar_name`
- `toggle_state`
- `share_supported`

## Event Debugging Checklist

1. Open GA4 DebugView.
2. Visit any SEO page and confirm `page_view` and `seo_page_view`.
3. Scroll to 25% and confirm `seo_scroll_depth`.
4. Click a `/scan` CTA and confirm `seo_scan_cta_click`.
5. Confirm scanner URL contains `utm_source=seo`, `utm_medium=site_cta`, `utm_campaign=skin_scan`, `entry_page`, and `cta_location`.
6. On scanner page, confirm `scanner_home_view`.
7. Start scan and confirm `start_scan_click`, `camera_start_requested`, and `camera_permission_result`.
8. Complete scan and confirm `scan_completed`, `regions_confirmed`, `analysis_completed`, and `results_viewed`.
9. Confirm backend events appear only after Render has `GA_API_SECRET` configured.

## Notes for Future User-Level Analytics

Current implementation is anonymous/session-level. When real user accounts exist, add a privacy-reviewed user identifier strategy:

- Use GA4 `user_id` only after login and consent review.
- Keep scan/report database IDs out of GA dimensions.
- Join user-level scan history in the product database, not GA.
- Use GA for aggregate funnel and behavior reporting, not individual medical/profile history.
