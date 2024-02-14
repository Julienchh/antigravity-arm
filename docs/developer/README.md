# 📖 Developer Documentation

## ⁉️ Purpose of this Documentation

This documentation is intended for **future developers** re-using our work, such as students from subsequent years. Assuming you have similar proficiencies as us, this guide aims to provide insight into our code's structure and how new features can be integrated seamlessly.

## ⁉️ Overview of the Project

Our project introduces a high-level interface over the Dynamixel V2 firmware, specifically designed to enable direct current and PWM (Pulse Width Modulation) control. This interface facilitates advanced manipulation of Dynamixel actuators, particularly the MX_106 and MX_64 models, by providing a simplified and intuitive means to interact with these devices at a lower level than typically offered by the pypot python lib.

### Key Components

- **`control_tables.py`**: This file maps the control table addresses for the MX_106 and MX_64 models. This mapping is crucial for accessing and modifying the various parameters of the Dynamixel actuators, such as speed, position, and more, in a structured and understandable manner.

- **`lib.py`**: Contains all the low-level functions necessary for sending and receiving packets to and from the actuators. This includes functions to read and set PWM or current values. It's the backbone of our interface, handling the intricacies of communication with the actuators.
  
- **`compensation_lib.py`** : Define functions to compute gravity torque, friction torque (polynomial model and Stribeck model) and compensate gravity.

- **`compensation.py`**: Utilizes the functions defined in `lib.py` and `compensation_lib.py` to implement specific behaviors such as gravity compensation algorithms that adjust the actuators' performance in real-time. This file is where the high-level logic is applied, making use of the foundational elements defined in the other scripts to achieve the desired control over the actuators. 

## ⁉️ Extending the Project

### Adding New Features

When considering the extension of this project with new features, it's important to have a thorough understanding of the existing codebase, especially the functionalities provided by `lib.py` and the control table mappings in `control_tables.py`. New features might include additional control strategies, support for more Dynamixel models, or improvements to the communication efficiency with the actuators.

### Modifying Existing Code

Modifications to existing code should be approached with caution, ensuring that changes do not disrupt the current functionality. It is recommended to thoroughly test any modifications in a controlled environment before integrating them into the main project.