.. currentmodule:: wildboar

###############
Getting started
###############


****************
Machine learning
****************

In general, the machine learning problem setting consists of $n$ samples of
data and the goal is to predict properties of unknown data. In particular,
Wildboar consider machine learning problems in which the samples are data
series, e.g., time series or otherwise temporally or logically ordered data.

.. note::
   For solving general machine learning problems with Python, consider using
   `scikit-learn <https://scikit-learn.org>`_.

Similar to general machine learning problems, temporal machine learning is
concerned with problems that fall into different categories

- Supervised learning, in which the data series are labeled with additional
  information. The additional information can be either numerical or nominal

- In classification problems the time series belong to one of two or more labels
  and the goal is to learn a function that can label unlabeled time series.

- In regression problems the time series are labeled with a numerical attribute
  and the task is to assign a new numerical value to an unlabeled time series.

**************************
Loading an example dataset
**************************

To start experimenting with Wildboar and temporal machine learning, we need
some data to explore. Wildboar bundles a few standard datasets from the time
series community collected in the `UCR Time series repository
<http://www.timeseriesclassification.com>`_.

In the following example, we load the dataset ``synthetic_control`` and the
``TwoLeadECG`` dataset.

.. code-block:: python

   from wildboar.datasets import load_synthetic_control, load_two_lead_ecg
   x, y = load_synthetic_control()
   x_train, x_test, y_train, y_test = load_two_lead_ecg(merge_train_test=False)

.. note::

   By setting ``merge_train_test`` to :python:`False`, the original training
   and testing splits from the UCR repository are preserved.

   A more robust and reliable method for splitting the datasets into training
   and testing partitions is to use the model selection functions from
   scikit-learn.

   .. code-block:: python

      from sklearn.model_selection import train_test_split
      x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

The datasets are Numpy ``ndarray`` s with :python:`x.ndim==2` and
:python:`y.ndim==1`. We can get the number of samples and time points.

.. code-block:: python

   n_samples, n_timestep = x.shape

.. note::

   Wildboar also supports multivariate time series using *3d*-arrays, i.e., we can
   get the shape of the dataset by :python:`n_samples, n_dims, n_timestep =
   x.shape`. Since operations are often performed over the temporal dimension, we
   opt for having that as the last dimension of the array. Since we prefer c-order
   arrays, this means that the data is contiguous in memory. A robust approach for
   getting the number of samples and number of time steps irrespective of univariate (*2d*)
   or multivariate (*3d*) time series is:

   .. code-block:: python

      n_samples, n_timestep = x.shape[0], x.shape[-1]

In the example, we use ``load_two_lead_ecg`` and ``load_synthetic_control`` to
load the datasets. A more general approach is to use the
:func:`~datasets.load_dataset`-function from the same modules.

.. code-block:: python

   from wildboar.datasets import load_dataset
   x, y = load_dataset("synthetic_control")

:func:`~datasets.load_dataset` accepts multiple parameters for specifying where
to load data from or how to preprocess the data. By default, Wildboar loads
datasets from the ``wildboar/ucr`` repository, which include datasets from UCR
time series repository. The user can specify a different repository using the
``repository`` argument. For example, we can load the regression task
``FloodModeling1`` from the UEA & UCR Time Series Extrinsic Regression
Repository, standardizing each time series with zero mean and unit variance.

.. code-block:: python

   x, y = load_dataset(
   "FloodModeling1", repository="wildboar/tsereg", preprocess="standardize"
   )

***********************
Learning and predicting
***********************

All estimators in Wildboar implements the same interface as all estimators of
scikit-learn. We can ``fit`` an estimator to an input dataset and ``predict``
the label of a new sample.

An example of a temporal estimator is the
:class:`ensemble.ShapeletForestClassifier` which implements a random shapelet
forest classifier.

.. code-block:: python

   from wildboar.ensemble import ShapeletForestClassifier
   clf = ShapeletForestClassifier()
   clf.fit(x_train, y_train)

We fit the classifier (`clf`) using the training samples, and can use the same
object to predict the label of a previously unseen sample.

.. code-block:: python

   clf.predict(x_test[-1:, :]) # outputs array([6.])

.. note::
   The predict function expects a ``ndarray`` of shape :python:`(n_samples,
   n_timestep)`, where ``n_timestep`` is the size of training timestep.

Wildboar also simplifies experimentation over multiple datasets by allowing the
user to repeatedly load several datasets from a repository.

.. code-block:: python

   from wildboar.datasets import load_datasets

   for name, (x_train, x_test, y_train, y_test) in load_datasets(
      "wildboar/ucr",
      collection="bake-off",
      merge_train_test=False,
      filter="n_samples<=300",
   ):
      clf = clone(clf)  # from sklearn import clone
      clf.fit(x, y)
      print(f"{name}: {clf.score(x, y)}")


In the example, we load all datasets in the ``bake-off`` collection from the
``wildboar/ucr`` repository, filtering datasets with less than 300 samples. For
each dataset that we load, we clone and fit the estimator and print the dataset
name and the predictive performance to the screen. You can :doc:`read more
about datasets in the API-documentation <wildboar:wildboar/datasets/index>`.

****************************************
Transforming time series to tabular data
****************************************

Despite the numerous estimators specialized for temporal data, an even larger
collection of methods exist for tabular data (e.g., as implemented by
`scikit-learn <https://scikit-learn.org>`_). For this purpose, Wildboar
implements several transformers that can be used to transform temporal data to
tabular data. All wildboar estimators follow the same convention as
scikit-learn and implements a ``fit``-method but instead of ``predict`` implements
``transform`` that outputs a new tabular representation of each input sample.

.. code-block:: python

   from wildboar.transform import RocketTransform
   rocket = RocketTransform()
   rocket.fit(x)
   tabluar_x = rocket.transform(x)

One of Wildboar's main design goals is to fully interoperate with scikit-learn
without user intervention. As such, we can use Wildboar transformers to build
:doc:`scikit-learn pipelines <sklearn:modules/generated/sklearn.pipeline.Pipeline>`.

.. code-block:: python

   from sklearn.pipeline import make_pipeline
   from sklearn.linear_model import LogisticRegression
   clf = make_pipeline(
   RocketTransform(),
   LogisticRegression(),
   )
   clf.fit(x, y)
   clf.score(x, y)

.. warning::
   In the above example, we train and evaluate the model on the same data. This is
   bad practice. Instead, we should use a proper hold-out dataset when estimating the
   pipelines performance.

***************************
Exploring model performance
***************************

Wildboar implements several methods for explaining classifiers, e.g., using
counterfactual reasoning or input dependencies.

.. code-block:: python

   from wildboar.explain import IntervalImportance
   i = IntervalImportance()
   i.fit(clf, x, y)
   i.plot(x, y=y)

The :class:`wildboar.explain.IntervalImportance`-class identifies temporal
regions that are responsible for the classifier performance. It does so by
breaking the dependency between continuous intervals and the label while
reevaluating the predictive performance of the classifier of sample-wise
shuffled intervals. In the example, we evaluate the in-sample importance, which
captures the reliance of the model on a particular interval.

.. ldimage:: /_static/fig/getting-started/interval.svg
   :align: center

The :meth:`explain.IntervalImportance.plot` method can be used to visualize the
interval importance, or we can return the full importance matrix.

.. code-block:: python

   >>> i.importance_.mean()
   [..., 0.31, 0.30, 0.34, ...]

*****************
Model persistence
*****************

All Wildboar models can be persisted to disk using
`pickle  <https://docs.python.org/3/library/pickle.html>`_

.. code-block:: python

   import pickle
   repr = pickle.dumps(clf) # clf fitted earlier
   clf_ = pickle.loads(repr)
   clf_.predict(x_test[-1:, :]) # outputs array([6.])

Models persisted using an older version of Wildboar is not guaranteed to
work when using a newer version (or vice versa).

.. warning::
   The pickle module is not secure. Only unpickle data you trust. `Read more in
   the Python documentation <https://docs.python.org/3/library/pickle.html>`_
