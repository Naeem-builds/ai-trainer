# OOP Concepts — Mini AI Model Trainer Framework
## Study Guide + Exam Cheat Sheet

---

## 1️⃣ ABSTRACTION (ABC)

**What:** Define an interface; force child classes to implement specific methods.

**Code:**
```python
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def train(self, data):
        pass
    
    @abstractmethod
    def evaluate(self, data):
        pass
```

**Key Points:**
- Cannot create `BaseModel()` directly — it's abstract
- `LinearRegressionModel` and `NeuralNetworkModel` MUST implement `train()` and `evaluate()`
- Forces a contract: "every model must have these methods"

**Exam Answer:** *Abstraction hides implementation details and forces child classes to follow a common interface.*

---

## 2️⃣ INHERITANCE (is-a relationship)

**What:** Child class inherits all attributes/methods from parent class.

**Code:**
```python
class LinearRegressionModel(BaseModel):  # inherits from BaseModel
    def __init__(self, learning_rate=0.01, epochs=10):
        super().__init__(config)  # calls parent's __init__
        # Now has access to self.config from parent
```

**Key Points:**
- `LinearRegressionModel` IS-A `BaseModel`
- `NeuralNetworkModel` IS-A `BaseModel`
- Both inherit `self.config` from parent
- Both use `super()` to call parent's `__init__`

**Exam Answer:** *Inheritance allows a child class to reuse code from a parent class and override specific methods.*

---

## 3️⃣ METHOD OVERRIDING

**What:** Child class provides its own implementation of a parent's method.

**Code:**
```python
# Parent (BaseModel) defines abstract train()
@abstractmethod
def train(self, data):
    pass

# Child 1: LinearRegressionModel overrides it
def train(self, data):
    print(f"LinearRegression: Training on {len(data)} samples...")

# Child 2: NeuralNetworkModel also overrides it (differently)
def train(self, data):
    print(f"NeuralNetwork {self.layers}: Training on {len(data)} samples...")
```

**Key Points:**
- Same method name, different behavior per class
- Called automatically based on object type
- Example: `lr_model.train(data)` vs `nn_model.train(data)` → different outputs

**Exam Answer:** *Method overriding allows a child class to provide a specific implementation of a method defined in the parent class.*

---

## 4️⃣ POLYMORPHISM

**What:** Same interface, different behaviors. One method works with multiple object types.

**Code:**
```python
class Trainer:
    def __init__(self, model: BaseModel, loader: DataLoader):
        self.model = model    # Could be LinearRegressionModel OR NeuralNetworkModel
        self.loader = loader
    
    def run(self):
        data = self.loader.get_data()
        self.model.train(data)      # Calls correct train() based on actual type
        self.model.evaluate(data)   # Calls correct evaluate() based on actual type

# Polymorphism in action:
trainer1 = Trainer(model=lr_model, loader=loader)     # Works with LR
trainer2 = Trainer(model=nn_model, loader=loader)     # Same Trainer, works with NN
trainer1.run()  # Different behavior from trainer2.run() — same method call
```

**Key Points:**
- `Trainer.run()` doesn't know if model is LR or NN
- It doesn't care — just calls `train()` and `evaluate()`
- The correct method is called automatically (polymorphism)

**Exam Answer:** *Polymorphism allows objects of different types to be treated through the same interface, with each object executing the appropriate method.*

---

## 5️⃣ COMPOSITION (has-a, OWNS relationship)

**What:** Parent class OWNS a child object. If parent is deleted, child is deleted too.

**Code:**
```python
class BaseModel(ABC):
    def __init__(self, config: ModelConfig):
        self.config = config  # OWNS a ModelConfig object
        # If BaseModel is deleted, config is also deleted

class LinearRegressionModel(BaseModel):
    def __init__(self, learning_rate=0.01, epochs=10):
        config = ModelConfig("LinearRegression", learning_rate, epochs)
        super().__init__(config)  # Pass config to parent
```

**Key Points:**
- `ModelConfig` is created INSIDE the model
- Tight coupling: model and config are inseparable
- Example: `model.config.learning_rate` — access via dot notation

**Diagram Symbol:** ◆ (solid diamond)

**Exam Answer:** *Composition is a strong "has-a" relationship where the parent owns the child object. If the parent is destroyed, the child is also destroyed.*

---

## 6️⃣ AGGREGATION (uses-a, BORROWS relationship)

**What:** Parent class USES a child object, but child exists independently.

**Code:**
```python
class Trainer:
    def __init__(self, model: BaseModel, loader: DataLoader):
        self.model = model      # USES a model (didn't create it)
        self.loader = loader    # USES a loader (didn't create it)

# Main code:
loader = DataLoader(dataset=[1.2, 3.4, 2.1])  # Created OUTSIDE
trainer = Trainer(model=lr_model, loader=loader)  # Passed IN
# If trainer is deleted, loader still exists!
```

**Key Points:**
- `DataLoader` is created OUTSIDE Trainer
- Loose coupling: Trainer just uses it, doesn't own it
- If Trainer dies, DataLoader survives
- Example: student uses a school library; library exists independently

**Diagram Symbol:** ◇ (empty diamond)

**Exam Answer:** *Aggregation is a weak "has-a" relationship where the parent uses the child object, but the child exists independently and can be used by other objects.*

---

## 7️⃣ CLASS ATTRIBUTES vs INSTANCE ATTRIBUTES

**What:** Class attributes are shared; instance attributes are per-object.

**Code:**
```python
class BaseModel(ABC):
    model_count = 0  # CLASS attribute — ONE copy for ALL objects

    def __init__(self, config: ModelConfig):
        self.config = config  # INSTANCE attribute — each object gets its own

# Usage:
lr_model = LinearRegressionModel()  # model_count = 1
nn_model = NeuralNetworkModel()     # model_count = 2

print(BaseModel.model_count)        # 2 (shared by all)
print(lr_model.config.learning_rate) # 0.01 (unique to lr_model)
print(nn_model.config.learning_rate) # 0.001 (unique to nn_model)
```

**Key Points:**
- Class attribute: `BaseModel.model_count` (access via class name)
- Instance attribute: `self.config` (access via object)
- Incrementing in `__init__` tracks total objects created

**Exam Answer:** *Class attributes are shared across all instances of a class, while instance attributes are unique to each object.*

---

## 8️⃣ MAGIC METHODS (__repr__)

**What:** Control how objects are displayed when printed.

**Code:**
```python
class ModelConfig:
    def __repr__(self):
        return f"[Config] {self.model_name} | lr={self.learning_rate} | epochs={self.epochs}"

# Usage:
config = ModelConfig("LinearRegression", 0.01, 10)
print(config)  # Output: [Config] LinearRegression | lr=0.01 | epochs=10
```

**Key Points:**
- `__repr__()` is called automatically when you `print()` an object
- Makes debugging easier (human-readable output)
- Other magic methods: `__init__()`, `__str__()`, `__eq__()`

**Exam Answer:** *Magic methods are special methods surrounded by underscores that define how objects behave in specific contexts.*

---

## 📊 COMPOSITION vs AGGREGATION (Quick Table)

| Aspect | Composition | Aggregation |
|--------|-------------|-------------|
| **Relationship** | OWNS | USES |
| **Lifetime** | Child dies with parent | Child lives independently |
| **Creation** | Child created INSIDE parent | Child created OUTSIDE, passed in |
| **Coupling** | Tight | Loose |
| **Code Example** | `BaseModel` owns `ModelConfig` | `Trainer` uses `DataLoader` |
| **Symbol** | ◆ (filled) | ◇ (empty) |
| **Real-world analogy** | Car owns engine (integrated) | School uses library (independent) |

---

## 🎯 Class Relationships in Your Project

```
ModelConfig
    ↓ (COMPOSITION: owned by)
BaseModel (ABC)
    ↓ (INHERITANCE: is-a)
    ├─ LinearRegressionModel
    └─ NeuralNetworkModel
            ↓ (AGGREGATION: uses-a)
        Trainer
            ↓ (AGGREGATION: uses-a)
        DataLoader
```

---

## ✅ Exam Tips

1. **For Composition:** "ModelConfig is created inside BaseModel → owned"
2. **For Aggregation:** "DataLoader is created outside, passed into Trainer → independent"
3. **For Polymorphism:** "Trainer.run() works for BOTH LR and NN models without changes"
4. **For Abstraction:** "BaseModel is abstract; you can't do `BaseModel()` directly"
5. **For Inheritance:** "Both child classes inherit `self.config` from parent via `super()`"

---

## 🚀 Running the Code

```bash
# Install (no dependencies needed — only stdlib)
uv init ai-trainer
cd ai-trainer
cp ai_trainer_framework.py .

# Run
uv run ai_trainer_framework.py

# Output:
# [Config] LinearRegression | lr=0.01 | epochs=10
# [Config] NeuralNetwork | lr=0.001 | epochs=20
# Models created: 2
# 
# --- Training LinearRegression ---
# LinearRegression: Training on 5 samples for 10 epochs (lr=0.01)
# LinearRegression: Evaluation MSE = 0.045
# 
# --- Training NeuralNetwork ---
# NeuralNetwork [64, 32, 1]: Training on 5 samples for 20 epochs (lr=0.001)
# NeuralNetwork: Evaluation Accuracy = 91.3%
```

---

## 💡 Key Takeaways

- **Abstraction** = Hide complexity, force interface
- **Inheritance** = Reuse code from parent
- **Polymorphism** = One interface, many implementations
- **Composition** = OWNS child (tight)
- **Aggregation** = USES child (loose)
- **Class attributes** = Shared, instance attributes = unique

Good luck on your exam! 🎯
