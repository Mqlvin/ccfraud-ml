This document overviews the features of the webapp written in Python with Flask.

### `/api`
The API takes 4 headers:
 - `amount`: The amount spent in the transaction.
 - `category`: The category of the transaction, e.g. `misc_net`, `healthcare_fitness`.
 - `dob`: The date of birth of the card holder, in format YYYY-mm-dd.
 - `gender`: The gender of the card holder, either `M` or `F`.

If you are missing headers, the response will be similar to:
```json
{"success": "false", "data": {"Missing headers": ["amount"]}}
```
Where the missing headers will be expressed.

If all headers are provided, but any of the headers are of an invalid format, for example the DoB contains letter, it will return an invalid format error, like:
```json
{"success": "true", "data": "Invalid format"}
```

If all headers are provided and they are of the correct format, fraud or not will be calculated and return like:
```json
{"success": "true", "data": {"is_fraud": "true"}}
```






### `/steps/<type>`
The `/steps` endpoint shows an SVG of the decision tree's steps, based on the training of the tree.
The steps endpoint has an additional argument, `<type>`.

The two available types are:
 - `limited` - This shows the decision tree of the feature selected model, with a max depth of 9 nodes.
 - `unlimited` - This shows the decision tree of the feature selected model, with no max depth.
 - `very-unlimited` - This shows the decision tree of the non-feature selected model, with no max depth, note this is quite a large file.





### `/graph`
The `/graph` endpoint is an endpoint complete with a GUI, and presents you a graph of increasing amount of money, and whether that is classified as fraud.

The graph plots two lines - for both male and female, as they're a binary value within our features.
The form has two entry boxes and takes inputs in the same format as the API.
Amount is not required as it is generated, between `£0` and `£2000`.