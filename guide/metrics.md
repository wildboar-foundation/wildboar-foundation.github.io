```{currentmodule} wildboar

```

# Metrics

```{toctree}
:hidden:
:maxdepth: 2

metrics/distance
```

Wildboar support both subsequence distance using
{func}`~distance.pairwise_subsequence_distance` and traditional distances using
{func}`~distance.pairwise_distance`. These and related functions support
different metrics, as specified by the `metric` argument and metric parameters
using the `metric_params` argument.

Distance metrics are functions $d(x, y)$ such that $d(x, y) < d(x, z)$ if time
series $x$ and $y$ are _"more similar"_ than $x$ and $z$. In Wildboar we use the
term loosely to denote any function obeying the above inequality. A
[true metric](https://en.wikipedia.org/wiki/Metric_space)
({octicon}`mortar-board`) must also satisfy the following:

1. The distance to itself is always zero i.e., $d(x, x) = 0.$.

2. The distance between two distinct points is always positive, i.e.,
   $d(x, y) \gt 0$, given $x\ne y$.

3. The distance is symmetrical, i.e., $d(x, y) = d(y, x)$ which is to say that
   the distance between $x$ and $y$ is the same as the distance between $y$ and
   $x$.

4. The triangle inequality holds, $d(x, z) \lt d(x, y) + d(y, z)$, i.e., there
   can be no _"shortcut"_ through $y$ that makes the distance shorter.

Similarity measures fall into three categories:

1. Non-elastic true metrics such as $Lp$-norm that do not support time-shift.

2. Elastic ({octicon}`iterations`) metrics that tolerate time-shifts but are not
   _true metrics_

3. Elastic metrics that tolerate time-shifts, but _that are true metrics_.

Wildboar also distinguishes between subsequence and non-subsequence metrics:

1.  Subsequence metrics computes the $min_{t'\in t} d(s, t')$ with
    `s.shape[-1] <= t.shape[-1]` (i.e., $s$ is shorter than $t$) and the
    notation represents "taking all subsequences in $t$ of the same length as
    $s$ and compute the distance, taking the minimum". Subsequence metrics are
    never true metrics unless `s.shape[-1] == t.shape[-1]`.

2.  Metrics computes the distance $d(s, t)$ with `s.shape[-1] == t.shape[-1]`
    unless the metric is _elastic_. Elastic metrics support distance
    computations between time series of unequal length, without computing the
    minimum distance between equal-length subsequences.

## Subsequence metrics

Wildboar implements
{ref}`several subsequence metrics <list_of_subsequence_metrics>`. The _elastic_
subsequence metrics are, as all subsequence metrics, implemented as the minimum
distance over a sliding window. As such, if we need the elastic distance between
two series and **not** the minimum distance, we should use the non-subsequence
metric. Moreover, subsequence metrics are only _true metrics_
({octicon}`mortar-board`) if we compute the distance between time series of
equal length, which makes the minimum subsequence distance equal to the
distance.

```{list-table}
:widths: 5, 5, 20, 15, 20, 35
:header-rows: 1
:name: list_of_subsequence_metrics

* - {octicon}`mortar-board`
  - {octicon}`iterations`
  - Metric name
  - `metric`
  - `metric_params`
  - Comments

* - {octicon}`check`
  -
  - Euclidean
  - `"euclidean"`
  - `{}`
  -

* - {octicon}`check`
  -
  - Normalized Euclidean
  - `"normalized_euclidean"`
  - `{}`
  - Euclidean distance, where length has been scaled to have unit norm.
    Undefined cases result in 0.

* - {octicon}`check`
  -
  - Scaled Euclidean
  - `"scaled_euclidean"` or `"mass"`
  - `{}`
  - Scales each subsequence to have zero mean and unit variance.

* - {octicon}`check`
  -
  - Manhattan
  - `"manhattan"`
  - `{}`
  -

* - {octicon}`check`
  -
  - Minkowski
  - `"minkowski"`
  - `{p: float}`
  -

* - {octicon}`check`
  -
  - Chebyshev
  - `"chebyshev"`
  - `{}`
  -

* -
  -
  - Cosine
  - `"cosine"`
  - `{}`
  -

* - {octicon}`check`
  -
  - Angular
  - `"angular"`
  - `{}`
  -

* -
  - {octicon}`check`
  - Dynamic time warping
  - `"dtw"`
  - `{"r": float}`
  - Window `r` in `[0, 1]`

* -
  - {octicon}`check`
  - Weighted DTW
  - `"wdtw"`
  - `{"r": float, "g": float}`
  - Window `r` in `[0, 1]`, default `1.0`. Phase difference penalty `g`, default `0.05`.

* -
  - {octicon}`check`
  - Derivative DTW
  - `"ddtw"`
  - `{"r": float}`
  - Window `r` in `[0, 1]`, default `1.0`.

* -
  - {octicon}`check`
  - Weighted Derivative DTW
  - `"wddtw"`
  - `{"r": float, "g": float}`
  - Window `r` in `[0, 1]`, default `1.0`. Phase difference penalty `g`, default `0.05`.

* -
  - {octicon}`check`
  - Scaled DTW
  - `"scaled_dtw"`
  - `{"r": float}`
  - Window `r` in `[0, 1]`

* -
  - {octicon}`check`
  - Longest common subsequence[^lcss]
  - `"lcss"`
  - `{r: float, epsilon: float}`
  - Window `r` in `[0, 1]`, default `1.0`.  Match `epsilon`, default `1.0`.

* - {octicon}`check`
  - {octicon}`check`
  - Edit distance with real penalty[^erp]
  - `"erp"`
  - `{r: float, g: float}`
  - Window `r` in `[0, 1]`, default `1.0`. Gap penalty `g`, default `0`.

* -
  - {octicon}`check`
  - Edit distance for real sequences[^edr]
  - `"edr"`
  - `{r: float, epsilon: float}`
  - Window `r` in `[0, 1]`, default `1.0`. Match `epsilon`, default `1/4*max(std(x), std(y))`.

* - {octicon}`check`
  - {octicon}`check`
  - Move-split-merge[^msm]
  - `"msm"`
  - `{r: float, c: float}`
  - Window `r` in `[0, 1]`, default `1.0`. Split/merge cost `c`, default `1`.

* - {octicon}`check`
  - {octicon}`check`
  - Time Warp Edit distance[^twe]
  - `"twe"`
  - `{r: float, edit_penalty: float, stiffness: float}`
  - Window `r` in `[0, 1]`. Edit penalty (:math:`\lambda`), default `1`.
    Stiffness ($\nu$), default `0.001`.
```

## Elastic and non-elastic metrics

```{list-table}
:widths: 5, 5, 20, 15, 20, 35
:header-rows: 1
:name: list_of_metrics
* - {octicon}`mortar-board`
  - {octicon}`iterations`
  - Metric name
  - `metric`
  - `metric_params`
  - Comments

* - {octicon}`check`
  -
  - Euclidean
  - `"euclidean"`
  - `{}`
  -

* - {octicon}`check`
  -
  - Normalized Euclidean
  - `"normalized_euclidean"`
  - `{}`
  - Euclidean distance, where length has been scaled to have unit norm.
    Undefined cases result in 0.

* - {octicon}`check`
  -
  - Manhattan
  - `"manhattan"`
  - `{}`
  -

* - {octicon}`check`
  -
  - Minkowski
  - `"minkowski"`
  - `{p: float}`
  -

* - {octicon}`check`
  -
  - Chebyshev
  - `"chebyshev"`
  - `{}`
  -

* -
  -
  - Cosine
  - `"cosine"`
  - `{}`
  -

* - {octicon}`check`
  -
  - Angular
  - `"angular"`
  - `{}`
  -

* -
  - {octicon}`check`
  - Longest common subsequence[^lcss]
  - `"lcss"`
  - `{r: float, epsilon: float}`
  - Window `r` in `[0, 1]`, default `1`.  Match `epsilon`, default `1`.

* - {octicon}`check`
  - {octicon}`check`
  - Edit distance with real penalty[^erp]
  - `"erp"`
  - `{r: float, g: float}`
  - Window `r` in `[0, 1]`. Gap penalty `g`, default `0`.

* -
  - {octicon}`check`
  - Edit distance for real sequences[^edr]
  - `"edr"`
  - `{r: float, epsilon: float}`
  - Window `r` in `[0, 1]`. Match `epsilon`, default `1/4*max(std(x), std(y))`.

* - {octicon}`check`
  - {octicon}`check`
  - Move-split-merge[^msm]
  - `"msm"`
  - `{r: float, c: float}`
  - Window `r` in `[0, 1]`. Split/merge cost `c`, default `1`.

* - {octicon}`check`
  - {octicon}`check`
  - Time Warp Edit distance[^twe]
  - `"twe"`
  - `{r: float, edit_penalty: float, stiffness: float}`
  - Window `r` in `[0, 1]`. Edit penalty ($\lambda$), default `1`.
    Stiffness ($\nu$), default `0.001`.

* -
  - {octicon}`check`
  - Dynamic time warping
  - `"dtw"`
  - `{"r": float}`
  - Window `r` in `[0, 1]`.

* -
  - {octicon}`check`
  - Weighted DTW
  - `"wdtw"`
  - `{"r": float, "g": float}`
  - Window `r` in `[0, 1]`. Phase difference penalty `g`, default `0.05`.

* -
  - {octicon}`check`
  - Derivative DTW
  - `"ddtw"`
  - `{"r": float}`
  - Window `r` in `[0, 1]`.

* -
  - {octicon}`check`
  - Weighted Derivative DTW
  - `"wddtw"`
  - `{"r": float, "g": float}`
  - Window `r` in `[0, 1]`. Phase difference penalty `g`, default `0.05`.
```

[^lcss]:
    Hirschberg, D. (1977). Algorithms for the longest common subsequence
    problem. Journal of the ACM (JACM).

[^edr]:
    Chen, L., & Ng, R. (2004). On the Marriage of Lp-Norms and Edit Distance
    (30). Proceedings of the Thirtieth International Conference on Very Large
    Data Base.

[^erp]:
    Chen, L., Özsu, M. T., & Oria, V. (2005). Robust and fast similarity search
    for moving object trajectories. Proceedings from Proceedings of the
    International Conference on Management of Data

[^msm]:
    Stefan, A., Athitsos, V., & Das, G. (2013). The Move-Split-Merge Metric for
    Time Series. IEEE Transactions on Knowledge and Data Engineering, 25(6),
    1425-1438.

[^twe]:
    Marteau, P.-F. (2008). Time warp edit distance with stiffness adjustment for
    time series matching. IEEE transactions on pattern analysis and machine
    intelligence, 31(2), 306-318.
