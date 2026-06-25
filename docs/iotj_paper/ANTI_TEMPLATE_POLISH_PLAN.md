# Anti-template Polish Plan

Applied in `paper-visual-polish-v2` as a minimal rewrite pass. No experiment numbers, claims, citations, or protocol definitions were changed.

## Candidate sentences

### 1. File: `main.tex` (Abstract)
Original:
> This paper proposes an out-of-band (OOB) guided cross-attentive RF-HSTU hybrid model...

Reason: Generic "This paper proposes" opener.
Suggested rewrite:
> We propose an out-of-band (OOB) guided cross-attentive RF-HSTU hybrid model...
Risk: low — applied.

### 2. File: `main.tex` (Abstract)
Original:
> These results highlight both the value of OOB-guided RF sequence modeling and the need for future receiver-calibration-aware LoRa RFFI.

Reason: Template closing with vague "highlight" and "future need".
Suggested rewrite:
> The results support OOB-guided RF sequence modeling for same-receiver cross-day authentication, while also showing that receiver-calibration-aware LoRa RFFI remains necessary for cross-receiver deployment.
Risk: low — applied; preserves limitation boundary.

### 3. File: `sections/01_introduction.tex`
Original:
> This motivates lightweight edge-side authentication mechanisms...

Reason: Passive "This motivates" without subject.
Suggested rewrite:
> Gateway-side physical-layer authentication can therefore complement protocol-layer security...
Risk: low — applied.

### 4. File: `sections/01_introduction.tex`
Original:
> In this paper, we propose \model...

Reason: Template phrase.
Suggested rewrite:
> We propose \model...
Risk: low — applied.

### 5. File: `sections/02_related_work.tex`
Original:
> In contrast, this paper focuses on a controlled representation-fusion question...

Reason: "this paper focuses" template.
Suggested rewrite:
> In contrast, our evaluation focuses on a controlled representation-fusion question...
Risk: low — applied.

### 6. File: `sections/07_discussion.tex`
Original:
> This distinction is important for practical IoT deployment.

Reason: Generic importance claim.
Suggested rewrite:
> This receiver-side placement matches practical LoRa deployments, where transmitters are typically constrained and gateways can support additional inference cost.
Risk: low — applied.

### 7. File: `sections/07_discussion.tex` (Future Work)
Original:
> Future work will focus on receiver-adaptive LoRa RFFI. Promising directions include...

Reason: Long template list.
Suggested rewrite:
> A natural next step is calibration methods that do not require target-receiver labels...
Risk: low — applied; shortened subsection.

### 8. File: `sections/08_conclusion.tex`
Original:
> Future work will therefore focus on receiver-adaptive calibration...

Reason: Template future-work closing.
Suggested rewrite:
> A natural next step is receiver-adaptive calibration and multi-receiver training without target-receiver labels...
Risk: low — applied.

## Do-not-touch sentences
- All numeric results (75.0±5.3, 54.2±14.2, bootstrap CI, deployment-shift accuracies)
- Day1–3 / Day4 / Day5 protocol definitions
- Receiver-invariant / receiver-independent negation statements
- Cross-receiver stress-test limitation paragraphs
- Equations and fusion mechanism definitions
- Table values and best/second marking rules

## Skipped candidates (left unchanged)
- Related Work survey opening sentences (already specific with citations)
- Method section technical prose (equation-adjacent)
- Results section numeric narrative
- Contribution bullet list (structured list format is acceptable for IoTJ)
