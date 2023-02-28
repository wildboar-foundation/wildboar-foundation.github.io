# Datasets

`````{warning}
The {mod}`~wildboar.datasets` module requires the package
[requests](https://pypi.org/projects/requests). We can install it using `pip`
or `conda`:

````{tab} pip
```shell
$ pip install requests
```
````

````{tab} conda
```shell
$ conda install requests
```
````

`````

Wildboar is distributed with an advanced system for handling dataset
repositories. A dataset repository can be used to load benchmark datasets or to
distribute or store datasets, in it simplest for we can use
{func}`~wildboar.datasets.load_dataset`:

```python
from wildboar.datasets import load_dataset
x, y = load_dataset('GunPoint', repository='wildboar/ucr')
```

```{toctree}
:maxdepth: 2
:hidden:

datasets/repositories
datasets/preprocess
```
