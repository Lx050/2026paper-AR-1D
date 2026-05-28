# PCA-B0 AI Context

Purpose: give an AI agent enough structured context to understand, execute, evaluate, and extend the PCA-B0 project without rereading the original PDF packages.

Source materials:

- `pca_b0_guiding_layer_v1/PCA_B0_guiding_charter_v1.pdf`
- `pca_b0_guiding_layer_v1/PCA_B0_guiding_charter_v1.md`
- `pca_b0_guiding_layer_v1/*.csv`
- `pca_b0_5week_experiment_runbooks_v3/pca_b0_detailed_v3/week1..week5`
- `pca_b0_vlm_pdf_reading_report.md`

Last rewritten for AI: 2026-05-25

---

## 0. Agent Instruction

If you are an AI agent working on this project, use this document as the canonical project context.

Your job is not to make images "prettier" in general. Your job is to test and implement a baseline called PCA-B0:

```text
Good Output = Core Consistency Gate + Perceptual Activation Ranking
```

Always preserve this decision order:

```text
1. Identify user-valued core invariants.
2. Reject candidates that lose those invariants.
3. Rank only accepted candidates by perceptual activation.
4. Validate automatic metrics against small human judgments.
5. Report failures honestly.
```

Never allow a high preference / beauty / emotion score to override a core consistency failure.

---

## 1. Project Definition

Project name: PCA-B0

Full name: Perceptual-Consistency Activation Baseline

Research object: reference-guided AIGC evaluation and selection.

Main thesis:

```text
AIGC output is not merely a photo-like object.
It is a display signal that should preserve user-recognized core value and activate the user's intended perceptual experience.
```

One-line doctrine:

```text
First preserve the user's core invariants, then choose the accepted candidate with the strongest perceptual activation.
```

Primary output type in phase 1: generated images.

Future output types allowed by doctrine: image, video, shader, 3D, point cloud, light field, AR, or other display signals.

Phase 1 non-goals:

- Do not train a foundation generation model from scratch.
- Do not claim automatic systems understand personal memory.
- Do not claim PCA-B0 is an aesthetic truth.
- Do not collapse every dimension into one unqualified total score.
- Do not equate reference similarity with user satisfaction.
- Do not equate emotion labels with perceptual activation.

---

## 2. Core Concepts

| Term | Meaning | Experimental proxy |
|---|---|---|
| Display signal | Output that the user can see or perceive | image in phase 1 |
| Reference image | User preference and subject-structure anchor | `reference_image` |
| Value anchor | Content the user already considers good | `core_value_tags`, `user_preference_statement` |
| Core invariant | What the user most does not want to lose | identity, shape, relation, emotion, culture symbol |
| Allowed deviation | Change that is allowed if core value is preserved | pose, background, style, clothing, composition |
| Core loss | Loss of user-forbidden or user-valued invariant | `forbidden_loss_flag`, human core-loss judgment |
| Core Consistency Gate | Minimum preservation filter before ranking | subject score, structure score, forbidden-loss flag |
| Perceptual Activation | User mental, emotional, memory, or meaning activation | emotion score, memory score, activation words, human choice |
| Activation Ranking | Ranking among candidates that passed the gate | weighted rank score |
| Absorbable failure | Failure fixable by allowed intervention | retry, rewrite, layout, reference, verifier |
| Non-absorbable failure | Failure not fixable under current system and budget | constraint conflict, model inability, missing evidence |

---

## 3. Formal Model

Each task should be represented as:

```text
T = (p, r, u, c, I, V, C, K)
```

Field meanings:

| Symbol | Meaning |
|---|---|
| `p` | prompt / user language intent |
| `r` | reference image or reference subject |
| `u` | user preference and history |
| `c` | cultural, regional, or usage context |
| `I` | invariants that must be preserved |
| `V` | variables that may change |
| `C` | task constraints |
| `K` | cost budget |

Gate:

```text
Accept(y) = C_subject(y, r) AND C_structure(y, p) AND C_forbidden_loss(y, u)
```

Ranking:

```text
Rank(y) =
  alpha * R_pref(y)
+ beta  * R_emotion(y)
+ gamma * R_memory(y)
+ delta * R_culture(y, c)
```

Final candidate:

```text
y* = argmax Rank(y) over candidates where Accept(y) = true
```

If no candidate passes the gate:

```text
Do not output the prettiest failed image.
Record failure type and next intervention.
```

---

## 4. Decision Rules

Use these rules exactly.

| Situation | Decision | Action |
|---|---|---|
| preference score high, subject consistency low | reject | core value precedes activation |
| subject consistency high, user dislikes output | gate pass, ranking failure | record consistency-only failure |
| automatic metric high, user rejects output | metric failure | add to evaluator failure set |
| deviates from reference, user prefers it | possible success | confirm no core invariant was lost |
| all candidates fail gate | generation or constraint failure | retry, rewrite, matched augmentation, oracle |
| humans cannot judge | task underspecified or conflicting | request clarification; do not force output |

Hard rule:

```text
Ranking scores may never cover up gate failure.
```

---

## 5. Failure Taxonomy

| ID | Type | Definition | Example | Next step |
|---|---|---|---|---|
| F1 | Task underspecified | User did not provide enough core invariants | "same cat" without reference | ask for more info or produce multiple interpretations |
| F2 | Wrong invariant | System locks or changes the wrong thing | locks all pixels and becomes stiff | separate invariant from variant |
| F3 | Missing representation | Task variable is absent from representation | count or spatial relation wrong | add object slot / relation graph |
| F4 | Missing coupling | Variable exists but does not affect generation | scene graph only in prompt | layout / attention / denoising coupling |
| F5 | Search failure | Solution exists but was not sampled | more seeds can succeed | retry / rerank |
| F6 | Constraint conflict | Task itself cannot be satisfied | two cats but three enclosed groups | expose conflict |
| F7 | Base model inability | Even oracle guidance fails | perfect layout still cannot draw it | change model / train / adapter |

---

## 6. Data Contract

Every candidate row should be compatible with this schema.

```json
{
  "task_id": "T001",
  "prompt": "text prompt",
  "reference_image": "path/url optional",
  "user_preference_statement": "what user values",
  "core_value_tags": ["friendly", "rounded"],
  "forbidden_loss": ["cold", "aggressive"],
  "allowed_deviation": ["color", "pose"],
  "task_type": "subject|spatial|count|text|culture|emotion",
  "target_region": "optional",
  "expected_text": "optional",
  "candidate_id": "T001_raw_s1000",
  "image_path": "outputs/candidates/...png",
  "intervention_level": "raw|retry|rewrite|matched|mismatched|oracle",
  "intervention_type": "optional",
  "seed": 1000,
  "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
  "subject_score": null,
  "structure_score": null,
  "forbidden_loss_flag": null,
  "accept_gate": null,
  "preference_score": null,
  "emotion_score": null,
  "memory_score": null,
  "culture_score": null,
  "rank_score": null,
  "rank_in_task": null,
  "human_choice": null,
  "human_reason": "optional",
  "activation_words": "optional",
  "failure_type": "optional",
  "notes": "optional"
}
```

Existing package schema uses some concrete scorer names:

```text
subject_gate_score
structure_gate_score
accepted_by_gate
imagereward
hpsv2
emotion_top1
emotion_conf
memorability_score
culture_score
activation_rank_score
rank_in_task
```

When writing new code, preserve compatibility with both naming styles or document the mapping.

---

## 7. Week-by-Week Execution Spec

### Week 1: Resource Audit and Environment Setup

Goal:

```text
Create a reproducible project skeleton and decide which resources support which doctrine layer.
```

Do:

- Create project directory structure.
- Create `README_research.md` with goal and non-goals.
- Configure Python/Conda environment.
- Configure Hugging Face cache and login.
- Build `resource_matrix.csv`.
- Verify dependency import smoke test.
- Create/validate `pca_b0_schema.json`.
- Create 3 smoke pilot tasks.
- Decide Week2 scorer priority.

Do not:

- Do not train models.
- Do not download all large datasets blindly.
- Do not write paper conclusions.

Required outputs:

```text
README_research.md
experiment_log.md
resource_matrix.csv
pca_b0_schema.json
data/pilot/tasks_smoke.csv
outputs/logs/week1_smoke_test.txt
reports/week1_report.md
```

Go/No-Go to Week2:

```text
environment smoke test OK
resource_matrix.csv has at least 15 resources
pca_b0_schema.json exists
tasks_smoke.csv exists and is readable by pandas
reports/week1_report.md lists blockers and decisions
```

### Week 2: Scorers and Unified CSV

Goal:

```text
Convert candidate images into comparable score rows.
```

Scorer priorities:

| Module | Priority | First implementation |
|---|---|---|
| Preference | highest | ImageReward required; HPSv2 or PickScore optional |
| Emotion | high | EmotionCLIP; fallback CLIP zero-shot emotion words |
| Subject | high | CLIP/DINO reference similarity |
| Structure | high | GenEval; fallback manual `structure_pass` |
| Text | medium | EasyOCR/PaddleOCR exact or contains |
| Memory | medium | LaMem/MemNet or proxy |

Rules:

- Every scorer must read CSV and write CSV.
- Missing images must become error rows, not script crashes.
- Keep scorer outputs separate before merge.
- Do not normalize all scores into one unexplained total.

Required outputs:

```text
outputs/scores/imagereward_scores.csv
outputs/scores/emotion_scores.csv
outputs/scores/subject_scores.csv
outputs/scores/week2_all_scores.csv
reports/week2_scorer_report.md
```

Quality checks:

```text
row count matches input or justified outer merge
missing image errors are explicit
min/max ranges are recorded before normalization
each scorer status is documented
```

### Week 3: Candidate Generation, Gate, Rank, Baselines

Goal:

```text
Run a small end-to-end experiment.
```

Pipeline:

```text
task table
-> raw candidate generation
-> scorer execution
-> consistency gate
-> activation ranking
-> baseline comparison
```

Task set:

```text
50 tasks total
10 subject
10 spatial
10 count/color
10 text
10 culture/emotion
```

Generation:

```text
4 seeds per task
store task_id, candidate_id, seed, image_path, seconds
```

Baselines:

| Method | Selection rule | What it tests |
|---|---|---|
| Raw | first seed per task | weakest baseline |
| Preference-only | highest ImageReward/HPS | beauty can lose core |
| Consistency-only | highest subject/structure | similarity can be dull |
| PCA-B0 | gate first, rank second | core preserved and activation optimized |

Gate/rank policy:

```text
gate_subject_pass = no reference OR subject score >= threshold
gate_structure_pass = pass or unknown unless structure evidence fails
gate_forbidden_pass = not forbidden_loss_detected
accepted_by_gate = all gate checks true
rank score is computed only for accepted candidates
rejected candidates receive sentinel rank score or reject reason
```

Required outputs:

```text
outputs/candidates/raw/metadata.csv
outputs/scores/week3_all_scores.csv
outputs/ranked/pca_b0_ranked.csv
reports/week3_pipeline_report.md
```

Report must include:

```text
at least 5 cases
why some candidates were rejected by gate
why some candidates were selected by rank
comparison against 4 baselines
```

### Week 4: Human Evaluation and Activation Words

Goal:

```text
Validate automatic metrics against human judgments.
```

Design:

- Select 20-30 tasks from Week3.
- Prepare 4 images per task: Raw, Preference-only, Consistency-only, PCA-B0.
- Randomize display order.
- Make 2x2 contact sheets labeled A/B/C/D.
- Do not tell annotators which method produced which image.

Questions for users:

```text
1. Which image do you like most?
2. Which image best preserves the good part of the reference?
3. Which image deviates from the reference but remains acceptable?
4. Which image loses the thing that should not be lost?
5. What does your favorite image make you think of? Give 3-8 words.
6. Why? One sentence.
```

Recommended sample:

```text
minimum: 5 users * 20 tasks = 100 choices
better: 10 users * 30 tasks = 300 choices
single-user time: <= 20 minutes
```

Privacy rule:

```text
If users provide private reference images, do not put them in a public repository.
Keep only anonymous IDs and derived scores.
```

Required outputs:

```text
pilot_data/annotation_items.csv
outputs/contact_sheets/*.jpg
pilot_data/human_annotations.csv
outputs/human_metrics.csv
reports/week4_human_eval_report.md
```

Week4 report must answer:

```text
Is PCA-B0 selected more often?
Does preference-only lose core invariants?
Is consistency-only less activating?
Do activation words support the theory?
Which task classes fail?
```

### Week 5: Analysis, Ablation, Report, Paper Outline

Goal:

```text
Turn the pilot into research material, not more unstructured image runs.
```

Do:

- Summarize all Week1-4 files.
- Make resource, method, and human-metric tables.
- Use descriptive statistics and bootstrap confidence intervals.
- Build a failure case library.
- Define ablations for the next experiment.
- Write paper outline.
- Run reproducibility and release checks.

Required tables:

| Table | Content |
|---|---|
| Resources | data/code/weights/purpose/risk |
| Methods | Raw, Preference-only, Consistency-only, PCA-B0 |
| Human Metrics | win / retention / loss / deviation rate |

Failure case library requirements:

| Failure set | Minimum examples |
|---|---:|
| Preference-only failure | 3 |
| Consistency-only failure | 3 |
| Emotion-overfit | 3 |
| Culture mismatch | 3 |
| Evaluator failure | 3 |

Suggested ablations:

| Ablation | Purpose |
|---|---|
| No Gate | prove preference/emotion alone can lose core consistency |
| No Activation | prove consistency alone can be dull |
| No Emotion | test emotion component contribution |
| No Culture | test culture/context contribution |
| Random Weights | prove arbitrary weights are not enough |

Required outputs:

```text
reports/final_5week_report.md
reports/tables/table_resources.md
reports/tables/table_human_metrics.md
reports/failure_cases/
paper_outline.md
```

---

## 8. Resource Map

Use resources only if they support the doctrine. Do not let dataset availability redefine the research problem.

| Resource type | Examples | Doctrine layer |
|---|---|---|
| Generation base | SDXL Base 1.0 | candidate generation |
| Preference | ImageReward, PickScore, HPSv2 | activation ranking |
| Emotion | EmoSet, ArtEmis, EmotionCLIP | activation ranking |
| Memory | LaMem, MemNet | activation ranking proxy |
| Subject consistency | DreamBench++, VBench, CLIP, DINO | consistency gate |
| Structure/relation | T2I-CompBench, GenEval, RelTR | consistency gate |
| Culture/context | GeoDE, Dollar Street, DIG-In | culture/context ranking and failure analysis |
| Concept vocabulary | THINGS | object/category grounding |

---

## 9. Reporting Rules

Use precise, conditional language.

Allowed:

```text
In this pilot sample...
Under this scorer configuration...
For these task types...
PCA-B0 reduced observed core-loss compared with preference-only.
Human evaluation suggests...
```

Not allowed:

```text
PCA-B0 solves AIGC evaluation.
PCA-B0 understands personal memory.
Emotion score equals perceptual activation.
Reference similarity equals user satisfaction.
The system knows what the user wants.
```

Every report must include weakening evidence:

```text
scorers that disagreed with humans
tasks where PCA-B0 did not beat preference-only
cases where gate was too strict
cases where emotion/memory proxies failed
culture/context fields with no explanatory signal
```

---

## 10. AI Agent Task Checklist

When continuing this project, follow this sequence.

```text
1. Read this AI_CONTEXT.md.
2. Check current project state and existing outputs.
3. Identify current week/stage.
4. Do not skip earlier required artifacts.
5. Preserve gate-before-rank logic.
6. Keep all outputs as reproducible CSV/Markdown files.
7. Never hide failed cases.
8. Before claiming completion, verify file existence and output row counts.
```

For a fresh implementation, start at Week 1.

For a paper/report writing task, use:

```text
guiding charter -> weekly reports -> human metrics -> failure cases -> limitations -> future work
```

For a code task, preserve this module split:

```text
scripts/scorers/
scripts/generation/
scripts/pipeline/
scripts/analysis/
scripts/human_eval/
configs/
data/pilot/
outputs/
reports/
```

---

## 11. Optional VLM Integration

The current package does not include a VLM scorer. If adding VLM later, use it as evidence, not final authority.

Good VLM roles:

- explain candidate contents in natural language
- check whether required objects appear
- check relation / count / OCR-like details
- detect forbidden loss candidates
- generate reject reasons for human audit

Bad VLM roles:

- replacing human evaluation
- producing an unverified final aesthetic score
- overriding core consistency gate with preference language
- making claims about personal memory without user data

Recommended VLM output schema:

```json
{
  "candidate_id": "T001_raw_s1000",
  "vlm_subject_pass": true,
  "vlm_structure_pass": true,
  "vlm_text_pass": null,
  "vlm_forbidden_loss_detected": false,
  "vlm_observed_core_values": ["friendly", "rounded"],
  "vlm_observed_deviations": ["pose"],
  "vlm_reject_reason": "",
  "vlm_confidence": 0.73,
  "vlm_notes": "Candidate preserves friendly rounded mascot but changes clothing color."
}
```

VLM values must be validated against Week4 human judgments before being treated as reliable.

---

## 12. Minimal Prompt for Future AI

Use this prompt when handing the project to another AI:

```text
You are working on PCA-B0: Perceptual-Consistency Activation Baseline for reference-guided AIGC evaluation.

Canonical rule:
Good Output = Core Consistency Gate + Perceptual Activation Ranking.

You must first reject candidates that lose user-valued core invariants.
Only accepted candidates may be ranked by preference, emotion, memory, or culture/context activation.
Metrics are evidence, not judges. Human small-sample evaluation is required for validation.

Use AI_CONTEXT.md as the canonical context.
Do not train a foundation model, do not claim automatic personal-memory understanding, and do not hide failed cases.
Before doing work, identify the current week/stage and required artifacts.
Before claiming completion, verify files, rows, and reports.
```

---

## 13. Current Local Files

At the time this context was written, the local workspace contains:

```text
pca_b0_guiding_layer_v1/
pca_b0_5week_experiment_runbooks_v3/
pca_b0_vlm_pdf_reading_report.md
AI_CONTEXT.md
```

Original archives remain:

```text
pca_b0_guiding_layer_v1.zip
pca_b0_5week_experiment_runbooks_v3.zip
```

