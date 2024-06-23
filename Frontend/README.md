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
