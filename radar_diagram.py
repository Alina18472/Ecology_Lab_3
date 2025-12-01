#radar_diagram.py

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


class RadarDiagram:
    def radar_factory(self, num_vars, frame='circle'):
        theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

        class RadarAxes(PolarAxes):

            name = 'radar'
            RESOLUTION = 1

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.set_theta_zero_location('N')

            def fill(self, *args, closed=True, **kwargs):
                return super().fill(closed=closed, *args, **kwargs)

            def plot(self, *args, **kwargs):
                lines = super().plot(*args, **kwargs)
                for line in lines:
                    self._close_line(line)

            def _close_line(self, line):
                x, y = line.get_data()
                if x[0] != x[-1]:
                    x = np.append(x, x[0])
                    y = np.append(y, y[0])
                    line.set_data(x, y)

            def set_varlabels(self, labels):
                self.set_thetagrids(np.degrees(theta), labels)

            def _gen_axes_patch(self):
                if frame == 'circle':
                    return Circle((0.5, 0.5), 0.5)
                elif frame == 'polygon':
                    return RegularPolygon((0.5, 0.5), num_vars,
                                          radius=.5, edgecolor="k")
                else:
                    raise ValueError("Unknown value for 'frame': %s" % frame)

            def _gen_axes_spines(self):
                if frame == 'circle':
                    return super()._gen_axes_spines()
                elif frame == 'polygon':
                    spine = Spine(axes=self,
                                  spine_type='circle',
                                  path=Path.unit_regular_polygon(num_vars))
                    spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                        + self.transAxes)
                    return {'polar': spine}
                else:
                    raise ValueError("Unknown value for 'frame': %s" % frame)

        register_projection(RadarAxes)
        return theta

    def draw(self, filename, initial_data, current_data, label, title, restrictions=None, show_both_lines=True):
        N = len(initial_data)
        theta = self.radar_factory(N, frame='polygon')

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='radar'))
        fig.subplots_adjust(top=0.85, bottom=0.05)

        ax.set_ylim(0, 1.0)

        if restrictions is not None:
            if len(restrictions) != N:
                raise ValueError(f"Длина restrictions ({len(restrictions)}) не совпадает с числом переменных ({N})")
            limit_line = restrictions
        else:
            limit_line = [1.0] * N

        ax.plot(theta, limit_line, color='green', linewidth=2, linestyle='--', alpha=0.7, label="Предельные значения")

        if show_both_lines:
            ax.plot(theta, initial_data, color='red', linewidth=2, label="Начальные потери")
            ax.plot(theta, current_data, color='blue', linewidth=2, label="Текущие потери")
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize='small')
        else:
            ax.plot(theta, initial_data, color='red', linewidth=2, label="Начальные потери")
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), fontsize='small')

        # Измененные метки для экологической модели
        var_labels = ["Cf1", "Cf2", "Cf3", "Cf4", "Cf5"]
        ax.set_varlabels(var_labels)

        fig.text(0.5, 0.965, title, horizontalalignment='center', color='black', weight='bold', size='large')
        fig.savefig(filename, bbox_inches='tight')
        plt.close(fig)