# Reflections

Round-by-round reflections on the optimisation strategy, kept alongside the
datasheet and model card. This file collects the write-ups; the numbers referenced
match the query history under `data/history/`.

## Final round — a reinforcement-learning lens

**How the explore-exploit balance evolved.** This is the multi-armed bandit
problem in a different costume, and that framing sharpened as the data grew.
Early on I leaned on exploration, which is really what a high UCB confidence
bonus does: it values a point for how uncertain it is, not its predicted score.
With almost no data that was right. As rounds accumulated the balance tilted
toward exploitation, unevenly by function. F5 is the clearest exploit case: once
its high-value region was confirmed, narrowing in kept paying off, up to a final
best of 431.6. F1 stayed exploratory, because no region ever produced a signal.
F6 is the cautionary one: its best came at the very first round and I kept
confirming it rather than exploring, which in bandit terms is getting stuck on an
arm that looked good early. There is also a finite-horizon effect: with few
queries left and no round after the last, information has little future value, so
the balance has to tip toward exploitation near the end.

**How feedback drove the updates.** Each returned output is a reward, and
refitting the surrogate on it is the update step. The GP's posterior mean acts
like a value estimate, much as a Q-value says what an action is worth, and each
result revises it near the query. A result that beats the prediction, like F5's
jump to 431.6, acts as a positive reward-prediction error that pulls later
queries toward that region; one that undershoots, like F6 drifting well below its
round-1 best, is a negative error that leads the model to down-weight the area.
The size of these updates shrank over time, large early on (a high
temporal-difference error) and vanishingly small later, much as Q-values
stabilise as an agent nears an optimal policy.

**Feedback, efficiency and delayed rewards.** The feedback is sparse and delayed:
one query per function per round, the result arriving the following round. That
is exactly the delayed-reward and credit-assignment problem RL wrestles with. You
cannot correct within a round, so a miscalibrated choice costs a whole cycle, as
on F6 and in F2's long flat stretch before it broke upward at round 10. Efficiency
came from the surrogate, which has to wring maximum information from each
expensive evaluation, the sample-efficiency pressure that makes model-based
methods attractive when rewards are costly.

**Iterative improvement, self-play and model type.** My process is closer to
model-based planning than model-free trial and error. Rather than sampling
blindly, I build a model of each function and use it to anticipate where a query
will pay off before spending it. The AlphaGo Zero parallel is loose but real:
each round's results retrain the model, which guides the next query, a
self-improving loop fed by its own data. The honest difference is there is no
learned policy network and no reward beyond the function value, so it is
bootstrapped search rather than true self-play.

**Applying RL ideas in future work.** Several transfer directly. Thompson
sampling would likely explore better than a fixed UCB weight. A DQN or PPO
meta-controller could adjust the exploration weight or switch kernels on the fly
rather than me tuning by hand, and an actor-critic policy could generate
candidates along the useful directions instead of sampling uniformly, which
matters above about ten dimensions. Contextual bandits suit decisions with side
information and would allocate a shared budget across functions toward whichever
is improving fastest. For any task with expensive, delayed feedback (A/B testing,
experiment design, system tuning) the bandit and RL toolkit is the natural fit.
