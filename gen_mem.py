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

def generate_rectangle(l, n):
    '''
    Function to create a rectangle of size l and  grid points n
    generated starting at the arrow and ending at the # in the
    direction the arrow points

    # > * * * *
    *         *
    *         *
    *         *
    *         *
    * * * * * *
    '''

    ext = l/2
    n_edge = n / 4
    s = l/n_edge 
    rectangle = []
    
    for i in range(n):
        k = (i%n_edge)+1
        if 0 <= i < n_edge:
            point = [-ext+(k*s), ext]
        if n_edge <= i < 2*n_edge:
            point = [ext, ext-(k*s)]
        if 2*n_edge <= i < 3*n_edge:
            point = [ext-(k*s), -ext]
        if 3*n_edge <= i < 4*n_edge:
            point = [-ext, -ext+(k*s)]
        
        rectangle.append(point)
    
    return np.array(rectangle)

def generate_circle(r, s, n):
    '''
    Function to generate a circle given a radius (r) and the spacing (s)
    if the number of points (n) is 0. If it is different then the spacing
    is computed for the number of given points starting the same way as the
    square on step to the right of 135 going anticlockwise and ending at 135
    '''

    if n == 0:
        a = 2*r*np.arcsin(s/(2*r)) # convert from spacing to arc length
        n = int(round(2*np.pi*r/a, 0))

    step = (2*np.pi / n)
    angles = np.linspace(3*np.pi/4-step, 3*np.pi/4-2*np.pi, n)
    x = r*np.cos(angles)
    y = r*np.sin(angles)
    circle = np.array(list(zip(x,y)))
    
    return circle

def generate_interpolation(lambdas, shape1, shape2):
    '''
    Interpolate between two shapes with the same number of points and correctly
    ordered using a set of lambdas
    '''

    curves = []
    for i in range(len(lambdas)):
        if i == 0:
            curves.append(shape1[i])
        else:
            lamb = lambdas[i]
            curve = []
            for j in range(len(shape1[i])):
                new_x = (1-lamb)*shape1[i][j][0]+lamb*shape2[i][j][0]
                new_y = (1-lamb)*shape1[i][j][1]+lamb*shape2[i][j][1]
                curve.append([new_x, new_y])
            curves.append(np.array(curve))
    return curves

def calculate_lambdas(size, exponent, exp_scale):
    '''
    Linear or exponential scaling between 0 and 1 
    '''

    lambdas = np.arange(0, 1+1/size, 1/size)
    if exp_scale == True: 
        lambdas = np.exp((1-1/(lambdas+1e-8)**exponent))
    return lambdas

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

    spacing = 1.875 # Minima of vdw CA-CA AlA
    length = 54.375 # Good size average 1.873
    extend = length / 2 
    main_radius = float(sys.argv[1])
    height = 7*1.875 # 13.125 A
    num_rects = len(np.arange(main_radius+spacing, length, spacing)) // 2
    num_points_grid = int(round(length / spacing, 0))

    # Create a set of rectangles of different size

    rectangles = []
    for i in range(num_rects,0,-1):
        tmp_length = length - 2*spacing*(i-1)
        tmp_points_grid = int(round(tmp_length / spacing, 0)) * 4
        rectangles.append(generate_rectangle(tmp_length, tmp_points_grid))
        
    # Create a set of circles of different size

    circles = []
    for i in range(num_rects):
        circle = generate_circle(main_radius+spacing*i, spacing, 0)
        #circle = generate_circle(main_radius+spacing*i, spacing, len(rectangles[i]))
        circles.append(circle)

    # Generate a linear set of lambdas

    lambdas = calculate_lambdas(len(circles)-1, 0, False)

    # Interpolate the number of grid points between analogous rectangles and
    # circles to try to keep a constant density

    num_points = []
    counter = 0
    for circ, rect, lamb in zip(circles, rectangles, lambdas):
        n_circ, n_rect = len(circ), len(rect)
        n_inter = int(round((1-lamb)*n_circ + lamb*n_rect,0))
        n_inter = n_inter - (n_circ-counter) // int(sys.argv[2])

        if n_inter % 4 != 0:
            #n_inter = n_inter + (-n_inter % 4) # round up to a multiple of 4
            n_inter = n_inter // 4 * 4  # round down to a multiple of 4
        num_points.append(n_inter)
        counter += 1

    # Using the new set of grid points generate new rectangles

    new_rectangles = []
    for i in range(num_rects,0,-1):
        tmp_length = length - 2*spacing*(i-1)
        tmp_points_grid = num_points[num_rects-i]
        new_rectangles.append(generate_rectangle(tmp_length, tmp_points_grid))
        
    # Using the new set of grid points generate new circles

    new_circles = []
    for i in range(num_rects):
        if i == 0:
            circle = generate_circle(main_radius+spacing*i, spacing, 0)
        else:
            circle = generate_circle(main_radius+spacing*i, spacing, num_points[i])
        new_circles.append(circle)

    # Interpolate between circles and rectangles 

    curves = generate_interpolation(lambdas, new_circles, new_rectangles)
    #curves = generate_interpolation(lambdas, circles, rectangles)

    # Bring all necessary components for output into a tinker xyz

    lines = []
    zs = np.arange(-height/2, height/2+spacing, spacing)

    for z in zs: 
        for point in curves[0]:
            lines.append(f"{'CA':6s}{point[0]+spacing/2:12.6f}{point[1]+spacing/2:12.6f}{z:12.6f}{1:6d}\n")
            
    for z in [zs[0],zs[-1]]:
        for curve in curves[1:]:
            for point in curve:
                lines.append(f"{'CA':6s}{point[0]+spacing/2:12.6f}{point[1]+spacing/2:12.6f}{z:12.6f}{1:6d}\n")

    # Write tinker xyz

    with open(f"rad_{main_radius}.xyz", "w") as f:
        f.write(f"{len(lines):8d}\n")
        for line in lines:
            f.write(line)

    # read positions of xyz to output PDB

    data = np.loadtxt(f"rad_{main_radius}.xyz", skiprows=1, usecols=[1,2,3])
    N = len(data)

    # write PDB

    out_pdb = open(f"rad_{main_radius}.pdb", "w")
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
    plt.savefig(f"2d_grid_{main_radius}.png", bbox_inches = 'tight', dpi = 120, transparent=True)

if __name__ == '__main__':
    main()