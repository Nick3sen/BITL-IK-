import matplotlib.pyplot as plt
import ikpy.utils.plot as plot_utils
target_position = [ 0, 0,0.46]

fig, ax = plot_utils.init_3d_figure()
fig.set_figheight(9)  
fig.set_figwidth(13)  
# my_chain.plot(ax, target=target_position)
plt.xlim(-0.5, 0.5)
plt.ylim(-0.5, 0.5)
ax.set_zlim(0, 0.6)
plt.show()
# plt.ion()

