# Optional prompting records and evaluation

Use this mode when requested to turn vocabulary into reusable model instructions or assess semantic anchors. Vocabulary generation, description-to-term selection, and behavioral evaluation are separate operations. Do not start a benchmark merely because the vocabulary will be used with AI.

## Build the record

Infer the intended task and deliverable from the request. Ask for missing task information only when it materially changes the expansion; otherwise state a bounded assumption. If several established terms fit, distinguish their senses and select the best fit. If none fits, describe the intent in plain language and disclose the gap.

For each selected term, provide:

- **Term and scope:** canonical name, intended sense, applicable version or edition; state when version is unspecified or inapplicable. Preserve source identity and label roles in ontology mode.
- **Meaning:** the source-grounded definition, its supporting references, and any unresolved ambiguity or evidence limitation. This is definition grounding, independent of model evidence.
- **Prompt expansion:** concrete instructions for applying the concept to this task, including relevant inputs or evidence to inspect, actions, scope limits, and the expected deliverable. Supply enough context for a receiving model that does not know the term. Distinguish source-defined requirements from local task choices; do not present an adaptation as a canonical procedure.
- **Success checks:** observable properties of the resulting artifact or execution, with the evidence needed to assess them. Avoid circular checks such as “correctly applies the method” or checks that merely repeat the name.
- **Model evidence:** `untested` when no behavioral records exist, or `tested` with model/version/date, tasks, prompt conditions, results, and a locator for the underlying records. Describe what was actually tested; `tested` records an experiment, not a favorable result or universal reliability.

Keep expansions proportional to the task. A static concept may need instructions for identification or selection rather than an invented execution procedure. A sourced definition alone is not an operational contract; an operational contract alone is not a completed evaluation.

Without relevant evidence for the receiving model, version, task, and prompt context, explicitly mark standalone term use as untested and recommend carrying the expansion with the term. Preserve older or narrower records while explaining their applicability limit. Evidence for a definition-only or contract-only condition does not establish support for the term alone. Neither recognition questions nor a model's claimed familiarity establish successful practical application.

Ordinary prose can use the five labels above. For requested JSON, use the optional per-term `prompting` object in [structured-output.md](structured-output.md); retain the existing term definition and provenance instead of duplicating them.

## Evaluate only when requested

When asked to establish robustness, prepare or run a bounded comparison with the available models and resources. If models or execution access are unavailable, deliver the evaluation specification and leave evidence untested. Do not fabricate run records or treat the generating model's own explanation as an experiment.

1. Choose representative tasks, including likely confusions with neighboring concepts. Derive acceptance criteria from authoritative material and the intended task before examining outputs; record which criteria are local adaptations. Use held-out tasks when tuning expansions so evaluation does not simply confirm their wording.
2. Compare the same tasks under these conditions:

   | Condition | Added guidance |
   | --- | --- |
   | `task_only` | None |
   | `term` | Canonical term with the intended sense/version qualifier |
   | `definition` | The generated definition |
   | `contract` | The operational expansion and success checks |
   | `paraphrase` | Meaning-equivalent plain language, when isolating the value of the name |

   Record whether the definition or contract includes the name. To isolate the name's contribution, keep the substantive guidance constant and vary only the name versus its plain-language equivalent. The four main conditions compare instruction packages; they do not alone isolate naming from added detail.
3. Repeat runs under comparable settings and fresh context, with the same task inputs, tools, system instructions, and resource limits. Use several intended deployment models for portability claims; scope a single-model result accordingly. Vary aliases, language, or context only as separately recorded conditions. Declare the run budget and any omissions.
4. Score actual artifacts or demonstrated execution against the same criteria. Use deterministic checks where appropriate and documented judgment for qualitative criteria; blind reviewers to conditions where feasible. Record failures, denominators, variation, and prompt length as well as average scores. Recognition and differentiation probes can supplement artifact evaluation but cannot replace it.
5. Retain exact prompts, inputs, outputs or artifacts, scoring rubric and judgments, task IDs, timestamps, model IDs and exposed versions, sampling/reasoning settings, tool context, and prompt lengths with their units. If a snapshot is unavailable, record the alias and that limitation. Report sample sizes and uncertainty; do not infer training-data density or universal portability from output differences.

Keep definition correctness, interpretation, task application, and consistency separate in the report. A stronger definition may fail to steer a model; familiar terminology may steer it toward an unsuitable interpretation. Revise recommendations from observed results without merging these questions into one “reliable” score.

## Method references

The [Semantic Anchors evaluation guidance](https://llm-coding.github.io/Semantic-Anchors/evaluations/) distinguishes recognition, application, differentiation, and consistency and discusses reproducibility and multiple-choice limitations. Its [contracts](https://llm-coding.github.io/Semantic-Anchors/contracts/) supply explicit project meanings. These inform this optional mode; they are not evidence that this skill's generated terms improve model behavior. The artifact comparisons above are a proposed evaluation design, not completed experiments.
