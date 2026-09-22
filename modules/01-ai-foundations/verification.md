# Module 01 Verification

Use this checklist before moving to Module 02.

## Reading Check

You should have completed all seven chapter files and reviewed:

- [concepts.md](concepts.md)
- [architecture.md](architecture.md)
- [project/README.md](project/README.md)

## Mini-Project Check

Run the success path:

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode mock
```

Expected result:

- exit code `0`
- a new JSON report file under `modules/01-ai-foundations/project/runs/`
- a printed summary with latency, status code, and token usage

Run the failure path:

```bash
python modules/01-ai-foundations/project/ai_workload_observer.py --mode mock --mock-file modules/01-ai-foundations/project/fixtures/mock-rate-limit.json
```

Expected result:

- non-zero exit code
- a JSON report with error metadata
- the error message visible in the console summary

## Understanding Check

You should be able to explain:

- the difference between AI, ML, deep learning, generative AI, and foundation models
- the infrastructure differences between training and inference
- why parameters, precision, and context windows influence runtime behavior
- how embeddings support retrieval and search systems
- why different AI workload types need different operational treatment
- where observability fits into the AI lifecycle

## Workbook Check

You should have at least:

- one note summarizing the workload types most relevant to your job
- one reflection on training versus inference
- one observer run artifact you inspected manually

## Exit Criteria

You are ready for Module 02 when:

- the mini-project runs successfully in mock mode
- you can interpret the fields in the generated report
- you can compare hosted, open-weight, self-hosted, and fine-tuned model strategies at a high level