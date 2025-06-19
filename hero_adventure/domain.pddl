(define (domain heroquest_simple)
  (:requirements :strips :typing)
  (:types hero tile key)
  (:predicates
    (AtHero ?h - hero ?t - tile)
    (HasKey ?h - hero ?k - key)
  )

  (:action Move
    :parameters (?h - hero ?from - tile ?to - tile)
    :precondition (AtHero ?h ?from)
    :effect (and (AtHero ?h ?to) (not (AtHero ?h ?from)))
  )

  (:action TakeKey
    :parameters (?h - hero ?t - tile ?k - key)
    :precondition (AtHero ?h ?t)
    :effect (HasKey ?h ?k)
  )
)