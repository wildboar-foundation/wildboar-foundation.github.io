```{role} python(code)
:language: python
:class: highlight
```

```{currentmodule} wildboar

```

# Repositories

We can either initialize repositories directly or use them together with the
{func}`~datasets.load_dataset`-function:

```python
from wildboar.datasets import load_dataset
x, y = load_dataset('GunPoint', repository='wildboar/ucr')
```

Installed repositories and dataset bundles can be listed using the function
{func}`~datasets.list_repositories` and {func}`~datasets.list_bundles`
respectively.

```python
>>> from wildboar.datasets import list_repositories, list_bundles, list_datasets
>>> list_repositories()
['wildboar']
>>> list_bundles("wildboar")
['ucr', 'ucr-tiny', ... (and more)]
>>> list_datasets("wildboar/ucr-tiny")
['Beef', 'Coffee', 'GunPoint', 'SyntheticControl', 'TwoLeadECG']
```

## Repository definitions

A wildboar repository string is composed of 2 required and two optional
components written as:

```
{repository}/{bundle}[:{version}][:{tag}]
└─────┬────┘ └───┬──┘└─────┬────┘└───┬──┘
      │          │         │         └── (optional) The tag as defined below.
      │          │         └── (optional) The version as defined below.
      │          └── (required) The bundle as listed by list_bundles().
      └── (required) The repository as listed by list_repositories().
```

Each part of the repository has the following requirements:

`{repository}`

: The repository identifier, as listed by {func}`~datasets.list_repositories`.
The identifier is composed of letters, i.e., matching the regular expression,
`\w+`.

`{bundle}`

: The bundle identifier, as listed by {func}`~datasets.list_bundles`. The
identifier is composed of alphanumeric characters and `-`, matching the regular
expression `[a-zA-Z0-9\-]+`.

`{version}`

: The bundle version (defaults to the version specified by the repository). The
version must match `{major}[.{minor}][.{revision}]`, where each component
matches the regular expression `\d+`.

`{tag}`

: The bundle tag (defaults to `default`). The bundle tag is composed of letters
and `-`, matching the regular expression `[a-zA-Z-]+`.

To exemplify, these are valid repository declarations:

`wildboar/ucr`

: the `ucr` bundle from the `wildboar` repository using the latest version and
the `default` tag.

`wildboar/ucr-tiny:1.0`

: the `ucr-tiny` bundle from the `wildboar` repository using the version `1.0`
and `default` tag.

`wildboar/outlier:1.0:hard`

: the `outlier` bundle, with version `1.0`, from the `wildboar` repository using
the tag `hard`.

## Installing repositories

A repository implements the interface of the class
`wildboar.datasets.Repository`

```{note}
The default wildboar-repository is implemented using a {class}`~datasets.JSONRepository`
which specifies (versioned) datasets on a JSON endpoint.
```

Repositories are installed using the function
{func}`~datasets.install_repository` which takes either a URL to a JSON-file or
an instance of (a subclass to) {class}`~datasets.Repository`.

```python
>>> from wildboar.datasets import install_repository
>>> install_repository("https://www.example.org/repo.json")
>>> list_repositories("example")
>>> load_dataset("example", repository="example/example")
```

Repositories can be refreshed using {func}`~datasets.refresh_repositories()`,
which accepts a repository name to refresh a specific repository or `None`
(default) to refresh all repositories. Additionally, we can specify an optional
refresh timeout (in seconds), and an optional cache location. Since 1.1,
Wildboar caches the repository definition locally to allow cached datasets to be
used while offline.

## Loading datasets

As described previously, {func}`~datasets.load_dataset` is the main entry-point
for easy loading of datasets, but we can also iteratively load multiple datasets
using {func}`~datasets.load_datasets`. Currently, Wildboar only installs one
repository by default, the `wildboar` repository. We hope that others will find
the feature usefull, and will distribute their datasets as Wildboar
repositories. One drawback of the current distribution approach, is that to load
a single dataset, the full bundle has to be downloaded. We hope to improve this
in the future and download assets on-demand. For small experiments, we can load
a small selection of datasets from the `wildboar/ucr-tiny` bundle, either using
{func}`~datasets.load_dataset` or using one of the named functions, e.g.,
{func}`~datasets.load_gun_point` (browse {mod}`wildboar.datasets` for all such
functions).

### Loading a single dataset

We can load a single dataset as follows:

```python
>>> from wildboar.datasets import load_dataset
>>> x, y = load_dataset("GunPoint", repository="wildboar/ucr-tiny")
Downloading ucr-tiny-v1.0.2-default.zip (688.43 KB)
  |██████████████████████████████████████████████----| 668.43/688.43 KB
>>> x.shape
(200, 150)
```

Wildboar offers additional operations that we can perform while loading
datasets, for example, we can
{doc}`preprocess the time series </guide/datasets/preprocess>` or return
optional training/testing parts by setting `merge_train_test` to
{python}`False`.

```python
>>> x_train, x_test, y_train, y_test = load_dataset("GunPoint", merge_train_test=False)
>>> x_train.shape, x_test.shape
((50, 150), (150, 150))
```

We can also force a re-download of an already cached bundle by setting `force`
to {python}`True`, and changing the `dtype` of the returned time series:

```python
>>> load_datasets("GunPoint", dtype=float, force=True)
# ... re-download dataset
```

```{note}
By default, the datasets downloaded from the `wildboar` repository are `np.float32`
to reduce the download size.
```

### Loading multiple datasets

When running experiments, a common workflow is to load multiple dataset, fit and
evaluate some estimator. In Wildboar, we can repeatedly load datasets from a
bundle using the {func}`~datasets.load_datasets`-function:

```python
>>> from wildboar.datasets import load_datasets
>>> for name, (x, y) in load_datasets("wildboar/ucr-tiny"):
...     print(name, x.shape)
...
Beef (60, 470)
Coffee (56, 286)
GunPoint (200, 150)
SyntheticControl (600, 60)
TwoLeadECG (1162, 82)
>>>
```

Loading multiple datasets also support setting the `merge_train_test` to
`False`:

```python
>>> for name, (x_train, x_test, y_train, y_test) in load_datasets("wildboar/ucr-tiny"):
...     print(name, x_train.shape)
...
```

### Filters

We can also specify filters to filter the datasets on the number of dimensions,
samples, timesteps, labels and dataset names. We specify filters with the
`filter` parameter, which accepts a `list`, `dict` or `str`. We express string
filters as:

```
                       ┌── Operator specification
           ┌───────────┴───────────┐
(attribute)[<|<=|>|>=|=|=~](\d+|\w+)
└────┬────┘└───────┬──────┘└───┬───┘
     │             │           └── A number or (part of) a dataset name
     │             └── The comparision operator
     └── The attribute name
```

The attribute name is one of (the self-explanatory) attributes:

`n_samples`

: (`numeric`) The number of samples.

`n_timesteps`

: (`numeric`) The number of time steps.

`n_dims`

: (`numeric`) The number of dimensions.

`n_labels`

: (`numeric`) The number of labels

`dataset`

: (`string`) The dataset name

The `numeric` comparison operators are `<`, `<=`, `>`, `>=` and `=`, for
less-than, less-than-or-equal, greater-than, greater-than-or-equal-to and
exactly-equal-to respectively. These are defined for the numerical attributes.
The string comparison operators are `=` and `=~`, for exactly-equal-to and
exists-in respectively.

Filters can be chained to support `and-also` using a `list` or a `dict`:

```python
>>> large = "n_samples>=100"
>>> large_multivariate = ["n_samples>=100", "n_dims>1"]
>>> large_multiclass = {
...     "n_samples": ">=100",
...     "n_labels": ">2",
... }
>>> load_datasets("wildboar/ucr-tiny", filter=large_multiclass)
<generator object load_datasets at 0x7f262ce95d00>
```

```{warning}
If we load multiple datasets with the parameter `merge_train_test` set to `False`
filters are applied to the **training** part only.
```

{func}`~datasets.load_datasets` also accepts all parameters that are valid for
{func}`~datasets.load_dataset`, so we can also preprocess the time series:

```python
>>> load_datasets("wildboar/ucr-tiny", filter=large, preprocess="minmax_scale")
<generator object load_datasets at 0x7f262ce95d00>
```

### Local cache

As noted above, Wildboar downloads, on-demand, datasets the first time we
request a bundle. The first time we download a bundle, it is cached to disk in a
user directory determined by the operating system. Wildboar caches datasets and
repositories in the following directories:

**Windows**

: `%LOCALAPPDATA%\cache\wildboar`

**GNU/Linux**

: `$XDG_HOME_DIR/wildboar`. If `$XDG_HOME_DIR` is unset, we default to `.cache`.

**macOS**

: `~/LibraryCaches/wildboar`.

**Fallback**

: `~/.cache/wildboar`

We can change the cache directory, either globally (for as long as the current
Python session lasts) with {func}`datasets.set_cache_dir` or locally (for a
specific operation) with then `cache_dir`-parameter:

```python
>>> from wildboar.datasets import set_cache_dir
>>> set_cache_dir("/path/to/wildboar-cache/") # Set the global cache
>>> load_dataset("GunPoint", cache_dir="/path/to/another/wildboar-cache/") # Another, local, cache here
```

If called without arguments, {func}`~datasets.set_cache_dir` resets the cache to
the default location based on the operating system.

## JSON repositories

By default, repositories installed with {func}`~datasets.install_repository`
should point to a JSON-file, which describes the available datasets and the
location where Wildboar can download them. The repository declaration is a
JSON-file:

```json
{
    "name": "example", // required
    "version": "1.0",  // required
    "wildboar_requires": "1.1", // required, the minimum required wildboar version
    "bundle_url": "https://example.org/download/{key}/{tag}-v{version}", // required, the data endpoint
    "bundles": [ // required
      {
        "key": "example", // required, unique key of the bundle
        "version": "1.0", // required, the default version of dataset
        "tag": "default"  // optional, the default tag
        "name": "UCR Time series repository", // required
        "description": "Example dataset", // optional
        "arrays": ["x", "y"] // optional
        "collections": {"key": ["example1", "example"]} // optional
      },
    ]
}
```

- The attributes `{key}`, `{version}` and `{tag}` in the `bundle_url` are
  replaced with the bundle-key, bundle-version and bundle tag from the
  repository string. All attributes are required in the url.

- The `arrays` attribute is optional. However, if it is not present, the dataset
  is assumed to be a single numpy array, where the last column contains the
  class label or a numpy-dict with both `x`, and `y` keys.

  - if any other value except `x` and/or `y` is present in the `arrays`-list, it
    will be loaded as an `extras`-dictionary and only returned if requested by
    the user.
  - if `y` is not present in arrays `load_dataset` return `None` for `y`

- The `bundles/version` attribute, is the default version of the bundle which is
  used unless the user specifies an alternative version in the repository
  string.

- The `bundles/tag` attribute is the default tag of the bundle which is used
  unless the user specifies an alternative bundle. If not specified, the tag is
  `default`.

- The `bundles/collections` attribute is a dictionary of named collections of
  datasets which can be specified when using
  `load_datasets(..., collection="key")`

The `bundle_url` points to a remote location that for each bundle `key`,
contains two files with extensions `.zip` and `.sha` respectively. In the
example, `bundle_url` should contain the two files `example/default-v1.0.zip`
and `example/default-v1.0.sha` The `.sha`-file should contain the `sha1` hash of
the `.zip`-file to ensure the integrity of the downloaded file. The `zip`-file
should contain the datasets.

By default, wildboar supports dataset bundles formatted as `zip`-files
containing `npy` or `npz`-files, as created by `numpy.save` and `numpy.savez`.
The datasets in the `zip`-file must be named according to the regular expression
`{dataset_name}(_TRAIN|_TEST)?.(npy|npz)`. That is, the dataset name (as
specified when using `load_dataset`) and optionally `_TRAIN` or `_TEST` followed
by the extension `npy` or `npz`. If there are multiple datasets with the same
name but different training or testing tags, they will be merged. As such, if
both `_TRAIN` and `_TEST` files are present for the same name, `load_dataset`
can return these train and test samples separately by setting
`merge_train_test=False`. For example, the `ucr`-bundle provides the default
train/test splits from the UCR time series repository.

```python
from wildboar.datasets import load_dataset
x_train, x_test, y_train, y_test = load_dataset(
    'GunPoint', repository='wildboar/ucr', merge_train_test=False
)
```

```

```
