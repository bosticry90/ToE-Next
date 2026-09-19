# Joint Standard-Model-plus-gravity EFT reference audit

**Disposition:** finite-order low-energy control surface established; **active cross-domain seam: NONE**. This is an audit of established effective theory, not a UV model, a complete joint EFT basis, or a calculation of new Wilson coefficients. It does not supersede the separate quasiclassical-recovery obligation in [SCIENTIFIC_BASELINE.md](SCIENTIFIC_BASELINE.md).

## Declared slice and authority ceiling

Use a four-dimensional, torsion-free Lorentzian metric with a spin structure; the Standard Model (SM) gauge group and field content; local Lorentz, diffeomorphism, and SM gauge invariance; and energies/curvatures within a controlled EFT regime. The displayed bulk slice is parity-even and uses one convenient local basis:

$$
S_{\rm loc}^{\rm ref}=\int d^4x\,\sqrt{-g}\left[
-\rho_\Lambda+\frac{M_0^2}{2}R+\mathcal L_{\rm SM}^{\rm cov}
-\xi R H^\dagger H+c_R R^2+c_{\rm Ric}R_{\mu\nu}R^{\mu\nu}
\right]+S_{\rm boundary}.
$$

Here $M_0^2$, $\rho_\Lambda$, $\xi$, $c_R$, and $c_{\rm Ric}$ are renormalized coefficients at a specified scale and in a specified scheme/basis. The signs of $R$ and $\xi$ must be translated before comparing papers. After electroweak symmetry breaking, a measured gravitational coefficient depends on the combination of $M_0^2$ and $\xi\langle H^\dagger H\rangle$; it is not a separate direct measurement of both. The effective cosmological term likewise includes vacuum contributions, not just the displayed bare parameter. This is a reference *slice*, not a claim that omitted operators vanish. [Calmet, Capozziello & Pryer (2017)](https://link.springer.com/article/10.1140/epjc/s10052-017-5172-3); [Donoghue (1994)](https://arxiv.org/abs/gr-qc/9405057).

**Two countings must remain distinct.** Under canonical local mass dimension, $[R]=2$, $[H^\dagger H]=2$, and $R^2$, $R_{\mu\nu}^2$, and $RH^\dagger H$ all have dimension four. In the pure-metric derivative/curvature expansion, the displayed sectors are $D_0$ (cosmological term), $D_2$ (Einstein-Hilbert), and $D_4$ (curvature squared). This does **not** exhaust a fixed order in $1/M_*^2$ or all joint matter-gravity amplitudes at four derivatives: for example, matter-curvature structures such as $RF_{\mu\nu}F^{\mu\nu}$ or $R_{\mu\nu}(D^\mu H)^\dagger D^\nu H$ lie outside the canonical-dimension-four slice. Nor is $M_*$ automatically the measured Planck scale. State the process, field content, matter thresholds, loop order, and power counting before using this as a calculational truncation. [Daas *et al.* (2024)](https://arxiv.org/abs/2405.12685); [Donoghue (1994)](https://arxiv.org/abs/gr-qc/9405057).

The further local terms (including dimension-six matter-curvature interactions and higher curvature operators), parity-odd/topological terms, threshold effects, and quantum-state/boundary data are **outside** this admitted bulk slice, not proven irrelevant. The minimal SM field content specified here does not include right-handed neutrinos, a dark-matter particle, or a solution to the observed neutrino-mass and cosmological-mechanism questions. The prior Babu-Khan SMEFT-plus-$N$ boundary therefore cannot be silently inserted into this SM-only slice.

At a specified loop order, an alternative **1PI effective-action** representation has the schematic form $\Gamma_{\rm joint}=S_{\rm loc}^{\rm ref}+\Gamma_{\rm nonlocal}+\cdots$. Low-energy massless propagation produces nonanalytic terms such as $R\log(-\Box/\mu^2)R$ and corresponding Ricci/Riemann kernels. Their coefficients are calculable given the active light spectrum, interactions, perturbative order, and prescription; the local $c_i(\mu)$ are not thereby predicted. The scale dependence cancels in complete observables at the computed order. Do not add a 1PI nonlocal loop contribution to a calculation that already includes the same active-field loops: that would double-count it. [Donoghue (1994)](https://arxiv.org/abs/gr-qc/9405057); [Calmet *et al.* (2017)](https://link.springer.com/article/10.1140/epjc/s10052-017-5172-3).

## Basis and renormalization controls

In four dimensions the Euler/Gauss-Bonnet density is

$$
E_4=R_{\mu\nu\rho\sigma}R^{\mu\nu\rho\sigma}
-4R_{\mu\nu}R^{\mu\nu}+R^2.
$$

For a constant coefficient on a suitable boundary-free spacetime, its integral is topological and contributes no local bulk metric equation. Thus $R^2$ and $R_{\mu\nu}^2$ are a permissible *local* curvature-squared bulk basis; omitting a separate local $R_{\mu\nu\rho\sigma}^2$ coefficient does **not** erase Riemann-curvature physics. $\Box R$ is a total divergence for constant coefficient, but boundaries require an explicit boundary prescription. A constant gravitational Pontryagin density is likewise topological in this local bulk discussion; neither topological nor boundary effects are declared absent. The local Gauss-Bonnet identity does **not** eliminate a nonlocal $R_{\mu\nu\rho\sigma}\log(-\Box/\mu^2)R^{\mu\nu\rho\sigma}$ kernel. [Daas *et al.* (2024)](https://arxiv.org/abs/2405.12685); [Calmet *et al.* (2017)](https://link.springer.com/article/10.1140/epjc/s10052-017-5172-3).

Local field redefinitions and lower-order equations of motion can shift curvature-squared terms in a vacuum calculation. With SM matter present, the same redefinition shifts effects into matter couplings/contact operators. Therefore a zero $c_R$ or $c_{\rm Ric}$ in one representation is not, by itself, a physical prediction; compare invariant amplitudes or other operational combinations in a consistent basis. [Daas *et al.* (2024)](https://arxiv.org/abs/2405.12685).

$\xi RH^\dagger H$ is part of the renormalizable curved-spacetime matter interface, not a discretionary decoration. Curved-space SM loops require its counterterm and cause $\xi$ to run. In the conventions and one-loop approximation of [Markkanen *et al.* (2018), Eq. 4.21](https://arxiv.org/abs/1804.02020), $\beta_\xi$ is proportional to $(\xi-1/6)$ times a combination of SM Higgs, Yukawa, and electroweak couplings. Thus $\xi=0$ at one scale is generally **not** an RG-invariant assertion, while that equation does not determine its boundary value. This source treats the metric as a curved background for the SM loop calculation; it is not itself a full dynamical quantum-gravity computation. $\xi$ is not independently established by a model-independent direct measurement; any numerical limit needs a declared cosmological or particle-physics model, scale, and basis.

## Coefficient-classification ledger

| Item | Class and status in this slice | What can be inferred operationally |
| --- | --- | --- |
| SM gauge, Yukawa, Higgs and mass inputs | Independent renormalized SM inputs in a chosen scheme; experimentally inferred, not derived by coupling to gravity. | SM cross sections, spectra, and other observables constrain combinations after threshold and scheme conversion. |
| $M_0^2$ and $\rho_\Lambda$ | Independent local gravitational coefficients in this basis; renormalized and scale/convention dependent. | Newtonian/relativistic gravity and cosmological expansion constrain effective combinations, including Higgs-vacuum and other vacuum contributions, not each displayed bare term separately. |
| $\xi$ | Independent local Higgs-curvature interface coefficient at a reference scale; generally radiatively generated/running. Setting it to zero is a scale-specific choice, not a consequence of minimal covariantization. | Constraints are model-, scale-, and basis-dependent; no unique direct value follows from current SM+GR evidence or the cited beta function. |
| $c_R,c_{\rm Ric}$ | Local curvature-squared Wilson coefficients in the chosen bulk basis; not calculable from the low-energy EFT without matching. Their numerical values and even allocation among sectors can change under field redefinitions and scale changes. | Experiments constrain process-dependent invariant combinations; no separate universal measurement of these two labels is assumed. |
| $E_4,\Box R$ (and constant Pontryagin term) | Local topology/boundary/basis bookkeeping under the stated assumptions, not extra independent bulk equations. | Boundary/topological effects require their own setup; they are not universally zero. |
| Nonlocal logarithmic kernels $b_i$ | Calculable low-energy loop coefficients **conditional** on active light fields, order, and prescription; distinct from arbitrary local Wilson inputs. | Their invariant contribution may enter observables together with local counterterms; no standalone detection is claimed. |
| Operational combinations | Basis-invariant predictions at a stated approximation, not additional freely chosen coefficients. | Solar-system, equivalence-principle, gravitational-wave, cosmological, or matter measurements constrain specified combinations only after a process-level map. |
| Omitted higher operators | Outside this finite slice, not measured zero or proven irrelevant. | Must be restored when the energy/curvature, accuracy, or chosen observable requires them. |

This ledger prevents both common errors: treating a basis coefficient as a directly observed fact, and treating a calculable loop kernel as an independently adjustable UV parameter. The observable is the appropriately renormalized, basis-independent prediction, not an isolated term in the displayed action.

## Assumption ledger and experimental interfaces

| Domain | Independent structure/input presently carried, not explained by this audit |
| --- | --- |
| SM | $SU(3)_c\times SU(2)_L\times U(1)_Y$, representations/generations, gauge couplings, Yukawa/flavor matrices, Higgs potential and electroweak vacuum, and applicable SM parameters such as the strong-CP angle. Their measured or bounded values are inputs to this reference theory. |
| Gravity | Four-dimensional metric/spin structure, diffeomorphism and local Lorentz invariance, Einstein-Hilbert leading dynamics, gravitational normalization, cosmological term, and the EFT regime/boundary or state prescription. |
| Matter-gravity interface | Coupling all included SM sectors to the same metric/vierbein and compatible spin/gauge connections; the allowed nonminimal $\xi RH^\dagger H$ term and its boundary value; threshold conventions. Universal metric coupling is an assumption tested in regimes, not derived by merely writing $\mathcal L_{\rm SM}^{\rm cov}$. |
| EFT and quantum corrections | Local Wilson data ($c_R,c_{\rm Ric}$ here and more beyond the slice), renormalization/matching prescription, active spectrum and quantum state for calculable nonlocal terms, and a justified cutoff/power counting. |

These rows are a **dependency ledger**, not a numerical count of independent parameters: field redefinitions, matching, symmetries, and an eventual UV theory can change that count. A future candidate would earn compression only by deriving a basis-independent relation or reducing genuine boundary inputs while preserving measured observables; renaming the same free inputs, setting $\xi$ or $c_i$ to zero in a preferred basis, or noting that $\beta_\xi$ depends on SM couplings would not suffice.

Operational controls include SM precision observables; gravitational light/time-delay tests such as [Cassini](https://www.nature.com/articles/nature01997); composition-dependent free-fall tests such as [MICROSCOPE](https://arxiv.org/abs/2209.15487); and joint gravity/matter propagation tests such as [GW170817/GRB 170817A](https://arxiv.org/abs/1710.05834). These establish the importance of the shared low-energy regime. **They do not individually measure $\xi$, $c_R$, or $c_{\rm Ric}$ without a specified background, basis, model, and likelihood.** The cosmological constant is operationally inferred through cosmology, with mechanism unsettled. Quasiclassical behavior remains a separate recovery requirement, not a term added to this EFT action.

## Cross-domain seam decision

**NONE_FOR_ACTIVE_SEAM.** The audit supplies a common SM-plus-gravity destination and exposes possible targets—e.g. an invariant relation involving Higgs-curvature response, curvature-squared amplitudes, or universal metric coupling—but neither established EFT nor the currently frozen candidate work predicts a new, model-specific relation among their independent boundary inputs. Known RG running of $\xi$ is conditional evolution, not a predicted initial value. No UV source, new physics calculation, coefficient fit, or candidate switch is admitted here. This conclusion leaves all earlier bounded Babu-Khan recovery results and the gravity-framework comparison unchanged.

## Primary sources and scope of use

- [Donoghue (1994), *General relativity as an effective field theory*](https://arxiv.org/abs/gr-qc/9405057): local gravitational EFT, low-energy/nonlocal separation, and authority ceiling of calculable infrared effects.
- [Markkanen, Nurmi, Rajantie & Stopyra (2018), *The 1-loop effective potential for the Standard Model in curved spacetime*](https://arxiv.org/abs/1804.02020): full-SM curved-background renormalization, including $\xi$ and curvature counterterms; not a dynamical-graviton result.
- [Calmet, Capozziello & Pryer (2017), *Gravitational effective action at second order in curvature and gravitational waves*](https://link.springer.com/article/10.1140/epjc/s10052-017-5172-3): explicit schematic SM-plus-gravity action, local/nonlocal split, Gauss-Bonnet and $\Box R$ treatment. Its speculative mode/ghost interpretation and numerical bounds are not adopted as baseline facts.
- [Daas, Laporte, Saueressig & van Dijk (2024), *Rethinking the EFT formulation of Gravity*](https://arxiv.org/abs/2405.12685): derivative counting, curvature bases, and field-redefinition caveat when matter is present.
