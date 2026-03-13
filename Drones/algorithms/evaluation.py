from __future__ import annotations

from typing import TYPE_CHECKING

from algorithms.utils import bfs_distance, dijkstra


if TYPE_CHECKING:
    from world.game_state import GameState


def evaluation_function(state: GameState) -> float:
    """
    Evaluation function for non-terminal states of the drone vs. hunters game.

    A good evaluation function can consider multiple factors, such as:
      (a) BFS distance from drone to nearest delivery point (closer is better).
          Uses actual path distance so walls and terrain are respected.
      (b) BFS distance from each hunter to the drone, traversing only normal
          terrain ('.' / ' ').  Hunters blocked by mountains, fog, or storms
          are treated as unreachable (distance = inf) and pose no threat.
      (c) BFS distance to a "safe" position (i.e., a position that is not in the path of any hunter).
      (d) Number of pending deliveries (fewer is better).
      (e) Current score (higher is better).
      (f) Delivery urgency: reward the drone for being close to a delivery it can
          reach strictly before any hunter, so it commits to nearby pickups
          rather than oscillating in place out of excessive hunter fear.
      (g) Adding a revisit penalty can help prevent the drone from getting stuck in cycles.

    Returns a value in [-1000, +1000].

    Tips:
    - Use state.get_drone_position() to get the drone's current (x, y) position.
    - Use state.get_hunter_positions() to get the list of hunter (x, y) positions.
    - Use state.get_pending_deliveries() to get the set of pending delivery (x, y) positions.
    - Use state.get_score() to get the current game score.
    - Use state.get_layout() to get the current layout.
    - Use state.is_win() and state.is_lose() to check terminal states.
    - Use bfs_distance(layout, start, goal, hunter_restricted) from algorithms.utils
      for cached BFS distances. hunter_restricted=True for hunter-only terrain.
    - Use dijkstra(layout, start, goal) from algorithms.utils for cached
      terrain-weighted shortest paths, returning (cost, path).
    - Consider edge cases: no pending deliveries, no hunters nearby.
    - A good evaluation function balances delivery progress with hunter avoidance.
    """
    # TODO: Implement your code here
    if state.is_win():
      print("WIN STATE EVALUATED")
      return 1000
    
    if state.is_lose():
      return -1000
    
    dron_pos = state.get_drone_position()
    pos_hunters = list(state.get_hunter_positions())
    pos_deliveries = list(state.get_pending_deliveries())
    past_score = state.get_score()
    
    
    new_score = past_score
    
    # Si el dron ya ha completado entregas se le premiará su progreso
    puntaje_entregas = -20*len(pos_deliveries)
    
    new_score+=puntaje_entregas
    # Ahora premiaremos que tan cerca esta de las entregas y se penalizará su distancia a las entregas lejanas
    puntaje_distancias_entregas = 0
    if pos_deliveries:
      
      mejor = float('inf')
      mas_cercana = 0
      
      i = 0
      while i<len(pos_deliveries):
        pos_d = pos_deliveries[i]
        dist_bfs = bfs_distance(state.get_layout(),dron_pos,pos_d)
        
        if mejor > dist_bfs:
          mejor = dist_bfs
          mas_cercana = i
        
        i+=1
      
      # Ahora miramos el costo de la entrega más cercana
      cost_dijkstra, _ = dijkstra(state.get_layout(),dron_pos,pos_deliveries[mas_cercana])
        
    puntaje_distancias_entregas-= 5*mejor
    if len(pos_deliveries) == 1:
      new_score-= 40*mejor
      
    puntaje_distancias_entregas-= cost_dijkstra
    
    
    new_score+= puntaje_distancias_entregas
    # Ahora se premiará la distancia a los cazadores
    puntaje_dist_hunters = 0
    if pos_hunters:
      j = 0
      pos_h = pos_hunters[j]
      menor_dist = float('inf')
      while j < len(pos_hunters):
        pos_h = pos_hunters[j]
        dist_bfs_h = bfs_distance(state.get_layout(),dron_pos,pos_h,hunter_restricted=True)
        
        if dist_bfs_h < menor_dist:
          menor_dist = dist_bfs_h
        
        j+=1
      
      if menor_dist <=2:
        puntaje_dist_hunters-=200
      elif menor_dist <= 4:
        puntaje_dist_hunters-=40
        
      else:
        puntaje_dist_hunters-=10
      
    
    new_score+=puntaje_dist_hunters
    #bonus por puntaje anterior
    # if past_score > 0:
    #   new_score+= past_score*0.5
    
    return max(-1000, min(1000, new_score))
