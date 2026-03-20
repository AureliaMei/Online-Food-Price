"""
tree_models.py — Percentile-aware decision tree for price range prediction.

Classes
-------
PercentileDecisionTree — wraps DecisionTreeRegressor, stores training y-values
    per leaf so any quantile can be computed at predict time.

    predict(X)                    → 1-D array of p50 per sample
    predict_percentiles(X)        → (n, 5) array: [p5, p25, p50, p75, p95]
    predict_interval(X, lo, hi)   → (n, 3) array: [lo_pct, p50, hi_pct]
"""

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.tree import DecisionTreeRegressor


class PercentileDecisionTree(BaseEstimator, RegressorMixin):
    """Decision tree that returns prediction intervals instead of point estimates.

    At fit time the training y-values for every leaf node are stored.
    At predict time any quantile can be looked up in O(n_samples) time.

    Parameters match DecisionTreeRegressor so cross_val_predict / clone work.
    """

    def __init__(self, max_depth=5, min_samples_leaf=15, random_state=42):
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.random_state = random_state

    # ------------------------------------------------------------------
    # Fit
    # ------------------------------------------------------------------
    def fit(self, X, y):
        self._tree = DecisionTreeRegressor(
            max_depth=self.max_depth,
            min_samples_leaf=self.min_samples_leaf,
            random_state=self.random_state,
        )
        self._tree.fit(X, y)

        # Store raw training y-values per leaf so any quantile is available
        leaf_ids = self._tree.apply(X)
        self._leaf_values_ = {}
        for leaf_id, yi in zip(leaf_ids, y):
            self._leaf_values_.setdefault(int(leaf_id), []).append(yi)
        # Convert lists to sorted arrays for fast np.percentile calls
        self._leaf_values_ = {
            k: np.sort(np.asarray(v)) for k, v in self._leaf_values_.items()
        }
        return self

    # ------------------------------------------------------------------
    # Predict helpers
    # ------------------------------------------------------------------
    def _percentile_for_leaf(self, leaf_id: int, q: float) -> float:
        return float(np.percentile(self._leaf_values_[leaf_id], q))

    def predict(self, X) -> np.ndarray:
        """Return p50 per sample (compatible with cross_val_predict)."""
        return self.predict_interval(X, lo=50, hi=50)[:, 0]

    def predict_percentiles(self, X) -> np.ndarray:
        """Return (n, 5) array: columns are p5, p25, p50, p75, p95."""
        leaf_ids = self._tree.apply(X)
        qs = [5, 25, 50, 75, 95]
        out = np.empty((len(leaf_ids), 5), dtype=np.float64)
        for i, lid in enumerate(leaf_ids):
            out[i] = [self._percentile_for_leaf(lid, q) for q in qs]
        return out

    def predict_interval(self, X, lo: float = 5, hi: float = 95) -> np.ndarray:
        """Return (n, 3) array: columns are [lo_pct, p50, hi_pct]."""
        leaf_ids = self._tree.apply(X)
        out = np.empty((len(leaf_ids), 3), dtype=np.float64)
        for i, lid in enumerate(leaf_ids):
            out[i, 0] = self._percentile_for_leaf(lid, lo)
            out[i, 1] = self._percentile_for_leaf(lid, 50)
            out[i, 2] = self._percentile_for_leaf(lid, hi)
        return out

    # ------------------------------------------------------------------
    # Pass-throughs to inner tree
    # ------------------------------------------------------------------
    @property
    def feature_importances_(self):
        return self._tree.feature_importances_

    @property
    def tree_(self):
        return self._tree.tree_

    @property
    def n_features_in_(self):
        return self._tree.n_features_in_

    def apply(self, X):
        return self._tree.apply(X)

    def get_n_leaves(self):
        return self._tree.get_n_leaves()

    def get_depth(self):
        return self._tree.get_depth()
