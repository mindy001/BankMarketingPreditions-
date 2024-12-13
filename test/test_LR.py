import pytest
import pandas as pd
import os
from unittest.mock import patch, MagicMock, mock_open
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import Pipeline
import pickle
import shutil
from model_LR import (load_and_clean_data, prepare_features_and_target,
                         create_column_transformer, create_pipeline,
                         evaluate_model, plot_confusion_matrix, save_model)

def test_load_and_clean_data():
    """Test the load_and_clean_data function."""
    # Mock data creation
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(1, 6)])
    data['y'] = y
    
    # Write to a mock CSV file
    file_path = 'sample_data.csv'
    data.to_csv(file_path, index=False)
    
    # Test load_and_clean_data function
    cleaned_data = load_and_clean_data(file_path)
    assert isinstance(cleaned_data, pd.DataFrame)
    assert 'y' in cleaned_data.columns  

    os.remove(file_path)  # Clean up after the test
    
    with pytest.raises(FileNotFoundError):
        load_and_clean_data("non_existent_file.csv")


def test_prepare_features_and_target():
    """Test the prepare_features_and_target function."""
    # Create mock data
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(1, 6)])
    data['y'] = y

    X_prepared, y_prepared = prepare_features_and_target(data)
    
    assert X_prepared.shape[0] == data.shape[0]  
    assert y_prepared.shape[0] == data.shape[0]  
    assert 'y' not in X_prepared.columns 


def test_create_column_transformer():
    """Test the create_column_transformer function."""
    ct = create_column_transformer()
    assert isinstance(ct, make_column_transformer)
    assert len(ct.transformers) == 2  


def test_create_pipeline():
    """Test the create_pipeline function."""
    ct = create_column_transformer()
    pipeline = create_pipeline(ct)
    assert isinstance(pipeline, Pipeline)
    assert 'preprocessor' in pipeline.named_steps  
    assert 'classifier' in pipeline.named_steps  


def test_evaluate_model():
    """Test the evaluate_model function."""
    y_true = [1, 0, 1, 1, 0]
    y_pred = [1, 0, 1, 0, 0]

    with patch('builtins.print') as mock_print:
        accuracy, precision, recall, f1 = evaluate_model(y_true, y_pred)
        
        assert accuracy == 0.8
        assert precision == 1.0
        assert recall == 0.6666666666666666
        assert f1 == 0.8
        
        mock_print.assert_any_call(f"Accuracy: 0.80")
        mock_print.assert_any_call(f"Precision: 1.00")
        mock_print.assert_any_call(f"Recall: 0.67")
        mock_print.assert_any_call(f"F1 Score: 0.80")


def test_plot_confusion_matrix():
    """Test the plot_confusion_matrix function."""
    y_true = [1, 0, 1, 1, 0]
    y_pred = [1, 0, 1, 0, 0]
    conf_matrix = confusion_matrix(y_true, y_pred)
    
    with patch('altair.Chart.save') as mock_save:
        plot_confusion_matrix(conf_matrix, "mock_output.html")
        mock_save.assert_called_once()  


def test_save_model():
    """Test the save_model function."""
    # Create a dummy model
    model = LogisticRegression(solver='liblinear')
    model.fit([[1, 2, 3]], [1]) 
    
    model_output_path = 'model.pkl'
    
    with patch('builtins.open', mock_open()) as mock_file:
        save_model(model, model_output_path)
        mock_file.assert_called_once_with(model_output_path, 'wb')
        assert os.path.exists(model_output_path) 


@patch('your_script.train_model') 
def test_train_model(mock_train_model):
    """Test the whole training flow."""
    # Prepare mock data
    X, y = make_classification(n_samples=100, n_features=5, random_state=42)
    data = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(1, 6)])
    data['y'] = y
    
   
    mock_csv_file = 'sample_data.csv'
    data.to_csv(mock_csv_file, index=False)
    
    model_output_path = 'model.pkl'
    confusion_matrix_output = 'confusion_matrix.html'


    mock_train_model(input_path=mock_csv_file,
                     model_output_path=model_output_path,
                     confusion_matrix_output=confusion_matrix_output)
    
    assert os.path.exists(model_output_path)
    assert os.path.exists(confusion_matrix_output)


    os.remove(mock_csv_file)
    os.remove(model_output_path)
    os.remove(confusion_matrix_output)


