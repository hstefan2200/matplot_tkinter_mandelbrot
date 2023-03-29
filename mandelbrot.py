import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

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
# img = visual(n, threshold=4, max_iter=50)

# fig = plt.figure()
# ax = fig.add_subplot(111,xlim=(0,n),ylim=(0,n),autoscale_on=False)
# ax.imshow(img, cmap='plasma')
# # ax = plt.imshow(img, cmap='plasma')
# # plt.axis('off')
# scale = 1.5
# f = zoom_factory(ax, base_scale=scale)
# plt.show()
def zoom_factory(im, base_scale=2.):
    prex = 0
    prey = 0
    prexdata = 0
    preydata = 0
    # max_iter = 25
    def zoom_fun(event):
        nonlocal prex, prey, prexdata, preydata
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
        cur_xlim = im.get_xlim()
        cur_ylim = im.get_ylim()

        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
        cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
        # log.debug((xdata, ydata))
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1 / base_scale
            # max_iter += 10
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = base_scale
            # max_iter -= 10
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)
        # set new limits
        im.set_xlim([
            xdata - cur_xrange * scale_factor,
            xdata + cur_xrange * scale_factor
        ])
        im.set_ylim([
            ydata - cur_yrange * scale_factor,
            ydata + cur_yrange * scale_factor
        ])       
        ax.figure.canvas.draw()  # force re-draw
    fig = im.get_figure()  # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event', zoom_fun)
    # return the function
    return zoom_fun
#progressive animation

def get_iter(x, y, threshold):
    c = complex(x, y)
    z = complex(0, 0)
    for i in range(threshold):
        z = z**2 + c
        if abs(z) > threshold:
            return i
    return threshold - 1
x_start,y_start = -2, -1.5
width,height = 3,3
# density = 250

def get_lin(density):
    re = np.linspace(x_start, x_start + width, width * density)
    im = np.linspace(y_start, y_start + height, density)
    return re, im

fig = plt.figure()#figsize=(10,10))
ax = plt.axes()
scale = 1.5
f = zoom_factory(ax, base_scale=scale)

# def onevent(event):
#     density = 250
#     if event.button == 'up':
#         density += 25
#     elif event.button == 'down':
#         density -= 25
#     else:
#         density = 250
#     re, im = get_lin(density)
    
def animate(i):

    # ax.clear()
    ax.set_xticks([], [])
    ax.set_yticks([], [])
    re, im = get_lin(600)
    X = np.empty((len(re), len(im)))
    threshold = round(1.15**(i + 1))
    for i in range(len(re)):
        for j in range(len(im)):
            X[i, j] = get_iter(re[i], im[j], threshold)
    img = ax.imshow(X.T, cmap='magma')
    return [img]

    # anim = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
    fig.canvas.draw_idle()
anim = animation.FuncAnimation(fig, animate, frames=45, interval=25, blit=True, repeat=False)
# test = fig.canvas.mpl_connect('scroll_event', onevent)

plt.show()

# plt.rcParams["animation.convert_path"] = "C:\Program Files\ImageMagick-7.1.0-Q16-HDRI\magick.exe"
# anim.save('mandelbrot.gif', writer='imagemagick', extra_args="convert")




