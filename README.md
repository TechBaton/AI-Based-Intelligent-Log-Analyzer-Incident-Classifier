
# AI-Powered Log Analysis & Incident Summarization

Automated system for parsing, analyzing, classifying, and summarizing large-scale system logs using NLP and machine learning techniques.

This project converts raw, noisy logs into actionable incident summaries with inferred severity and frequency-based prioritization.

# FEATURES

Format-agnostic log parsing (Windows, Linux, app logs)

Robust text cleaning for ML pipelines

TF-IDF–based vectorization

Machine learning–based log classification

Semantic + frequency-based severity assignment

Concise incident summarization

Scales to thousands of log entries


# FILE DESCRIPTIONS

# app.log

Input log file

Can be replaced with large datasets (Kaggle, GitHub logs, production logs)

# log_parser.py

Central parsing module

Reads raw logs

Extracts timestamp, log level, service/component, and message

Generates cleaned messages using the universal cleaner

Acts as the single source of truth for downstream modules

# universal_log_cleaner.py

Format-agnostic log text cleaner

Removes timestamps, IDs, hex codes, file paths, versions, and noise

Retains meaningful semantic tokens

Used internally by log_parser.py

# vectorize_logs.py

Converts cleaned log messages into numerical features

Uses TF-IDF vectorization

Prepares data for machine learning models

# classify_logs.py

Machine learning–based log classification

Uses TF-IDF features and Logistic Regression

Performs train/test split

Outputs classification metrics and sample predictions

Serves as a baseline classifier

# severity.py

Infers severity of log events

Uses semantic keyword detection and frequency-based escalation

Severity levels:
LOW

MEDIUM

HIGH

CRITICAL

# summarizer.py

Groups semantically similar log events

Aggregates frequency and time ranges

Produces concise, human-readable incident summaries

Example output:

224 occurrences in CBS between 2016-09-28 04:30 and 2016-09-29 02:03:
failed to get next element

# SYSTEM DESIGN PRINCIPLES

No hardcoded log formats

Clear separation of responsibilities

Reusable, modular components

Robust to noisy real-world logs

Explainable ML decisions

# HOW TO RUN

From the project root directory:

python classify_logs.py
python severity.py
python summarizer.py

Each module operates independently using app.log as input.

# USE CASES

Automated log triaging

Incident detection and prioritization

Observability pipelines

DevOps / SRE tooling

Large-scale system debugging

# FINAL OUTPUT

The system reduces thousands of raw log lines into:

Structured data

Classified events

Severity-ranked incidents

Concise summaries for human analysis


# AUTHOR

Built as a hands-on project demonstrating applied machine learning, NLP, and system design for real-world log analysis by Aditya Amol Kulkarni
