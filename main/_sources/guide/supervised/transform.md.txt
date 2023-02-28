```{role} python(code)
:language: python
:class: highlight
```

```{currentmodule} wildboar

```

# Transform-based estimators

RocketClassifier and RocketRegressor uses a random convolutional embdding to
represent time series and fit a ridge regression model to the representation.
For benchmark tasks, this transformation and estimator configuration often give
state-of-the-art predictive performance.
