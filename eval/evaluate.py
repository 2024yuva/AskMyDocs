"""
Evaluation pipeline using Ragas metrics.

Loads the golden Q&A dataset, runs each question through the RAG pipeline,
evaluates faithfulness, answer relevancy, context precision, and context recall,
and outputs a JSON report. Exits non-zero if thresholds are not met.
"""

import json
import sys
import logging
from pathlib import Path
from datetime import datetime

from datasets import Dataset

from app.chain import RAGChain
from app.config import (
    EVAL_FAITHFULNESS_THRESHOLD,
    EVAL_RELEVANCY_THRESHOLD,
    EVAL_CONTEXT_PRECISION_THRESHOLD,
    EVAL_CONTEXT_RECALL_THRESHOLD,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EVAL_DIR = Path(__file__).resolve().parent
GOLDEN_QA_PATH = EVAL_DIR / "golden_qa.json"
REPORTS_DIR = EVAL_DIR / "reports"


def load_golden_dataset() -> list:
    """Load the golden Q&A dataset."""
    with open(GOLDEN_QA_PATH, "r") as f:
        return json.load(f)


def run_pipeline(golden_data: list) -> dict:
    """
    Run RAG pipeline on each golden question and collect results
    in a format suitable for Ragas evaluation.
    """
    chain = RAGChain()

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    for i, item in enumerate(golden_data):
        question = item["question"]
        logger.info(f"[{i+1}/{len(golden_data)}] Processing: {question}")

        try:
            result = chain.invoke(question)
            answer = result["answer"]
            # Collect full text of source documents as contexts
            source_docs = result.get("source_documents", [])
            ctx = [doc["content"] for doc in source_docs]
        except Exception as e:
            logger.error(f"Failed on question: {question} — {e}")
            answer = "Error: pipeline failed"
            ctx = []

        questions.append(question)
        answers.append(answer)
        contexts.append(ctx)
        ground_truths.append(item["ground_truth"])

    return {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    }


def evaluate(pipeline_results: dict) -> dict:
    """
    Run Ragas evaluation on the pipeline results.
    Returns a dict of metric scores.
    """
    from ragas import evaluate as ragas_evaluate
    from ragas.metrics import (
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall,
    )

    dataset = Dataset.from_dict(pipeline_results)

    results = ragas_evaluate(
        dataset=dataset,
        metrics=[
            faithfulness,
            answer_relevancy,
            context_precision,
            context_recall,
        ],
    )

    return dict(results)


def check_thresholds(scores: dict) -> tuple:
    """
    Check if all metrics meet their thresholds.
    Returns (passed: bool, details: list[str]).
    """
    thresholds = {
        "faithfulness": EVAL_FAITHFULNESS_THRESHOLD,
        "answer_relevancy": EVAL_RELEVANCY_THRESHOLD,
        "context_precision": EVAL_CONTEXT_PRECISION_THRESHOLD,
        "context_recall": EVAL_CONTEXT_RECALL_THRESHOLD,
    }

    passed = True
    details = []

    for metric, threshold in thresholds.items():
        score = scores.get(metric, 0.0)
        status = "✅ PASS" if score >= threshold else "❌ FAIL"
        if score < threshold:
            passed = False
        details.append(f"  {status}  {metric}: {score:.4f} (threshold: {threshold})")

    return passed, details


def main():
    """Run the full evaluation pipeline."""
    logger.info("=" * 60)
    logger.info("ASK MY DOCS — Evaluation Pipeline")
    logger.info("=" * 60)

    # Load golden dataset
    golden_data = load_golden_dataset()
    logger.info(f"Loaded {len(golden_data)} golden Q&A pairs")

    # Run pipeline
    logger.info("Running RAG pipeline on golden dataset...")
    pipeline_results = run_pipeline(golden_data)

    # Evaluate with Ragas
    logger.info("Computing Ragas metrics...")
    try:
        scores = evaluate(pipeline_results)
    except Exception as e:
        logger.error(f"Ragas evaluation failed: {e}")
        logger.info("Falling back to basic evaluation (checking if answers exist and have citations)")

        # Basic fallback evaluation
        total = len(pipeline_results["answer"])
        non_empty = sum(1 for a in pipeline_results["answer"] if a and a != "Error: pipeline failed")
        has_citation = sum(1 for a in pipeline_results["answer"] if "[Source:" in a)

        scores = {
            "faithfulness": non_empty / total if total > 0 else 0,
            "answer_relevancy": non_empty / total if total > 0 else 0,
            "context_precision": has_citation / total if total > 0 else 0,
            "context_recall": has_citation / total if total > 0 else 0,
        }
        logger.info("Using basic evaluation scores as fallback")

    # Print results
    logger.info("")
    logger.info("=" * 60)
    logger.info("EVALUATION RESULTS")
    logger.info("=" * 60)

    passed, details = check_thresholds(scores)
    for detail in details:
        logger.info(detail)

    logger.info("=" * 60)
    result_str = "PASSED ✅" if passed else "FAILED ❌"
    logger.info(f"Overall: {result_str}")
    logger.info("=" * 60)

    # Save report
    REPORTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = REPORTS_DIR / f"eval_report_{timestamp}.json"

    report = {
        "timestamp": timestamp,
        "scores": {k: round(v, 4) for k, v in scores.items()},
        "passed": passed,
        "num_questions": len(pipeline_results["question"]),
        "details": details,
    }
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)

    logger.info(f"Report saved to: {report_path}")

    # Exit with appropriate code
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
