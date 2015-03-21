# kanban-simulator
Simulator to help teaching kanban, specially how the WIP limit affects the system's performance.

### Proof of Concept

The proof of concept shows how to:

- use SimPy to run a simulation
- use Tornado's websockets to broadcast the events coming from the simulation

Next steps should be:

- separate concerns
- record the simulation events?
- change the simulation example, using cards in a kanban board instead of cars
- show metrics (lead time, cycle time and queue sizes)
- include a dashboard to change the simulation parameters
- include WIP limits in the simulation
