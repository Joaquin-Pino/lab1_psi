
**IMPORTANTE**

Escribo el contenido del informe en un md por ahora para comodidad de trabajo mientras se realiza el código y avanzar el informe a la vez

## Tarea 1

### Deducción de la formula frecuencia_alias

El aliasing (o solapamiento) ocurre porque las funciones trigonométricas son periódicas. Se repiten infinitamente cada $2\pi$ radianes. Con esto en cuenta se realiza el siguiente paso a paso para deducir la formula utilizada:

1. Establecer la señal senoidal continua con una frecuencia $f$:
$$x(t) = \cos(2\pi f y)$$

2. Muestrearla en una frecuencia $f_s$ y remplazar el tiempo por saldos discretos $t=n/f_s$ (donde $n = 0, 1, 2,...$):
$$x[n] = \cos\left(2\pi f \frac{n}{f_s}\right)$$

3. Analizar el caso de borde, cuando $f$ es mayor que la frecuencia de muestreo (Frecuencia de Nyquist). Por ejemplo con $f_s = 10 Hz$ (Nyquist es $5 Hz$) y probar una frecuencia alta $f = 13 Hz$. Si reemplazamos en la formula tenemos que:
$$x[n] = \cos\left(2\pi (13) \frac{n}{10}\right) = \cos\left(2\pi \cdot 1.3 \cdot n\right)$$

4. El número $1.3$ se puede separar en un número entero y un decimal: $1.3 = 1 + 0.3$. Entonces:
$$\cos\left(2\pi (1 + 0.3) n\right) = \cos\left(2\pi n + 2\pi (0.3) n\right)$$

5. Este es el paso importante, la función coseno se repite cada vez que avanza un ciclo completo de $2\pi n $ radianes, por lo que el término $2\pi n $ desaparece de los valores que arroja la muestra, así quedando:

$$\cos\left(2\pi (0.3) n\right) = \cos\left(2\pi (3) \frac{n}{10}\right)$$

Con esto podemos observar como tras una simplificación matemática una señal senoidal de $13 Hz$ muestreda a $10 Hz$ produce exactamente los mismo valores que una señal de $3 Hz$.

Esta demostración es para considerar que la frecuencia alias va a dar los mismos resultados al muestrear senoidales de $f ∈ {3, 7, 13, 23} Hz$ con $fs = 10 Hz.$

Con esto en cuenta comenzamos a hacer la formula de la frecuencia alias aparente en $[0,f_s/2]$.

1. Realizar el recorte a la frecuencia
$$f % f_s$$

2. Aplicar desplazamiento para que el "reflejo" de la señal coincida con el recorte
$$(f + f_s/2) \% f_s$$

3. Devolver la escala a su posición original restando el desplazamiento

$$(f + f_s/2) \% f_s - f_s/2$$

4. Aplicar valor absoluto para dejar toda la señal en el lado positivo para tener valores coherentes, una frecuencia negativa no existe. Así dando la formula resultante:

$$|(f + f_s/2) \% f_s - f_s/2|$$

La cual en python sería: np.abs((f + fs / 2) % fs - fs / 2)
