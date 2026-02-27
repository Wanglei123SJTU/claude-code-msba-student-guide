# Objective
Identify latent attitude factors behind store preferences (`X1`-`X5`) and use them to map consumers into actionable market segments.

# Method
- Read and validated `inputs/assg1.csv` (30 rows, no missing values, no duplicates, valid 0-9 scale).
- Standardized `X1`-`X5` and computed correlation structure (`outputs/correlation_matrix.csv`, `outputs/correlation_clustermap.png`).
- Ran PCA on standardized attributes (`outputs/pca_summary.csv`, `outputs/pca_loadings.csv`, `outputs/factor_equations.md`).
- Retained factors using eigenvalue>1 and cumulative explained variance criteria.
- Built a 2D consumer map using PC1 and PC2 (`outputs/consumer_map_pc1_pc2.png`).
- Estimated segment count from the map and supported it with KMeans silhouette on PC1-PC2 (`outputs/kmeans_silhouette_pc12.csv`), then profiled segments (`outputs/segment_profiles.csv`, `outputs/segment_sizes.csv`).

# Key Results
- Strong associations in original attributes:
  - `X1` and `X3` strongly positive (`r=0.879`).
  - `X2` strongly negative with `X1` (`r=-0.711`) and `X3` (`r=-0.832`).
  - `X4` and `X5` moderately/strongly positive (`r=0.664`).
- PCA concentration:
  - PC1 explains `53.43%`, PC2 explains `37.04%`, and PC1+PC2 explain `90.48%` total variance.
  - Retained components: `2` (Kaiser and >=80% cumulative both agree).
- Factor interpretation from loadings:
  - PC1 (Service Engagement Orientation): high on `X1`/`X3`, negative on `X2`.
  - PC2 (Discount-Value Orientation): high on `X4`/`X5`.
- Segment structure (best silhouette at `k=3`, silhouette `0.609`):
  - Discount-Oriented Pragmatists: `43.33%` (13/30), high `X4`,`X5`, low `X1`,`X3`.
  - Independent Department-Store Browsers: `20.00%` (6/30), low `X4`,`X5`,`X3`.
  - Service-Seeking Quality Shoppers: `36.67%` (11/30), high `X1`,`X3`, low `X2`, lower `X5`.

# Business Interpretation
- The market appears to have three distinct preference clusters rather than one uniform customer base.
- The likely most profitable segment is **Service-Seeking Quality Shoppers** (`36.67%`) because they value service interaction and appear less discount-driven (`X5` relatively low), which usually supports better gross margins in higher-service retail formats.
- Discount-Oriented Pragmatists are largest but likely more price-sensitive, requiring tighter pricing/promotions to convert.
- Independent Department-Store Browsers may respond to store environment and self-guided shopping rather than high-touch service.

# Limitations and Next Steps
- Sample size is small (`n=30`), so segment sizes and centroids may be unstable.
- No direct outcomes (profit, spend, basket size, retention) are provided, so profitability is inferred from attitudes, not measured.
- PCA and KMeans are sensitive to sample composition and scaling assumptions.
- Next steps:
  - Collect a larger, representative sample and validate segment stability with holdout data.
  - Link segments to transactional metrics to test profitability assumptions.
  - Test targeted positioning/messaging per segment and measure uplift experimentally.
