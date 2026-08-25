#!/usr/bin/env python3
"""Reproduce the variance audit in Agrawal, Gans & Goldfarb (2025).

The script verifies the interior solution symbolically and constructs a
deterministic counterexample using independent continuous uniforms. It writes
the same two-panel figure to PDF and PNG under extra/figures/.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "extra" / "figures"


def symbolic_checks() -> None:
    e, alpha, Delta, s, theta = sp.symbols(
        "e alpha Delta s theta", positive=True, finite=True
    )
    objective = alpha * Delta * sp.sqrt(s * e + theta) - e
    foc = sp.diff(objective, e)
    e_star = alpha**2 * Delta**2 * s / 4 - theta / s
    assert sp.simplify(foc.subs(e, e_star)) == 0

    optimized = sp.simplify(objective.subs(e, e_star))
    expected = alpha**2 * Delta**2 * s / 4 + theta / s
    assert sp.simplify(optimized - expected) == 0

    a0, var_g_over_s = sp.symbols("a0 var_g_over_s", real=True)
    variance = sp.Symbol("A", real=True) + a0 * theta + var_g_over_s * theta**2
    assert sp.diff(variance, theta) == a0 + 2 * theta * var_g_over_s
    assert sp.solve(sp.diff(variance, theta), theta)[0] == -a0 / (2 * var_g_over_s)


def uniform_nodes(low: float, high: float, n: int = 180) -> tuple[np.ndarray, np.ndarray]:
    """Gauss-Legendre nodes and probability weights for U[low, high]."""
    nodes, weights = leggauss(n)
    values = (low + high) / 2 + (high - low) * nodes / 2
    return values, weights / 2


def weighted_mean(values: np.ndarray, weights: np.ndarray) -> float:
    return float(np.sum(values * weights))


def counterexample() -> dict[str, float]:
    # Independent continuous uniforms. Delta is calibrated once so theta*=1.7007.
    alpha, wa = uniform_nodes(0.9, 1.1)
    skill, ws = uniform_nodes(0.7, 1.3)
    gamma0, wg0 = uniform_nodes(0.6, 0.9)
    gamma, wg = uniform_nodes(0.2, 0.5)
    discount = 0.8
    Delta = 6.777159970189924

    e_alpha2 = weighted_mean(alpha**2, wa)
    e_alpha4 = weighted_mean(alpha**4, wa)
    mu_s = weighted_mean(skill, ws)
    e_s2 = weighted_mean(skill**2, ws)
    e_inv_s = weighted_mean(1 / skill, ws)
    e_inv_s2 = weighted_mean(1 / skill**2, ws)

    Gamma = gamma0[:, None] / (1 - discount * gamma[None, :])
    joint_w = wg0[:, None] * wg[None, :]
    e_Gamma = float(np.sum(joint_w * Gamma))
    e_Gamma2 = float(np.sum(joint_w * Gamma**2))
    var_Gamma = e_Gamma2 - e_Gamma**2
    var_G_over_s = e_Gamma2 * e_inv_s2 - (e_Gamma * e_inv_s) ** 2

    condition_lhs = e_Gamma2 / e_Gamma**2
    condition_rhs = mu_s * e_inv_s
    a0 = (
        Delta**2
        * e_alpha2
        / 2
        * (e_Gamma2 - e_Gamma**2 * mu_s * e_inv_s)
    )
    theta_star = -a0 / (2 * var_G_over_s)
    slope_at_one = a0 + 2 * var_G_over_s
    common_interior_limit = (0.9**2 * Delta**2 * 0.7**2) / 4

    assert condition_lhs < condition_rhs
    assert abs(theta_star - 1.7007) < 2e-4
    assert slope_at_one < 0
    assert theta_star < common_interior_limit

    theta_grid = np.linspace(0, 3.4, 500)
    baseline_scale = Delta**2 / 4
    e_M = baseline_scale * e_alpha2 * mu_s + theta_grid * e_inv_s
    e_M2 = (
        baseline_scale**2 * e_alpha4 * e_s2
        + 2 * baseline_scale * theta_grid * e_alpha2
        + theta_grid**2 * e_inv_s2
    )
    var_M = e_M2 - e_M**2
    var_V = e_Gamma2 * var_M + var_Gamma * e_M**2
    var_adoption_benefit = theta_grid**2 * var_G_over_s

    FIG_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
        }
    )
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1), constrained_layout=True)
    navy, red, gold = "#263657", "#B64C4C", "#DCA54A"

    axes[0].plot(theta_grid, var_V, color=navy, linewidth=2.4)
    axes[0].axvline(theta_star, color=gold, linestyle="--", linewidth=1.8)
    axes[0].scatter([theta_star], [np.interp(theta_star, theta_grid, var_V)], color=gold, zorder=3)
    axes[0].set_title("Valor total: U dentro del régimen interior")
    axes[0].set_xlabel(r"Calidad de la herramienta $\theta$")
    axes[0].set_ylabel(r"$\mathrm{Var}[V(\theta)]$")
    axes[0].annotate(
        rf"$\theta^*={theta_star:.4f}$",
        xy=(theta_star, np.interp(theta_star, theta_grid, var_V)),
        xytext=(theta_star + 0.35, np.max(var_V) - 0.025),
        arrowprops={"arrowstyle": "->", "color": gold},
        color=navy,
    )

    axes[1].plot(theta_grid, var_adoption_benefit, color=red, linewidth=2.4)
    axes[1].set_title("Beneficio de adopción: varianza creciente")
    axes[1].set_xlabel(r"Calidad de la herramienta $\theta$")
    axes[1].set_ylabel(r"$\mathrm{Var}[V(\theta)-V(0)]$")
    axes[1].annotate(
        r"$\theta^2\mathrm{Var}(\Gamma/s)$",
        xy=(2.7, np.interp(2.7, theta_grid, var_adoption_benefit)),
        xytext=(1.1, np.max(var_adoption_benefit) * 0.74),
        arrowprops={"arrowstyle": "->", "color": red},
        color=red,
    )

    for ax in axes:
        ax.grid(alpha=0.22)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_xlim(0, theta_grid[-1])

    fig.suptitle("Dos objetos distintos de varianza", fontsize=15, fontweight="bold", color=navy)
    fig.savefig(FIG_DIR / "variance-comparison.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / "variance-comparison.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    return {
        "condition_lhs": condition_lhs,
        "condition_rhs": condition_rhs,
        "theta_star": theta_star,
        "slope_at_one": slope_at_one,
        "common_interior_limit": common_interior_limit,
        "Delta": Delta,
    }


if __name__ == "__main__":
    symbolic_checks()
    result = counterexample()
    print("SymPy checks: PASS")
    print(f"Condition (30): {result['condition_lhs']:.6f} < {result['condition_rhs']:.6f}")
    print(f"theta*: {result['theta_star']:.6f}")
    print(f"dVar[V]/dtheta at theta=1: {result['slope_at_one']:.6f}")
    print(f"Common interior limit: {result['common_interior_limit']:.6f}")
    print(f"Delta: {result['Delta']:.9f}")
    print(f"Figures: {FIG_DIR / 'variance-comparison.pdf'}")
