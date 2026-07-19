# Style & Automation Review Checklist

## 1. Automation Gate (check first)

- [ ] CI/CD ran formatters/linters (ESLint, Prettier, Black, RuboCop, etc.) — **if failed, reject PR without human review**
- [ ] Pre-commit hooks (e.g. Husky) present? If not and formatting issues exist — suggest adding them

## 2. Style Guide Compliance

- [ ] Style violations match what's documented in team's style guide (Google, Airbnb, etc.) — not reviewer's taste
- [ ] Undocumented cases → must match surrounding existing code style
- [ ] If author's style doesn't violate standards or surrounding code — **accept it**, even if reviewer prefers otherwise

## 3. PR Scope (no mixed changes)

- [ ] PR mixes logic changes with bulk reformatting (e.g. re-indenting whole file)? → **request separate PR for reformatting**
- [ ] Reason: mixed PRs obscure intent, pollute git history, complicate rollback
