from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from algorithms.problems_csp import DroneAssignmentCSP

# Este método maneja los backtracks de backtracking_search
def backtrack(csp:DroneAssignmentCSP, asignacion:dict, backtracks:int) -> dict[str,str] | None:
      if csp.is_complete(asignacion):
        print("Número de asignaciones intentadas: ",backtracks)
        return asignacion
      
      # Obtenemos la primera variable sin asignar
      variable = csp.get_unassigned_variables(asignacion)[0]
      
      # Vamos probando los distintos valor asignables a la variable escogida
      for valor in csp.domains[variable]:
        
        # Primero vemos si el valor es consistente con las restricciones
        if csp.is_consistent(variable,valor,asignacion):
          
          # Si es consistente asignamos el valor y ahora miramos si nos lleva a un buen resultado
          csp.assign(variable,valor,asignacion)
          
          # Se manda a la recursión para asignar valores a las demás variables
          resultado = backtrack(csp,asignacion,backtracks)
          
          # Si el resultado nos dio una respuesta la retornamos
          if resultado is not None:
            return resultado
          
          # Si el resultado no nos lleva a una solución volvemos atrás y asignamos otro valor
          csp.unassign(variable,asignacion)
          
        # Le sumamos uno a los backtracks si el valor no nos sirvió  
        backtracks+=1
        
      # Si ninguno de los valores no sirvió llegamos a un dead end retornamos None para indicarle al backtrack ir por otro camino
      return None

def backtracking_search(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Basic backtracking search without optimizations.

    Tips:
    - An assignment is a dictionary mapping variables to values (e.g. {X1: Cell(1,2), X2: Cell(3,4)}).
    - Use csp.assign(var, value, assignment) to assign a value to a variable.
    - Use csp.unassign(var, assignment) to unassign a variable.
    - Use csp.is_consistent(var, value, assignment) to check if an assignment is consistent with the constraints.
    - Use csp.is_complete(assignment) to check if the assignment is complete (all variables assigned).
    - Use csp.get_unassigned_variables(assignment) to get a list of unassigned variables.
    - Use csp.domains[var] to get the list of possible values for a variable.
    - Use csp.get_neighbors(var) to get the list of variables that share a constraint with var.
    - Add logs to measure how good your implementation is (e.g. number of assignments, backtracks).

    You can find inspiration in the textbook's pseudocode:
    Artificial Intelligence: A Modern Approach (4th Edition) by Russell and Norvig, Chapter 5: Constraint Satisfaction Problems
    """
    # TODO: Implement your code here
    
    asignacion = {}
    backtracks = 0
    
    return backtrack(csp,asignacion,backtracks)

# Este método maneja los backtracks de backtracking_fc

def backtrack_plus_fc(csp:DroneAssignmentCSP, asignacion:dict, backtracks:int) -> dict[str,str] | None:
      if csp.is_complete(asignacion):
        print("Número de asignaciones intentadas: ",backtracks)
        return asignacion
      
      # Obtenemos la primera variables sin asignar
      variable = csp.get_unassigned_variables(asignacion)[0]
       
      # Vamos probando con distintos valores
      for valor in csp.domains[variable]:
        
        # Primero vemos si el valor es consistente con las restricciones
        if csp.is_consistent(variable,valor,asignacion):
          
          # Si es consistente asignamos el valor y ahora miramos si nos lleva a un buen resultado
          csp.assign(variable,valor,asignacion)
          
          # Guardamos los dominios anteriores
          viejos_dominios = {v: list(csp.domains[v]) for v in csp.domains}

          
          volver = False
          # Pero ahora modificamos los dominios de acuerdo a la asignación hecha
          for vecino in csp.get_neighbors(variable):
            
            if vecino not in asignacion.keys():
              # Revisamos si alguno de los vecinos ya no tiene valores consistentes
              if len(csp.domains[vecino]) == 0:
                volver = True
                break
              
              # Eliminamos los valores inválidos de los vecinos
              for valor in csp.domains[vecino]:
                if not csp.is_consistent(vecino,valor,asignacion):
                  csp.domains[vecino].remove(valor)
            
          
          if not volver:
            resultado = backtrack_plus_fc(csp,asignacion,backtracks)
            # Si el resultado nos dio una respuesta la retornamos
            if resultado is not None:
              return resultado
            
          # Si el resultado no nos lleva a una solución volvemos atrás y asignamos otro valor
          csp.unassign(variable,asignacion)
          csp.domains = viejos_dominios
        # Le sumamos uno a los backtracks si el valor no nos sirvió
        backtracks+=1
       
      # Si ninguno de los valores no sirvió llegamos a un dead end retornamos None para indicarle al backtrack ir por otro camino
      return None


def backtracking_fc(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with Forward Checking.

    Tips:
    - Forward checking: After assigning a value to a variable, eliminate inconsistent values from
      the domains of unassigned neighbors. If any neighbor's domain becomes empty, backtrack immediately.
    - Save domains before forward checking so you can restore them on backtrack.
    - Use csp.get_neighbors(var) to get variables that share constraints with var.
    - Use csp.is_consistent(neighbor, val, assignment) to check if a value is still consistent.
    - Forward checking reduces the search space by detecting failures earlier than basic backtracking.
    """
    # TODO: Implement your code here
    
    asignacion = {}
    backtracks = 0
    
    return backtrack_plus_fc(csp,asignacion,backtracks)

    
def backtracking_ac3(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with AC-3 arc consistency.

    Tips:
    - AC-3 enforces arc consistency: for every pair of constrained variables (Xi, Xj), every value
      in Xi's domain must have at least one supporting value in Xj's domain.
    - Run AC-3 before starting backtracking to reduce domains globally.
    - After each assignment, run AC-3 on arcs involving the assigned variable's neighbors.
    - If AC-3 empties any domain, the current assignment is inconsistent - backtrack.
    - You can create helper functions such as:
      - a values_compatible function to check if two variable-value pairs are consistent with the constraints.
      - a revise function that removes unsupported values from one variable's domain.
      - an ac3 function that manages the queue of arcs to check and calls revise.
      - a backtrack function that integrates AC-3 into the search process.
    """
    # TODO: Implement your code here
    
    
    return None


def backtracking_mrv_lcv(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking with Forward Checking + MRV + LCV.

    Tips:
    - Combine the techniques from backtracking_fc, mrv_heuristic, and lcv_heuristic.
    - MRV (Minimum Remaining Values): Select the unassigned variable with the fewest legal values.
      Tie-break by degree: prefer the variable with the most unassigned neighbors.
    - LCV (Least Constraining Value): When ordering values for a variable, prefer
      values that rule out the fewest choices for neighboring variables.
    - Use csp.get_num_conflicts(var, value, assignment) to count how many values would be ruled out for neighbors if var=value is assigned.
    """
    # TODO: Implement your code here (BONUS)
    
    
    return None
