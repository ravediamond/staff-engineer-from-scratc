# Questions

1. Derive the DPO loss from the KL-regularised RL objective, in words and one equation.
2. What does β control in DPO?
3. DPO vs PPO-based RLHF vs best-of-N: when each?
4. Process vs outcome rewards: trade-offs, and which you would use for an agent that calls tools.
5. What are "verifiable rewards" and why are they popular for reasoning models?

## Model answers

1. max_π E[r(x,y)] − β KL(π‖π_ref) has optimum π*(y|x) ∝ π_ref(y|x) exp(r(x,y)/β), so r = β log(π*/π_ref) + β log Z(x). Substitute into Bradley–Terry: Z cancels in the difference, giving L = −log σ(β[(log π_c − log ref_c) − (log π_r − log ref_r)]). Policy training with an implicit reward, no explicit RM.
2. The strength of the implicit KL regularization: larger β keeps the policy closer to the reference (the sigmoid saturates after smaller log-ratio changes); smaller β allows bigger moves and more over-fitting to the preference data.
3. BoN: no training, quick quality gain, costs inference ×N; a good first step and a way to calibrate RM usefulness. DPO: offline, stable and cheap; good when you have quality preference data close to the policy's distribution. PPO/GRPO-style online RL: when you need exploration beyond the data and have a reliable reward (RM or verifiable), at higher infrastructure cost and tuning risk.
4. Outcome rewards are cheap to label (final answer right or wrong) but give sparse credit assignment and reward lucky wrong reasoning. Process rewards give dense signals and localize errors, but are expensive to label and can be gamed step by step. For tool-using agents: verifiable outcome signals (task success, tests pass) plus cheap automatic process signals (tool call valid, schema-correct, no error) plus a PRM or judge on critical steps.
5. Rewards computed by a checker rather than a learned model: unit tests, exact math answers, compilers, schema validators. They are hard to hack (if the checker is sound) and scale without labellers, so RL can push hard without the over-optimization of learned RMs (GRPO-style training of reasoning models). Risks: checker gaps (tests that don't cover behavior) get exploited.
