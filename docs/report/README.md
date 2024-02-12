

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


### The mathematics behind it all

### The motor caracterization


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
