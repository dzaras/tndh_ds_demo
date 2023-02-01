# NLP Model
### Preprocessing Pipeline

The preprocessing pipeline converts autopsy PDFs to preprocessed narrative text.

The pipeline is run from 1_run_preprocessing_pipeline.ipynb, which performs three tasks:

Converts autopsy PDFs to text (autopsy_to_text.ipynb)
Extracts narrative text (extract_narratives.ipynb)
Preprocesses text (preprocess_narratives.ipynb)
Requires installation of scispacy model "en_core_sci_sm" as follows:

pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_core_sci_sm-0.5.0.tar.gz

### Train

The training scripts structure the preprocessed narratives for Bag-of-Words models, tune hyperparameters using cross validation, and evaluate model discrimination and calibration using bootstrapped samples. The models achieving the median discrimination are saved and used for calculating SHAP values.

There are two main scripts to run:

/train/2_hyperparameter_tuning_cv.ipynb

Determines optimized hyperparameters for SVM, random forest, and gradient boosted trees classifiers
/train/3_model_eval_bootstrap.ipynb

Trains tuned logistic regression, SVM, random forest, and gradient boosted trees classifiers on bootstrapped samples
Provides 95% CIs of discrimination and calibration metrics
Saves models achieving median discrimination
Generates SHAP values and plots

### Summary

To train the NLP models, run the following scripts:

1_run_preprocessing_pipeline.ipynb
/train/2_hyperparameter_tuning_cv.ipynb

/train/3_model_eval_bootstrap.ipynb

### Additional Code for Manuscript

/train/calc_spiegelhalter_z.R - generates p-values for model calibration

/train/post_hoc_analysis.ipynb - compares model performance among different subgroups
