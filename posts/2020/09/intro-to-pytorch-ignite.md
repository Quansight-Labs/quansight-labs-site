<!--
.. title: PyTorch-Ignite: training and evaluating neural networks flexibly and transparently
.. slug: pytorch-ignite
.. date: 2020-08-01 09:00:00 UTC-00:00
.. author: Victor Fomin, Sylvain Desroziers
.. tags: Labs, Python, Deep Learning, PyTorch, Machine Learning, Neural Networks, Tutorial
.. category:
.. link:
.. description:
.. type: text
-->

# PyTorch-Ignite: training and evaluating neural networks flexibly and transparently

<div align="center">
<img width=512 src="https://i.ibb.co/WtbmXJQ/ignite-blog.jpg"/>

Victor Fomin (Quansight, FR), Sylvain Desroziers (IFPEN, FR)
</div>

This post is a general introduction of PyTorch-Ignite. It tends to give a brief but illustrative overview of what PyTorch-Ignite can offer for Deep Learning enthusiasts, professionals and researchers. Following the same philosophy as PyTorch, PyTorch-Ignite aims to keep it simple, flexible and extensible but performant and scalable.

Throughout this tutorial, we will introduce the basic concepts of PyTorch-Ignite with the training and evaluation of a MNIST classifier as a beginner application case. We also assume that the reader is familiar with PyTorch.

This tutorial can be also executed in Google Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1gFIPXmUX73HWlLSxFvvYEweQBD_OPx1t)

## Content

- [PyTorch-Ignite: What and Why ?](#pytorch-ignite--what-and-why)
- [Quick-start example](#quick-start-example)
- [Advanced features](#advanced-features)
  * Power of Events & Handlers
  * Out-of-the-box metrics and handlers  
  * Distributed and XLA devices support
- [Projects using PyTorch-Ignite](#projects-using-pytorch-ignite)
- [Project news](#project-news)


# PyTorch-Ignite: What and Why ?

PyTorch-Ignite is a high-level library to help with training and evaluating neural networks in PyTorch flexibly and transparently.

PyTorch-Ignite is designed to be at the crossroads of high-level Plug & Play features and under-the-hood expansion possibilities. PyTorch-Ignite aims to improve deep learning community's technical skills by promoting best practices. 
Things are not hidden behind a divine tool that does everything, but remain within the reach of users. 

PyTorch-Ignite takes a "Do-It-Yourself" approach as research is unpredictable and it is important to capture its requirements without blocking things.


## 🔥 PyTorch + Ignite 🔥

PyTorch-Ignite wraps native PyTorch abstractions such as Modules, Optimizers, and DataLoaders in thin abstractions which allow your models to be separated from their training framework completely. This is achieved by a way of inverting control using an abstraction known as the **Engine**. The **Engine** is responsible for running an arbitrary function - typically a training or evaluation function and emitting events along the way.

Built-in event system represented by **Events** class ensures Engine's flexibility thus facilitates interaction on each step of the run.
With this approach user can completely customize the flow of events during the run. 

In summary, PyTorch-Ignite is
- Extremely simple engine and event system = Training loop abstraction
- Out-of-the-box metrics to easily evaluate models
- Built-in handlers to compose training pipeline, save artifacts and log parameters and metrics

Additional benefits of using PyTorch-Ignite are 
- Less code than pure PyTorch while ensuring maximum control and simplicity
- More factorized code


<table>
<tr>

<th>
Pure PyTorch
</th>

<th>
PyTorch-Ignite
</th>

</tr>
<tr>

<td>

```python
model = Net()
train_loader, val_loader = get_data_loaders(train_batch_size, val_batch_size)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.8)
criterion = torch.nn.NLLLoss()

max_epochs = 10
validate_every = 100
checkpoint_every = 100

def validate(model, val_loader):
    model = model.eval()
    num_correct = 0
    num_examples = 0
    for batch in val_loader:
        input, target = batch
        output = model(input)
        correct = torch.eq(torch.round(output).type(target.type()), target).view(-1)
        num_correct += torch.sum(correct).item()
        num_examples += correct.shape[0]
    return num_correct / num_examples


def checkpoint(model, optimizer, checkpoint_dir):
    filepath = "{}/{}".format(checkpoint_dir, "checkpoint.pt")
    obj = {"model": model.state_dict(), "optimizer":optimizer.state_dict()}
    torch.save(obj, filepath)


iteration = 0

for epoch in range(max_epochs):
    for batch in train_loader:
        model = model.train()
        optimizer.zero_grad()
        input, target = batch
        output = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        if iteration % validate_every == 0:
            binary_accuracy = validate(model, val_loader)
            print("After {} iterations, binary accuracy = {:.2f}"
                  .format(iteration, binary_accuracy))

        if iteration % checkpoint_every == 0:
            checkpoint(model, optimizer, checkpoint_dir)
        iteration += 1
```

</td>

<td>

```python
model = Net()
train_loader, val_loader = get_data_loaders(train_batch_size, val_batch_size)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01, momentum=0.8)
criterion = torch.nn.NLLLoss()

max_epochs = 10
validate_every = 100
checkpoint_every = 100

trainer = create_supervised_trainer(model, optimizer, criterion)
evaluator = create_supervised_evaluator(model, metrics={'accuracy': Accuracy()})

@trainer.on(Events.ITERATION_COMPLETED(every=validate_every))
def validate(trainer):
    evaluator.run(val_loader)
    metrics = evaluator.state.metrics
    print("After {} iterations, binary accuracy = {:.2f}"
          .format(trainer.state.iteration, metrics['accuracy']))


checkpointer = ModelCheckpoint(checkpoint_dir, n_saved=3, create_dir=True)
trainer.add_event_handler(Events.ITERATION_COMPLETED(every=checkpoint_every),
                          checkpointer, {'mymodel': model})

trainer.run(train_loader, max_epochs=max_epochs)























```

</td>

</tr>
</table>



### About the design of PyTorch-Ignite

PyTorch-Ignite allows you to compose your application without being focused on a super multi-purpose object, but rather on weakly coupled components allowing advanced customization.

The design of the library is guided by:
- Anticipating new software or use-cases to come in future without centralizing everything in a single class.
- Avoiding configurations with tons of parameters complicated to manage and maintain.
- Providing tools targeted to maximizing cohesion and minimizing coupling.
- Keeping it simple.


# Quick-start example

In this section we will use PyTorch-Ignite to build and train a classifier of the well-known [MNIST](http://yann.lecun.com/exdb/mnist/) dataset. This simple example will introduce the principal concepts behind PyTorch-Ignite.

For additional information and details about the API, please, refer to the project's [documentation](https://pytorch.org/ignite/).


```python
!pip install pytorch-ignite
```

    Collecting pytorch-ignite    
    Installing collected packages: pytorch-ignite
    Successfully installed pytorch-ignite-0.4.1


## Common PyTorch code

First, we define our model, training and validation datasets, optimizer and loss function:


```python
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import SGD
from torch.utils.data import DataLoader

from torchvision.transforms import Compose, ToTensor, Normalize
from torchvision.datasets import MNIST

# transform to normalize the data
transform = Compose([ToTensor(), Normalize((0.1307,), (0.3081,))])

# Download and load the training data
trainset = MNIST("data", download=True, train=True, transform=transform)
train_loader = DataLoader(trainset, batch_size=128, shuffle=True)

# Download and load the test data
validationset = MNIST("data", train=False, transform=transform)
val_loader = DataLoader(validationset, batch_size=256, shuffle=False)

# Define a class of CNN model (as you want)
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x, dim=-1)

device = "cuda"

# Define a model on move it on CUDA device
model = Net().to(device)

# Define a NLL loss
criterion = nn.NLLLoss()

# Define a SGD optimizer
optimizer = SGD(model.parameters(), lr=0.01, momentum=0.8)
```

The above code is pure PyTorch and is typically user defined and is required for any pipeline.

## Trainer and evaluator's setup

Model's trainer is an engine that loops multiple times over the training dataset and updates model parameters. Let's see how we define such a trainer using PyTorch-Ignite. To do this, PyTorch-Ignite introduces the generic class [`Engine`](https://pytorch.org/ignite/concepts.html#engine) that is an abstraction that loops provided data, executes a processing function and returns a result:


```python
from ignite.engine import Engine

def train_step(engine, batch):
    x, y = batch
    x = x.to(device)
    y = y.to(device)

    model.train()
    y_pred = model(x)
    loss = criterion(y_pred, y)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss

# Define a trainer engine
trainer = Engine(train_step)
```

Only one argument needed to construct the trainer is `train_step` function.

Similarly, model evaluation can be done with an engine that runs a single time over the validation dataset and computes metrics.


```python
def validation_step(engine, batch):
    model.eval()
    with torch.no_grad():
        x, y = batch[0], batch[1]
        x = x.to("cuda")
        y = y.to("cuda")

        y_pred = model(x)

        return y_pred, y

evaluator = Engine(validation_step)
```

This allows the construction of training logic from the simplest to the most complicated scenario. 

The type of output of the process functions (i.e. `loss` or `y_pred, y` in the above examples) is not restricted. These functions can return everything user wants. Output is set to an engine's internal object `engine.state.output` and can be used further for any type of processing.

## Events and Handers

To improve the Engine’s flexibility, a configurable event system is introduced to facilitate the interaction on each step of the run. Namely, Engine allows to add handlers on various [`Events`](https://pytorch.org/ignite/concepts.html#events-and-handlers) that are triggered during the run. When an event is triggered, attached handlers (named functions, lambdas, class functions) are executed. Here is a schema when built-in events are triggered by default: 
```
fire_event(Events.STARTED)
while epoch < max_epochs:
    fire_event(Events.EPOCH_STARTED)
    # run once on data
    for batch in data:
        fire_event(Events.ITERATION_STARTED)

        output = process_function(batch)

        fire_event(Events.ITERATION_COMPLETED)
    fire_event(Events.EPOCH_COMPLETED)
fire_event(Events.COMPLETED)
```

Note that each engine (i.e. `trainer` and `evaluator`) has its own event system which allows to define its own engine's process logic.

Using `Events` and handlers, it is possible to completely customize the engine's runs in a very intuitive way:


```python
from ignite.engine import Events

# Show a message when the training begins
@trainer.on(Events.STARTED)
def start_message():
    print("Start training!")

# Handler can be want you want, here a lambda ! 
trainer.add_event_handler(
    Events.COMPLETED, 
    lambda _: print("Training completed!")
)

# Run evaluator on val_loader every trainer's epoch completed
@trainer.on(Events.EPOCH_COMPLETED)
def run_validation():
    evaluator.run(val_loader)
```

In the code above, `run_validation` function is attached to the `trainer` and will be triggered at each completed epoch to launch model's validation with `evaluator`. This shows that engines can be embedded to create complex pipelines. 

Handlers offer unparalleled flexibility compared to callbacks as they can be any function: e.g. lambda, simple function, class method etc. Thus, we do not require to inherit from an interface and override its abstract methods which could unnecessarily bulk up your code and its complexity.

The possibilities of customization are endless as Pytorch-Ignite allows you to get hold of your application workflow. As mentioned before, there is no magic nor fully automatated things in PyTorch-Ignite.

## Model evaluation metrics

Metrics are another nice example of what the handlers for PyTorch-Ignite are and how to use them. In our example, we use built-in metrics `Accuracy` and `Loss`.


```python
from ignite.metrics import Accuracy, Loss

# Accuracy and loss metrics are defined
val_metrics = {
  "accuracy": Accuracy(),
  "loss": Loss(criterion)
}

# Attach metrics to the evaluator
for name, metric in val_metrics.items():
    metric.attach(evaluator, name)
```

PyTorch-Ignite metrics can be elegantly combined with each other.



```python
from ignite.metrics import Precision, Recall

# Build F1 score
precision = Precision(average=False)
recall = Recall(average=False)
F1 = (precision * recall * 2 / (precision + recall)).mean()

# and attach it to evaluator
F1.attach(evaluator, "f1")
```

To make general things even easier, [helper methods](https://pytorch.org/ignite/engine.html#ignite-engine) are available for the creation of such supervised `Engine` as above. Thus, let's define another evaluator applied to the training dataset in this way.


```python
from ignite.engine import create_supervised_evaluator

# Define another evaluator with default validation function and attach metrics
train_evaluator = create_supervised_evaluator(model, metrics=val_metrics, device="cuda")

# Run train_evaluator on train_loader every trainer's epoch completed
@trainer.on(Events.EPOCH_COMPLETED)
def run_train_validation():
    train_evaluator.run(train_loader)
```

The reason why do we want to have two separate evaluators (`evaluator` and `train_evaluator`) is that they can have different attached handlers and logic to perform. For example, if we would like store the best model defined by the validation metric value, this role is delegated to `evaluator` which computes metrics over validation dataset.

## Common training handlers

From now, we have `trainer` that will call evaluators `evaluator` and `train_evaluator` at every completed epoch. Thus, each evaluator will run and compute corresponding metrics but it would be very helpful to have an adapted display of the results.

Using the customization potential of the engine's system, we can add simple handlers for this logging purposes:


```python
@evaluator.on(Events.COMPLETED)
def log_validation_results():
    metrics = evaluator.state.metrics
    print("Validation Results - Epoch: {}  Avg accuracy: {:.2f} Avg loss: {:.2f} Avg F1: {:.2f}"
          .format(trainer.state.epoch, metrics["accuracy"], metrics["loss"], metrics["f1"]))
    
@train_evaluator.on(Events.COMPLETED)
def log_train_results():
    metrics = train_evaluator.state.metrics
    print("  Training Results - Epoch: {}  Avg accuracy: {:.2f} Avg loss: {:.2f}"
          .format(trainer.state.epoch, metrics["accuracy"], metrics["loss"]))
```

Let's see how to add some others helpful features to our application.

* PyTorch-Ignite provides [`ProgressBar`](https://pytorch.org/ignite/contrib/handlers.html#tqdm-logger) handler to show engine's progression.


```python
from ignite.contrib.handlers import ProgressBar

ProgressBar().attach(trainer, output_transform=lambda x: {'batch loss': x})
```

* [`ModelCheckpoint`](https://pytorch.org/ignite/handlers.html#ignite.handlers.ModelCheckpoint) handler can be used to periodically save objects which have attribute `state_dict`.


```python
from ignite.handlers import ModelCheckpoint, global_step_from_engine

# Score function to select relevant metric, here f1
def score_function(engine):
    return engine.state.metrics["f1"]

# Checkpoint to store n_saved best models wrt score function
model_checkpoint = ModelCheckpoint(
    "quick-start-mnist-output",
    n_saved=2,
    filename_prefix="best",
    score_function=score_function,
    score_name="f1",
    global_step_transform=global_step_from_engine(trainer),
)
  
# Save the model (if relevant) every epoch completed of evaluator
evaluator.add_event_handler(Events.COMPLETED, model_checkpoint, {"model": model});
```

* PyTorch-Ignite provides wrappers to modern tools to track experiments. For example, [`TensorBoardLogger`](https://pytorch.org/ignite/contrib/handlers.html#ignite.contrib.handlers.tensorboard_logger.TensorboardLogger) handler allows to log metric results, model's and optimizer's parameters, gradients etc during the training and validation for TensorBoard.


```python
from ignite.contrib.handlers import TensorboardLogger

# Define a Tensorboard logger
tb_logger = TensorboardLogger(log_dir="quick-start-mnist-output")

# Attach handler to plot trainer's loss every 100 iterations
tb_logger.attach_output_handler(
    trainer,
    event_name=Events.ITERATION_COMPLETED(every=100),
    tag="training",
    output_transform=lambda loss: {"batchloss": loss},
)

# Attach handler to dump evaluator's metrics every epoch completed
for tag, evaluator in [("training", train_evaluator), ("validation", evaluator)]:
    tb_logger.attach_output_handler(
        evaluator,
        event_name=Events.EPOCH_COMPLETED,
        tag=tag,
        metric_names="all",
        global_step_transform=global_step_from_engine(trainer),
    )
```

It is possible to extend the use of the Tensorboard logger very simply by integrating user-defined functions. For example, here is how to display images and predictions during training:


```python
import matplotlib.pyplot as plt

# Store predictions and scores using matplotlib
def predictions_gt_images_handler(engine, logger, *args, **kwargs):
    x, _ = engine.state.batch
    y_pred, y = engine.state.output
    # y_pred is log softmax value
    num_x = num_y = 8
    le = num_x * num_y
    probs, preds = torch.max(torch.exp(y_pred[:le]), dim=1)
    fig = plt.figure(figsize=(20, 20))
    for idx in range(le):
        ax = fig.add_subplot(num_x, num_y, idx + 1, xticks=[], yticks=[])
        ax.imshow(x[idx].squeeze(), cmap="Greys")
        ax.set_title("{0} {1:.1f}% (label: {2})".format(
            preds[idx],
            probs[idx] * 100.0,
            y[idx]),
            color=("green" if preds[idx] == y[idx] else "red")
        )
    logger.writer.add_figure('predictions vs actuals', figure=fig, global_step=trainer.state.epoch)

# Attach custom function to evaluator at first iteration
tb_logger.attach(
    evaluator,
    log_handler=predictions_gt_images_handler,
    event_name=Events.ITERATION_COMPLETED(once=1),
);
```

All that is left to do now is to  run the `trainer` on data `train_loader` for a number of epochs.


```python
trainer.run(train_loader, max_epochs=5)

# Once everything is done, let's close the logger
tb_logger.close()
```

    Start training!
    Validation Results - Epoch: 1  Avg accuracy: 0.94 Avg loss: 0.20 Avg F1: 0.94
      Training Results - Epoch: 1  Avg accuracy: 0.94 Avg loss: 0.21
    Validation Results - Epoch: 2  Avg accuracy: 0.96 Avg loss: 0.12 Avg F1: 0.96
      Training Results - Epoch: 2  Avg accuracy: 0.96 Avg loss: 0.13
    Validation Results - Epoch: 3  Avg accuracy: 0.97 Avg loss: 0.10 Avg F1: 0.97
      Training Results - Epoch: 3  Avg accuracy: 0.97 Avg loss: 0.10
    Validation Results - Epoch: 4  Avg accuracy: 0.98 Avg loss: 0.07 Avg F1: 0.98
      Training Results - Epoch: 4  Avg accuracy: 0.97 Avg loss: 0.09
    Validation Results - Epoch: 5  Avg accuracy: 0.98 Avg loss: 0.07 Avg F1: 0.98
      Training Results - Epoch: 5  Avg accuracy: 0.98 Avg loss: 0.08
    Training completed!


We can inspect results using `tensorboard`. We can observe two tabs "Scalars" and "Images".



```python
%load_ext tensorboard

%tensorboard --logdir=.
```

## 5 takeaways

* Mostly any training logic can be coded as a `train_step` method and a trainer built using this method.

* The essence of the library is **`Engine`** class that loops a given number of times over a dataset and executes a processing function.

* Highly customizable **event system** simplifies interaction with the engine on each step of the run.

* PyTorch-Ignite provides a set of built-in handlers and metrics for common tasks. 

* PyTorch-Ignite is easy to extend.

# Advanced features

In this section we would like to present some advanced features of PyTorch-Ignite for experienced users. We will cover more in details events and handlers, metrics and distributed computations on GPUs and TPUs. Feel free to skip this section now and come back later if you are a beginner.



## Power of Events & Handlers

We have seen throughout the quick-start example that events and handlers are perfect to execute any number of functions whenever you wish. In addition to that we provide several ways to extend it even more by
- Built-in events filtering
- Stacking events to share the action
- Adding custom events to go beyond built-in standard events

Let's see these features in details.


### Built-in events filtering

User can simply filter out events to skip triggering the handler. Let's create a dummy trainer:


```python
from ignite.engine import Engine, Events


trainer = Engine(lambda e, batch: None)
```

Let's consider a use-case when we would like to train a model and run periodically its validation on several development datasets, e.g. devset1 and devset2:


```python
# We run the validation on devset1 every 5 epochs
@trainer.on(Events.EPOCH_COMPLETED(every=5))
def run_validation1():
    print("Epoch {}: Validation on devset 1".format(trainer.state.epoch))
    # evaluator.run(devset1)

# We run another validation on devset2 every 10 epochs
@trainer.on(Events.EPOCH_COMPLETED(every=10))
def run_validation2():
    print("Epoch {}: Validation on devset 2".format(trainer.state.epoch))
    # evaluator.run(devset2)

train_data = [0, 1, 2, 3, 4]
trainer.run(train_data, max_epochs=50);
```

    Epoch 5: Validation on devset 1
    Epoch 10: Validation on devset 1
    Epoch 10: Validation on devset 2
    Epoch 15: Validation on devset 1
    Epoch 20: Validation on devset 1
    Epoch 20: Validation on devset 2
    Epoch 25: Validation on devset 1
    Epoch 30: Validation on devset 1
    Epoch 30: Validation on devset 2
    Epoch 35: Validation on devset 1
    Epoch 40: Validation on devset 1
    Epoch 40: Validation on devset 2
    Epoch 45: Validation on devset 1
    Epoch 50: Validation on devset 1
    Epoch 50: Validation on devset 2


Let's now consider another situation when we would like to make a single change once achieved a certain epoch or iteration. For example, let's change the training dataset on 5-th epoch from low resolution images to high resolution images:


```python
def train_step(e, batch):
    print("Epoch {} - {} : batch={}".format(e.state.epoch, e.state.iteration, batch))

trainer = Engine(train_step)

small_res_data = [0, 1, 2, ]
high_res_data = [10, 11, 12]

# We run the following handler once on 5-th epoch started
@trainer.on(Events.EPOCH_STARTED(once=5))
def change_train_dataset():
    print("Epoch {}: Change training dataset".format(trainer.state.epoch))
    trainer.set_data(high_res_data)

trainer.run(small_res_data, max_epochs=10);
```

    Epoch 1 - 1 : batch=0
    Epoch 1 - 2 : batch=1
    Epoch 1 - 3 : batch=2
    Epoch 2 - 4 : batch=0
    Epoch 2 - 5 : batch=1
    Epoch 2 - 6 : batch=2
    Epoch 3 - 7 : batch=0
    Epoch 3 - 8 : batch=1
    Epoch 3 - 9 : batch=2
    Epoch 4 - 10 : batch=0
    Epoch 4 - 11 : batch=1
    Epoch 4 - 12 : batch=2
    Epoch 5: Change training dataset
    Epoch 5 - 13 : batch=10
    Epoch 5 - 14 : batch=11
    Epoch 5 - 15 : batch=12
    Epoch 6 - 16 : batch=10
    Epoch 6 - 17 : batch=11
    Epoch 6 - 18 : batch=12
    Epoch 7 - 19 : batch=10
    Epoch 7 - 20 : batch=11
    Epoch 7 - 21 : batch=12
    Epoch 8 - 22 : batch=10
    Epoch 8 - 23 : batch=11
    Epoch 8 - 24 : batch=12
    Epoch 9 - 25 : batch=10
    Epoch 9 - 26 : batch=11
    Epoch 9 - 27 : batch=12
    Epoch 10 - 28 : batch=10
    Epoch 10 - 29 : batch=11
    Epoch 10 - 30 : batch=12


Let's now consider another situation when we would like to trigger a handler with completely custom logic. For example, we would like to dump model gradients if training loss satisfies a certain condition:


```python
# Let's predefine for simplicity training losses
train_losses = [2.0, 1.9, 1.7, 1.5, 1.6, 1.2, 0.9, 0.8, 1.0, 0.8, 0.7, 0.4, 0.2, 0.1, 0.1, 0.01]

trainer = Engine(lambda e, batch: train_losses[e.state.iteration - 1])

# We define our custom logic when to execute a handler
def custom_event_filter(trainer, event):
    if 0.1 < trainer.state.output < 1.0:
        return True
    return False

# We run the following handler every iteration completed under our custom_event_filter condition:
@trainer.on(Events.ITERATION_COMPLETED(event_filter=custom_event_filter))
def dump_model_grads():
    print("{} - loss={}: dump model grads".format(trainer.state.iteration, trainer.state.output))

train_data = [0, ]
trainer.run(train_data, max_epochs=len(train_losses));
```

    7 - loss=0.9: dump model grads
    8 - loss=0.8: dump model grads
    10 - loss=0.8: dump model grads
    11 - loss=0.7: dump model grads
    12 - loss=0.4: dump model grads
    13 - loss=0.2: dump model grads


### Stack events to share the action

User can trigger the same handler on events of differen types. For example, let's run a handler for model's validation every 3 epochs and when the training is completed:


```python
trainer = Engine(lambda e, batch: None)

# We run the validation on devset1 every 5 epochs
@trainer.on(Events.EPOCH_COMPLETED(every=3) | Events.COMPLETED)
def run_validation():
    print("Epoch {} - event={}: Validation".format(trainer.state.epoch, trainer.last_event_name))
    # evaluator.run(devset)

train_data = [0, 1, 2, 3, 4]
trainer.run(train_data, max_epochs=20);
```

    Epoch 3 - event=epoch_completed: Validation
    Epoch 6 - event=epoch_completed: Validation
    Epoch 9 - event=epoch_completed: Validation
    Epoch 12 - event=epoch_completed: Validation
    Epoch 15 - event=epoch_completed: Validation
    Epoch 18 - event=epoch_completed: Validation
    Epoch 20 - event=completed: Validation


### Add custom events

User can add its own events to go beyond built-in standard events. For example,
let's define new events related to backward and optimizer step calls. This can help us to attach specific handlers on these events in a configurable manner.


```python
from ignite.engine import EventEnum


class BackpropEvents(EventEnum):
    BACKWARD_STARTED = 'backward_started'
    BACKWARD_COMPLETED = 'backward_completed'
    OPTIM_STEP_COMPLETED = 'optim_step_completed'


def update(engine, batch):
    # ...
    # loss = criterion(y_pred, y)
    engine.fire_event(BackpropEvents.BACKWARD_STARTED)
    # loss.backward()
    engine.fire_event(BackpropEvents.BACKWARD_COMPLETED)
    # optimizer.step()
    engine.fire_event(BackpropEvents.OPTIM_STEP_COMPLETED)
    # ...    

trainer = Engine(update)
trainer.register_events(*BackpropEvents)

def function_before_backprop():
    print("{} - before backprop".format(trainer.state.iteration))

trainer.add_event_handler(BackpropEvents.BACKWARD_STARTED, function_before_backprop)

def function_after_backprop():
    print("{} - after backprop".format(trainer.state.iteration))

trainer.add_event_handler(BackpropEvents.BACKWARD_COMPLETED, function_after_backprop)

train_data = [0, 1, 2, 3, 4]
trainer.run(train_data, max_epochs=2);
```

    1 - before backprop
    1 - after backprop
    2 - before backprop
    2 - after backprop
    3 - before backprop
    3 - after backprop
    4 - before backprop
    4 - after backprop
    5 - before backprop
    5 - after backprop
    6 - before backprop
    6 - after backprop
    7 - before backprop
    7 - after backprop
    8 - before backprop
    8 - after backprop
    9 - before backprop
    9 - after backprop
    10 - before backprop
    10 - after backprop


## Out-of-the-box metrics

PyTorch-Ignite proposes an ensemble of metrics dedicated to many Deep Learning tasks (classification, regression, segmentation, etc). Most of our metrics provide a way to compute various quantities of interest in an online fashion without having to store the entire output history of a model.

* For classification : `Precision`, `Recall`, `Accuracy`, `ConfusionMatrix` and more!
* For segmentation : `DiceCoefficient`, `IoU`, `mIOU` and more!
* ~20 regression metrics, e.g. MSE, MAE, MedianAbsoluteError, etc 
* Metrics that store the entire output history per epoch
  - Possible to use with `scikit-learn` metrics, e.g. `EpochMetric`, `AveragePrecision`, `ROC_AUC`, etc
* Easily composable to assemble a custom metric
* Easily extendable to [create custom metrics](https://pytorch.org/ignite/metrics.html#how-to-create-a-custom-metric)

Complete list of metrics provided by PyTorch-Ignite can be found [here](https://pytorch.org/ignite/metrics.html#complete-list-of-metrics) and [here](https://pytorch.org/ignite/contrib/metrics.html#ignite-contrib-metrics).

We provide two kinds of public APIs:
- metric is attached to `Engine`
- metric's `reset, update, compute` methods 


### More on `reset, update, compute` public API 

Let's demonstrate this API on a simple example using `Accuracy` metric. Idea behind this API is that we accumulate internally certain counters on `update` call. Metric value is computed on `compute` call and counters are reset on `reset` call.


```python
import torch
from ignite.metrics import Accuracy

acc = Accuracy()

# Start accumulation
acc.reset()

y_target = torch.tensor([0, 1, 2, 1,])
# y_pred is logits computed by the model
y_pred = torch.tensor([
    [10.0, 0.1, -1.0],  # correct 
    [2.0, -1.0, -2.0],  # incorrect
    [1.0, -1.0, 4.0],   # correct
    [0.0, 5.0, -1.0],   # correct
])
acc.update((y_pred, y_target))

# Compute accuracy on 4 samples
print("After 1st update, accuracy=", acc.compute())

y_target = torch.tensor([1, 2, 0, 2])
# y_pred is logits computed by the model
y_pred = torch.tensor([
    [2.0, 1.0, -1.0],   # incorrect
    [0.0, 1.0, -2.0],   # incorrect
    [2.6, 1.0, -4.0],   # correct
    [1.0, -3.0, 2.0],   # correct
])
acc.update((y_pred, y_target))

# Compute accuracy on 8 samples
print("After 2nd update, accuracy=", acc.compute())
```

    After 1st update, accuracy= 0.75
    After 2nd update, accuracy= 0.625


### Composable metrics

User can compose their own metrics with ease from existing ones using arithmetic operations or torch methods. For example, error metric defined as `100 * (1.0 - accuracy)` can be coded straight forward:


```python
import torch
from ignite.metrics import Accuracy

acc = Accuracy()
error = 100.0 * (1.0 - acc) 

# Start accumulation
acc.reset()

y_target = torch.tensor([0, 1, 2, 1,])
# y_pred is logits computed by the model
y_pred = torch.tensor([
    [10.0, 0.1, -1.0],  # correct 
    [2.0, -1.0, -2.0],  # incorrect
    [1.0, -1.0, 4.0],   # correct
    [0.0, 5.0, -1.0],   # correct
])
acc.update((y_pred, y_target))

# Compute error on 4 samples
print("After 1st update, error=", error.compute())

y_target = torch.tensor([1, 2, 0, 2])
# y_pred is logits computed by the model
y_pred = torch.tensor([
    [2.0, 1.0, -1.0],   # incorrect
    [0.0, 1.0, -2.0],   # incorrect
    [2.6, 1.0, -4.0],   # correct
    [1.0, -3.0, 2.0],   # correct
])
acc.update((y_pred, y_target))

# Compute err on 8 samples
print("After 2nd update, error=", error.compute())
```

    After 1st update, error= 25.0
    After 2nd update, error= 37.5


In case if custom metric can not be expressed as arithmetic operations of base metrics, please, follow [this guide](https://pytorch.org/ignite/metrics.html#how-to-create-a-custom-metric) to implement the custom metric.

## Out-of-the-box handlers

PyTorch-Ignite proposes various commonly used handlers to simplify the 
application code:

- Common training handlers: `Checkpoint`, `EarlyStopping`, `Timer`, `TerminateOnNan`
- Optimizer's parameter scheduling (learning rate, momentum, etc)
  - concat schedulers, add warm-up, cyclical scheduling, piecewise-linear scheduling, and more! See [examples](https://pytorch.org/ignite/contrib/handlers.html#more-on-parameter-scheduling).
- Time profiling
- Logging to experiment tracking systems:
  - Tensorboard, Visdom, MLflow, Polyaxon, Neptune, Trains, etc.

Complete list of handlers provided by PyTorch-Ignite can be found [here](https://pytorch.org/ignite/handlers.html#complete-list-of-handlers) and [here](https://pytorch.org/ignite/contrib/handlers.html#ignite-contrib-handlers).


### Common training handlers

With out-of-the-box [`Checkpoint`](https://pytorch.org/ignite/handlers.html#ignite.handlers.Checkpoint) handler user can easily save the training state/best models to the filesystem or a cloud.

[`EarlyStopping`](https://pytorch.org/ignite/handlers.html#ignite.handlers.EarlyStopping) and [`TerminateOnNan`](https://pytorch.org/ignite/handlers.html#ignite.handlers.TerminateOnNan) helps to stop the training if overfitting or diverged.

All those things can be easily added to the trainer one by one or with [helper methods](https://pytorch.org/ignite/contrib/engines.html#module-ignite.contrib.engines.common). 

Let's consider an example of using helper methods.


```python
import torch
import torch.nn as nn
import torch.optim as optim

from ignite.engine import create_supervised_trainer, create_supervised_evaluator, Events
from ignite.metrics import Accuracy
import ignite.contrib.engines.common as common

train_data = [[torch.rand(2, 4), torch.randint(0, 5, size=(2, ))] for _ in range(10)]
val_data = [[torch.rand(2, 4), torch.randint(0, 5, size=(2, ))] for _ in range(10)]
epoch_length = len(train_data)

model = nn.Linear(4, 5)
optimizer = optim.SGD(model.parameters(), lr=0.01)
# step_size is expressed in iterations
lr_scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=epoch_length, gamma=0.88)

# Let's define some dummy trainer and evaluator
trainer = create_supervised_trainer(model, optimizer, nn.CrossEntropyLoss())
evaluator = create_supervised_evaluator(model, metrics={"accuracy": Accuracy()})


@trainer.on(Events.EPOCH_COMPLETED)
def run_validation():
    evaluator.run(val_data)

# training state to save
to_save = {
    "trainer": trainer, "model": model,
    "optimizer": optimizer, "lr_scheduler": lr_scheduler
}
metric_names = ["batch loss", ]

common.setup_common_training_handlers(
    trainer=trainer,
    to_save=to_save,
    output_path="checkpoints",
    save_every_iters=epoch_length,
    lr_scheduler=lr_scheduler,
    output_names=metric_names,
    with_pbars=True,
)

tb_logger = common.setup_tb_logging("tb_logs", trainer, optimizer, evaluators=evaluator)

common.save_best_model_by_val_score(
    "best_models",
    evaluator=evaluator,
    model=model,
    metric_name="accuracy",
    n_saved=2,
    trainer=trainer,
    tag="val",
)

trainer.run(train_data, max_epochs=5)

tb_logger.close()
```


```python
!ls -all "checkpoints"
!ls -all "best_models"
!ls -all "tb_logs"
```

    total 12
    drwxr-xr-x 2 root root 4096 Aug 31 11:27 .
    drwxr-xr-x 1 root root 4096 Aug 31 11:27 ..
    -rw------- 1 root root 1657 Aug 31 11:27 training_checkpoint_50.pt
    total 16
    drwxr-xr-x 2 root root 4096 Aug 31 11:27  .
    drwxr-xr-x 1 root root 4096 Aug 31 11:27  ..
    -rw------- 1 root root 1145 Aug 31 11:27 'best_model_2_val_accuracy=0.3000.pt'
    -rw------- 1 root root 1145 Aug 31 11:27 'best_model_3_val_accuracy=0.3000.pt'
    total 12
    drwxr-xr-x 2 root root 4096 Aug 31 11:27 .
    drwxr-xr-x 1 root root 4096 Aug 31 11:27 ..
    -rw-r--r-- 1 root root  325 Aug 31 11:27 events.out.tfevents.1598873224.3aa7adc24d3d.115.1


In the above code, `common.setup_common_training_handlers` method adds `TerminateOnNan`, a handler to use `lr_scheduler` (expressed in iterations), training state checkpointing, exposes `batch loss` output as exponential moving averaged metric for logging and add a progress bar to the trainer.

Next, `common.setup_tb_logging` method returns TensorBoard logger which is automatically configured to log trainer's metrics (i.e. `batch loss`), optimizer's learning rate and evaluator's metrics.

Finally, `common.save_best_model_by_val_score` setups a handler to save best 2 models according to validation accuracy metric value.


## Distributed and XLA devices support

PyTorch offers a distributed communication package for writing and running parallel applications on multiple devices and machines. The native interface provides commonly used collective operations and allows to address multi-CPU and multi-GPU computations seamlessly using [torch `DistributedDataParallel`](https://pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html) module and the well-known `mpi`, `gloo` and `nccl` backends. Recently, users can also run PyTorch on XLA devices, like TPUs, with the `torch_xla` package. However, writing distributed training code working on GPUs and TPUs is not a trivial task due to some API specificities. The purpose of the PyTorch-Ignite `ignite.distributed` package introduced in version 0.4 is to unify the code for native torch distributed API, torch xla API on XLA devices and also supporting other distributed frameworks (e.g. Horovod).

To make distributed configuration setup easier, [`Parallel`](https://pytorch.org/ignite/distributed.html#ignite.distributed.launcher.Parallel) context manager has been introduced:



```python
code = """
import ignite.distributed as idist

def training(local_rank, config, **kwargs):
    print(idist.get_rank(), ': run with config:', config, '- backend=', idist.backend())
    # do the training ...
  
backend = 'gloo' # or "xla-tpu" or None
dist_configs = {'nproc_per_node': 2}  # or dist_configs = {...}
config = {'c': 12345}

if __name__ == '__main__':

    with idist.Parallel(backend=backend, **dist_configs) as parallel:
        parallel.run(training, config, a=1, b=2)
"""
!echo "{code}" > main.py
!python main.py
```

    2020-08-31 11:27:07,128 ignite.distributed.launcher.Parallel INFO: Initialized distributed launcher with backend: 'gloo'
    2020-08-31 11:27:07,128 ignite.distributed.launcher.Parallel INFO: - Parameters to spawn processes: 
    	nproc_per_node: 2
    	nnodes: 1
    	node_rank: 0
    2020-08-31 11:27:07,128 ignite.distributed.launcher.Parallel INFO: Spawn function '<function training at 0x7f32b8ac9d08>' in 2 processes
    0 : run with config: {'c': 12345} - backend= gloo
    1 : run with config: {'c': 12345} - backend= gloo
    2020-08-31 11:27:09,959 ignite.distributed.launcher.Parallel INFO: End of run


The above code with a single modification can run on a GPU, single-node multiple GPUs, single or multiple TPUs etc. It can be executed with `torch.distributed.launch` tool or by python and spawning required number of processes. For more details, see [our documentation](https://pytorch.org/ignite/distributed.html). 


In addition, methods like `auto_model()`, `auto_optim()` and `auto_dataloader()` helps to adapt in a transparent way provided model, optimizer and data loaders to existing configuration:

```python
# main.py

import ignite.distributed as idist

def training(local_rank, config, **kwargs):

    print(idist.get_rank(), ": run with config:", config, "- backend=", idist.backend())

    train_loader = idist.auto_dataloader(dataset, batch_size=32, num_workers=12, shuffle=True, **kwargs)
    # batch size, num_workers and sampler are automatically adapted to existing configuration
    # ...
    model = resnet50()
    optimizer = optim.SGD(model.parameters(), lr=0.01)

    # if training with Nvidia/Apex for Automatic Mixed Precision (AMP)
    # model, optimizer = amp.initialize(model, optimizer, opt_level=opt_level)

    model = idist.auto_model(model)
    # model is DDP or DP or just itself according to existing configuration
    # ...
    optimizer = idist.auto_optim(optimizer)
    # optimizer is itself, except XLA configuration and overrides `step()` method.
    # User can safely call `optimizer.step()` (behind `xm.optimizer_step(optimizier)` is performed)

backend = "nccl"  # torch native distributed configuration on multiple GPUs
# backend = "xla-tpu"  # XLA TPUs distributed configuration
# backend = None  # no distributed configuration
with idist.Parallel(backend=backend, **dist_configs) as parallel:
    parallel.run(training, config, a=1, b=2)
```

Please, note that these `auto_*` methods are optional and user can use some of them and specifically setup certain parts of the code if required. The advantage of this approach is that there is no under the hood inevitable objects' patching and overriding.

More details about distributed helpers provided by PyTorch-Ignite can be found in [the documentation](https://pytorch.org/ignite/distributed.html).
Complete example of CIFAR10 training can be found [here](https://github.com/pytorch/ignite/tree/master/examples/contrib/cifar10).

A detailed tutorial with distributed helpers will be published in another article.

# Projects using PyTorch-Ignite

There is a list of research papers with code, blog articles, tutorials, toolkits and other projects that are using PyTorch-Ignite. Detailed overview can be found [here](https://github.com/pytorch/ignite#projects-using-ignite).

To start your project using PyTorch-Ignite is simple and can require only to pass through this quick-start example and [library "Concepts"](https://pytorch.org/ignite/concepts.html).

In addition we also provide several tutorials:

-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/TextCNN.ipynb)  [Text Classification using Convolutional Neural
    Networks](https://github.com/pytorch/ignite/blob/master/examples/notebooks/TextCNN.ipynb) 
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/VAE.ipynb)  [Variational Auto
    Encoders](https://github.com/pytorch/ignite/blob/master/examples/notebooks/VAE.ipynb) 
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/FashionMNIST.ipynb)  [Convolutional Neural Networks for Classifying Fashion-MNIST
    Dataset](https://github.com/pytorch/ignite/blob/master/examples/notebooks/FashionMNIST.ipynb)
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/CycleGAN_with_nvidia_apex.ipynb)  [Training Cycle-GAN on Horses to
    Zebras with Nvidia/Apex](https://github.com/pytorch/ignite/blob/master/examples/notebooks/CycleGAN_with_nvidia_apex.ipynb) 
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/CycleGAN_with_torch_cuda_amp.ipynb)  [Another training Cycle-GAN on Horses to
    Zebras with Native Torch CUDA AMP](https://github.com/pytorch/ignite/blob/master/examples/notebooks/CycleGAN_with_torch_cuda_amp.ipynb)
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/EfficientNet_Cifar100_finetuning.ipynb)  [Finetuning EfficientNet-B0 on
    CIFAR100](https://github.com/pytorch/ignite/blob/master/examples/notebooks/EfficientNet_Cifar100_finetuning.ipynb)
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/Cifar10_Ax_hyperparam_tuning.ipynb)  [Hyperparameters tuning with
    Ax](https://github.com/pytorch/ignite/blob/master/examples/notebooks/Cifar10_Ax_hyperparam_tuning.ipynb) 
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/FastaiLRFinder_MNIST.ipynb)  [Basic example of LR finder on 
    MNIST](https://github.com/pytorch/ignite/blob/master/examples/notebooks/FastaiLRFinder_MNIST.ipynb)
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/Cifar100_bench_amp.ipynb)  [Benchmark mixed precision training on Cifar100: 
    torch.cuda.amp vs nvidia/apex](https://github.com/pytorch/ignite/blob/master/examples/notebooks/Cifar100_bench_amp.ipynb) 
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pytorch/ignite/blob/master/examples/notebooks/MNIST_on_TPU.ipynb)  [MNIST training on a single 
    TPU](https://github.com/pytorch/ignite/blob/master/examples/notebooks/MNIST_on_TPU.ipynb)
-   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1E9zJrptnLJ_PKhmaP5Vhb6DTVRvyrKHx) [CIFAR10 Training on multiple TPUs](https://github.com/pytorch/ignite/tree/master/examples/contrib/cifar10)

and examples:
- [cifar10](https://github.com/pytorch/ignite/tree/master/examples/contrib/cifar10) (single/multi-GPU, DDP, AMP, TPUs)
- [basic RL](https://github.com/pytorch/ignite/tree/master/examples/reinforcement_learning)
- [reproducible baselines for vision tasks](https://github.com/pytorch/ignite/tree/master/examples/references):
  -   classification on ImageNet (single/multi-GPU, DDP, AMP)
  -   semantic segmentation on Pascal VOC2012 (single/multi-GPU, DDP, AMP)


Library can be installed with pip/conda. More info and guides can be found [here](https://github.com/pytorch/ignite#installation).


# Project news

Instead of conclusion, we would like to announce some of current project news:

---

<div align="center">

<img width=150 src="data:image/png;base64,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" />


</div>


🎊🚄 [Trains Ignite server](https://app.ignite.trains.allegro.ai) is open to everyone to browse our reproducible experiment logs, compare performances and restart any run on their own [Trains server](https://github.com/allegroai/trains) and associated infrastructure. Many thanks to the folks at [Allegro AI](https://allegro.ai/) who are making this possible!

--- 

<div align="center">
<img width=150 src="https://numfocus.org/wp-content/uploads/2018/01/optNumFocus_LRG.png" />

<img width=175 src="https://labs.quansight.org/images/quansight_labs_logo.png" />
</div>

🎉🎊 Since June 2020, PyTorch-Ignite has joined [NumFOCUS as an affiliated project](https://numfocus.org/sponsored-projects/affiliated-projects) and [Quansight Labs](https://labs.quansight.org/projects/). We believe that it will be a new step in our project’s development and promoting open practices in research and industry.



--- 

<div align="center">

<a href="https://www.mentored-sprints.dev/">
<img width=320 src="https://the-turing-way.netlify.app/_images/community.jpg" />
</a>

</div>

🎉 <img width=20 src="https://global.pydata.org/assets/images/pydata.png"/> We are pleased to announce that we will run a mentored sprint session to contribute to PyTorch-Ignite at PyData Global 2020. We are looking forward to seeing you in November at this event!

--- 

<div align="center">

<img width=200 src="https://raw.githubusercontent.com/pytorch/ignite/master/assets/ignite_logo.svg" />

</div>


 .\ | 📈💻 The project is currently maintained by a team of volunteers and we are looking for motivated contributors to help us to move quickly forward. Please, see the [contribution guidelines](https://github.com/pytorch/ignite/blob/master/CONTRIBUTING.md) for more information.


--- 

<img width=20 src="https://github.githubassets.com/images/icons/emoji/octocat.png"/> Checkout the project on [Github](https://github.com/pytorch/ignite) and follow us on [twitter](https://twitter.com/pytorch_ignite). For any questions, support or issues, please [reach out to us](https://github.com/pytorch/ignite#communication). For all other questions and inquiries, please send an email to contact@pytorch-ignite.ai

