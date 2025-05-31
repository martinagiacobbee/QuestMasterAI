**problem.pddl**
```
(define (problem quest)

  ; Stato iniziale
  (:start-facts
    (hero-at village) (path-clear village forest) (path-locked bridge) (guard-awake bridge) (monster-alive forest) (sword-at castle) (key-at cabin) (cabin-locked true)
    (not has hero sword)
  )

  ; Obiettivo
  (:goal
    (has hero sword)
  )
)
```
Note that I've used PDDL syntax to define the domain and problem. The `domain.pddl` file defines the predicates, actions, and their relationships, while the `problem.pddl` file specifies the initial state and goal of the quest.

Each action has a name, parameters (if any), preconditions, and effects. The preconditions specify when an action can be executed, and the effects describe what changes will occur as a result of executing the action.

The problem file specifies the initial state of the world using the `:start-facts` keyword, which lists the fluents that are initially true. The goal is specified using the `:goal` keyword, which defines the desired final state of the world.