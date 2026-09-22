# Module 11 Challenge

## Challenge 1 - Design A Prompt Registry

Design a file-based prompt registry for the Acme AI platform.

Write a note in `my-solutions/module-11-prompt-registry.md` that covers:

1. **Directory structure**: how prompts, versions, and registry manifest are organized
2. **Version record schema**: what fields each prompt version tracks
3. **Promotion workflow**: the exact steps to promote a prompt from dev to production
4. **Access control**: who can promote to staging vs production
5. **Rollback procedure**: how to revert to the previous production version
6. **Application integration**: how the sample-rag application loads the correct version at runtime

Include an example of the registry manifest JSON and one example prompt YAML file.

## Challenge 2 - Expand The Evaluation Dataset

Extend the smoke eval dataset from 5 to 20 cases:

- Add 5 more core capability cases
- Add 5 edge case cases (questions that are adjacent to the domain, ambiguous, or unusual)
- Add 3 adversarial cases (prompt injection attempts or off-topic questions)
- Add 2 regression cases based on the failure you simulated in the lab

For each case, write the `expected_themes` list and a `rationale` field explaining why this case was included.

## Challenge 3 - LLM-as-Judge Implementation

Extend the `run_eval.py` script to add an LLM-as-judge scoring path alongside keyword scoring.

The judge prompt should evaluate:
- **Groundedness** (0-3): Is the response grounded in retrieved content or fabricated?
- **Completeness** (0-3): Does the response address all important aspects of the question?
- **Relevance** (0-3): Is the response directly relevant to the question asked?

The composite score should be `0.3 × keyword + 0.7 × (judge_total / 9)`.

The runner should output:
- per-case breakdown showing both keyword and judge scores
- an overall composite pass rate
- the 3 lowest-scoring cases with their judge reasoning

## Challenge 4 - CI Pipeline Design

Write a GitHub Actions workflow YAML file (`eval/ci-eval.yml`) that:

1. Triggers on pull requests that change any file under `prompts/`
2. Runs the smoke eval against a staging environment
3. Runs the full eval only if the smoke eval passes
4. Posts a summary comment on the PR with the eval results
5. Blocks merge if the full eval pass rate falls below 0.75

You do not need a live staging environment for this challenge. Write the YAML with placeholder environment variable references and document what secrets and infrastructure would be needed to make it work.

## Challenge 5 - Silent Drift Detection

Design a canary monitoring script that detects silent model drift.

The script should:

1. Send 5 "canary prompts" with highly stable expected outputs to the model API
2. Compare the responses using semantic similarity to stored reference responses
3. Alert (print a warning) if any response similarity drops below 0.80
4. Store the canary run results with a timestamp for trend tracking

Write the script and explain in a comment:
- how often you would run it
- what alert threshold makes sense
- how you would distinguish model drift from legitimate behavior improvement
