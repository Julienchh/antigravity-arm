

# 📖 Report
## ⁉️ Specifications

First, let us introduce the ins and outs of the subject at hand: the anti-gravity arm. That is, we present what was demanded of us and why, and what was expected to come out of this work.

### Context 

This project was conducted in the context of the development of the robot Reachy, created by Pollen Robotics. This humanoid robot aimed to be **interacting with humans**, which poses **security problematics**. Indeed, the arms of the Reachy are articulated using Dynamixel servomotors ; those are controlled using position command which uses maximum torque. Thus, the positioning of both arms may cause injuries if done improperly. To solve such issues, a **control using torque command** can be implemented. That is why the project was proposed to us.

### Existing matter

A complete model of the Reachy was lent to us for this project. The main developper on this part of the project, Remi Fabre, also gave us a link to a repository of a [firmware](https://github.com/RhobanProject/Dynaban) he, and some other developers of the Rhoban team, developed a few years ago.

During this project, we will use the **motors** of the Reachy's shoulder (**MX-64** and **MX-106**), and the **pypot python library**. 

### Goal 

We implemented an **anti-gravity "finger"**, that is a one degree of freedom arm. Because of a lack of time, we are only able to give leads for the implementation of a two-degree of freedom solution. The **expected output** is a program that when launched, enables position control with torque command on the finger.

## 🔎 Implemented approch

Now, let's focus on the science which the project is based off ; on one hand, the project has been implemented following specific mathematical models. On a second hand, some constants appearing in the models priorly defined are to be emprically computed. A section containing all the notations is at disposal.

### 📑 Notations


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

### 📐 The mathematics behind it all 

The finger is crafted with a Dynamixel motor MX-106. Attached to its shaft is a metal ruler of known dimensions $l\times L \times e$ and mass $m$.

The situation can be modelled as a rectangular prism attached to its end to the motor shaft as presented on the following figure :

<div style='text-align: center;'>
<img width=380 src='../../assets/Rotation_barre_position_vitesse_angulaire.svg'></img>
<p>Figure of the model</p>
</div>

The torque needed by the motor to overcome gravity is the following :
$$T_m = T_s + T_f$$

where $T_s$ and $T_f$ are respectively the inertial torque and the friction torque.

In this situation, the intertial torque is the following:

$$T_s = -m\ g\ R\ cos(q)$$

where $R$ is the center of mass. This one can also be expressed along the following equation :

$$R = \dfrac{1}{m} {\int\int\int}_V \rho(r)r\mathrm{d}V $$

In the case of a homogeneously distributed ruler, one gets the following:

$$\dfrac{1}{m} {\int\int\int}_V \rho(r)r\mathrm{d}V = \dfrac{el\rho}{m} \int_0^L r\mathrm{d}r = \dfrac{L}{2}$$

So the actual inertial torque in this model can be expressed as follows:

$$T_s = -m\ g\ \dfrac{L}{2} cos(q)$$

The friction torque can be modelled according to different models, more or less complex. We decided to go for the Coulomb-Stribeck equation which is composed of two main compounds : a term combining the two types of Coulomb friction, that is stiction and dynamic friction ; and a term for viscous friction. The equation is the following:

$$T_{f}=f_{C}\operatorname{sgn}({\omega})+(f_{s}-f_{C})e^{-\left({\omega}/{\omega_s}\right)^{2}}+b{\omega} 
$$

Notably, the viscous friction torque at a constant non-zero speed can be expressed as follows :

$$T_m = b \omega$$

### ⚙️ The motor caracterization


Describe your **approach** and how you proceeded to solve the problems reported by the client
 the work to solve this problem.

Add links to relevant sections to your user documentation and developer documentation but do not duplicate information.

## 📈 Analysis of results

**Qualify** and **quantify** your achievements. Make measurements from your work, e.g.:

* **User tests**: Setup a methodology to test the efficiency of your project against users. It may use pre-experiment and post-experiment questionnaires. The most users the better to draw meaningful conclusions from your experiments. Radar diagrams are good to summarize such results.
* **Table of data**: Provide (short) extracts of data and relevant statistics (distribution, mean, standard deviation, p-values...)
* **Plots**: Most data are more demonstrative when represented as plots. 

Draw conclusions, **interpret** the results and make recommandations to your client for your future of the work.
It is totally fine to have results that are not as good as initially expected. Be honest and analyse why you did not manage to reach the objectives.
