import numpy as np


def get_centroid(obj):
    o = obj.sum(axis=0) / len(obj)

    return o[0][0], o[0][1]


def normalization(x, y):
    x_norm = np.interp(x, (-np.pi, np.pi), (0, 127)).astype(np.float)
    y_norm = np.interp(y, (0, max(y)), (0, 127)).astype(np.float)
    x_vals, y_interp = linear_interpolation(x_norm, y_norm)
    # plt.plot(x_norm, y_norm, 'v')
    # plt.plot(x_vals, y_interp, 'o')
    # plt.plot(x_vals.astype(int), y_interp.astype(int), 'x')
    # plt.plot(x_vals.round(0), y_interp.round(0), '.')
    # plt.show()
    cd = np.zeros((128, 128), np.uint8)
    for i in range(0, 128):
        cdx = x_vals[i].astype(int)
        cdy = y_interp[i].astype(int)
        cd[127 - cdy][cdx] = 255

    return cd, x_vals, y_interp


def linear_interpolation(x, y):
    x_vals = np.linspace(0, 127, 128)
    y_interp = np.interp(x_vals, x, y)

    return x_vals, y_interp


def fourier_transform(d):
    after_transformation = np.abs(np.fft.fft(d))
    return after_transformation[1:]


def log_pol_fourier_transform(obj):
    x, y = log_pol_transform(obj)
    _, x_norm, y_norm = normalization(y, x)
    distances = fourier_transform(y_norm)

    return distances


def unl_fourier_transform(obj):
    x, y = unl_transform(obj)
    cd, x_norm, y_norm = normalization(y, x)
    distances = fourier_transform(y_norm)

    return distances


def log_pol_transform(obj):
    p = np.zeros(len(obj))
    w = np.zeros(len(obj))
    ox, oy = get_centroid(obj)
    for i in range(len(obj)):
        nx = obj[i][0][0] - ox
        ny = obj[i][0][1] - oy
        p[i] = np.log10(np.sqrt(np.power(nx, 2) + np.power(ny, 2)))
        w[i] = np.arctan2(ny, nx)
    w, p = zip(*sorted(zip(w, p)))

    return p, w


def unl_transform(obj):
    p = np.zeros(len(obj))
    ox, oy = get_centroid(obj)
    for i in range(len(obj)):
        nx = obj[i][0][0] - ox
        ny = obj[i][0][1] - oy
        p[i] = np.sqrt(np.power(nx, 2) + np.power(ny, 2))

    distance_max = p.max()
    w = []
    p = []
    for idx in range(len(obj)-1):
        p0 = obj[idx]
        p1 = obj[idx+1]

        samples_num = 10
        for t in np.linspace(0.0, 1.0, samples_num):
            r_n = r_norm_t(t, [p0, p1], [ox, oy], distance_max)
            a = angle_t(t, [p0, p1], [ox, oy])
            w.append(a)
            p.append(r_n)

    w, p = zip(*sorted(zip(w, p)))

    return p, w


def angle_t(t, segment, center):
    (x0, y0) = segment[0][0]
    (x1, y1) = segment[1][0]
    (cx, cy) = center
    return np.arctan2(y0 + t*(y1 - y0) - cy, x0 + t*(x1 - x0) - cx)


def r_t(t, segment, center):
    (x0, y0) = segment[0][0]
    (x1, y1) = segment[1][0]
    (cx, cy) = center

    a = x0 + t*(x1 - x0) - cx
    b = y0 + t*(y1 - y0) - cy
    r = np.sqrt(a*a + b*b)

    return r


def r_norm_t(t, segment, center, distance_max):
    return r_t(t, segment, center) / distance_max
