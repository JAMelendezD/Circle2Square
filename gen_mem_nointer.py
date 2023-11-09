import sys
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams.update({'font.size': 24})
plt.rcParams.update({'font.family': 'serif',"font.serif" : "Times New Roman", "text.usetex": True})

def write_pdb(f,box,positions):
    '''
    Function to write coordinates as a pdb to a file
    '''

    pdb_format = "{:6s}{:5d} {:^4s}{:1s}{:3s} {:1s}{:4d}{:1s}   {:8.3f}{:8.3f}{:8.3f}{:6.2f}{:6.2f}          {:>2s}{:2s}\n"
    fixed_format = ['ATOM',
                    'INDEX',
                    'ATYPE',
                    '',
                    '',
                    'A',
                    'INDEX',
                    '',
                    'POSX',
                    'POSY',
                    'POSZ',
                    1.00,
                    1.00,
                    'AELE',
                    '']

    f.write('CRYST1 {:8.3f}{:8.3f}{:8.3f}{:8.2f}{:8.2f}{:8.2f}\n'.format(*box,90,90,90))
    f.write('MODEL {:>8d}\n'.format(0))
    for i in range(len(positions)):
        fixed_format[1] = i+1
        fixed_format[2] = 'CA'
        fixed_format[4] = 'MEM'
        fixed_format[6] = i+1
        fixed_format[8] = positions[i][0]
        fixed_format[9] = positions[i][1]
        fixed_format[10] = positions[i][2]
        fixed_format[13] = 'C'
        f.write(pdb_format.format(*fixed_format))
    f.write('TER\n')
    f.write('ENDMDL\n')
    return

def generate_grid(s, l):
    '''
    Function to generate a grid
    '''

    x = np.arange(-l/2, l/2+s, s)
    y = np.arange(-l/2, l/2+s, s)
    n = len(x)

    grid = []

    for i in range(n):
        for j in range(n):
            grid.append([x[i], y[j]])
    
    return np.array(grid)

def generate_circle(r, s):
    '''
    Function to generate a circle given a radius (r) and the spacing (s)
    if the number of points (n) is 0. If it is different then the spacing
    is computed for the number of given points starting the same way as the
    square on step to the right of 135 going anticlockwise and ending at 135
    '''

    a = 2*r*np.arcsin(s/(2*r)) # convert from spacing to arc length
    n = int(round(2*np.pi*r/a, 0))
    new_radius = (n*a) / (2*np.pi)
    
    if new_radius < r:
        new_radius = ((n+1)*a) / (2*np.pi)

    step = (2*np.pi / n)
    angles = np.linspace(0+step, 2*np.pi, n)
    x = new_radius*np.cos(angles)
    y = new_radius*np.sin(angles)
    circle = np.array(list(zip(x,y)))
    
    print(n)

    return circle, new_radius

def remove_grid_atoms(grid, circle, new_rad, spacing, eps):

    inside_ind = []
    for i in range(len(grid)):
        if  grid[i][0]**2+grid[i][1]**2 <= new_rad**2:
            inside_ind.append(i)

    new_grid = np.delete(grid, inside_ind, axis = 0)

    inside_ind = []
    for i in range(len(new_grid)):
        for j in range(len(circle)):
            dis = np.linalg.norm(new_grid[i] - circle[j])
            if dis <= eps:
                inside_ind.append(i)

    last_grid = np.delete(new_grid, inside_ind, axis = 0)

    return last_grid

def pbc_min_dist(pos, box):
    '''
    Compute the minumum distance of an array of 3d positions with itself
    taking into considerations periodic boundary conditions given a box
    '''

    n = len(pos)
    r_mins = []
    for i in range(n):
        vectors = np.remainder(pos[i] - pos + box[0]/2.0, box[0]) - box[0]/2.0
        rs = np.linalg.norm(vectors, axis = 1)
        r_mins.append(np.min(rs[rs != 0]))
    return r_mins

def main():
    spacing = 3.636
    length = 54.54
    extend = length / 2
    height = 4*spacing
    radius = float(sys.argv[1])
    grid = generate_grid(spacing, length)
    circle, new_rad = generate_circle(radius, spacing)
    print(radius, new_rad)
    eps = float(sys.argv[2])

    final_grid = remove_grid_atoms(grid, circle, new_rad, spacing, eps)

    # Bring all necessary components for output into a tinker xyz

    lines = []
    zs = np.arange(-height/2, height/2+spacing, spacing)

    for z in zs: 
        for point in circle:
            lines.append(f"{'CA':6s}{point[0]+spacing/2:12.6f}{point[1]+spacing/2:12.6f}{z:12.6f}{1:6d}\n")
            
    for z in [zs[0],zs[-1]]:
        for point in final_grid:
            lines.append(f"{'CA':6s}{point[0]+spacing/2:12.6f}{point[1]+spacing/2:12.6f}{z:12.6f}{1:6d}\n")

    # Write tinker xyz

    with open(f"rad_{radius}.xyz", "w") as f:
        f.write(f"{len(lines):8d}\n")
        for line in lines:
            f.write(line)

    # read positions of xyz to output PDB

    data = np.loadtxt(f"rad_{radius}.xyz", skiprows=1, usecols=[1,2,3])
    N = len(data)

    # write PDB

    out_pdb = open(f"rad_{radius}.pdb", "w")
    box = [length+spacing,length+spacing,length+spacing]
    translated = data + length / 2
    write_pdb(out_pdb, box, translated)
    out_pdb.close()

    min_dists = pbc_min_dist(translated, box)
    info = f"N: {N:5d} / Min: {np.min(min_dists):5.3f} / Max: {np.max(min_dists):5.3f} / Ave: {np.mean(min_dists):5.3f}"
    print(info)

    fig = plt.figure(figsize = (8,8))
    plt.scatter(data[:, 0], data[:,1], c=np.array(min_dists)-spacing, cmap='seismic', edgecolor = 'k', clip_on = False, s = 80, vmin = -0.5, vmax = 0.5)
    plt.xticks([])
    plt.yticks([])
    plt.xlim(-extend+spacing/2,extend+spacing/2)
    plt.ylim(-extend+spacing/2,extend+spacing/2)
    plt.title(info, color = 'white')
    plt.savefig(f"2d_grid_{radius}.png", bbox_inches = 'tight', dpi = 120, transparent=True)

if __name__ == '__main__':
    main()