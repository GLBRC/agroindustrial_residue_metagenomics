# AutoML Leaderboard

| Best model   | name                                                         | model_type     | metric_type   |   metric_value |   train_time |
|:-------------|:-------------------------------------------------------------|:---------------|:--------------|---------------:|-------------:|
|              | [1_Baseline](1_Baseline/README.md)                           | Baseline       | logloss       |     1.37455    |         0.62 |
|              | [2_DecisionTree](2_DecisionTree/README.md)                   | Decision Tree  | logloss       |     0.0888997  |        19.9  |
|              | [3_Linear](3_Linear/README.md)                               | Linear         | logloss       |     0.0663769  |         7.91 |
| **the best** | [4_Default_LightGBM](4_Default_LightGBM/README.md)           | LightGBM       | logloss       |     0.00121498 |        10.29 |
|              | [5_Default_Xgboost](5_Default_Xgboost/README.md)             | Xgboost        | logloss       |     0.0515309  |         9.92 |
|              | [6_Default_CatBoost](6_Default_CatBoost/README.md)           | CatBoost       | logloss       |     0.00224122 |        26.92 |
|              | [7_Default_NeuralNetwork](7_Default_NeuralNetwork/README.md) | Neural Network | logloss       |     0.166366   |         1.92 |
|              | [8_Default_RandomForest](8_Default_RandomForest/README.md)   | Random Forest  | logloss       |     0.70066    |        10.56 |
|              | [9_Default_ExtraTrees](9_Default_ExtraTrees/README.md)       | Extra Trees    | logloss       |     0.31948    |        15.97 |
|              | [Ensemble](Ensemble/README.md)                               | Ensemble       | logloss       |     0.00121498 |         0.3  |

### AutoML Performance
![AutoML Performance](ldb_performance.png)

### AutoML Performance Boxplot
![AutoML Performance Boxplot](ldb_performance_boxplot.png)

### Features Importance
![features importance across models](features_heatmap.png)



### Spearman Correlation of Models
![models spearman correlation](correlation_heatmap.png)

