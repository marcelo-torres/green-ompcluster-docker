import csv
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

topologies_def = {
    'trivial': ('Trivial', 0),
    'stencil_1d': ('Stencil 1D', 1),
    'stencil_1d_periodic': ('Stencil 1D\nPeriodic', 2),
    'dom': ('DOM', 3),
    'tree': ('Tree', 4),
    'fft': ('FFT', 5),
    'no_comm': ('No\ncommunication', 6),
    'spread -period 2': ('Spread\nPeriod 2', 7)
}

algorithm_style = {
    'HEFT': ('blue', '^', 'HEFT'),
    'MOHEFT': ('red', '+', 'MOHEFT'),
    'G-MOHEFT': ('orange', '.', 'GMOHEFT')
}



experiment_files = [
    ('experiment-2-1.csv', '+0h'),
    ('experiment-2-2.csv', '+6h'),
    ('experiment-2-3.csv', '+12h'),
    ('experiment-2-4.csv', '+18h')
]

output = None #'makespan-vs-brown-energy-topologies.png'

fig = plt.figure()
fig.set_size_inches(12, 15)

gs = fig.add_gridspec(8, 4, hspace=0, wspace=0)
axs = gs.subplots(sharex='col', sharey='row')

exp = 0
for experiment_file, title in experiment_files:


    with open(experiment_file, newline='\n') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        
        i = 0
        for row in spamreader:
            i+=1
            if i == 1:
                continue

            makespan = float(row[0])
            brown_energy = float(row[1])
            algorithm = row[2]
            topology = row[3]

            color, shape, label = algorithm_style[algorithm]

            name, row = topologies_def[topology]

            ax = axs[row, exp]

            ax.scatter(makespan, brown_energy, color=color, marker=shape, s=28)
            ax.grid(True, which='major', linewidth=0.5, color='gray')
            

            if exp == 3:
                ax2 = ax.twinx()
                ax2.set_ylabel(name)
                ax2.set_yticks([])
                ax2.grid(False)
                ax2.spines['top'].set_visible(False)
                ax2.spines['right'].set_visible(False)
                ax2.spines['bottom'].set_visible(False)
                ax2.spines['left'].set_visible(False)


            is_first_row = row == 0
            last_row = len(topologies_def)-1

            if is_first_row:
                ax.set_title(title)

            if row == last_row and exp == 0:
                ax.set_xlabel('Makespan (minutes)')

            
            if row == last_row-1 and exp == 0:
                ax.set_ylabel('Brown energy (kJ)')

            
            ax.set_xlim(0, 1100)
            ax.set_ylim(0, 15000)

            y_end = '15.000' if is_first_row else ''

            ax.set_yticks([0, 5000, 10000, 15000], ['0', '5.000', '10.000', y_end])
            ax.set_xticks([200, 400, 600, 800, 1000], ['200', '400', '600', '800', '1.000'])

    exp += 1

#plt.legend()

handles = []
for algorithm in algorithm_style:
    color, shape, label = algorithm_style[algorithm]
    handle = mlines.Line2D([], [], color=color, marker=shape, linestyle='None', markersize=10, label=label)
    handles.append(handle)
plt.legend(handles=handles, loc='upper left', bbox_to_anchor=(-1.8, -0.5), ncol=3)

#plt.tight_layout()
if output:
    plt.savefig(output)
else: 
    plt.show()
