(define (problem heroquest_simple_problem)
  (:domain heroquest_simple)
  (:objects
    hero1 - hero
    tile1 tile2 tile3 - tile
    key1 - key
  )
  (:init
    (AtHero hero1 tile1)
  )
  (:goal
    (and
      (HasKey hero1 key1)
      (AtHero hero1 tile3)
    )
  )
)