import matplotlib.pyplot as plt
import numpy as np


def mbrot(d, h, n, r, x_s, x_e, y_s, y_e):
    x = np.linspace(x_s, x_e, num=d+1)
    y = np.linspace(y_s, y_e*h/d, num=h+1)
    # x = np.linspace(0, 2, num=d+1)
    # y = np.linspace(0, 2*h/d, num=h+1)
    
    A, B = np.meshgrid(x - 1, y - h / d)
    C = 2.0 * (A + B * 1j) - 0.5
    
    Z = np.zeros_like(C)
    S = np.zeros(C.shape)
    
    for k in range(n):
        M = abs(Z) < r
        S[M] = S[M] + np.exp(-abs(Z[M]))
        Z[M] = Z[M] ** 2 + C[M]
    return S ** 0.1





def zoom_factory(base_scale=2.):
    prex = 0
    prey = 0
    prexdata = 0
    preydata = 0
    d = 800 #width
    h = 600 # height
    n = 100 #iterations
    r = 500 #escp radius
    x_s, x_e = 0, 2
    y_s, y_e = 0, 2
    if d == 800 and h == 600 and n == 100:
        frac = mbrot (d, h, n, r, x_s, x_e, y_s, y_e)  
    
    def zoom_fun(event):
        nonlocal prex, prey, prexdata, preydata, ax, d, n, h, r, x_s, x_e, y_s, y_e
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
        # cur_xlim = (x_s, x_e)
        # cur_ylim = (y_s, y_e)
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()

        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
        cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
        cur_n = n
        cur_r = r

        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
            # n = cur_n + 50
            # r = cur_r -35
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
            # n = cur_n - 50
            # r = cur_r + 75
        else:
            # deal with something that should never happen
            scale_factor = 1
            n = 100 #iterations
            r = 500 #escp radius
            print(event.button)
        # set new limits
        xl1, xl2 = xdata - cur_xrange * scale_factor, xdata + cur_xrange * scale_factor
        yl1, yl2 = ydata - cur_yrange * scale_factor, ydata + cur_yrange * scale_factor
        ax.set_xlim([xl1, xl2])
        ax.set_ylim([ yl1, yl2])

        x_s, x_e = xl1 , xl2
        y_s, y_e = yl1 , yl2 *h/d
        frac = mbrot(d, h, n, r, x_s, x_e, y_s, y_e)
        im.set_data(frac)     
        fig.canvas.draw_idle()  # force re-draw
        plt.pause(1)
    fig = plt.figure()
    ax = fig.subplots()
    im = ax.imshow(frac,
        cmap=plt.cm.twilight_shifted, interpolation = 'bicubic', data = frac,
           extent=(x_s, x_e, y_s, y_e))
    fig = ax.get_figure()  # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event', zoom_fun)
    # return the function
    return zoom_fun

scale = 1.2
f = zoom_factory(base_scale=scale)
plt.show()