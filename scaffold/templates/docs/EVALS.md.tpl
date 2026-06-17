# Evals — measuring output accuracy

Tests verify that the machine works. Evals verify that the *outputs* are right. These are different properties.

## 1. Golden task set
<!-- OWNER: Define 10-30 representative tasks that the system should handle correctly.
     These are your benchmark — the AI cannot invent them. -->

Format:
```yaml
- id: gt-001
  prompt: "<the task as the owner would type it>"
  expected:
    must_include: ["<key element 1>", "<key element 2>"]
    must_not_include: []
  rubric_notes: "<what 'good' means for this task, in your words>"
```

## 2. Metrics
<!-- Define what "accurate" means for YOUR project. Examples: -->
- **Task completion rate**: % of golden tasks that produce a correct result
- **Quality score**: Per-task rubric score (1-5), judged by human or LLM judge

## 3. Rubrics — OWNER FILLS THE BLANKS
<!-- The judge (human or LLM) is only as good as these rubrics.
     Define what "good output" looks like for each type of output your system produces. -->

## 4. Trigger policy
The eval suite MUST run when any of these change:
1. Prompts or system instructions
2. Model version
3. Core processing logic

A score drop is treated like a failing test: the change doesn't merge until explained or fixed.
