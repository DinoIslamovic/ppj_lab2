## Step-by-Step Breakdown: LR(1) Item Set Construction

Below is a **step-by-step expansion** of the canonical LR(1) parser item set construction algorithm. Each main step from the outline above is broken into sub-steps, so you can follow or implement the process directly. This outlines both the theory and the concrete procedures you would run in code or by hand.

### 1. **Augment the Grammar**
- **a.** Add a new start symbol (e.g., S' if S was the original start symbol).
- **b.** Create a new production: S' → S

### 2. **Compute FIRST Sets**
- **a.** For every terminal, set $$ FIRST(x) = \{x\} $$.
- **b.** For every nonterminal, initially set $$ FIRST(NT) = \emptyset $$.
- **c.** For every production $$ A \rightarrow \beta $$, update $$ FIRST(A) $$ with the $$ FIRST(\beta) $$ set, using these rules:
  - If $$ \beta $$ starts with a terminal, add it to $$ FIRST(A) $$.
  - If $$ \beta = X_1 X_2 \ldots X_n $$, accumulate all terminals that can start any string derivable from $$ \beta $$.
  - If $$ X_i $$ can derive empty, continue to $$ X_{i+1} $$; add $$ \varepsilon $$ if all parts can derive empty.
- **d.** Repeat step c until no more changes (fixed-point iteration).[1]

### 3. **Form the Initial LR(1) Item Set (I₀)**
- **a.** Start with the item $$[S' \rightarrow - S, \$]$$ (dot at the start, lookahead is end marker).
- **b.** Compute its **closure** (see next section).

### 4. **Compute Closure of a Set of LR(1) Items**
Given a set of LR(1) items `I`, compute `CLOSURE(I)` as follows:
- **a.** Initialize set $$ C = I $$.
- **b.** For each item $$[A \rightarrow \alpha - B \beta, a]$$ in $$ C $$ where the dot is before a nonterminal B:
  - **i.** For each production $$ B \rightarrow \gamma $$:
    - Construct sequence $$ \delta = \beta a $$ (remaining input after B followed by the current lookahead).
    - For each terminal $$ b $$ in $$ FIRST(\delta) $$:
      - If $$[B \rightarrow - \gamma, b]$$ not in $$ C $$, add it to $$ C $$.[6][1]
- **c.** Repeat step b until no new items are added.

### 5. **GOTO Operation**
- For a set of items $$ I $$ and a grammar symbol $$ X $$, `GOTO(I, X)` is constructed as follows:
  - **a.** For each item $$[A \rightarrow \alpha - X \beta, a]$$ in $$ I $$:
    - Move the dot past X, forming $$[A \rightarrow \alpha X - \beta, a]$$.
    - Collect all such items into a set J.
  - **b.** Set `GOTO(I, X) = CLOSURE(J)`.

### 6. **Create the Canonical Collection of LR(1) Item Sets**
- **a.** Initialize a collection C with just the (already-closed) initial set I₀.
- **b.** For each set in C and each grammar symbol X, compute `GOTO(set, X)`.
  - **i.** If this produces a new set not equal to any in C, add it to C.
- **c.** Repeat (b) until no new sets are created.

### 7. **Build Parsing Tables**
- **a.** For each state (item set), and for each item $$[A \rightarrow \alpha - a \beta, b]$$ with dot before terminal a, ACTION[state, a] is shift to the state for `GOTO(set, a)`.
- **b.** For items with the dot at the end, $$[A \rightarrow \gamma-, a]$$, set ACTION[state, a] to reduce by $$ A \rightarrow \gamma $$.
- **c.** For the start production [S' → S-, $], set ACTION[state, $] = accept.
- **d.** For nonterminals X, set GOTO[state, X] to the index of the set `GOTO(set, X)` if that set exists.

***

**Ask if you want a worked example, code, or to focus on a particular phase!**

***

[1](https://www.eecis.udel.edu/~cavazos/cisc672-fall08/lectures/Lecture-10.pdf)
[2](https://web.stanford.edu/class/archive/cs/cs143/cs143.1128/handouts/110%20LR%20and%20SLR%20Parsing.pdf)
[3](https://serokell.io/blog/how-to-implement-lr1-parser)
[4](https://www.geeksforgeeks.org/compiler-design/lr-parser/)
[5](https://cse.iitkgp.ac.in/~bivasm/notes/scribe/11CS30015.doc)
[6](https://stackoverflow.com/questions/14103199/lr1-item-dfa-computing-lookaheads)
[7](https://chaosinmotion.com/wp-content/uploads/2017/08/ocyacc-building-lr1-glr.pdf)
[8](https://www.seas.upenn.edu/~cis5110/notes/cis511-sl9.pdf)
[9](https://www.youtube.com/watch?v=ukCW2WX7u0c)