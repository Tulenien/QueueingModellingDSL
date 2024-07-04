# QueueingModellingDSL

This project endeavors to develop a Domain-Specific Language (DSL) tailored to the field of Queueing Theory, specifically designed for the modeling of queueing systems (Q-systems).

A Queueing System, or Q-system, can be formally defined as a system equipped with a service facility to which units of a certain nature arrive for service. In instances where the number of units present in the system exceeds the service facility's concurrent handling capacity, a queue, or waiting line, is formed.

The purpose of queue modeling lies in the simulation of the system before its actual implementation. This simulation serves several crucial functions, including:
1. Conservation of Resources.
2. Provision of Basic Estimates.
3. Identification of Potential Problems.
4. System Capacity Evaluation.

## Core terminology
### Delta t / Event Modeling
`Delta t` modeling involves the use of the smallest possible time increment, updating the global system time during each iteration. `Generators` and `Processors` handlers are invoked at each iteration, producing results and managing the progression of tasks. System unit is invoked only if their next call calculated time is less than the global time.

`Event` modeling operates independently of time and involves creating a priorities list of system events before next iteration and invoking corresponding system units by that list. This approach often yields more accurate results compared to `Delta t` modeling.

### Information Source

An `Information Source`, or `Generator`, denotes a point in the system where units are introduced or produced. The generation of new `Tasks` or `Requests` follows distribution laws, constant or random time increments, or condition-based criteria. `Information Sources` may have constraints related to the type or quantity of `Task` produced.

### Queue

A `Queue` serves as the repository for all requests within the system. It is commonly implemented using a queue data structure, adhering to the "First In, First Out" (FIFO) principle. When `Processors` become available, `Requests` at the front of the `Queue` progress to the processing stage. The `Queue` may be finite, necessitating the deletion of incoming requests if directed to an already full `Queue`.

### Processor

The `Processor` constitutes the central component of the Q-system, responsible for task processing. Similar to `Generators`, processing times may be constant, conditional, or follow distribution laws. Following processing, `Tasks` are timestamped and either routed to a finished storage or returned to the queue, contingent on predefined criteria.

### Request / Task

`Tasks`, or `Requests`, serve to encapsulate information about generation and processing timestamps, return occurrences, status, and type. This comprehensive data enables post-simulation analysis to elucidate the flow of each request throughout the system.

## Example of Q-system
![image](https://github.com/Tulenien/QueueingModellingDSL/blob/master/queue_model_example.png)


## Installation

1. Clone this project from [the repository](https://github.com/Tulenien/QueueingModellingDSL.git).:

```bash
git clone https://github.com/Tulenien/QueueingModellingDSL.git
```

2. Create python virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

- Windows
```bash
.\venv\Scripts\activate.bat
```
- Unix/Linux, Mac
```bash
source ./venv/bin/activate
```

4. Install all the dependencies with pip:

```python
pip install git+https://github.com/Tulenien/QueueingModellingDSL.git
```

5. Launch with GUI:

```python
python main.py
```

## Work Example 

1. The application with be launched with GUI by default. In the main menu you will see three options:
![image](https://github.com/Tulenien/QueueingModellingDSL/blob/master/media/screenshots/image.png)

`Input Model Parameters` button will ask you to setup the system by showing you windows with the system and system modules forms interactively by the usage of buttons `BACK` and `SUBMIT`.

`Load TextX Model` button will open a file system dialog window where you will need to choose the model file which you would like to use as your system layout for current simulation.

`Use Saved TextX Model` will you the last loaded model file path for simulation. It uses the model file from this repository by default.

Both `Load TextX Model` and `Use Saved TextX Model` options after resolved successfully will open the simulation window (described in step 5)

2. Current window will open if you chose to enter the system layout parameters interactively. You will be suggested a combobox with the supported system modes. When you will change the mode, the form will be changed accordingly. After you input everything in the form without errors, the `SUBMIT` button will save your parameters and proceed to the next window. 

![image](https://github.com/Tulenien/QueueingModellingDSL/blob/master/media/screenshots/image1.png)

3. In the current window you can choose the different generators and add them to the system. Generator can be added if the name and distribution parameters are filled correctly. You can change distribution types freely, that will change the form accordingly. After you fill the form, you can press `ADD` button and the generator will be added to the system. You can do it multiple times. Then you are finished, press `SUBMIT` button to move forward.

If you need to change the generator parameters you need to choose it in the combobox labeled `Choose information sources`. That will fill the form with the currently stored information and replace `ADD` button with the `SAVE` button. After you change the generator, you will need to press the `SAVE` button to save it and `SUBMIT`button to proceed.

![image](https://github.com/Tulenien/QueueingModellingDSL/blob/master/media/screenshots/image2.png)

4. This window is for adding the processors to the system. The works exactly like the previous step describes. 

Important note: generators are connected to the common pool of requests, all requests from it can be taken into processing by any of the processing units on the system.

![image](https://github.com/Tulenien/QueueingModellingDSL/blob/master/media/screenshots/image3.png)

5. When you get to the simulation screen you will be shown the current system layout. You can redact it by going back through the forms and edit the data (with the `BACK` button) or start simulation with the current system layout by clicking `SIMULATE` button.

![image](https://github.com/Tulenien/QueueingModellingDSL/blob/master/media/screenshots/image4.png)

6. This window shows results of the simulation. It depicts all the requests created by information sources, then processed by processing unit and stored in the system until the simulation ends according to the type of the system and current system constraints values. Requests are stored in the order the exited the system by time.

Current window indicates that the experiment is finished and you can go to the main window to try the other layout or go back into simulation window and recreate it with the current setup by using `MAIN MENU` or `BACK` buttons accordingly.

![image](https://github.com/Tulenien/QueueingModellingDSL/blob/master/media/screenshots/image5.png)

