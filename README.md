# Autonomous Driving with Reinforcement Learning for First-Prioritizing Safety over Security

This project implements a reinforcement learning (RL) system to ensure **safety** and **security** in autonomous driving environments. It uses **Proximal Policy Optimization (PPO)** to train agents for safe driving behavior and for detecting and mitigating security threats such as **GPS spoofing** and **Man-in-the-Middle (MitM) attacks**. The system follows a **MAPE-K loop** to monitor, analyze, plan, and execute decisions based on environmental data and security threats.

## Table of Contents
- [Features](#features)
- [Setup](#setup)
- [Training](#training)
- [Running the MAPE-K Loop](#running-the-mape-k-loop)
- [Project Structure](#project-structure)

## Features
- **Safety Agent** trained to avoid collisions, maintain speed, and perform lane changes.
- **Security Agent** trained to detect and mitigate GPS spoofing and MitM attacks.
- **MAPE-K Loop** to dynamically adjust driving behavior and handle detected threats.
- Supports custom environments for simulating security threats.
- Parallelized training using `stable-baselines3` for efficient agent training.

## Setup

### 1- Clone the Repository
```bash
git https://github.com/Iamafshiin/SafeDriveRL.git
cd SafeDriveRL
```
### 2- Run this for installing requirements
```bash
pip install -r requirements.txt
```

## Training Explanation

This project uses **Proximal Policy Optimization (PPO)** to train two agents: a **Safety Agent** responsible for ensuring safe driving behavior, and a **Security Agent** designed to detect and respond to security threats such as GPS spoofing and Man-in-the-Middle (MitM) attacks.

### Safety Agent Training

The **Safety Agent** is trained using the `highway-v0` environment from `highway-env`. This environment simulates typical highway driving scenarios where the agent needs to learn:
- How to avoid collisions with other vehicles.
- How to stay within its lane and perform lane changes safely.
- How to maintain optimal speed and keep safe distances from surrounding vehicles.

The agent learns by receiving rewards for safe driving behaviors and penalties for risky behaviors such as collisions or lane violations. 

To train the **Safety Agent**, run the following script:

```bash
python train_safety_agent.py
```

### Security Agent Training

The **Security Agent** is responsible for detecting and responding to potential security threats, such as **GPS spoofing** and **Man-in-the-Middle (MitM) attacks**. The agent is trained using a custom-built environment called `SecurityEnvironment`, which simulates these threats in a controlled setting. The goal of the agent is to:
- **Detect GPS spoofing**: Identify when the GPS data has been manipulated or falsified.
- **Detect MitM attacks**: Recognize anomalies in communication data that might indicate a network-based attack.
- **Take appropriate action**: The agent needs to respond to the threats by taking defensive actions, such as alerting the system or initiating countermeasures.

#### How It Works

The agent receives observations from the environment that include indicators of potential attacks (e.g., abnormal GPS data or network anomalies). Based on these observations, the agent selects an action:
- Action 0: Do nothing (normal operation).
- Action 1: Detect and respond to GPS spoofing.
- Action 2: Detect and respond to MitM attack.

The agent receives **positive rewards** for correctly detecting and responding to security threats and **negative rewards** (penalties) for missing attacks or generating false positives.

#### Training Procedure

The **Security Agent** is trained using the **Proximal Policy Optimization (PPO)** algorithm, which learns from the environment by optimizing a policy to maximize long-term rewards. The PPO algorithm is well-suited for environments where agents need to continuously learn from interactions with dynamic environments.

To train the **Security Agent**, follow these steps:

**Run the training script**:
   
```bash
python train_security_agent.py
```

### Running the MAPE-K Loop

The **MAPE-K loop** (Monitor, Analyze, Plan, Execute, Knowledge) is a key component in this project, designed to dynamically adjust the behavior of the system based on observations from the environment. The loop integrates both the **Safety Agent** and **Security Agent** to ensure that the vehicle can handle normal driving tasks while simultaneously detecting and responding to potential security threats, such as GPS spoofing or MitM attacks.

#### Overview of the MAPE-K Loop

- **Monitor**: The loop continuously observes the environment and collects data about the current state of the vehicle, nearby obstacles, and potential security threats.
  
- **Analyze**: The system processes this data to determine if any anomalies or security threats have occurred. For example, it checks whether GPS data has been manipulated or whether there are signs of a network attack.
  
- **Plan**: Based on the analysis, the system decides on a course of action. If a security threat is detected, the system may modify the action suggested by the Safety Agent. For instance, if GPS spoofing is detected, the vehicle may slow down or switch to a backup localization system.
  
- **Execute**: The planned action is executed, either continuing the normal driving behavior suggested by the Safety Agent or overriding it based on the security analysis.
  
- **Knowledge**: Throughout the process, the system collects performance metrics, which can be used to further refine the agent's behavior over time. This helps the agents improve their decision-making in future episodes.

#### How to Run the MAPE-K Loop

Once both the Safety Agent and Security Agent have been trained, you can run the MAPE-K loop by executing the following command:

```bash
python main.py
```

## Project Structure

The project is organized into several scripts and directories that facilitate training, running simulations, and handling security threats in an autonomous driving environment. Below is the structure of the project:

```bash
SafeDriveRL/
│
├── README.md               # Project documentation
├── train_safety_agent.py    # Script to train the safety agent using PPO
├── train_security_agent.py  # Script to train the security agent for threat detection
├── main.py                  # Main script running the MAPE-K loop (integrating safety and security agents)
├── mapek_loop.py            # MAPE-K loop logic for adjusting actions based on analysis
├── security_env.py          # Custom security environment for simulating GPS spoofing and MitM attacks
├── models/                  # Directory to save trained models
│   ├── safety_ppo_model/    # Saved PPO model for the safety agent
│   └── security_ppo_model/  # Saved PPO model for the security agent
└── requirments.txt           
```

## Please cite this repo as follows:

```
Afshin Hasani, Mehran Alidoost Nia, Reza Ebrahimi Atani "Autonomous Driving with Reinforcement Learning for First-Prioritizing Safety over Security," 2024, GitHub, GitHub repository, https://github.com/eleurent/highway-env.
```
