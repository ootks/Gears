from cmath import *
import pygame
import time

# Number of cricles to use
n_freqs = 2
# Number of samples to take for integral
n_samples = 4 * n_freqs

# Example function that produces a heart (the coordinates are complex).
def heart(t):
    return (16 * (sin(2 * pi *t) ** 3)) + (13 * cos(2 * pi * t) - 5 * cos(4 * pi * t) - 2 * cos(6 * pi * t) - cos(8 * pi *t)) * 1j

# Turns a complex number to a real pair
def c2p(c):
    return (int(c.real),int(c.imag))

# Displays a dot
def display(c, center):
    x = 10 * (c - center) + (750 + 750j)
    return c2p(x)

# Computes a single Fourier coefficient with a Riemann sum.
def fourier_coefficient(f, k, samples):
    return sum(exp(-2j * pi * k * t / samples) * f(t / samples) for t in range(samples))/samples

def fourier_reconstruction(f, max_freq, samples):
    fourier_coefficients = [fourier_coefficient(f, k, samples) for k in range(-max_freq, max_freq+1)]
    def g(t):
        return sum(coeff * exp(2j * pi * (k - max_freq) * t) for k, coeff in enumerate(fourier_coefficients))
    return g

g = fourier_reconstruction(heart, n_freqs, n_samples)
reconstruction = [g(t/1000) for t in range(1000)]

pygame.init()
screen = pygame.display.set_mode((1500, 1500))

center = sum(reconstruction[t] for t in range(-n_freqs, n_freqs)) / (2 * n_freqs)
print(center)

fourier_coefficients = [fourier_coefficient(heart, k, n_samples) for k in range(-n_freqs, n_freqs+1)]
print(list(zip(fourier_coefficients, range(-n_freqs, n_freqs + 1))))
print(list(zip([abs(z) for z in fourier_coefficients], range(-n_freqs, n_freqs + 1))))
print(fourier_coefficients)
print([abs(x) for x in fourier_coefficients])

def draw_circles(fourier_coefficients, t):
    point = fourier_coefficients[n_freqs]
    pygame.draw.circle(screen, (255,0,255), display(point, center), 2)
    color = (255, 0, 255)
    for j in range(1, n_freqs):
        coeff = fourier_coefficients[n_freqs + j + 1]
        pygame.draw.circle(screen, (255 / j,0,255/j), display(point, center), int(10*abs(coeff)), 1)
        point = point + coeff * exp(2j * pi * (j+1) * t)
        pygame.draw.circle(screen, (255/j,0,255/j), display(point, center), 2)

        coeff = fourier_coefficients[n_freqs - j]
        pygame.draw.circle(screen, (255/j,0,255/j), display(point, center), int(10*abs(coeff)), 1)
        point = point + coeff * exp(-2j * pi * j * t)
        pygame.draw.circle(screen, (255/j,0,255/j), display(point, center), 2)

    coeff = fourier_coefficients[n_freqs - j]
    pygame.draw.circle(screen, (255/j,0,255/j), display(point, center), int(10*abs(coeff)), 1)
    point = point + coeff * exp(-2j * pi * j * t)
    pygame.draw.circle(screen, (255/j,0,255/j), display(point, center), 2)


trace = []
for t in range(1000):
    screen.fill((0,0,0))
    draw_circles(fourier_coefficients, t/1000)
    trace.append(reconstruction[t])
    for t in trace:
        pygame.draw.circle(screen, (0,255,0), display(t, center), 2)
    pygame.display.flip()
    time.sleep(0.01)
