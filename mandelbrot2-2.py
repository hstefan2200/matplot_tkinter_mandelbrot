import matplotlib.pyplot as plt
import numpy as np

def zoom_factory(base_scale=2.):
    prex = 0
    prey = 0
    prexdata = 0
    preydata = 0
    npts = 300 #width
    hpts = 200 # height
    max_iter = 100
    
    x_start,y_start = -2, -1.5
    # width,height = 3,3
    
    x_lin = np.linspace(x_start, abs(x_start), num = npts +1)
    y_lin = np.linspace(y_start, 2 * hpts/npts, num = hpts +1)
    
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
    
    def zoom_fun(event):
        nonlocal prex, prey, prexdata, preydata, max_iter, npts, ax, x_lin, y_lin, c_arr, z_arr,x_start,y_start,hpts
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
        x_start = np.int32(cur_xlim[0])
        cur_ylim = ax.get_ylim()
        y_start = np.int32(cur_ylim[0])

        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
        cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
        cur_npts = npts
        cur_max_iter = max_iter
        # log.debug((xdata, ydata))
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
            max_iter = cur_max_iter +25
            npts = cur_npts +50
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
            max_iter = cur_max_iter
            npts = cur_npts
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
        x_lin = np.linspace(x_start, abs(x_start), num = npts +1)
        y_lin = np.linspace(y_start, 2 * hpts/npts, num = hpts +1)
        # x_lin = np.linspace(x_start, x_start + width, width +1)
        # y_lin = np.linspace(y_start, y_start + height, height +1)
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
        im.set_data(exit_times.T)     
        fig.canvas.draw_idle()  # force re-draw
        plt.pause(1)
    fig = plt.figure()
    ax = fig.subplots()
    # if x_start == -2 and y_start == -1.5:
    im = ax.imshow(exit_times.T,
        cmap=plt.cm.twilight_shifted,
            extent=(x_lin.min(), x_lin.max(), y_lin.min(), y_lin.max()))#,
            #data = exit_times.T)
    fig = ax.get_figure()  # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event', zoom_fun)
    # return the function
    return zoom_fun

scale = 1.2
f = zoom_factory(base_scale=scale)
plt.show()