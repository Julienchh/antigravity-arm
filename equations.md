# Notations


|Symbole        |Definition     |Unit         
|---------------|---------------|------------
$PWM$ | PWM peak duty cycle | $\%$ 
$U$ | Motor tension | $V$ 
$U_{alim}$ | Power supply tension | $V$ 
$i$ | Current intensity in the motor | $
$e$ | Back EMF | $V$ 
$R$ | Motor resistance | $\Omega$ 
$K_m$ | Motor torque constant | $V.s.rad^{-1}$ 
$\omega$ | Angular velocity | $rad.s^{-1}$ 
$\omega_s$ | Stribeck velocity | $rad.s^{-1}$ 
$T_m$ | Motor torque | $N.m$ 
$T_s$ | Inertial torque | $N.m$ 
$T_f$ | Friction torque | $N.m$ 
$f_s$ | Stiction torque | $N.m$
$f_C$ | Dynamic friction torque | $N.m$
$b$ | Viscous friction constant | $kg.m^2.s^{-1}$
$J_\Delta$ | Moment of inertia of the solid | $kg \cdot m^2$ 
$V$ | Solid's volume | $m^3$ 
$r_\Delta$ | Distance to each point from the solid's rotation axis $\Delta$ | $m$ 
$\rho$ | Material density | $kg.m^{-3}$ 
$m$ | Arm mass | $kg$ 
$dm$ | Elementary mass | $kg$ 
$l$ | Solid's height | $m$ 
$e$ | Solid's thickness | $m$ 
$L$ | Solid's length | $m$ 


# Gravity compensation

## Physics model

### Moment of inertia of the solid

$$J_\Delta = \int_V r^2 dm$$

$r$ being the distance of each point from the solid's rotation axis $\Delta$.

$$J_\Delta = \rho le \left[ \frac{x^3}{3} \right]^L_0 = \rho le \frac{L^3}{3} = \frac{mL^2}{3}$$

### Inertial torque

$$T_s = -m\ g\ L\ cos(q)$$


### Friction torque

$$T_{f}=f_{C}\operatorname{sgn}({\omega})+(f_{s}-f_{C})e^{-\left({\omega}/{\omega_s}\right)^{2}}+b{\omega} 
$$

### Viscous friction (at a constant non-zero speed)

$$T_m = b \omega$$

### Center of mass

$$R = \dfrac{1}{m} {\int\int\int}_V \rho(r)r\mathrm{d}V $$

In the case of a homogeneously distributed ruler, one gets the following:

$$\dfrac{1}{m} {\int\int\int}_V \rho(r)r\mathrm{d}V = \dfrac{el\rho}{m} \int_0^L r\mathrm{d}r = \dfrac{L}{2}$$
### Motor torque

$$T_m = T_s + T_f$$


## Electronics model
### Back EMF
$$e = K_m \omega_m $$

### Tension command

$$ U = \dfrac{R T_m}{K_m} + e $$

### Current command

$$ i = \dfrac{T_m}{K_m} $$