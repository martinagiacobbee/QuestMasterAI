Here are the contents of `domain.pddl` and `problem.pddl`:

**domain.pddl**
```
(define (domain hero)

  ; Predicati
  (predicates
    (?hero-at x)  ; Hero is at location x
    (?path-clear x)  ; Path from village to forest/x is clear
    (?path-locked x)  ; Path from village to forest/x is locked
    (?guard-awake x)  ; Guard is awake at location x
    (?monster-alive x)  ; Monster is alive in location x
    (?sword-at x)  ; Sword is at location x
    (?key-at x)  ; Key is at location x
    (?cabin-locked -)  ; Cabin is locked

    ; Azioni
  (actions
    (move-hero-from-village-to-forest)  ; Hero moves from village to forest
      :parameters (?x)
      :preconditions (?hero-at village) (?path-clear village forest)
      :effects (?hero-at ?x) (- ?path-clear village forest)

    (unlock-path-bridge)  ; Unlock the path at the bridge
      :parameters ()
      :preconditions (?hero-at bridge) (?path-locked bridge)
      :effects (- ?path-locked bridge)

    (wake-guard-up)  ; Wake up the guard at the bridge
      :parameters ()
      :preconditions (?hero-at bridge) (?guard-asleep bridge)
      :effects (+ ?guard-awake bridge)

    (slay-monster)  ; Slay the monster in the forest
      :parameters (?x)
      :preconditions (?hero-at ?x) (?monster-alive ?x)
      :effects (- ?monster-alive ?x)

    (take-sword-from-castle)  ; Take the sword from the castle
      :parameters ()
      :preconditions (?hero-at castle) (?sword-at castle)
      :effects (+ has hero sword) (- ?sword-at castle)

    (unlock-cabin)  ; Unlock the cabin
      :parameters ()
      :preconditions (?hero-at cabin) (?cabin-locked true)
      :effects (- ?cabin-locked true)

    (take-key-from-cabin)  ; Take the key from the cabin
      :parameters ()
      :preconditions (?hero-at cabin) (?key-at cabin)
      :effects (+ has hero key) (- ?key-at cabin)

    (trick-guard-at-bridge)  ; Trick the guard at the bridge
      :parameters ()
      :preconditions (?hero-at bridge) (?guard-awake bridge)
      :effects (- ?guard-awake bridge)

  )
)
```