"""
Module containing custom transformers for data preprocessing.

Includes transformers for dropping specified features, filling missing values,
extracting deck from cabin, extracting titles from names, transforming
family-related features, standardizing numerical features, and creating dummy
variables for categorical features.

#### Classes:
- DropperTransformer:
    Transformer to drop specified features from the dataset.
- FillerNA:
    Transformer to fill missing values in categorical and numerical features.
- DeckExtractor:
    Transformer to extract deck information from the 'Cabin' feature.
- TitleExtractor:
    Transformer to extract titles from the 'Name' feature.
- FamilyTransformer:
    Transformer to compute family size and whether a passenger is alone.
- StandardizeTransformer:
    Transformer to standardize numerical features.
- DummiesTransformer:
    Transformer to create dummy variables for categorical features.

#### Functions:
- prepare_dataset: Returns the dataset after the sample piplene composed of the
    transformers in the module

"""

from typing import Self, Optional
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd


class DropperTransformer(BaseEstimator, TransformerMixin):
    """
    Drops specified features from the dataset.

    By default, they are the following: ['Name', 'Ticket', 'Cabin', 'Sex',
    'Embarked', 'Title', 'SibSp', 'Parch']

    #### Parameters:
    - features: list of str
        Those define which columns are dropped by the transformer.
        If the value is None, then the default values are used.
    """

    def __init__(self, features: list[str] = None):
        self.features = [
            'Name',
            'Ticket',
            'Cabin',
            'Sex',
            'Embarked',
            'Title',
            'SibSp',
            'Parch',
        ]

    def fit(self, data) -> Self:
        """
        Does practically nothing. Created to support sklearn API.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns referene on `self`.
        """
        return self

    def transform(self, data) -> Self:
        """
        Drops the columns of the data.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns table with droped columns.
        """
        return data.drop(self.features, axis=1)


class FillerNA(BaseEstimator, TransformerMixin):
    """
    Fills NA values in the dataset with the specified function.
    Categorical and numerical features are treated differently.

    #### Parameters:
    - categorical_features: list of str
        This parameter describes categorical features that are going to be
        processed
    - categorical_function:
        If the value of this is equal to 'mode', then the mode is found
        and assigned to the NA fields. Equals to 'mode' by default
    - numerical_features: list of str
        This parameter describes numerical features that are going to be
        processed
    - numerical_function:
        If the value of this is equal to 'mean' or 'median', then the
        respective statitic is calculated and assigned to the NA fields
        Equals to 'median' by default
    - categorical_values:
        This values are assigned instead of NA values in the dataset.
        If the valid categorical funtion is passed, then these values
        are ignored
    - numerical_values:
        This values are assigned instead of NA values in the dataset.
        If the valid numerical funtion is passed, then these values
        are ignored
    """

    def __init__(
        self,
        categorical_features: list[str] = None,
        categorical_function: Optional[str] = 'mode',
        numerical_features: list[str] = None,
        numerical_function: Optional[str] = 'median',
        categorical_values=None,
        numerical_values=None
    ):
        self.categorical_function = categorical_function
        self.categorical_values = categorical_values

        self.categorical_features = [] if categorical_features is None else \
            categorical_features

        self.numerical_function = numerical_function
        self.numerical_values = numerical_values
        self.numerical_features = [] if numerical_features is None else \
            numerical_features

    def fit(self, data) -> Self:
        """
        Calculates the values that are going to substitute NA values in the
        dataset. If the function is not passed, then the values that were
        passed in the constructor remain the same.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returs reference to `self`.
        """
        if self.categorical_function == 'mode':
            self.categorical_values = []
            for feature in self.categorical_features:
                self.categorical_values.append(data[feature].mode()[0])

        if self.numerical_function == 'mean':
            self.numerical_values = []
            for feature in self.numerical_features:
                self.numerical_values.append(data[feature].mean()[0])
        elif self.numerical_function == 'median':
            self.numerical_values = []
            for feature in self.numerical_features:
                self.numerical_values.append(data[feature].median())

        return self

    def transform(self, data):
        """
        Fills the fields with the values that were calculated during
        the function `fit`

        #### Parameters:
        - data:
            Dataset to process

        #### Retunrns
        Returns table with filled NA fields.
        """
        new_data = data.copy()
        for feature, value in zip(self.categorical_features, self.categorical_values):
            new_data[feature] = new_data[feature].fillna(value)

        for feature, value in zip(self.numerical_features, self.numerical_values):
            new_data[feature] = new_data[feature].fillna(value)

        return new_data


class DeckExtractor(BaseEstimator, TransformerMixin):
    """
    Extracts Deck label of the Titanic from the Cabin feature

    #### Parameters:
    - feature_name: str
        The name of the feature in the source dataset. Equals to "Cabin" by
        default
    - new_feature_name: str
        The new name for the Deck to be stored. Equals to "Deck" by default
    """

    def __init__(
        self,
        feature_name: str = 'Cabin',
        new_feature_name: str = 'Deck'
    ):
        self.feature_name = feature_name
        self.new_feature_name = new_feature_name

    def fit(self, data) -> Self:
        """
        Does practically nothing. Created to support sklearn API.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns reference to `self`.
        """
        return self

    def extract_deck(self, cabin: str) -> str:
        """
        Extracts the Deck label from the string.

        #### Parameters:
        - cabin: str
            The cabin number in string

        #### Returns::
        The Deck label of the Titanic. If the cabin parameter is NA, then
        the default deck is equal to "U".

        """
        if pd.isna(cabin):
            return 'U'

        return cabin[0]

    def transform(self, data):
        """
        Performs the extraction of the Deck label from the Cabin feature
        and stores it in the new column named `self.new_feature_name`.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns the data with a new column of the Deck label.
        """
        new_data = data.copy()
        new_data[self.new_feature_name] = \
            data[self.feature_name].apply(self.extract_deck)

        return new_data


class TitleExtractor(BaseEstimator, TransformerMixin):
    """
    Extracts Title of a person from the Name feature.

    #### Parameters:
    - feature_name: str
        The name of the feature that denotes name of the person.
        Equals to 'Name' by default
    - new_feature_name: str
        The name of the feature that is going to be created to store Title
    - rare_label: str
        The label that is going to be assigned in case whether the source
        title is less frequent that the indicated `threshold`
    - threshold: int | float
        - The minimum threshold for a title to not be considered as rare.
    """

    def __init__(
        self,
        feature_name: str = 'Name',
        new_feature_name: str = 'Title',
        rare_label: str = 'Rare',
        threshold: int | float = 8
    ):
        self.threshold = threshold
        self.rare_label = rare_label

    def transform_if_rare(self, title: str, counts):
        """
        The method that identifies whether the title is rare.

        #### Parameters:
        - title: str
            The title of a person
        - counts:
            Value counts of all the titles in the dataset

        #### Returns:
        Returs the passed title if it is not rare, otherwise it substitutes
        with the rare value defined in the constructor.
        """
        if counts[title] < self.threshold:
            return self.rare_label

        return title

    def fill_rare(self, titles):
        """
        Fills the rare titles with the rare label defined in the constructor.

        #### Parameters:
        - titles:
            A collection of titles extracted from Name feature.

        #### Returns:
        Returns the titles with subsituted rare titles. The value for
        substitution is defined in the constructor.
        """
        counts = titles.value_counts()
        titles = titles.apply(lambda x: self.transform_if_rare(x, counts))
        return titles

    def extract_title(self, name) -> str:
        """
        Extracts the title from the Name feature.

        #### Parameters:
        - name: str
            The name of the passenger in the Titanic

        #### Returns:
        Returns title of a passenger.
        """
        return name.split(', ')[1].split('.')[0]

    def fit(self, data) -> Self:
        """
        Does practically nothing. Created to support sklearn API.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns reference to `self`.
        """
        return self

    def transform(self, data):
        """
        Performs the extraction of the title from the Name feature.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns the dataset with Title feature extracted.

        """
        new_data = data.copy()
        titles = data['Name'].apply(self.extract_title)
        titles = self.fill_rare(titles)

        new_data['Title'] = titles
        return new_data


class FamilyTransformer(BaseEstimator, TransformerMixin):
    """
    Transforms the Titanic dataset and extracts family info about the
    passenger. That is, the number of people traveling with a person is
    calculated and the solitude feature is also extracted.

    #### Parameters:
    - sibsp_feature_name: str
        The name of the feature in a source dataset that denotes the number
        of siblings and spouses. Equals to "SibSp" by default
    - parch_feature_name: str
        The name of the feature in a source dataset that denotes the number
        of parents and children. Equals to "Parch" by default
    - new_alone_feature_name: str
        The name of the feature that is going to be created where True means
        that the passenger travels alone. Equals to "Alone" by default
    - new_familysize_feature_name: str
        The name of the feature that is going to be created to store
        the number of family members traveling together. Equals "FamilySize"
        by default
    """

    def __init__(
        self,
        sibsp_feature_name: str = 'SibSp',
        parch_feature_name: str = 'Parch',
        new_alone_feature_name: str = 'Alone',
        new_familysize_feature_name: str = 'FamilySize'
    ):
        self.sibsp_feature_name = sibsp_feature_name
        self.parch_feature_name = parch_feature_name
        self.new_alone_feature_name = new_alone_feature_name
        self.new_familysize_feature_name = new_familysize_feature_name

    def fit(self, data) -> Self:
        """
        Does practically nothing. Created to support sklearn API.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns
        Returns the reference to `self`.
        """
        return self

    def transform(self, data):
        """
        Performs the extraction of family features.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns processed dataset with Alone and FamilySize feature.
        """
        new_data = data.copy()
        family_size = data[self.sibsp_feature_name] + \
            data[self.parch_feature_name]

        new_data[self.new_familysize_feature_name] = family_size
        new_data[self.new_alone_feature_name] = \
            family_size.apply(lambda x: True if x == 0 else False)

        return new_data


class StandardizeTransformer(BaseEstimator, TransformerMixin):
    """
    Standardizes specified features as a TransformerMixin. Uses StandardScaler
    from sklearn library under the hood.

    #### Parameters:
    - features: list of str
        Features that are going to be standardized. If the parameter
        is not specified, then ['Age', 'Fare'] is a default value
    """
    def __init__(self, features: list[str] = None):
        self.features = ['Age', 'Fare'] if features is None else features
        self.scaler = StandardScaler()

    def fit(self, data) -> Self:
        """
        Fits data into the StandardScaler.

        #### Parameters;
        - data:
            Dataset to process

        #### Returns:
        Returns the reference to `self`.
        """
        self.scaler = self.scaler.fit(data[self.features])

        return self

    def transform(self, data):
        """
        Standardizes features that were indicated in the constructor.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns the processed data with standardized features.
        """
        new_data = data.copy()
        new_values = self.scaler.transform(data[self.features])

        for feature, values in zip(self.features, new_values.T):
            new_data[feature] = values

        return new_data


class DummiesTransformer(BaseEstimator, TransformerMixin):
    """
    Creates one-hot encoding of specified features and adds to the dataset.

    #### Parameters;
    - features: list of str
        Features that are going to be encoded. If this parameter is not passed,
        then the default features are: ["Embarked", "Title", "Sex"]
    """

    def __init__(self, features: list[str] = None):
        self.features = ['Embarked', 'Title', 'Sex']
        if features is not None:
            self.features = features

    def fit(self, data) -> Self:
        """
        Does practically nothing. Created to support sklearn API.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns the reference to `self`.
        """
        return self

    def transform(self, data):
        """
        Concatenates the dataset with created one-hot encodings.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns the processed dataset with additional one-hot encodings
        """
        return pd.concat([data, pd.get_dummies(data[self.features])], axis=1)


class OrdinalTransformer(BaseEstimator, TransformerMixin):
    """
    Transforms categorical value into ordinal by sorting and enumerating
    values.

    #### Parameters
    - features: list of str
        The names of the features that are going to be ordinalized. Equals
        to ['Deck'] by default
    """

    def __init__(self, features: list[str] = None):
        self.features = ['Deck']
        if features is not None:
            self.features = features

    def fit(self, data) -> Self:
        """
        Does practically nothing. Created to support sklearn API.

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Returns the reference to `self`.
        """
        return self

    def transform(self, data):
        """
        Performs ordinalization of the features indicated in the construcotor

        #### Parameters:
        - data:
            Dataset to process

        #### Returns:
        Processed dataset with the features changed from categorical to ordinal
        type.
        """
        new_data = data.copy()

        for feature in self.features:
            sorted_uniques = sorted(list(new_data[feature].unique()))
            mapping = {value: i for i, value in enumerate(sorted_uniques)}
            new_data[feature] = new_data[feature].apply(lambda x: mapping[x])

        return new_data


def prepare_dataset(data):
    """
    Processes dataset with a sample pipeline constructed from the transformers
    created in this module.

    #### Parameters:
    - data:
        Dataset to process

    #### Returns:
    Returns processed dataset.
    """
    return Pipeline([
        ('Deck', DeckExtractor()),
        ('Filling na', FillerNA(categorical_features=['Embarked'], numerical_features=['Age'])),
        ('Standardization', StandardizeTransformer()),
        ('Family', FamilyTransformer()),
        ('Title', TitleExtractor()),
        ('Dummy', DummiesTransformer()),
        ('Ordinal', OrdinalTransformer()),
        ('Dropper', DropperTransformer())
    ]).fit_transform(data)
