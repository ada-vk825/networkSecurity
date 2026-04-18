from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    '''Data Ingestion Artifact is the artifact that is generated after the data ingestion process is completed
    Args: train_file_path: str: The file path of the training file
          test_file_path: str: The file path of the testing file
    '''
    train_file_path: str
    test_file_path: str

