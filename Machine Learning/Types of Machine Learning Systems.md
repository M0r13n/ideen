# Types of Machine Learning

## Supervised Learning

- learning based on labelled training data
- good for **classification** (Spam, hand written letters, speech)
- good for **predictions** based on *predictors* => Regression
- Examples:
  - k-Nearest-Neighbours
  - Linear Regression
  - Logistic Regression

## Unsupervised Learning

- learning based on unlabelled training data
- good for **clustering**: group visitors based on similar attributes
- good for **visualisation**: visualise complex data in 2D or 3D 
- good for **dimensionality reduction**: simplify data without loosing much information
  - it can be a good idea to reduce the dimensionality of training data **before feeding it into another algorithm** (e.g. Supervised Learning) in order to improve performance and efficiency
- good for **anomaly detection**: detect outliers
- good for **association rule learning**: discover relations between attributes

## Semisupervised Learning

- learning based on partially labelled data
- Google Photos combines a clustering algorithm (unsupervised) to detect similar faces on photos. The user then has to label a single photo for the algorithm to find any photo of than person.

## Reinforcement Learning

- an ***agent*** learns by itself based on ***rewards*** or **penalties**
- learns a **policy** (best strategy)
- examples:
  - Go
  - Self driving cars
  - Walking robots

## Batch Learning

- training on a large set of data
- for new data the training data has to be updated
- the model needs to be trained from scratch for each update
- GPT is an example

## Online Learning

- system updates itself continuously while new data arrives
- **learning rate** defines how *fast* the system adapts to new training data
  - high: rapid adaption of new data and high dementia
  - low: learn slower but remember more

## Instance-based Learning

- learn examples by heart
- generalise new cases using a **similarity measure**
- *GPT uses instance-based learning to predict the next word in a sequence based on the context provided be the preceding words*

## Model-based Learning

- build a model from the data
- make predictions based on that model
- examples:
  - linear model (linear function from college)
    - Life satisfaction based in GDP per capita
    - $lf=\theta_0 + \theta_1 \times GDP_{per\_capita}$
    - $\theta_0$ and $\theta_1$ are two model parameters
    - an model-based algorithm then learns the best values for these parameters
    - performance measure by **fitness function** or **cost function**
  - decision tree to decide whether a person will play tennis based on weather
    - developer defines the conditions
    - system learns the structure of the decision tree
- Typical learning process:
  1. collect the data
  2. select a model
  3. train the model on the training data (minimise cost function)
  4. use the model to make predictions