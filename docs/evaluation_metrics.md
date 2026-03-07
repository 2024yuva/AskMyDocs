# Evaluation Metrics for RAG Systems

## Why Evaluate RAG?

Evaluating RAG systems is crucial because:
- **Retrieval quality** directly impacts answer quality
- **Hallucination detection** ensures factual accuracy
- **Citation accuracy** maintains trust and transparency
- **Regression detection** prevents quality degradation over time

Without systematic evaluation, teams rely on "vibe checks" — manually reading outputs and guessing if they look correct. This approach doesn't scale and misses subtle quality issues.

## Key Metrics

### Faithfulness
Faithfulness measures whether the generated answer is factually consistent with the retrieved context. A faithful answer only contains claims that can be supported by the retrieved documents.

- **Score range**: 0.0 to 1.0
- **High score**: All claims in the answer are supported by context
- **Low score**: The answer contains fabricated or unsupported claims
- **Why it matters**: Prevents hallucination and ensures trustworthy outputs

### Answer Relevancy
Answer relevancy evaluates how well the generated answer addresses the original question. An answer can be faithful (supported by context) but still irrelevant if it doesn't actually address what was asked.

- **Score range**: 0.0 to 1.0
- **High score**: The answer directly and completely addresses the question
- **Low score**: The answer is off-topic or only partially addresses the question
- **Why it matters**: Ensures the system is actually helpful to users

### Context Precision
Context precision measures what fraction of the retrieved documents are actually relevant to the question. High precision means the retrieval system is focused and doesn't include irrelevant noise.

- **Score range**: 0.0 to 1.0
- **High score**: Most retrieved documents are relevant
- **Low score**: Many retrieved documents are irrelevant noise
- **Why it matters**: Irrelevant context can confuse the LLM and degrade answer quality

### Context Recall
Context recall measures what fraction of the information needed to answer the question was successfully retrieved. High recall means the retrieval system found all the necessary information.

- **Score range**: 0.0 to 1.0
- **High score**: All necessary information was retrieved
- **Low score**: Important information was missed during retrieval
- **Why it matters**: Missing context leads to incomplete or incorrect answers

## Evaluation Workflow

### 1. Create a Golden Dataset
A golden dataset contains:
- **Questions**: Representative queries users might ask
- **Ground truth answers**: The expected correct answers
- **Expected sources**: The documents that should be retrieved

### 2. Run the Pipeline
For each question in the golden dataset:
1. Run the RAG pipeline to get retrieved contexts and generated answer
2. Collect the intermediate results (retrieved docs, generated text)

### 3. Compute Metrics
Use evaluation frameworks like Ragas to automatically compute:
- Faithfulness score
- Answer relevancy score
- Context precision score
- Context recall score

### 4. Set Thresholds and Gate
Define minimum acceptable thresholds for each metric:
- If any metric falls below the threshold, the build fails
- This prevents deploying a system that has regressed in quality
- Typical thresholds: 0.6-0.8 depending on the metric and use case

## CI/CD Integration

Integrate evaluation into your CI/CD pipeline:
1. On every PR, run the evaluation suite against the golden dataset
2. Compare scores against baseline thresholds
3. Fail the PR if any metric drops below threshold
4. Generate a report showing metric scores over time

This ensures that code changes (prompt modifications, retrieval tuning, model updates) don't silently degrade system quality.

## Tools and Frameworks

### Ragas
Ragas is a popular open-source evaluation framework that provides:
- Pre-built metrics for RAG evaluation
- Support for custom metrics
- Integration with LangChain and LlamaIndex
- Experiment tracking and comparison

### LangSmith
LangSmith provides:
- Tracing for debugging LLM applications
- Dataset management for evaluation
- Online evaluation with human feedback
- A/B testing and comparison
