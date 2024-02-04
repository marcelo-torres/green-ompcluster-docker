
DEFAULT_ROUND = 2

HEFT_TEST = 'heft_test'
MOHEFT_ENERGY = 'moheft_energy'
MOHEFT_GREEN_ENERGY = 'moheft_green_energy'

def extract_metricts_from_objectives(objective, algorithm):

    makespan = None
    green_energy = None
    brown_energy = None
    total_energy = None

    if algorithm == HEFT_TEST:
        makespan = objective[0]
        total_energy = objective[1]
        brown_energy = objective[2]

    if algorithm == MOHEFT_ENERGY:
        makespan = objective[0]
        total_energy = objective[1]
        brown_energy = objective[2]

    if algorithm == MOHEFT_GREEN_ENERGY:
        makespan = objective[0]
        brown_energy = objective[1]
        total_energy = objective[2]

    green_energy = total_energy - brown_energy

    return makespan, total_energy, green_energy, brown_energy


def format_objectives(objectives_line, algorithm):

    for i in range(11):
        objectives_line = objectives_line.replace(f'[{i}]:', '')
    
    #print('objectives_line ' + objectives_line)
    #objectives_line = objectives_line.replace('  ', ' ').strip().replace(' ', ',')
    

    objectives = objectives_line.split('Objectives')
    
    data = []

    for objective in objectives:
        if objective == '':
            continue
        objective = objective.replace('  ', ' ').strip().split(' ')
        objective = list(
            map(float, objective)
        )

        makespan, total_energy, green_energy, brown_energy = extract_metricts_from_objectives(objective, algorithm)

        makespan = round(makespan/60, DEFAULT_ROUND)
        total_energy = round(total_energy/1000, DEFAULT_ROUND)
        green_energy = round(green_energy/1000, DEFAULT_ROUND)
        brown_energy = round(brown_energy/1000, DEFAULT_ROUND)

        objective_list = [makespan, total_energy, green_energy, brown_energy]
        objective_list = list(
            map(str, objective_list)
        )
        data.append(objective_list)
    return data

    data = objectives_line.split(',')
    new_data = []
    for index, d in enumerate(data):
        is_makespan = (index % 2) == 0
        d = float(d)
        if is_makespan:    
            d /= 60
        else:
            d /= 1000
        d = round(d, DEFAULT_ROUND)
        d = str(d)
        new_data.append(d)
    
    return ','.join(new_data)

def isBlank (myString):
    return not (myString and myString.strip().replace('\n', ''))

def isExperiment(line):
    return line.startswith("===")

def isAlgorithm(line):
    return line in [HEFT_TEST, MOHEFT_ENERGY, MOHEFT_GREEN_ENERGY]

def isTopology(line):
    return line in ['trivial', 'stencil_1d', 'stencil_1d_periodic', 'dom', 'tree', 'fft', 'nearest', 'no_comm', 'spread -period 2', 'random_nearest']

if __name__ == '__main__':
    file = 'output-64-32_11c_new.txt'

    with open(file) as f:
        ignore_line = True

        experiments = {}

        current_experiment = None
        current_algorithm = None
        current_algorithm_name = None
        topology = None

        for item in f.readlines():

            if ignore_line:
                ignore_line = False
                continue

            item = item.strip()

            if isBlank(item) or not item:
                continue

            if isExperiment(item):
                item = item.replace('=', '').replace(' ', '')
                current_experiment = {}
                experiments[item] = current_experiment
                continue
            
            if isAlgorithm(item):
                current_algorithm_name = item
                current_algorithm = {}
                current_experiment[current_algorithm_name] = current_algorithm
                continue

            if isTopology(item):
                topology = item
                continue

            
            data = format_objectives(item, current_algorithm_name)
            current_algorithm[topology] = data


    for experiment_name in experiments.keys():
        experiment = experiments[experiment_name]

        print(experiment_name)

        with open(f'{experiment_name}.csv', 'w') as o:

            t = 1 * ',Makespan(min),Energia Total (Kj),Energia Verde (kJ), Energia Marrom (Kj)'
            o.write(f'Algoritmo,Topologia{t}\n')
            for algorithm_name in experiment.keys():
                algorithm = experiment[algorithm_name]
                
                #print(f'\t{algorithm_name}')

                for topology in algorithm.keys():
                    data = algorithm[topology]
                    #print(f'\t\t{topology}')
                    #print(f'\t\t\t{algorithm[topology]}')
                    for d in data:
                        print(d)
                        d = ','.join(d)
                        o.write(f'{algorithm_name},{topology},{d}\n')       