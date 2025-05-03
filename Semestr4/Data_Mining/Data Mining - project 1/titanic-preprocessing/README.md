# Titanic Dataset Preprocessing


## About the project
This repository is created for educational purposes. Famous Kaggle competition [Titanic - Machine Learning from Distaster](https://www.kaggle.com/competitions/titanic) was considered, namely, its dataset about passengers. The description of the dataset among with the problem definition can be found on the website.

It is also important to understand that this was also an attempt to present an environment whithin which you can experiment with different features and ways to process them. Of course, in some situation the implementation is strongly coupled with the dataset, however, in this way we employ our knowledge about dataset.

Additionally, the code follows the schema of [Transformer Mixin](https://scikit-learn.org/stable/modules/generated/sklearn.base.TransformerMixin.html) class from `scikit-learn` library to be support the Pipeline API.

## Files
Each file in the repository has it's own purpose.
| File name | Meaning |
| -- | -- |
| [analysis.ipynb](analysis.ipynb)  | Exploratory analysis of the features
| [preprocessing.py](preprocessing.py) | The library itself
| [samples.ipynb](samples.ipynb) | A set of use cases from the library
| [tests.ipynb](tests.ipynb) | The comparison of cross-validation metric with respect to how data was prepared
| [train.csv](train.csv) | The training dataset. If you want to download or to play around with testing data as well, you should visit the following [section](https://www.kaggle.com/competitions/titanic/data) of the competition.
| [improved_dataset.csv](improved_dataset.csv) | The improved dataset

## Getting started

### Prerequisites

The library alone uses only [Pandas](https://pandas.pydata.org/) and [scikit-learn](https://scikit-learn.org/stable/index.html).

As for the date of writing this description, the following command is used to download the dependencies:

- if you are using [conda](https://conda.io/en/latest/):
```sh
conda install pandas scikit-learn
```

- if you are using [pip](https://pypi.org/project/pip/):
```sh
pip install pandas scikit-learn
```

However, you might also want to play around with the analysis. Here are additional packages for data visualization and Jupyter Notebook support:
```sh
# conda
conda install ipykernel matplotlib seaborn
```

```sh
# pip
pip install ipykernel matplotlib seaborn
```

## Installation
If you have all those dependencies described above, the usage is simply "plug and play".

You just have to clone the repository:
```sh
git clone https://github.com/AndrewChmutov/titanic-preprocessing
```

Then, you can use the files within the repository. As for the usage of the library, you just have to copy [preprocessing.py](preprocessing.py) to whatever directory you are interested in and then import in the project using Python language, for example:
```py
import preprocessing
```
or any other appropriate way the language allows.
