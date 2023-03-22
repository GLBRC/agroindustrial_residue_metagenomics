# Summary of Ensemble

[<< Go back](../README.md)


## Ensemble structure
| Model              |   Weight |
|:-------------------|---------:|
| 4_Default_LightGBM |        1 |

### Metric details
|           |   Grp1_ferment_no_MCFA |   Grp2_intermediate_to_MCFA |   Grp3_ferment_to_MCFA |   Grp4_other |   accuracy |   macro avg |   weighted avg |    logloss |
|:----------|-----------------------:|----------------------------:|-----------------------:|-------------:|-----------:|------------:|---------------:|-----------:|
| precision |                      1 |                           1 |                      1 |            1 |          1 |           1 |              1 | 0.00121498 |
| recall    |                      1 |                           1 |                      1 |            1 |          1 |           1 |              1 | 0.00121498 |
| f1-score  |                      1 |                           1 |                      1 |            1 |          1 |           1 |              1 | 0.00121498 |
| support   |                      5 |                           5 |                      5 |            7 |          1 |          22 |             22 | 0.00121498 |


## Confusion matrix
|                                      |   Predicted as Grp1_ferment_no_MCFA |   Predicted as Grp2_intermediate_to_MCFA |   Predicted as Grp3_ferment_to_MCFA |   Predicted as Grp4_other |
|:-------------------------------------|------------------------------------:|-----------------------------------------:|------------------------------------:|--------------------------:|
| Labeled as Grp1_ferment_no_MCFA      |                                   5 |                                        0 |                                   0 |                         0 |
| Labeled as Grp2_intermediate_to_MCFA |                                   0 |                                        5 |                                   0 |                         0 |
| Labeled as Grp3_ferment_to_MCFA      |                                   0 |                                        0 |                                   5 |                         0 |
| Labeled as Grp4_other                |                                   0 |                                        0 |                                   0 |                         7 |

## Learning curves
![Learning curves](learning_curves.png)
## Confusion Matrix

![Confusion Matrix](confusion_matrix.png)


## Normalized Confusion Matrix

![Normalized Confusion Matrix](confusion_matrix_normalized.png)


## ROC Curve

![ROC Curve](roc_curve.png)


## Precision Recall Curve

![Precision Recall Curve](precision_recall_curve.png)



[<< Go back](../README.md)
