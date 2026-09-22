# Module 11 References

## MLOps and LLMOps Foundations

- [MLOps Principles](https://ml-ops.org/) — foundational MLOps concepts and practices
- [Hidden Technical Debt in Machine Learning Systems (Google)](https://proceedings.neurips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf) — the classic paper that motivated MLOps as a discipline
- [Operationalizing Machine Learning (Shankar et al.)](https://arxiv.org/abs/2209.09125) — empirical study of production ML pain points

## Prompt Management

- [Promptfoo](https://github.com/promptfoo/promptfoo) — open-source CLI for prompt testing and evaluation
- [LangSmith](https://docs.smith.langchain.com/) — LangChain's platform for prompt management and tracing
- [Weights & Biases Prompts](https://docs.wandb.ai/guides/prompts) — prompt versioning and evaluation tracking

## Evaluation

- [RAGAS](https://github.com/explodinggradients/ragas) — framework for evaluating RAG systems
- [DeepEval](https://github.com/confident-ai/deepeval) — LLM evaluation framework with multiple built-in metrics
- [Evals (OpenAI)](https://github.com/openai/evals) — OpenAI's open-source evaluation framework
- [LLM-as-a-Judge paper](https://arxiv.org/abs/2306.05685) — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
- [G-Eval](https://arxiv.org/abs/2303.16634) — NLG evaluation using GPT-4 with chain-of-thought
- [Chatbot Arena](https://lmarena.ai/) — human preference-based model comparison

## Regression Detection

- [A Framework for Evaluating LLMs](https://hamel.dev/blog/posts/evals/) — Hamel Husain's practical guide to building eval systems
- [Who Validates the Validators (Shankar et al.)](https://arxiv.org/abs/2405.03029) — on the reliability of LLM-as-judge evaluation

## CI/CD For AI

- [GitHub Actions documentation](https://docs.github.com/en/actions) — for building AI CI pipelines
- [Canary Deployments for ML Models](https://www.kubeflow.org/docs/components/serving/overview/) — Kubeflow serving patterns
- [Continuous Delivery for Machine Learning (CD4ML)](https://martinfowler.com/articles/cd4ml.html) — Martin Fowler on applying CD to ML systems

## Human Feedback

- [Reinforcement Learning from Human Feedback (RLHF)](https://arxiv.org/abs/1706.03741) — original RLHF paper
- [Direct Preference Optimization (DPO)](https://arxiv.org/abs/2305.18290) — DPO paper, an RLHF alternative
- [Data Annotation Best Practices](https://labelbox.com/blog/data-annotation-best-practices/) — practical annotation guidance

## Tooling

- [MLflow](https://mlflow.org/) — experiment tracking, model registry, and deployment
- [DVC (Data Version Control)](https://dvc.org/) — versioning for data and ML pipelines
- [OpenLLMetry](https://github.com/traceloop/openllmetry) — OpenTelemetry-based observability for LLMs
