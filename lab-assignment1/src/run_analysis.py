#!/usr/bin/env python
"""Reproducible analysis for Assignment 1 (Consumer Segmentation using PCA)."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

# Avoid a known MKL/KMeans warning on Windows and keep behavior deterministic.
os.environ.setdefault("OMP_NUM_THREADS", "1")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler


@dataclass
class Paths:
    input_csv: Path = Path("inputs/assg1.csv")
    output_dir: Path = Path("outputs")

    @property
    def features(self) -> list[str]:
        return ["X1", "X2", "X3", "X4", "X5"]


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_pca_summary(pca: PCA) -> pd.DataFrame:
    pc_names = [f"PC{i}" for i in range(1, len(pca.explained_variance_) + 1)]
    return pd.DataFrame(
        {
            "component": pc_names,
            "eigenvalue": pca.explained_variance_,
            "explained_variance_ratio": pca.explained_variance_ratio_,
            "cumulative_explained_variance_ratio": np.cumsum(
                pca.explained_variance_ratio_
            ),
        }
    )


def write_runtime_info(out_dir: Path) -> None:
    import platform
    import sys

    info = {
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "libraries": {
            "pandas": pd.__version__,
            "numpy": np.__version__,
            "seaborn": sns.__version__,
            "matplotlib": matplotlib.__version__,
        },
    }
    (out_dir / "runtime_info.json").write_text(
        json.dumps(info, indent=2), encoding="utf-8"
    )


def write_data_quality_report(df: pd.DataFrame, features: list[str], out_dir: Path) -> None:
    lines: list[str] = []
    lines.append("# Data Quality Report")
    lines.append("")
    lines.append(f"- Rows: {len(df)}")
    lines.append(f"- Columns: {len(df.columns)}")
    lines.append(f"- Variables analyzed: {', '.join(features)}")
    lines.append("")
    lines.append("## Schema")
    lines.append("")
    for col, dtype in df.dtypes.items():
        lines.append(f"- `{col}`: `{dtype}`")
    lines.append("")
    lines.append("## Structural Checks")
    lines.append("")
    lines.append(f"- Missing values (all columns): {int(df.isna().sum().sum())}")
    lines.append(f"- Duplicate rows: {int(df.duplicated().sum())}")
    lines.append(f"- Unique `Resp` IDs: {bool(df['Resp'].is_unique)}")
    resp_expected = set(range(1, len(df) + 1))
    resp_actual = set(df["Resp"].astype(int).tolist())
    lines.append(f"- `Resp` equals 1..N exactly: {resp_actual == resp_expected}")
    lines.append("")
    lines.append("## Range and Type Checks (`X1`-`X5`)")
    lines.append("")
    for col in features:
        non_numeric = int(pd.to_numeric(df[col], errors="coerce").isna().sum())
        out_of_range = int(((df[col] < 0) | (df[col] > 9)).sum())
        non_integer = int((df[col] % 1 != 0).sum())
        lines.append(
            f"- `{col}`: non_numeric={non_numeric}, out_of_0_to_9={out_of_range}, non_integer={non_integer}"
        )

    (out_dir / "data_quality_report.md").write_text("\n".join(lines), encoding="utf-8")


def save_correlation_visuals(corr: pd.DataFrame, out_dir: Path) -> None:
    plt.figure(figsize=(7, 5))
    sns.heatmap(
        corr,
        annot=True,
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        square=True,
        fmt=".2f",
    )
    plt.title("Correlation Heatmap (X1-X5)")
    plt.tight_layout()
    plt.savefig(out_dir / "correlation_heatmap.png", dpi=200)
    plt.close()

    cluster_grid = sns.clustermap(
        corr,
        annot=True,
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        figsize=(7, 7),
        fmt=".2f",
    )
    cluster_grid.fig.suptitle("Correlation Clustermap (X1-X5)", y=1.02)
    cluster_grid.fig.savefig(out_dir / "correlation_clustermap.png", dpi=200)
    plt.close(cluster_grid.fig)


def save_scree_plot(pca_summary: pd.DataFrame, out_dir: Path) -> None:
    x = np.arange(1, len(pca_summary) + 1)
    evr = pca_summary["explained_variance_ratio"].to_numpy()
    cev = pca_summary["cumulative_explained_variance_ratio"].to_numpy()

    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax1.bar(x, evr, color="#1f77b4", alpha=0.75, label="Explained variance ratio")
    ax1.set_xlabel("Principal Component")
    ax1.set_ylabel("Explained variance ratio")
    ax1.set_xticks(x)

    ax2 = ax1.twinx()
    ax2.plot(x, cev, color="#d62728", marker="o", label="Cumulative explained ratio")
    ax2.set_ylabel("Cumulative explained variance ratio")
    ax2.set_ylim(0, 1.05)

    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc="center right")
    plt.title("PCA Scree Plot")
    plt.tight_layout()
    plt.savefig(out_dir / "pca_scree_plot.png", dpi=200)
    plt.close(fig)


def build_equations(loadings: pd.DataFrame) -> list[str]:
    equations = []
    for var in loadings.index:
        parts = [f"({loadings.loc[var, c]:+.3f})*F{i}" for i, c in enumerate(loadings.columns, start=1)]
        eq = f"{var}_z = " + " + ".join(parts)
        equations.append(eq)
    return equations


def choose_kmeans_k(pc12: np.ndarray) -> tuple[int, pd.DataFrame]:
    rows = []
    max_k = min(6, len(pc12) - 1)
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = km.fit_predict(pc12)
        sil = silhouette_score(pc12, labels)
        rows.append({"k": k, "silhouette": sil})
    sil_df = pd.DataFrame(rows).sort_values("k").reset_index(drop=True)
    best_k = int(sil_df.loc[sil_df["silhouette"].idxmax(), "k"])
    return best_k, sil_df


def name_segments(profile: pd.DataFrame) -> dict[int, str]:
    names: dict[int, str] = {}
    for idx, row in profile.iterrows():
        if row["X4"] >= 6 and row["X5"] >= 6:
            names[idx] = "Discount-Oriented Pragmatists"
        elif row["X1"] >= 6 and row["X3"] >= 6 and row["X5"] <= 5:
            names[idx] = "Service-Seeking Quality Shoppers"
        elif row["X4"] <= 3 and row["X5"] <= 3 and row["X3"] <= 3:
            names[idx] = "Independent Department-Store Browsers"
        else:
            names[idx] = f"Mixed Preference Segment {idx}"
    return names


def main() -> None:
    paths = Paths()
    ensure_output_dir(paths.output_dir)
    write_runtime_info(paths.output_dir)

    df = pd.read_csv(paths.input_csv)
    features = paths.features
    X = df[features].copy()

    write_data_quality_report(df, features, paths.output_dir)

    raw_desc = X.describe().T
    raw_desc.to_csv(paths.output_dir / "descriptive_stats_raw.csv")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=features, index=df.index)
    scaled_desc = X_scaled_df.describe().T
    scaled_desc.to_csv(paths.output_dir / "descriptive_stats_scaled.csv")

    corr = X.corr()
    corr.to_csv(paths.output_dir / "correlation_matrix.csv")
    save_correlation_visuals(corr, paths.output_dir)

    pca = PCA()
    pcs = pca.fit_transform(X_scaled_df)
    pca_summary = get_pca_summary(pca)
    pca_summary.to_csv(paths.output_dir / "pca_summary.csv", index=False)
    save_scree_plot(pca_summary, paths.output_dir)

    component_names = [f"PC{i}" for i in range(1, len(features) + 1)]
    weights = pd.DataFrame(pca.components_.T, index=features, columns=component_names)
    loadings = weights * np.sqrt(pca.explained_variance_)
    weights.to_csv(paths.output_dir / "pca_weights.csv")
    loadings.to_csv(paths.output_dir / "pca_loadings.csv")

    scores = pd.DataFrame(pcs, columns=component_names, index=df.index)
    scores.insert(0, "Resp", df["Resp"].to_numpy())
    scores.to_csv(paths.output_dir / "pca_scores.csv", index=False)

    equations = build_equations(loadings)
    n_retain_kaiser = int((pca.explained_variance_ > 1).sum())
    n_retain_80pct = int(np.argmax(np.cumsum(pca.explained_variance_ratio_) >= 0.8) + 1)
    with (paths.output_dir / "factor_equations.md").open("w", encoding="utf-8") as f:
        f.write("# PCA Equations (Standardized Variables)\n\n")
        for eq in equations:
            f.write(f"- `{eq}`\n")
        f.write("\n")
        f.write("## Retention Diagnostics\n\n")
        f.write(f"- Components with eigenvalue > 1 (Kaiser): {n_retain_kaiser}\n")
        f.write(f"- Components needed for >=80% cumulative variance: {n_retain_80pct}\n")

    pc12 = pcs[:, :2]
    best_k, sil_df = choose_kmeans_k(pc12)
    sil_df.to_csv(paths.output_dir / "kmeans_silhouette_pc12.csv", index=False)

    km = KMeans(n_clusters=best_k, random_state=42, n_init=20)
    seg = km.fit_predict(pc12)
    df_seg = df.copy()
    df_seg["segment_id"] = seg

    profile = df_seg.groupby("segment_id")[features].mean().round(3)
    segment_sizes = (
        df_seg["segment_id"]
        .value_counts()
        .sort_index()
        .rename_axis("segment_id")
        .reset_index(name="count")
    )
    segment_sizes["pct"] = (segment_sizes["count"] / len(df_seg) * 100).round(2)

    seg_names = name_segments(profile)
    segment_sizes["segment_name"] = segment_sizes["segment_id"].map(seg_names)
    profile["segment_name"] = profile.index.map(seg_names)

    segment_sizes.to_csv(paths.output_dir / "segment_sizes.csv", index=False)
    profile.to_csv(paths.output_dir / "segment_profiles.csv")

    pc_map = pd.DataFrame({"PC1": pc12[:, 0], "PC2": pc12[:, 1], "Resp": df["Resp"], "segment_id": seg})
    pc_map["segment_name"] = pc_map["segment_id"].map(seg_names)
    pc_map.to_csv(paths.output_dir / "pc12_with_segments.csv", index=False)

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=pc_map,
        x="PC1",
        y="PC2",
        hue="segment_name",
        style="segment_name",
        s=90,
        palette="Set2",
    )
    for _, row in pc_map.iterrows():
        plt.text(row["PC1"] + 0.03, row["PC2"] + 0.03, str(int(row["Resp"])), fontsize=7)
    plt.axhline(0, color="gray", linewidth=0.8, alpha=0.5)
    plt.axvline(0, color="gray", linewidth=0.8, alpha=0.5)
    plt.xlabel("PC1: Service Engagement Orientation")
    plt.ylabel("PC2: Discount-Value Orientation")
    plt.title("Consumer Map on First Two Principal Components")
    plt.legend(title="Segment", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(paths.output_dir / "consumer_map_pc1_pc2.png", dpi=220)
    plt.close()

    key_metrics = {
        "rows": int(len(df)),
        "features": features,
        "retained_components_kaiser": n_retain_kaiser,
        "retained_components_80pct": n_retain_80pct,
        "best_k_by_silhouette_on_pc12": best_k,
        "explained_variance_ratio_pc1": float(pca.explained_variance_ratio_[0]),
        "explained_variance_ratio_pc2": float(pca.explained_variance_ratio_[1]),
        "explained_variance_ratio_pc1_pc2": float(np.sum(pca.explained_variance_ratio_[:2])),
    }
    (paths.output_dir / "key_metrics.json").write_text(
        json.dumps(key_metrics, indent=2), encoding="utf-8"
    )

    print("Analysis complete.")
    print(f"Best k on PC1-PC2 (silhouette): {best_k}")
    print(f"PC1+PC2 explained variance: {key_metrics['explained_variance_ratio_pc1_pc2']:.4f}")


if __name__ == "__main__":
    main()

