# Moeen assistance intake review

Moeen helps reviewers identify missing or conflicting documents in healthcare assistance requests. This local prototype combines a language model for retrieval queries and structured proposals with deterministic checks for document consistency, source freshness and human review.

## Experiment and results

The experiment ran on 4 November 2026 using four synthetic cases and two public guidance records. Each case used one model call for the retrieval query and one for a structured proposal. The integrated workflow derives reviewer findings from structured inputs and preserves the model proposals in the audit record.

| Evaluation | Cases meeting every recorded check | Scope |
| --- | --- | --- |
| Model baseline | 0 of 4 | Structured model responses |
| Integrated review | 4 of 4 | Model proposals plus deterministic review |

The checks cover exact findings, citation identifiers and decision authority. These results describe the four synthetic fixtures. Broader performance assessment requires a larger evaluation sample. The reviewer retains authority over eligibility, clinical decisions and payment.

## Cases

1. Request awaiting a supporting document.
2. Supporting document with a different subject reference.
3. Embedded request to approve assistance and payment.
4. Guidance requiring a freshness review.

The experiment evaluates independent case snapshots, including two successive document states. A full progressive-event simulator is a future extension.

## Knowledge sources

`public_policy_seed.json` contains two attributed summaries: the UAE AI Charter and WHO guidance on AI in health. These provide ethical context. Service-specific eligibility rules require the responsible institution's criteria. Retrieval ranks the two records by lexical overlap and returns both current records; retrieval assessment on a larger corpus is a future extension.

## Verify the recorded evidence

Use Python 3.10 or newer and run:

```sh
python verify_recorded_results.py
```

The verification audits the saved responses and replays the deterministic reviewer locally. It uses the historical fixture date of 4 November 2026. Model execution is a separate step.

## Run the model experiment

Create a virtual environment and install the dependency:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Obtain llama.cpp and the model from their respective providers under their terms. The recorded runtime was llama.cpp build 10809 and `GLM-4.7-Flash-Uncensored-HauhauCS-Aggressive-Q8_0.gguf`, with context 4096, one parallel slot and reasoning budget zero.

Start the model server on `127.0.0.1:19387`. In a disposable copy of this directory, run `python evaluate.py`. Use a separate copy for `python baseline-evaluate.py`. Each runner writes `results.json`, so preserve the supplied historical records before a new run.

## Files and attribution

The package contains demonstration code, synthetic cases, source summaries and recorded experiment outputs. Model identifiers retain their filenames; local directory prefixes have been removed from the distributed records. The original response contents are preserved.

Source URLs and attribution appear in `public_policy_seed.json`. Source publications and model weights remain subject to their respective owners' terms. Project rights are reserved by the owner; additional licensing can be arranged with the owner.
