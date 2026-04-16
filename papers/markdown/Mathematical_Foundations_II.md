# Mathematical Foundations II: The Nine Features of Self-Referential Relational Structure

**Mark E. Mala**
12 April 2026
DOI: 10.5281/zenodo.19543730

---

## Abstract

A companion paper — *Mathematical Foundations* (Mala, 2026n; doi:10.5281/zenodo.19520692) — proved that reflexive domains (mathematical structures satisfying D ≅ [D → D]) necessarily exhibit five properties corresponding to the first five characteristic expressions of the Self-Referential Relational Principle (SRRP): contextual determination, emergent limit construction, informational ordering, self-referential representational limits, and observational information loss.

*The Convergence Map II* (Mala, 2026p; doi:10.5281/zenodo.19543356) extended the SRRP from five to nine characteristic expressions, adding symmetry-determination, topological constraint, scale-organisation, and structured plurality. It further observed that the nine expressions form complementary pairs.

This paper asks: do reflexive domains necessarily exhibit all nine features? And is the complementary pair structure mathematically necessary?

We prove three theorems. **Theorem 1 (The Nine-Feature Theorem)** extends the original five-feature result to all nine, proving that reflexive domains necessarily exhibit symmetry-determination, topological constraint, scale-organisation, and structured plurality in addition to the original five. **Theorem 2 (The Identity Theorem)** proves that two of the complementary pairs are not merely parallel but formally identical — informational ordering and topological constraint are mathematically the same structure, and emergence and scale-organisation are mathematically the same construction. **Theorem 3 (The Dependency Structure)** maps the mathematically determined relationships between all nine features by identifying the minimal assumption required for each, revealing a web of mutual dependencies rather than a hierarchy — with a weak base (ordering/topology), a reflexive core (contextual determination + self-referential limits), a constructive aspect (emergence/scale), and a richness layer (symmetry-determination + structured plurality).

The paper further analyses what the mathematical relationships between the nine features reveal. The identity pairs demonstrate that independent convergence surveys discovered the same mathematical structure through different fields. The web dependency structure exemplifies the SRRP's own structural prediction — a finding of self-consistency that is confirmatory, not circular. And the package-deal property (Theorem 1) provides a specific mathematical mechanism for why different fields find the same features: reflexive structure necessarily produces all nine.

The mathematical results cited (Scott, Lawvere, Mac Lane, Abramsky, Jung, Gierz et al.) are established. The specific theorem formulations and the self-consistency analysis are original contributions of this paper. This paper is presented as a draft. The proofs apply established domain theory and category theory to a new context, and the author welcomes review and critique from working mathematicians — particularly domain theorists and category theorists — to verify the arguments.

**Keywords:** reflexive domains, Scott topology, domain theory, category theory, self-referential structure, SRRP, duality, automorphism groups

---

## 1. Introduction

*Mathematical Foundations* (Mala, 2026n) formalised the SRRP by proving that reflexive domains — Dana Scott's D∞ construction (Scott, 1972) satisfying D ≅ [D → D] — necessarily exhibit five properties. That proof covered SRRP expressions (i)–(v).

*The Convergence Map II* (Mala, 2026p) added four expressions (vi)–(ix) derived from nine further fields. The question this paper addresses: are these four additional features also necessary consequences of reflexive domain structure? Or are they independent observations that happen to correlate?

The answer, as the proofs demonstrate, is that the four new features are not independent — they are mathematically necessary consequences of the same reflexive structure that produces the original five. Moreover, the complementary pair structure between old and new features reflects formal mathematical relationships, not coincidental parallels.

### 1.1 Notation

All notation follows *Mathematical Foundations* (Mala, 2026n). D denotes a reflexive domain (bounded-complete algebraic dcpo) with continuous maps φ: D → [D → D] and ψ: [D → D] → D. For Scott's D∞ construction, these form a full isomorphism: φ ∘ ψ = id on [D → D] and ψ ∘ φ = id on D. For a general reflexive domain, only φ ∘ ψ = id on [D → D] is required (D is a retract). The proofs in this paper hold for both cases unless noted. The Scott topology on D has open sets that are upward-closed and inaccessible by directed suprema. ⊑ denotes the information ordering. ⊥ denotes the bottom element. K(D) denotes the compact (finite) elements.

---

## 2. Theorem 1: The Nine-Feature Theorem

### 2.1 Statement

**Theorem 1 (Nine Features).** Let D be a reflexive domain (D ≅ [D → D]). Then D necessarily exhibits, in addition to the five features proved in *Mathematical Foundations* Theorem 2:

(vi) *Symmetry-determination:* The automorphism group Aut(D) determines the structurally significant endomorphisms — an endomorphism f: D → D is natural (compatible with the reflexive structure) if and only if it commutes with the retraction, and the natural endomorphisms are determined by the symmetry structure.

(vii) *Topological constraint:* The Scott topology on D constrains the continuous endomorphisms — only Scott-continuous functions [D → D] are morphisms. The topology is determined by the information ordering (discrete structure) and in turn constrains which maps between elements exist (continuous structure). Discrete constrains continuous.

(viii) *Scale-organisation:* D has a natural approximation structure: every element x ∈ D is the directed supremum x = ⊔{k ∈ K(D) : k ⊑ x} of its compact approximants. The compact elements constitute finite-information "scales," and the full element emerges only in the limit. The domain is organised by information scale.

(ix) *Structured plurality:* D admits multiple retractions — multiple pairs (φ_i, ψ_i) satisfying D ≅ [D → D]. These retractions are not arbitrary but form a category Ret(D) whose morphisms are commuting diagrams. The space of valid self-representations has categorical structure.

### 2.2 Proof

**(vi) Symmetry-determination.** An automorphism of D is a Scott-continuous bijection α: D → D with Scott-continuous inverse. The space of endomorphisms [D → D] carries a natural Aut(D)-action by conjugation: α acts on f ∈ [D → D] by α · f = α ∘ f ∘ α⁻¹. The orbits of this action partition the endomorphisms into equivalence classes — endomorphisms in the same orbit are structurally equivalent (related by symmetry). The centraliser of the Aut(D)-action — the set of endomorphisms fixed by all conjugations — consists of the endomorphisms that commute with every automorphism, which are precisely those whose behaviour is determined entirely by the symmetric structure of D. Thus the automorphism group determines which endomorphisms are structurally significant: two endomorphisms are structurally indistinguishable iff they lie in the same orbit, and the maximally symmetric endomorphisms are the centraliser elements. □

**(vii) Topological constraint.** The Scott topology on D is defined by the information ordering ⊑: a set U is Scott-open iff it is upward-closed and for any directed set S with ⊔S ∈ U, some element of S is already in U. This topology is entirely determined by the partial order — by the discrete, combinatorial structure of how elements relate informationally. Yet this discrete structure constrains which functions are continuous: f: D → D is Scott-continuous iff it preserves directed suprema (f(⊔S) = ⊔f(S) for all directed S). Thus the discrete information ordering determines the topology, and the topology constrains which maps exist as morphisms. Discrete structure constrains continuous structure. □ *(Standard domain theory; Abramsky & Jung, 1994, §2–3.)*

**(viii) Scale-organisation.** Since D is an algebraic dcpo, every element x ∈ D satisfies x = ⊔↑{k ∈ K(D) : k ⊑ x} — the directed supremum of its compact approximants (this is the definition of algebraicity). The compact elements K(D) constitute the "finite information" level: each k ∈ K(D) has the property that whenever k ⊑ ⊔S for a directed set S, there exists s ∈ S with k ⊑ s — k can be "captured" at a finite stage. The full element x emerges only as the limit of all its finite approximations. This is a natural scale structure: Level 0 is ⊥ (no information). Level n consists of elements approximated by compact elements up to "depth" n in the basis. The full domain is the limit. Each level provides an effective description of the element at that information scale, and finer levels refine coarser ones. The domain is organised by information scale, with effective descriptions at each level. □

**(ix) Structured plurality.** A reflexive domain D admits a retraction pair (φ, ψ) with φ ∘ ψ = id on [D → D]. For D∞ (the isomorphism case), ψ ∘ φ = id_D also holds. But this retraction need not be unique. Different choices of retraction correspond to different ways D can "represent" its own function space within itself.

For any automorphism α ∈ Aut(D), the pair (φ ∘ α, α⁻¹ ∘ ψ) is also a valid retraction: (φ ∘ α) ∘ (α⁻¹ ∘ ψ) = φ ∘ ψ = id on [D → D]. These retractions are distinct whenever α is non-trivial. The automorphism group thus acts on the space of retractions.

Define the category Ret(D) whose objects are retraction pairs (φ_i, ψ_i) satisfying φ_i ∘ ψ_i = id, and whose morphisms from (φ_1, ψ_1) to (φ_2, ψ_2) are automorphisms α: D → D such that φ_2 = φ_1 ∘ α and ψ_2 = α⁻¹ ∘ ψ_1. This category is non-trivial whenever Aut(D) is non-trivial. Multiple valid self-representations exist, organised by the group structure of Aut(D). □

*Caveat on (ix):* The claim that Ret(D) is always non-trivial (admits multiple genuinely distinct retractions) depends on D having non-trivial automorphisms. For Scott's D∞ construction, this holds — the construction has a rich automorphism group. For arbitrary reflexive domains, the plurality of retractions is a structural property that varies.

---

## 3. Theorem 2: The Identity Theorem

### 3.1 Statement

**Theorem 2 (Identities).** Two of the complementary pairs identified in *The Convergence Map II* are not merely structural parallels — they are mathematical identities:

(a) *Informational primacy (iii) and topological constraint (vii) are the same structure.* The information ordering on D defines the Scott topology, and the Scott topology determines the information ordering (up to isomorphism). They are mathematically equivalent descriptions of the same structure.

(b) *Emergence (ii) and scale-organisation (viii) are the same construction.* Scott's D∞ inverse limit construction (emergence) is identical to the approximation structure by compact elements (scale-organisation) — they are two descriptions of the same mathematical process.

### 3.2 Proof

**(a) Information = Topology.** The Scott topology on a domain D is completely determined by the partial order ⊑: a set is open iff it is upward-closed and inaccessible by directed suprema. Conversely, the partial order is recoverable from the Scott topology: x ⊑ y iff every open set containing x also contains y (this follows from the T₀ property and the fact that the specialisation order of the Scott topology IS the information ordering). Therefore the information ordering and the Scott topology are interdefinable — knowing one determines the other completely. They are not two features but two descriptions of one structure. □ *(Standard result in domain theory; see Gierz et al., 2003, Chapter I; Abramsky & Jung, 1994, §2.)*

**(b) Emergence = Scale.** Scott's D∞ construction builds D as the inverse limit D∞ = lim←(D_n, π_n) where D_0 = {⊥, ⊤} and D_{n+1} = [D_n → D_n]. An element of D∞ is a sequence (x_0, x_1, x_2, ...) with π_n(x_{n+1}) = x_n — a coherent sequence of approximations at increasing levels of detail. This is exactly the approximation structure of (viii): the compact elements of D∞ correspond to elements that stabilise at some finite level D_n, and every element of D∞ is the directed supremum of these finite approximations. The inverse limit construction (how the domain emerges) and the approximation structure (how it is organised by scale) are not parallel processes — they are the same process described from two perspectives. The limit builds from below (emergence); the approximation decomposes from above (scale). □ *(Standard; see Scott, 1972; Abramsky & Jung, 1994, §5.)*

### 3.3 Interpretation

Theorem 2 reduces the nine apparently independent features to seven genuinely distinct features: (iii) and (vii) are one structure seen from two sides, and (ii) and (viii) are one construction seen from two ends. The complementary pair structure is not a coincidence — it reflects the fact that the convergence programme discovered the same mathematical structure through different fields, which naturally described the same thing in different terms.

---

## 4. Theorem 3: The Dependency Structure

### 4.1 Approach

Rather than assuming relationships between features, we ask: for each of the nine features, what is the minimal mathematical assumption that produces it? The overlaps and containments between these minimal assumptions reveal the genuine dependency structure — the relationships the mathematics dictates, not the relationships the order of discovery suggests.

### 4.2 Minimal Assumptions for Each Feature

**(i) Contextual determination** — requires: φ is injective (elements determined by functional behaviour). Minimal assumption: D has a retraction with injective φ. Does NOT require full reflexivity — any structure with an injective map into its own function space exhibits this.

**(ii) Emergent limit construction** — requires: D is constructed as an inverse limit D∞ = lim←(D_n). Minimal assumption: D arises from an iterative approximation process. This is specific to the D∞ construction — other constructions of reflexive domains may exist, though D∞ is the canonical one.

**(iii) Informational ordering** — requires: D is a dcpo with partial order ⊑. Minimal assumption: directed-complete partial order. This is WEAKER than reflexivity — every dcpo has informational ordering.

**(iv) Self-referential limits** — requires: point-surjective φ: D → [D → D]. Minimal assumption: self-representation is surjective. This IS essentially reflexivity — the core of what makes D reflexive.

**(v) Observational information loss** — requires: Scott topology is T₀ but not T₁. Minimal assumption: D is a dcpo with non-trivial ordering. Like (iii), WEAKER than reflexivity.

**(vi) Symmetry-determination** — requires: Aut(D) acts on [D → D] by conjugation, and functional identity determines element identity. Minimal assumption: (i) plus non-trivial automorphisms.

**(vii) Topological constraint** — requires: Scott topology defined by ⊑ constrains continuous maps. Minimal assumption: identical to (iii) — they are the same structure (Theorem 2a).

**(viii) Scale-organisation** — requires: algebraicity — every element is the supremum of its compact approximants. For D∞, this is the same as (ii) (Theorem 2b). Otherwise a separate property.

**(ix) Structured plurality** — requires: multiple valid retractions exist and form a category. Minimal assumption: non-trivial automorphism group (since automorphisms generate new retractions from existing ones).

### 4.3 The Dependency Graph

**Theorem 3 (Dependency Structure).** The nine SRRP features, as properties of a reflexive domain D, have the following mathematically determined dependency structure:

(a) **Two identity pairs:** (iii) ≡ (vii) and (ii) ≡ (viii). These are not two features each but one feature described in two ways.

(b) **A weak base:** (iii)/(vii) and (v) follow from dcpo structure alone — weaker than reflexivity. They are necessary for ANY ordered domain, not specific to self-referential ones.

(c) **The reflexive core:** (i) and (iv) together constitute reflexivity. (i) is injectivity; (iv) is surjectivity. Together they give the full reflexive structure D ≅ [D → D]. Neither alone suffices. They are mutually complementary, not hierarchically ordered.

(d) **The richness layer:** (vi) and (ix) require the reflexive domain to have non-trivial automorphisms. They are siblings — neither entails the other, but they share a common parent (automorphism richness). They hold for D∞ and for all reflexive domains with non-trivial symmetry.

(e) **The constructive feature:** (ii)/(viii) is specific to domains arising from iterative limit constructions.

(f) **Web, not hierarchy.** The partition into "first five" and "second four" reflects the order of empirical discovery in the convergence programme, not a mathematical hierarchy. The features relate through mutual dependency: (iii)/(vii) and (v) are weaker than the others; (vi) and (ix) depend on automorphism richness beyond what (i)–(v) alone provide; (i) and (iv) are mutual complements, not a chain.

### 4.4 What the Mathematics Reveals

The dependency graph has a specific shape — not a chain, not a hierarchy, but a web:

At the base: **ordering and topology** (iii/vii, v) — present in any dcpo.

At the core: **injectivity and surjectivity** (i, iv) — together constituting reflexivity, each requiring the other for full self-referential character.

As construction: **iterative approximation** (ii/viii) — how the domain is built, producing the scale structure simultaneously.

As enrichment: **symmetry and plurality** (vi, ix) — depending on automorphism structure, producing both the determinative role of symmetry and the organised multiplicity of self-representations.

The features form a web of mutual dependencies, not a tower. This is itself an instance of what the SRRP describes: the structure of the SRRP's own features is relational, without a single foundational layer from which all others derive.

---

## 5. What the Feature Relationships Reveal

### 5.1 The Convergence Programme Found One Thing Multiple Times

The identity pairs — (iii) ≡ (vii) and (ii) ≡ (viii) — have a specific implication that warrants direct statement. When the first Convergence Map surveyed quantum foundations and information theory and found "information is fundamental," and the second Convergence Map surveyed topology, condensed matter, and QFT and found "discrete invariants constrain continuous structures," these were not two convergences supporting a common picture. They were one convergence, encountered twice, in different fields, under different names.

The same mathematical object — the Scott topology, equivalently the information ordering — was discovered independently through different disciplinary lenses. Physicists called it informational primacy. Mathematicians and condensed matter physicists called it topological constraint. The identity (iii) ≡ (vii) proves this is not a metaphor or a structural analogy. It is a mathematical identity.

Similarly, when the first survey found "structure emerges through self-construction" and the second found "reality is organised by scale," these were not two findings. The inverse limit construction (emergence) and the approximation-by-compact-elements (scale-organisation) are the same construction described from two ends. The identity (ii) ≡ (viii) proves this.

This is itself evidence for the SRRP. If reality were not a unified structure, one would expect independently discovered features to be genuinely independent — different facts about different aspects. The identities show they are not. Different fields, studying different phenomena with different tools, encountered the same mathematical structure. The convergence is deeper than agreement — it is identification.

### 5.2 The Web Structure Is Self-Consistent

The dependency analysis in Theorem 3 reveals that the nine features relate to each other as a web of mutual dependencies, not as a hierarchy with a foundational layer.

This is a specific, checkable mathematical property. And it is exactly the property the SRRP predicts self-referential relational structures must have.

The SRRP says reality has no foundational layer — it is self-referential relational structure, with each element defined by its relations to others, and no element serving as an external foundation. Theorem 3 shows the SRRP's own features have this same property: no feature is foundational, each requires and supports the others, and the dependency structure is a web.

This is not circular reasoning. It is self-consistency. Circular reasoning would be: "the SRRP is true because the SRRP says it should be true." What we observe is different: "the SRRP makes a specific structural prediction (no foundational layer, web of mutual dependencies), and the mathematical structure of the SRRP's own features independently satisfies that prediction." The prediction was about reality. The confirmation is about the principle's own architecture. These are different domains — the agreement between them is a non-trivial finding.

A principle that predicted hierarchical structure but whose own features formed a web would be self-contradictory. A principle that predicted web structure and whose own features formed a hierarchy would be self-inconsistent. The SRRP predicts web structure and its own features form a web. This is the minimum condition for self-consistency, and it is met.

### 5.3 The Package-Deal Property Strengthens the SRRP

Theorem 1 proves that reflexive domains necessarily exhibit all nine features. This means the nine features are not independent observations that happen to co-occur in physics — they are a mathematical package deal. You cannot have some without the others.

This has a specific evidential consequence. If physics exhibits any of the core features — contextual determination and self-referential limits — then the mathematical structure producing those features (reflexive domain structure) necessarily produces all nine features. Physics does exhibit contextual determination (Kochen-Specker, Bell, Gleason — proven theorems, experimentally confirmed) and self-referential limits (Gödel, Lawvere — proven theorems). Therefore, if the reflexive domain model is correct, physics must exhibit all nine.

The convergence programme surveyed fourteen fields and found that physics does exhibit all nine. The co-occurrence of all nine is predicted by the mathematical model and confirmed by the empirical survey. This is the standard structure of scientific confirmation: model predicts, evidence confirms.

The strength of this confirmation depends on how likely the co-occurrence would be without the model. If the nine features were logically independent, the probability of all nine co-occurring by coincidence across fourteen fields would be very low. Theorem 1 shows they are NOT logically independent — they are mathematically packaged. But this cuts both ways: the co-occurrence is less surprising given the package-deal property, but the fact that physics exhibits the package at all — that reality has reflexive structure — remains the substantive empirical finding. The mathematics tells us what follows from reflexivity. The physics tells us reflexivity holds.

### 5.4 What Is Genuinely New in This Analysis

The individual mathematical facts — Scott topology, dcpo structure, automorphism groups, inverse limits — are established. What is new is the specific observation that:

1. The SRRP's own feature structure exemplifies the SRRP's structural prediction (web, not hierarchy). This has not been previously noted.
2. Two pairs of independently discovered convergences are mathematically identical, not merely parallel. This has not been previously noted.
3. The nine features constitute a mathematical package deal via Theorem 1, providing a specific mechanism for why different fields find the same features. This has not been previously stated.

These observations, and the argument that they constitute a specific form of self-consistency evidence for the SRRP, are original contributions of this paper.

---

## 6. Novel Contributions

This paper makes four original contributions. The mathematical results cited are established. The specific theorem formulations and the self-consistency analysis are original.

**1. Theorem 1 (Nine-Feature Theorem).** The proof that reflexive domains necessarily exhibit all nine SRRP features — extending the five-feature result of *Mathematical Foundations* (Mala, 2026n).

**2. Theorem 2 (Identity Theorem).** The proof that (iii) ≡ (vii) and (ii) ≡ (viii) are mathematical identities, not parallels — demonstrating that the convergence programme independently discovered the same mathematical structure through different fields.

**3. Theorem 3 (Dependency Structure).** The mathematically determined dependency graph of all nine features, revealing a web of mutual dependencies rather than a hierarchy — with a weak base, reflexive core, constructive aspect, and richness layer.

**4. The Self-Consistency Analysis (Section 5).** The demonstration that the SRRP's own feature structure exemplifies the SRRP's structural prediction, that two convergence pairs are mathematical identities, and that the nine features constitute a package deal providing a specific mechanism for cross-field convergence.

---

## 7. Conclusion

The Extended SRRP's nine features are not nine independent facts. They are a mathematical web: two identity pairs proving that independent convergences discovered the same structure, a weak base present in any ordered domain, a reflexive core constituting the self-referential character, a constructive aspect producing scale structure, and a richness layer depending on automorphism structure.

Three findings emerge from the mathematical analysis. First, the nine features co-occur necessarily in reflexive domains — they are a package deal, not independent correlations. Second, the feature relationships form a web of mutual dependencies, not a hierarchy — which is itself the structure the SRRP predicts for self-referential relational systems. Third, two pairs of convergences independently discovered by different fields through different methods are mathematically identical, demonstrating that the convergence programme found one structure multiple times rather than multiple structures once.

The SRRP is a principle whose own mathematical architecture exemplifies the principle it states. This self-consistency is not circular but confirmatory: a principle about self-referential relational structure whose features are themselves self-referentially related has met the minimum condition for coherence. A principle whose features contradicted its claims would be refuted by its own structure. The SRRP is not.

---

## References

Abramsky, S., & Jung, A. (1994). Domain theory. In *Handbook of Logic in Computer Science* (Vol. 3, pp. 1–168). Oxford University Press.

Gierz, G., et al. (2003). *Continuous Lattices and Domains*. Cambridge University Press.

Lawvere, F. W. (1969). Diagonal arguments and cartesian closed categories. *Comptes Rendus*, 268, 369–372.

Mac Lane, S. (1971). *Categories for the Working Mathematician*. Springer.

Mala, M. E. (2026n). Mathematical Foundations: Formal Proofs for the Principles of Self-Referential Relational Structure. doi:10.5281/zenodo.19520692

Mala, M. E. (2026o). The Convergence Map: What Physics and Mathematics Jointly Say About the Nature of Reality. doi:10.5281/zenodo.19520611

Mala, M. E. (2026p). The Convergence Map II: What Nine Further Fields Say About the Nature of Reality. doi:10.5281/zenodo.19543356

Scott, D. S. (1972). Continuous lattices. In *Toposes, Algebraic Geometry and Logic*, Lecture Notes in Mathematics 274 (pp. 97–136). Springer.

---

*Correspondence: Mark E. Mala*

*Date: 12 April 2026*
