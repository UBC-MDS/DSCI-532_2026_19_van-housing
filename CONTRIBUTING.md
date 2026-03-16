# Contributing to the Van-Housing Dashboard

Contributions of all kinds are welcome here, and they are greatly appreciated!
Every little bit helps, and credit will always be given.

## Types of Contributions

### Report Bugs

Report bugs at https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/issues.

If you are reporting a bug, please follow the template guidelines. The more
detailed your report, the easier and thus faster we can help you.

### Fix Bugs

Look through the GitHub issues for bugs. When you decide to work on an issue,
please assign yourself to it and add a comment that you'll be working on it too.

### Write Documentation

We could always use more documentation, whether as part of the official
documentation, in docstrings, or even on the web in blog posts, articles, and
such. Just [open an issue](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/issues)
to let us know what you will be working on so that we can provide you with guidance.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing/issues. If your feedback
fits the format of one of the issue templates, please use that. Remember that
this is a volunteer-driven project and everybody has limited time.

## Get Started!

Ready to contribute? Here's how to set it up for local development.

1. Fork the [van-housing repository](https://github.com/UBC-MDS/DSCI-532_2026_19_van-housing) on GitHub.

2. Clone your fork locally:
```bash
   git clone git@github.com:UBC-MDS/DSCI-532_2026_19_van-housing.git
```

3. Create a branch for local development using `main` as a starting point:
```bash
   git checkout main
   git checkout -b feat/name-of-your-feature
```
   Now you can make your changes locally.

4. Commit your changes and push your branch to GitHub. Please use
   [semantic commit messages](https://www.conventionalcommits.org/).

5. Open the link displayed in the message when pushing your new branch in order
   to submit a pull request.

## Prerequisites

Before you make a substantial pull request, you should always file an issue and
make sure someone from the team agrees that it's a problem. If you've found a
bug, create an associated issue and assign yourself to it before starting work.

## Pull Request Process

1. **No self-merges** — Authors must not merge their own PRs.
2. **Review required** — At least one reviewer approval is required before merging any code-bearing PR.
3. **Link to issues** — Use `Closes #X` or `Fixes #X` in the PR description body to link the PR to the relevant issue.
4. **Design note** — Every PR description must include a brief note explaining the approach, trade-offs, or rationale for the changes.
5. **Spec first** — Update specification documents before writing code for any substantial feature.
6. New code should follow the [PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).

## Pull Request Guidelines

Before you submit a pull request, please check that it meets these guidelines:

1. The pull request should include tests where applicable.
2. If the pull request adds functionality, the docs should be updated. Put your
   new functionality into a function with a docstring.
3. Your pull request will automatically be checked by the full test suite.
   It needs to pass all of them before it can be considered for merging.
4. Include `Closes #X` in the description to link to the issue.
5. Include a brief design note in the PR description.

## Running Tests

Tests can be run from the repo root with:
```bash
pytest
```

Playwright tests require a running browser — install with:
```bash
playwright install chromium
```

## Code of Conduct

Please note that this project is released with a [Contributor Code of
Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to
abide by its terms.

## M3 Retrospective

### What worked well
- Work was divided across team members with clear ownership of modules.
- Regular communication helped unblock teammates quickly when merge conflicts arose.
- PR-based development kept the main branch stable.

### What did not work well
- Spec documents were sometimes updated after code was written rather than before.
- Some earlier PRs were merged without a peer review.
- Testing was left to the end of the milestone rather than being written alongside features.

## M4 Collaboration Norms

For Milestone 4, we committed to:

- Requiring at least one peer review before merging any PR, no exceptions.
- Keeping PRs scoped to one feature or fix with atomic, meaningful commits.
- Every team member resolves at least one feedback item through a documented PR.
- Updating spec documents before writing implementation code.
- Avoiding deadline-eve bursts — contributions spread throughout the milestone.

## Attribution

These contributing guidelines were adapted from the
[dplyr contributing guidelines](https://github.com/tidyverse/dplyr/blob/master/.github/CONTRIBUTING.md)
and the [Breast Cancer Predictor Project](https://github.com/ttimbers/breast_cancer_predictor/blob/master/CONTRIBUTING.md).