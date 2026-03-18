"""
Mini AI Model Trainer Framework
Demonstrates all core OOP concepts: Abstraction, Inheritance, Polymorphism,
Composition, Aggregation, Class/Instance Attributes, Method Overriding.
"""

from abc import ABC, abstractmethod
import random

# ─────────────────────────────────────────────
# CLASS 1: ModelConfig
# OOP Concept: Instance Attributes, Magic Method (__repr__)
# ─────────────────────────────────────────────
class ModelConfig:
    """Stores settings for a model — used as a COMPOSITION object inside models."""

    def __init__(self, model_name, learning_rate=0.01, epochs=10):
        # INSTANCE ATTRIBUTES — each object gets its own copy
        self.model_name = model_name
        self.learning_rate = learning_rate
        self.epochs = epochs

    def __repr__(self):
        # MAGIC METHOD — controls how the object looks when printed
        return f"[Config] {self.model_name} | lr={self.learning_rate} | epochs={self.epochs}"


# ─────────────────────────────────────────────
# CLASS 2: BaseModel (Abstract Base Class)
# OOP Concept: Abstraction, Class Attribute
# ─────────────────────────────────────────────
class BaseModel(ABC):
    """Abstract base class — defines the interface every model MUST follow."""

    # CLASS ATTRIBUTE — shared across ALL instances, tracks total models created
    model_count = 0

    def __init__(self, config: ModelConfig):
        # COMPOSITION — BaseModel OWNS a ModelConfig object
        # (if the model is deleted, its config is deleted too)
        self.config = config

        # Increment the class attribute every time a model is created
        BaseModel.model_count += 1

    # ABSTRACT METHODS — child classes are FORCED to implement these
    @abstractmethod
    def train(self, data):
        pass

    @abstractmethod
    def evaluate(self, data):
        pass


# ─────────────────────────────────────────────
# CLASS 3: LinearRegressionModel
# OOP Concept: Single Inheritance, Method Overriding, super()
# ─────────────────────────────────────────────
class LinearRegressionModel(BaseModel):
    """Linear Regression model — inherits from BaseModel."""

    def __init__(self, learning_rate=0.01, epochs=10):
        # Create a ModelConfig (COMPOSITION happening here)
        config = ModelConfig("LinearRegression", learning_rate, epochs)

        # super() — calls the parent class (BaseModel) __init__
        # This sets self.config and increments model_count
        super().__init__(config)

    # METHOD OVERRIDING — redefines train() from BaseModel
    def train(self, data):
        print(f"LinearRegression: Training on {len(data)} samples "
              f"for {self.config.epochs} epochs (lr={self.config.learning_rate})")

    # METHOD OVERRIDING — redefines evaluate() from BaseModel
    def evaluate(self, data):
        # Simulate an MSE score (random for demo purposes)
        mse = round(random.uniform(0.01, 0.09), 3)
        print(f"LinearRegression: Evaluation MSE = {mse}")


# ─────────────────────────────────────────────
# CLASS 4: NeuralNetworkModel
# OOP Concept: Single Inheritance, Method Overriding, super(), extra attribute
# ─────────────────────────────────────────────
class NeuralNetworkModel(BaseModel):
    """Neural Network model — inherits from BaseModel, adds a layers attribute."""

    def __init__(self, learning_rate=0.001, epochs=20, layers=None):
        config = ModelConfig("NeuralNetwork", learning_rate, epochs)

        # super() — calls BaseModel.__init__
        super().__init__(config)

        # Extra INSTANCE ATTRIBUTE specific to NeuralNetwork
        self.layers = layers if layers is not None else [64, 32, 1]

    # METHOD OVERRIDING — different training output than LinearRegression
    def train(self, data):
        print(f"NeuralNetwork {self.layers}: Training on {len(data)} samples "
              f"for {self.config.epochs} epochs (lr={self.config.learning_rate})")

    # METHOD OVERRIDING — uses accuracy instead of MSE
    def evaluate(self, data):
        accuracy = round(random.uniform(85.0, 97.0), 1)
        print(f"NeuralNetwork: Evaluation Accuracy = {accuracy}%")


# ─────────────────────────────────────────────
# CLASS 5: DataLoader
# OOP Concept: Independent class (used in Aggregation with Trainer)
# ─────────────────────────────────────────────
class DataLoader:
    """Holds the dataset. Passed INTO Trainer — this is AGGREGATION.
    (DataLoader exists independently; Trainer just uses it.)"""

    def __init__(self, dataset: list):
        # INSTANCE ATTRIBUTE
        self.dataset = dataset

    def get_data(self):
        return self.dataset


# ─────────────────────────────────────────────
# CLASS 6: Trainer
# OOP Concept: Aggregation, Polymorphism
# ─────────────────────────────────────────────
class Trainer:
    """Orchestrates the full pipeline: load data → train → evaluate."""

    def __init__(self, model: BaseModel, loader: DataLoader):
        # AGGREGATION — Trainer receives DataLoader from outside
        # (DataLoader was created externally, Trainer doesn't own it)
        self.model = model
        self.loader = loader

    def run(self):
        """POLYMORPHISM — run() works with ANY model (LR or NN or future models).
        It doesn't care which model it is — just calls train() and evaluate()."""
        data = self.loader.get_data()
        model_name = self.model.config.model_name

        print(f"\n--- Training {model_name} ---")
        self.model.train(data)    # Calls the correct train() based on object type
        self.model.evaluate(data) # Calls the correct evaluate() based on object type


# ─────────────────────────────────────────────
# MAIN — Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":

    # Create two models
    lr_model = LinearRegressionModel(learning_rate=0.01, epochs=10)
    nn_model = NeuralNetworkModel(learning_rate=0.001, epochs=20, layers=[64, 32, 1])

    # __repr__ magic method in action — prints config nicely
    print(lr_model.config)
    print(nn_model.config)

    # CLASS ATTRIBUTE — shared count of all models created
    print(f"Models created: {BaseModel.model_count}")

    # Create DataLoader (exists independently — AGGREGATION)
    loader = DataLoader(dataset=[1.2, 3.4, 2.1, 5.6, 4.3])

    # POLYMORPHISM — same Trainer.run() works for both models
    trainer1 = Trainer(model=lr_model, loader=loader)
    trainer1.run()

    trainer2 = Trainer(model=nn_model, loader=loader)
    trainer2.run()
