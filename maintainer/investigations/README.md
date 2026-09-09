# Maintainer Investigations

This directory stores suspected Playbook bugs, behavioral anomalies, and unresolved governance questions before they are strong enough to become formal defects or admitted work.

Each investigation should preserve:

- observed behavior / evidence;
- why it may be a problem;
- competing explanations (policy wording, routing/loading, runtime/tool limitation, model behavior, environment, or other relevant cause);
- missing discriminating evidence;
- current classification (`SUSPECTED`, `INCONCLUSIVE`, or equivalent evidence-bounded wording);
- next evidence action, if any.

Do not convert an investigation into a canonical bug, policy defect, or Task merely because it is persisted here. Formal behavioral scenarios belong under `evals/` only after admission.
