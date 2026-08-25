# Auditoría algebraica, slips y extensiones

Este documento contiene el álgebra deliberadamente omitida del README.

## 1. Tecnología especializada y solución interior

La sección 4 usa

$$
p(se;\theta)=\sqrt{se+\theta},\qquad c(e)=e.
$$

El agente maximiza (M(e;\theta)=\alpha\Delta\sqrt{se+\theta}-e). La condición de primer orden produce

$$
e^*(\theta)=\frac{\alpha^2\Delta^2s}{4}-\frac{\theta}{s},
\qquad
M(\theta)=\frac{\alpha^2\Delta^2s}{4}+\frac{\theta}{s}.
$$

Con (gamma(0)=gamma_0) y (gamma(t)=gamma) para (t>0),

$$
\Gamma=\frac{\gamma_0}{1-\delta\gamma},
\qquad
V(\theta)=\Gamma\left(\frac{\alpha^2\Delta^2s}{4}+\frac{\theta}{s}\right).
$$

## 2. Media y varianza

Bajo independencia,

$$
\frac{d\mathbb E[V(\theta)]}{d\theta}
=\mathbb E[\Gamma]\mathbb E[1/s]>0.
$$

Escriba (M(\theta)=A+\theta/s), con (A=\alpha^2\Delta^2s/4). Como (Gamma) es independiente de (M),

$$
\operatorname{Var}(V)=\mathbb E[\Gamma^2]\operatorname{Var}(M)
+\operatorname{Var}(\Gamma)\mathbb E[M]^2.
$$

Al derivar y simplificar:

$$
\frac{d}{d\theta}\operatorname{Var}[V(\theta)]
=a_0+2\theta\operatorname{Var}(\Gamma/s),
$$

$$
a_0=\frac{\Delta^2\mathbb E[\alpha^2]}{2}
\left\{\mathbb E[\Gamma^2]
-\mathbb E[\Gamma]^2\mu_s\mathbb E[1/s]\right\}.
$$

La condición (30) equivale a (a_0<0). Si (operatorname{Var}(\Gamma/s)>0), el mínimo único es

$$
\theta^*=\frac{\Delta^2\mathbb E[\alpha^2]}{4}
\frac{\mathbb E[\Gamma]^2\mu_s\mathbb E[1/s]-\mathbb E[\Gamma^2]}
{\operatorname{Var}(\Gamma/s)}.
$$

## 3. Dos objetos distintos

La Proposición 3 estudia (operatorname{Var}[V_i(\theta)]). En cambio,

$$
B_i(\theta)=V_i(\theta)-V_i(0)=\theta\Gamma_i/s_i,
\qquad
\operatorname{Var}[B_i(\theta)]=\theta^2\operatorname{Var}(\Gamma/s).
$$

La primera puede tener U; la segunda crece para (	heta>0).

## 4. Slip de la ecuación (32)

La condición (30) garantiza pendiente negativa en cero y (	heta^*>0). Para pendiente positiva en uno también se necesita

$$
a_0+2\operatorname{Var}(\Gamma/s)>0
\quad\Longleftrightarrow\quad
\theta^*<1.
$$

`sim.py` usa uniformes independientes:

$$
\alpha\sim U[0.9,1.1],\ s\sim U[0.7,1.3],\
\gamma_0\sim U[0.6,0.9],\ \gamma\sim U[0.2,0.5],
$$

con (delta=0.8) y (Delta\approx6.77716). Se obtiene

$$
1.022930<1.031732,
\quad \theta^*\approx1.7007,
\quad \operatorname{Var}'[V(1)]\approx-0.09239.
$$

La condición (30) se cumple, pero la pendiente sigue negativa en uno. El límite interior común es (4.5574), mayor que el punto de giro.

## 5. Positividad e inconsistencia de dominio

La solución interior real exige

$$
e^*(\theta)>0
\Longleftrightarrow \alpha^2\Delta^2s^2>4\theta.
$$

El paper declara (Delta>2/(s\sqrt{\alpha})), que no coincide con esta condición y omite (	heta). Con parámetros fijos no puede haber interioridad para todo (	heta\in[0,\infty)). Además, (sqrt{se+\theta}) puede exceder uno aunque (p) se defina como probabilidad.

Fuera del interior:

$$
e^*(\theta)=\max\left\{\frac{\alpha^2\Delta^2s}{4}-\frac{\theta}{s},0\right\},
$$

y las fórmulas lineales usadas por la Proposición 3 dejan de aplicar.

## 6. Salvedades de la Proposición 2

Para

$$
\Gamma=\sum_{k\ge0}\delta^k\prod_{i=0}^{k}\gamma(i),
$$

la derivada correcta es

$$
\frac{\partial\Gamma}{\partial\gamma(t)}
=\sum_{k=t}^{\infty}\delta^k
\prod_{\substack{i=0\\i\ne t}}^{k}\gamma(i).
$$

La Proposición 2(4) muestra solo el término (k=t) y omite efectos futuros; el apéndice sí contiene la suma. Además, (p_{s\theta}<0) a esfuerzo fijo no basta para comparar la ganancia óptima por habilidad, pues los dos estados evalúan (p_s) en esfuerzos diferentes. Hace falta single crossing o una condición global equivalente.

## 7. Casos límite

- (s) constante elimina la fuerza igualadora (1/s): la heterogeneidad de (Gamma) eleva la varianza.
- (Gamma) constante deja la U generada por habilidad heterogénea.
- Si (operatorname{Var}(\Gamma/s)=0), no hay U estricta.
- Fuera del rango interior común aparece una mezcla de soluciones interiores y esquinas; la cuadrática agregada ya no aplica.
