import math

from perlin_noise import PerlinNoise
import noise


class Noise:

    @staticmethod
    def simplex_noise(size: tuple):
        return Noise._noise_map(size=size, simplex=True)

    @staticmethod
    def perlin_noise(size: tuple, octaves: int, scale: int, persistence: float, lacunarity: float):
        return Noise._noise_map(size=size, octaves=octaves, scale=scale, persistence=persistence, lacunarity=lacunarity,
                                simplex=False)

    @staticmethod
    def _noise_map(size: tuple, octaves: int, scale: int, persistence: float,
                   lacunarity: float, simplex: bool = False):
        min_noise_val = math.inf
        max_noise_val = -math.inf

        noisemap = []
        for z in range(size[1]):
            row = []
            for x in range(size[0]):
                val = 0.0
                if simplex:
                    val = noise.snoise2(x / scale, z / scale)
                else:
                    val = noise.pnoise2(x / scale, z / scale, octaves=octaves, persistence=persistence,
                                        lacunarity=lacunarity)
                max_noise_val = max(max_noise_val, val)
                min_noise_val = min(min_noise_val, val)
                row.append(val)
            noisemap.append(row)

        for z in range(size[1]):
            for x in range(size[0]):
                noisemap[z][x] = (noisemap[z][x] - min_noise_val) / (max_noise_val - min_noise_val)

        return noisemap


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    noisemap = Noise.perlin_noise(size=(200, 200), octaves=6, scale=100, persistence=0.5, lacunarity=2.0)
    plt.figure()
    plt.imshow(noisemap, cmap='gray')
    imagemap = []
    for z in range(len(noisemap)):
        row = []
        for x in range(len(noisemap[0])):
            val = noisemap[z][x]
            if noisemap[z][x] < 0.3:
                row.append([92, 174, 204])
            elif noisemap[z][x] < 0.4:
                row.append([107, 202, 237])
            elif noisemap[z][x] < 0.5:
                row.append([245, 243, 181])
            elif noisemap[z][x] < 0.6:
                row.append([43, 189, 54])
            elif noisemap[z][x] < 0.8:
                row.append([33, 145, 41])
            elif noisemap[z][x] < 0.9:
                row.append([159, 148, 132])
            else:
                row.append([255, 255, 255])
        imagemap.append(row)
    plt.figure()
    plt.imshow(imagemap)
    plt.show()
