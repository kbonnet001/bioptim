# Ceci est l'example de la doc
# D'abord on import ce dont on a besoin

from bioptim import (
    TorqueBiorbdModel,
    OptimalControlProgram,
    BoundsList,
    InitialGuessList,
    ObjectiveFcn,
    Objective,
    # VariableScalingList
)
from scipy.interpolate import interp1d

# on définit un bioMod, on va charger le fichier.bioMod, ici pendule
bio_model = TorqueBiorbdModel("../models/pendulum.bioMod")

# Contraintes --> conditions intiales et finales
# Bounds are optional (default -inf -> inf)
x_bounds = BoundsList()
x_bounds["q"] = bio_model.bounds_from_ranges("q")
x_bounds["q"][:, [0, -1]] = 0  # on commence avec un angle de 0
x_bounds["q"][1, -1] = 3.14  # on veut finir avec cet angle en rad (pi donc 180)
x_bounds["qdot"] = bio_model.bounds_from_ranges("qdot")
x_bounds["qdot"][:, [0, -1]] = 0  # on commence et on fini à vitesse nulle

# Contraintes --> borner les valeurs de tau
u_bounds = BoundsList()
u_bounds["tau"] = [-100, 0], [100, 0]  # on met des borde à tau (contraintes)

# On créer une fonction objective : type Lagrange et minimiser le torque
#### ObjectiveFcn.Lagrange.MINIMIZE_TORQUE n'exite pas :0
# donc fait avec autre chose
objective_functions = Objective(ObjectiveFcn.Lagrange.MINIMIZE_CONTROL, key="tau")

# Parfois on peut mettre des guess mais pas obligé, ça dépend des méthodes je crois
# + on initialise
# Initial guess is optional (default = 0)
x_init = InitialGuessList()
# x_init["q"] = [0, 0]
# x_init["qdot"] = [0, 0]
u_init = InitialGuessList()
# u_init = [0, 0]

# x_scaling = VariableScalingList()
# x_scaling.add("q", scaling=[1, 3])
# x_scaling.add("qdot", scaling=[85, 85])

# u_scaling = VariableScalingList()
# u_scaling.add("tau", scaling=[900, 1])

# On peut déclarer notre ocp
ocp = OptimalControlProgram(
    bio_model,  # le biomodel, ici le pendule
    n_shooting=25,  # le nombre de stage k, N ?
    phase_time=3,  # temps total en seconde
    x_bounds=x_bounds,  # les contraintes sur les états
    u_bounds=u_bounds,  # les contraintes sur les controles
    x_init=x_init,  # conditions initiales
    u_init=u_init,
    objective_functions=objective_functions,  # la fonction objective
)

# Permet de vérifier si l'ocp est écrit correctement
# probablement de virifer les tailles des matrices, si ce qu'on a mis est ok etc
# ocp.check_conditioning()

sol = ocp.solve()  # résolution
# sol.detailed_cost  # Invoke this for adding the details of the objectives to sol for later manipulations
# sol.print_cost()  # le cout final
sol.animate(viewer="pyorerun")  # l'animation de la simulation
sol.graphs()  # pour voir les graph
