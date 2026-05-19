# RyCSV – Kobuki Control

Open-loop and closed-loop control of a Kobuki differential-drive robot in Gazebo using ROS. Extends the kinematic model from [RyCSV-1](../RyCSV-1-Kobuki_kinematics) with a sigmoid-based proportional controller for autonomous waypoint navigation.

---
## How to Use the Package

Clone this repository inside your catkin workspace and build the package:

```
git clone https://github.com/Canborda/robotics-labs.git
catkin build kobuki_control
source devel/setup.bash
```

Make sure you have the following Python library installed (used by the `keyop_node`):

- [Pynput](https://pypi.org/project/pynput/)

The package offers two operating modes:

<br>

### Open-Loop Mode (Keyboard Teleoperation)

<br>

```
roslaunch kobuki_control open_loop.launch
```

This launches the simulation environment, the keyboard teleoperation node, and the kinematic model node. Use the keyboard to manually drive the robot — the same controls as in RyCSV-1 apply (W/S for linear velocity, A/D for angular velocity, X to stop, ESC to quit).

<br>

### Closed-Loop Mode (Autonomous Navigation)

<br>

**Step 1** – Start the Gazebo simulation with the Kobuki model:
```
roslaunch kobuki_control spawn_robot.launch
```

**Step 2** – Launch the navigation stack (in a new terminal):
```
roslaunch kobuki_control navigation.launch
```

The `reference_listener` node will prompt for waypoint input on the terminal. Enter one or more `(x,y)` coordinates separated by spaces, or type `saved_1` to run a pre-saved route. Type `q` to stop.

```
>> (2.0,1.5) (0.0,3.0) (-1.5,0.0)
>> saved_1
>> q
```

---
## Nodes

### Open-Loop Nodes

| Node | Script | Description |
|------|--------|-------------|
| `keyop_node` | `kobuki_teleop.py` | Reads keyboard input and publishes `Twist` to `/velocity_topic` |
| `model_node` | `kobuki_model.py` | Converts body velocity to wheel speeds via the Jacobian model |

### Closed-Loop Nodes

| Node | Script | Description |
|------|--------|-------------|
| `pose_node` | `read_pose.py` | Reads Gazebo model state and publishes robot pose to `/current_pose_topic` |
| `reference_listener_node` | `reference_listener.py` | Accepts `(x,y)` waypoints from CLI and enqueues them |
| `reference_manager_node` | `reference_manager.py` | Manages the waypoint queue and sends the next reference when the current one is reached |
| `kobuki_controller_node` | `kobuki_controller.py` | Computes velocity commands from pose error using a sigmoid controller |
| `model_node` | `kobuki_model.py` | Converts body velocity to wheel speeds via the Jacobian model |

---
## Controller

The closed-loop controller is a **sigmoid-based proportional controller** that produces smooth velocity commands without abrupt transitions.

Given the position error `eₚ = √(eₓ² + eᵧ²)` and heading error `eθ`, the commands are:

```
Vx = 2·Vc / (1 + exp(−20·eₚ)) − Vc

Wz = 2·Wc / (1 + exp(−eθ/5)) − Wc
```

With the following tuning parameters:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `Vc` | 0.3 m/s | Linear cruise velocity |
| `Wc` | 60 deg/s | Angular cruise velocity |
| `MIN_ERROR` | 0.1 m | Threshold to request next waypoint |
| `MIN_STOP` | 0.01 m | Threshold to fully stop at waypoint |

The target heading `θ_ref` is continuously updated to point from the robot's current position toward the active waypoint.

---
## ROS Graph

### Open-Loop

```
[keyop_node] → /velocity_topic (Twist) → [model_node] → /wheel_left_ctrl/command  (Float64)
                                                        → /wheel_right_ctrl/command (Float64)
```

### Closed-Loop

```
Gazebo → [pose_node] → /current_pose_topic (Pose2D) ──────────────────────────→ [controller]
                                                                                       ↑
[reference_listener] → /add_reference_topic → [reference_manager] → /current_reference_topic

[controller] → /velocity_topic → [model_node] → /wheel_left_ctrl/command
                                               → /wheel_right_ctrl/command
[controller] → /next_pose_flag_topic → [reference_manager]
```

---
> ## Contributors
>
> [Camilo Andrés Borda Gil](https://github.com/Canborda) (caabordagi@unal.edu.co)  
> Daniel Fernando Diaz Coy (dafdiazco@unal.edu.co)  
> Andrés Felipe Rivera Torres (afriverat@unal.edu.co)

---
