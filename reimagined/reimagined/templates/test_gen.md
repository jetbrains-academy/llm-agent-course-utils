## INSTRUCTIONS

You're a professional tester and an experienced Python developer.
You've been asked to write tests for all classes in a given file.
Below, you'll find an example how to write good tests for a class.

**Requirements:**
* Use typings for all the functions
* When importing a class from a file, use relative imports and tasks directory (e.g. `from ..tasks.f02_tokenization import Tokenizer`)
* Use pytest, pytest-mock and their fixtures
* Take your time and think thoroughly about the tests
* Make sure your test PASS over the provided code


### Structure of tasks directory

```bash
tasks/
    └── f01_data_first_look.py
    └── f02_tokenization.py
    └── f03_glove_embeddings.py
    └── f04_embedding_visualization.py
    └── f05_clf_knn_baseline.py
    └── f06_word_counts.py
    └── f07_clf_naive_bayes.py
    └── f08_clf_logreg_with_word_counts.py
    └── f09_clf_logreg_with_embs.py
```


## EXAMPLE

Input:
```python
class GloVeEmbeddings:
    """Class to load and work with GloVe embeddings."""
    
    def __init__(self, model_name: str = 'glove-twitter-25') -> None:
        """Initialize the class and load the GloVe model."""
        self.model = api.load(model_name)
        self._unknown_emb = np.zeros(self.model.vector_size)

    def get_word_vectors(self, words: list):
        """Get the vector representations for a list of words.
        
        Note: In case a word is not in the vocabulary, return a zero vector."""
        return np.array([self.model.get_vector(word) if word in self.model else self._unknown_emb for word in words])
    
    def get_phrase_embedding(self, phrase: str) -> np.ndarray:
        """
        Convert phrase to a vector by aggregating word embeddings.
        - Lowercase the phrase
        - Tokenize the phrase
        - Average the word vectors for all words in the tokenized phrase
        - Skip words not in the model's vocabulary
        - If all words are missing from the vocabulary, return zeros
        """
        phrase_tok = Tokenizer().tokenize(phrase)
        phrase_vectors = [self.model.get_vector(word) for word in phrase_tok if word in self.model]
        
        if len(phrase_vectors) == 0:
            return np.zeros(self.model.vector_size)

        return np.mean(phrase_vectors, axis=0)

    def compute_phrase_vectors(self, phrases: list[str], max_tokens: int | None = 30) -> np.ndarray:
        """Truncate and compute vectors for a list of phrases.
        
        Args:
            phrases (list[str]): List of phrases to compute embeddings for.
            max_tokens (int): Maximum number of tokens to consider in each phrase. (If None, consider all tokens)
        """
        if max_tokens is not None:
            phrases = [" ".join(phrase.split()[:max_tokens]) for phrase in phrases]
        return np.array([self.get_phrase_embedding(phrase) for phrase in phrases])
```


Output:

YOUR REASONING HERE

```python
import pytest
import pytest_mock
import numpy as np
import gensim.downloader as api
from gensim.models import KeyedVectors
from typing import List

from ..tasks.f03_glove_embeddings import GloVeEmbeddings
from ..tasks.f02_tokenization import Tokenizer

VOCAB = {{
    "hello": np.full(5, 2),
    "world": np.full(5, 4),
    "<UNK>": np.zeros(5)
}}

@pytest.fixture
def mock_glove_model(mocker: pytest_mock.MockFixture) -> KeyedVectors:
    """Creates a dummy GloVe model using gensim KeyedVectors and mocks the model loading."""
    dummy_model = KeyedVectors(vector_size=5)
    
    words = list(VOCAB.keys())
    embs = list(VOCAB.values())
    dummy_model.add_vectors(words, embs)
    
    mocker.patch.object(api, 'load', return_value=dummy_model) # now api.load will return dummy_model
    return dummy_model

@pytest.fixture
def glove_embeddings() -> GloVeEmbeddings:
    return GloVeEmbeddings(model_name='mock-glove')


@pytest.mark.parametrize(
    "words, expected_vectors",
    [
        (["hello", "world"], [VOCAB["hello"], VOCAB["world"]]),
        ([], []),
        (["unknown"], [VOCAB["<UNK>"]])
    ],
    ids=["common_words", "empty_list", "unknown_word"]
)
def test_get_word_vectors(mock_glove_model: KeyedVectors, glove_embeddings: GloVeEmbeddings, words: List[str], expected_vectors: List[np.ndarray]) -> None:
    vectors = glove_embeddings.get_word_vectors(words)
    
    assert len(vectors) == len(expected_vectors)
    for vec, exp_vec in zip(vectors, expected_vectors):
        assert np.array_equal(vec, exp_vec)


@pytest.mark.parametrize(
    "phrase, tokenized, expected_embedding",
    [
        (
            "Hello world",
            ["hello", "world"],
            np.full(5, 3)
        ),
        (
            "unknown world",
            ["unknown", "world"],
            np.full(5, 4)
        ),
        (
            "unknown token",
            ["unknown", "token"],
            np.zeros(VOCAB["hello"].shape)
        ),
    ],
    ids=["all_known", "mixed_known_unknown", "all_unknown"]
)
def test_get_phrase_embedding_is_correct_and_uses_tokenizer(
                                mock_glove_model: KeyedVectors,
                                glove_embeddings: GloVeEmbeddings, mocker: pytest_mock.MockFixture,
                                phrase: str, tokenized: List[str], expected_embedding: np.ndarray
                            ) -> None:
    mock_tokenizer = mocker.patch.object(Tokenizer, 'tokenize', return_value=tokenized)
    embedding = glove_embeddings.get_phrase_embedding(phrase)

    assert mock_tokenizer.called_once_with(phrase)  # tokenizer is used
    assert np.array_equal(embedding, expected_embedding)

def test_compute_phrase_vectors(mock_glove_model: KeyedVectors, glove_embeddings: GloVeEmbeddings, 
                                mocker: pytest_mock.MockFixture) -> None:
    mock_get_phrase_embedding = mocker.patch.object(GloVeEmbeddings, 'get_phrase_embedding')
    phrases = ["Hello world", "Another example", "Testing phrase"]
    mock_get_phrase_embedding.side_effect = [
        np.array([1.0, 1.0, 1.0]),
        np.array([2.0, 2.0, 2.0]),
        np.array([3.0, 3.0, 3.0])
    ]
    
    result = glove_embeddings.compute_phrase_vectors(phrases, max_tokens=None)
    
    assert len(result) == len(phrases), "Number of embeddings should match the number of phrases"
    assert all(np.array_equal(res, np.full(3, i+1)) for i, res in enumerate(result))
    assert mock_get_phrase_embedding.call_count == len(phrases), "Expected get_phrase_embedding to be called for each phrase"
```

### Another example of good tests

Sometimes, it's enough to do simple tests to cover the functionality of the class.

Input:
```python
class EmbeddingReducer:
    """Class to reduce word embeddings using t-SNE."""
    def reduce(self, word_vectors: np.ndarray) -> np.ndarray:
        """Performs dimensionality reduction using t-SNE and visualizes the word vectors."""
        # Apply t-SNE to reduce dimensions to 2
        word_tsne = TSNE(n_components=2).fit_transform(word_vectors)
        word_tsne = (word_tsne - word_tsne.mean(axis=0)) / word_tsne.std(axis=0)
        return word_tsne
```

Output:
```python
import pytest
import numpy as np

from ..tasks.f04_embedding_visualization import EmbeddingReducer


@pytest.fixture
def embedding_reducer() -> EmbeddingReducer:
    """Fixture for creating an instance of EmbeddingReducer."""
    return EmbeddingReducer()

@pytest.fixture
def sample_data() -> np.ndarray:
    """Create a sample data consisting of 3 clusters."""
    emb_size = 50
    cluster1 = np.random.normal(loc=np.full(emb_size, -2), scale=0.5, size=(30, emb_size))
    cluster2 = np.random.normal(loc=np.full(emb_size, 0), scale=0.5, size=(20, emb_size))
    cluster3 = np.random.normal(loc=np.full(emb_size, 2), scale=0.5, size=(10, emb_size))
    return np.vstack([cluster1, cluster2, cluster3])

def test_reduce_output_shape_and_normalization(embedding_reducer: EmbeddingReducer, sample_data: np.ndarray) -> None:
    """Test the reduce method of EmbeddingReducer."""
    reduced_vectors = embedding_reducer.reduce(sample_data)
    
    assert reduced_vectors.shape == (len(sample_data), 2), "The reduced vectors should have 2 dimensions"
    
    assert np.allclose(reduced_vectors.mean(axis=0), 0.0, atol=1e-6), "Reduced vectors should be centered around 0"
    assert np.allclose(reduced_vectors.std(axis=0), 1.0, atol=1e-6), "Reduced vectors should have a standard deviation of 1"
```


### Your task

Input:
```python
{code}
```

Output:

