# Linear Regression

## Problem Description
> Dataset: Dataset1.txt, Dataset2.txt

In this assignment, you need to implement closed form solution (that contains least square objective function), Gradient Descent algorithm (Batch or Stochastic with enough epochs) for linear regression on heights (X) and weights (Y). Please perform the following tasks:
  - Normalize the datasets so that the values of each feature change between 0 (for min value of the feature) and 1 (for max. value of the feature). Note that this task is very important for the desired results of the upcoming tasks.
  - Train each model separately on the normalized datasets and plot the datasets alongside with the obtained regression model. For these plots, the X axis should be the height feature and the Y axis should be the weight feature.
  - One of these datasets have some outliers(Dataset2). Does it affect the robustness of the model? Explain. (think about effect outlier on regression)
  - Plot J(Ɵ) in terms of Ɵ1 in [-2:2] and Ɵ2 in [-2:2]. (in 2D and 3D figure) (what is Ɵ1 and Ɵ2? Think about line equation. Ɵ1 can be slope and Ɵ2 can be y-intercept and in linear regression you should estimate line parameters)
  - Explain what does the normalization process do? When would it be useful to normalize the data?
  - In your class you learned about sigmoid function. Explain when we use this function in learning and what is the output of that. Plot sigmoid function (binary sigmoid)
