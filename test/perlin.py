import math

from perlin_noise import PerlinNoise


class Noise:
    @staticmethod
    def noise_map(size: tuple, seed: int, octaves: int, scale: int):
        noise1 = PerlinNoise(octaves=octaves, seed=seed)
        noise2 = PerlinNoise(octaves=octaves*2, seed=seed)
        noise3 = PerlinNoise(octaves=octaves*4, seed=seed)
        noise4 = PerlinNoise(octaves=octaves*8, seed=seed)

        min_noise_val = math.inf
        max_noise_val = -math.inf

        noisemap = []
        for z in range(size[1]):
            row = []
            for x in range(size[0]):
                noise_val = noise1([x/scale, z/scale])
                noise_val += 0.5 * noise2([x/scale, z/scale])
                noise_val += 0.25 * noise3([x/scale, z/scale])
                noise_val += 0.125 * noise4([x/scale, z/scale])
                row.append(noise_val)

                min_noise_val = min(noise_val, min_noise_val)
                max_noise_val = max(noise_val, max_noise_val)
            noisemap.append(row)

        for z in range(size[1]):
            for x in range(size[0]):
                noisemap[z][x] = (noisemap[z][x] - min_noise_val)/(max_noise_val-min_noise_val)

        return noisemap


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    noisemap = Noise.noise_map(size=(100, 100), seed=1, octaves=3, scale=100)
    imagemap = []
    for z in range(len(noisemap)):
        row = []
        for x in range(len(noisemap[0])):
            if noisemap[z][x] < 0.4:
                row.append([92, 174, 204])
            elif noisemap[z][x] < 0.5:
                row.append([245, 243, 181])
            elif noisemap[z][x] < 0.8:
                row.append([111, 247, 120])
            else:
                row.append([255, 255, 255])
        imagemap.append(row)
    plt.imshow(imagemap)
    plt.show()

