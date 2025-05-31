Here are the generated files:

**domain.pddl**
```
(define (domain stazione-spaziale)

  ; Predicati
  (predicates 
    (astronaut-at ?location) ; l'astronauta è in un dato luogo
    (path-clear ?corridor) ; il corridoio è libero dalle barriere
    (system-malfunction ?security-system) ; il sistema di sicurezza è malfunzionante
    (lab-locked ?status) ; il laboratorio è chiuso (vero o falso)
    (android-in ?location) ; l'androide è in un dato luogo
    (keycard-at ?storage) ; la chiave è nella storage
    (suit-damaged ?status) ; il costume è danneggiato (vero o falso)

  ; Azioni
  (action 
    move-astronaut 
      (parameters (?from - location) (?to - location)) 
    ; muovi l'astronauta da un luogo all'altro
    :preconditions ((and (astronaut-at ?from) (path-clear ?corridor)))
    :effects ((and (not (astronaut-at ?from)) (astronaut-at ?to))
              (and (not (system-malfunction security)) 
                  (when (and (lab-locked true)) (set lab-locked false))))

  (action 
    disable-security-system 
      ()
    ; disattiva il sistema di sicurezza
    :preconditions ((and (astronaut-at airlock) (system-malfunction security)))
    :effects ((not (system-malfunction security)))

  (action 
    open-lab-door 
      ()
    ; apre la porta del laboratorio
    :preconditions ((and (astronaut-at corridor) (lab-locked true)))
    :effects ((set lab-locked false))

  (action 
    rescue-android 
      ()
    ; salva l'androide
    :preconditions ((and (astronaut-at lab) (android-in lab) (lab-locked false)))
    :effects ((not (android-in lab)))

)

)