import matplotlib.pyplot as plt
from matplotlib import figure as fg
import numpy as np

def zoom_factory(base_scale=2.):
    prex = 0
    prey = 0
    prexdata = 0
    preydata = 0
    max_iter = 25    
    
    npts = 300
    max_iter = 100
    x_lin = np.linspace(-2, 1, 2 * npts)
    y_lin = np.linspace(-1, 1, npts)
    
    #broadcast X to a square array
    c_arr = x_lin[:, None] + 1J * y_lin
    #initial value is always zero
    z_arr = np.zeros_like(c_arr)
    
    exit_times = max_iter * np.ones(c_arr.shape, np.int32)
    mask = exit_times > 0
    
    for k in range(max_iter):
        z_arr[mask] = z_arr[mask] * z_arr[mask] + c_arr[mask]
        mask, old_mask = abs(z_arr) < 2, mask
        #use XOR to detect the area which has changed 
        exit_times[mask ^ old_mask] = k
    
    fig = plt.figure()
    ax = fig.subplots()
    
    ax.imshow(exit_times.T,
           cmap=plt.cm.twilight_shifted,
           extent=(x_lin.min(), x_lin.max(), y_lin.min(), y_lin.max()),
           data = exit_times.T)
    
    
    def zoom_fun(event):
        nonlocal prex, prey, prexdata, preydata, max_iter, npts, ax, x_lin, y_lin, c_arr, z_arr
        curx = event.x
        cury = event.y
        # if not changed mouse position(or changed so little)
        # remain the pre scale center
        if abs(curx - prex) < 10 and abs(cury - prey) < 10:
            # remain same
            xdata = prexdata
            ydata = preydata
        # if changed mouse position ,also change the cur scale center
        else:
            # change
            xdata = event.xdata  # get event x location
            ydata = event.ydata  # get event y location

            # update previous location data
            prex = event.x
            prey = event.y
            prexdata = xdata
            preydata = ydata
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()

        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
        cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
        # cur_npts = npts
        # cur_max_iter = max_iter
        # log.debug((xdata, ydata))
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
            max_iter += 75
            npts += 100
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
            max_iter -= 75
            npts -= 100
        else:
            # deal with something that should never happen
            scale_factor = 1
            max_iter = 100
            npts = 300
            print(event.button)
        # set new limits
        ax.set_xlim([
            xdata - cur_xrange * scale_factor,
            xdata + cur_xrange * scale_factor
        ])
        ax.set_ylim([
            ydata - cur_yrange * scale_factor,
            ydata + cur_yrange * scale_factor
        ])
        x_lin = np.linspace(-2, 1, 2 * npts)
        y_lin = np.linspace(-1, 1, npts)
            #broadcast X to a square array
        c_arr = x_lin[:, None] + 1J * y_lin
        #initial value is always zero
        z_arr = np.zeros_like(c_arr)
    
        exit_times = max_iter * np.ones(c_arr.shape, np.int32)
        mask = exit_times > 0
        
        for k in range(max_iter):
            z_arr[mask] = z_arr[mask] * z_arr[mask] + c_arr[mask]
            mask, old_mask = abs(z_arr) < 2, mask
            #use XOR to detect the area which has changed 
            exit_times[mask ^ old_mask] = k
             
        fig.canvas.draw()  # force re-draw
    fig = ax.get_figure()  # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event', zoom_fun)
    # return the function
    return zoom_fun


# npts = 300
# max_iter = 100
 
# X = np.linspace(-2, 1, 2 * npts)
# Y = np.linspace(-1, 1, npts)
 
# #broadcast X to a square array
# C = X[:, None] + 1J * Y
# #initial value is always zero
# Z = np.zeros_like(C)
 
# exit_times = max_iter * np.ones(C.shape, np.int32)
# mask = exit_times > 0
 
# for k in range(max_iter):
#     Z[mask] = Z[mask] * Z[mask] + C[mask]
#     mask, old_mask = abs(Z) < 2, mask
#     #use XOR to detect the area which has changed 
#     exit_times[mask ^ old_mask] = k
    
    
# fig = plt.figure()
# ax = fig.subplots()

# ax.imshow(exit_times.T,
#            cmap=plt.cm.twilight_shifted,
#            extent=(X.min(), X.max(), Y.min(), Y.max()),
#            data = exit_times.T)

scale = 1.5
f = zoom_factory(base_scale=scale)

plt.show()





# n = 1000
# img = visual(n, threshold=4, max_iter=150)
# # print(img)
# fig = plt.figure()
# ax = fig.add_subplot(111,xlim=(0,n),ylim=(0,n),autoscale_on=False)
# im = ax.imshow(img, cmap='magma')
# scale = 1.5
# f = zoom_factory(ax, base_scale=scale)
# plt.show()


# def get_iter(c:complex, threshold=4, max_iter:int=25):
#     z = c
#     i = 1
#     while i < max_iter and (z * z.conjugate()).real < threshold:
#         z = z * z + c
#         i += 1
#     return i

# def visual(n, threshold, max_iter=25):
#     mx = 2.48 / (n-1)
#     my = 2.46 / (n-1)
#     mapper = lambda x, y: (mx*x-2, my*y-1.13)
#     drawing = np.full((n, n), 255)
#     for x in range(n):
#         for y in range(n):
#             iter = get_iter(complex(*mapper(x,y)), threshold=threshold, max_iter=max_iter)
#             drawing[y][x] = 255 -iter
#     return drawing


# n = 1000
# img = visual(n, threshold=4, max_iter=150)
# # print(img)
# fig = plt.figure()
# ax = fig.add_subplot(111,xlim=(0,n),ylim=(0,n),autoscale_on=False)
# im = ax.imshow(img, cmap='magma')
# scale = 1.5
# f = zoom_factory(ax, base_scale=scale)
# plt.show()
