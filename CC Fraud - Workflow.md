### Prerequisites

First, the dataset is downloaded and extracted.
Using `Jupyter Notebooks`, I can load the dataset into an dataframe using `pandas` function `read_csv`
I then loop through the features in the file and see what's available.

`['#', 'trans_date_trans_time', 'cc_num', 'merchant', 'category', 'amt', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip', 'lat', 'long', 'city_pop', 'job', 'dob', 'trans_num', 'unix_time', 'merch_lat', 'merch_long', 'is_fraud']`

These is the 23 headers. To start off, we will attempt to train a decision tree with all parameters.
We correctly identify `is_fraud` as the target classes, so we remove that feature from the dataset, leaving us with 22 features.

I wrap this loading in a function, returning the `DataFrame` loaded by `pandas`, and the feature names for the data and target.



### Handling data formatting

Next, we have to ensure all items are of a number type (e.g. `float` or `integer`).
To do this, we have to transform features of other types to integers. In most cases, this means converting categorical data into a set of unique integers and their category (so each element in a category is given a single unique integer). To do this, we can use a class in `sklearn.preprocessing` called `LabelEncoder`. This class has a `.fit()` method which takes all the values of a feature in the *training* dataset. Now the set of `<unique integers, categories>` have been made, you can use the `.transform()` method to create a new array of integers for a specific category, based on what the `LabelEncoder` has assigned a category, e.g...

The default categorical data is:
`["Farmer", "Baker", "Shopkeeper", "Baker", "Pilot"]`

We use `LabelEncoder` which abstracts a behind-the-scenes set of the categories and unique integers:
```
{
	"Farmer":0,
	"Baker":1,
	"Shopkeeper":2,
	"Pilot":3
}
```

Finally, we reassign the categorical feature in our `DataFrame` into integers assigned by the `LabelEncoder`:
`[0, 1, 2, 1, 3]`

We apply this method to all categorical data. We ensure to keep all the `LabelEncoder` objects stored, as we will need them later to `.inverse_transform()` any integers back into their categories.



We also have to convert dates and timestamps into a numerical format, such as unix. Unfortunately the DoB feature in this dataset was difficult to convert as many dates were before 1970, which is before the epoch and are impossible to express with a positive unix timestamp. Decision trees can handle negative numbers, however due to limitations with the OS (classic Windows) it proved very difficult to make unix timestamps for numbers before 1970, so we just opted to remove the hyphen in the date format (`1930-06-15` > `19300615`). This method worked fine.



### Training

Now, all data is numerical which means it can now be trained by `scikit-learn`'s inbuilt `DecisionTreeClassifier`. Testing is as any other class with `scikit-learn`, simply running a `.fit()` method with a list of features and their targets. This all worked as normal.



### Performance measuring

Now it was time to test the data. Luckily the dataset came with two files - both a training and testing dataset, which was convenient as I didn't have to split it myself, however it did mean it would've been more difficult to do iterative training while preserving the same number of training samples. Anyway, to test the data we load in the test dataset, and use the `DecisionTreeClassifier` objects `.predict()` method, and pass it a list of features from the test dataset. The `.predict()` methods returns it's prediction for every entry in the test dataset, being either true or false (1 or 0) to `is_fraud`. However, this is where problems started to arise.
Essentially, the `LabelEncoder` only classified categorical data it found in the train dataset, however the test dataset had unseen categories on certain features, for example a town `Springville` was present in the test dataset, but not the training dataset. This caused a lot of errors among many features, so we removed all features throwing the error. Luckily, none of the features were very useful, including `first` and `last` name, `city`, `street`, `job` and `trans_num`.

By removing all these problematic features, we have 16 (22 - 6) features left. It worked and we, finally, got performance results on our first trained model. For performance, we record `accuracy`, `precision`, `recall` and `F1` score. We look at `F1` score as it is less bias than the other numbers, and generally more of a overall consensus of the other 3 performance measures.

On our first model, we leave the `DecisionTreeClassifier`'s hyperparameters at default, with a `criterion` of `gini`, the `splitter` as `best` and no `max_depth`. The results aren't great, with an `F1` score of only `62.165%`.

I continue training with various combinations of hyperparameters, changing `criterion`, `splitter` and `max_depth` to try maximize the `F1` performance measure of the model. With each try I add the hyperparameters and performance measures to a spreadsheet, so I can easily view (and graph if needed) the best hyperparameters to use.

Note, these models were being trained with all the available features, and the highest performance recorded was:

|Hyperparameters (all working features)|Accuracy|Precision|Recall|F1|
|---|---|---|---|---|
|criterion:entropy splitter:best max_depth:9|99.781|86.525|84.031|85.233|
|criterion:log_loss splitter:best max_depth:9|99.781|86.525|84.031|85.233|

- `Accuracy` - Accuracy is the amount of times the model predicts the testing dataset correct, however it can be bias due to class imbalance, which I explain in more detail in the consensus (the end).
- `Precision` - Precision is calculated by the model's false positives. A higher precision indicates a lower number of false positives. This is good as it doesn't fail due to class imbalance.
- `Recall` - Recall is calculated by model's chance of avoiding false negatives.
- `F1` - `F1` score is a consensus score based on both precision and recall. The `F1` score ranges between `0` and `1,` `1` being the highest performant model and `0` being the lowest performant value.

This was okay, but we could take further steps to try improve the classification performance of the model.



### Feature selection
We could use feature selection to try refine the tree, disregarding useless factors which may be incorrectly classifying some entries. Feature selection removes data with does not correlate with the target result.

We used "Spearman's Correlation", however if the data is gaussian you could also use "Pearson's Correlation".

To do this, `scipy` has a great in-built function, allowing you to provide both an array of features, and the targets. For each feature, it's values are compared to the target's values to determine whether the data correlates or not. A higher result value from this `spearmanr` method means a better correlation, and the result will also always be between `-1` and `1`. Both `1` and `-1` mean perfect correlation (`-1` just being inverse correlation). We take the absolute or squared value of these features' correlations, and order them from highest to lowest. Then, pick the top most relevant features (5-10 we originally thought) to train the model with - and disregard the rest.

I put the features and their correlations to the targets on a spreadsheet, and these were the following values:

|Correlation (Spearman)|Value|
|---|---|
|amt:is_fraud|0.08792435761|
|category:is_fraud|0.01971369952|
|dob:is_fraud|0.0113201643|
|gender:is_fraud|0.00764153419|
|#:is_fraud|0.004767475533|
|unix_time:is_fraud|0.004767475193|
|trans_date_trans_time:is_fraud|0.004767185918|
|long:is_fraud|0.00320966084|
|merch_long:is_fraud|0.003205265793|

The feature name \# refers to the index of the entry in the dataset, simply a counter, and completely unrelated to the target class.
Because of this, we assumed anything at or below the same correlation value of this was pointless, as the \# feature has no real meaning.
This lead us to make the decision of picking the top 4 features as the relevant features, and we decided to train our model based on those.



### Training with select features
We started a new notebook for training with select features, copying the old notebook. We could keep all the code the same - except change `data_cols` (the feature name array) to only contain our select features. The rest of the code worked alongside whatever was in `data_cols`, so this was the only change needed. We also had to remove some other code with made reference to the features no longer in use, both for loading the training and testing dataset.

Now, the `DecisionTreeClassifier` object could now be trained again, except now with only our select features. I went through a similar testing routine, trying many combinations of the hyperparameters `criterion`, `splitter` and `max_depth`.

Overall, the `F1` was value generally higher on the lowest values, so the range of `F1` across our training with selected features was lower than the range across training with all features. This means the `F1` score was generally more consistent.

The best performing `F1` values with select features had the same hyperparameters as the best performing `F1` values with all features:

|Hyperparameters (select features)|Accuracy|Precision|Recall|F1|
|---|---|---|---|---|
|criterion:entropy splitter:best max_depth:9|99.786|87.333|83.569|85.35|
|criterion:log_loss splitter:best max_depth:9|99.786|87.333|83.569|85.35|

Comparing the performance measures of the select and all features trained models:
- The lowest scoring values had a difference of `~9%`, where selecting specific features helped improve the `F1` score.
- The highest values had a difference of only `~0.117%`, where selecting specific features marginally helped improve the `F1` score.



### Consensus
To help improve model performance:
- Selecting the most relevant features is important, as it stops classification based on irrelevant features.
- It's also important to try many different hyperparameters. For example, limiting tree depth was extremely beneficial as it stopped overfitting, meaning there aren't lots of tiny exceptions for anomalies in the training dataset. If this happens, any testing data which falls into these exceptions will be mis-categorised, hence reducing the performance of the model.

It's also interesting to note that `accuracy` performance of all the models were always above `98.5%`, despite the `F1` ranging around `25%`. This is due to an imbalance of classes in the data, as there were many `is_fraud == 0` and not many `is_fraud == 1`. This meant that if the model theoretically assumed every transaction wasn't fraud, it's accuracy would be equal to `100% - (% of dataset that is fraud)`, and as said before, the percentage of fraud in the dataset is very low, so the accuracy was always very high.
This shows it's better to use something like `F1`, as it's more conclusive of all performance measures and give you a slightly better consensus of the model performance.

Another great takeaway is that we can use the `pickle` library in Python to save and load objects from memory. This means once a classifier is trained, it can be saved to secondary storage and can be reloaded again for later use, meaning you don't need to load the dataset and train the model every time the model is used, and furthermore allows you to distribute the model without needing other users of it to train it themselves locally.

Finally, learning a basic understanding of Jupyter Notebooks is extremely helpful, as it allows you to quickly work and patch together a Python program while keeping everything globally scoped, which in most cases is quite nice and increases productivity massively (as long as the cells aren't always out of sync). It's a great playground for individual code snippets before you compile it all into a final script.
