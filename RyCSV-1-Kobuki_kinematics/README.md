# RyCSV – Kobuki Kinematics

Keyboard teleoperation of a Kobuki differential-drive robot using ROS, with wheel velocities computed from a Jacobian-based kinematic model. Supports both RViz visualization and Gazebo simulation.

---
## How to Use the Package

Clone this repository inside your catkin workspace and build the package:

```
git clone https://github.com/Canborda/robotics-labs.git
catkin build kobuki_kinematics
source devel/setup.bash
```

Make sure you have the following Python library installed (used by the `keyop_node`):

- [Pynput](https://pypi.org/project/pynput/)

There are two ways to launch the package:

### Manual Launch

**Step 1** – Start the simulation environments and load the robot model:
```
roslaunch kobuki_kinematics test_simulation.launch
```
This opens both **RViz** and **Gazebo** with the Kobuki URDF model and spawns the `controller_manager` for the wheel joints.

**Step 2** – Run the teleoperation node (in a new terminal):
```
rosrun kobuki_kinematics kobuki_teleop
```
This starts the `keyop_node`, which listens for keyboard input and publishes `Twist` messages to `/velocity_topic`.

**Step 3** – Run the kinematic model node (in a new terminal):
```
rosrun kobuki_kinematics kobuki_model
```
This starts the `model_node`, which subscribes to `/velocity_topic`, applies the inverse kinematic model, and publishes the resulting wheel angular velocities to `/left_wheel_ctrl/command` and `/right_wheel_ctrl/command`.

<br>

### Complete Launch

<br>

```
roslaunch kobuki_kinematics kobuki_final.launch
```

This single command starts all three components above automatically.

---
## Keyboard Controls

| Key | Action |
|-----|--------|
| `W` | Increase linear velocity (Vx +0.02 m/s) |
| `S` | Decrease linear velocity (Vx −0.02 m/s) |
| `A` | Increase angular velocity (ω +10 deg/s) |
| `D` | Decrease angular velocity (ω −10 deg/s) |
| `X` | Stop (set Vx = 0, ω = 0) |
| `ESC` | Quit node |

---
## Kinematic Model

The Kobuki is a differential-drive robot. Its kinematic model maps the body-frame velocity vector `[Vx, Vy, ω]` to individual wheel angular velocities `[φ̇_L, φ̇_R]` using a Jacobian derived from the wheel geometry:

```
J1 = [[sin(αL + βL),  -cos(αL + βL),  -l·cos(βL)],
      [sin(αR + βR),  -cos(αR + βR),  -l·cos(βR)]]

J2 = r · I₂

φ̇ = J2⁻¹ · J1 · [Vx, Vy, ω]
```

With the following robot parameters:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `r` | 0.038 m | Wheel radius |
| `l` | 0.115 m | Half track width |
| `αL`, `βL` | π/2, 0 | Left wheel orientation angles |
| `αR`, `βR` | −π/2, π | Right wheel orientation angles |

The CLI displays the current velocity state and computed wheel speeds in real time:

```
----------------------------------------------------------------------
For Vx++ use w          For ω++ use a           For STOP use x
For Vx-- use s          For ω-- use d           Press ESC to quit
----------------------------------------------------------------------

        Vx = 0.20 m/s          Left wheel = 5.263 rpm
        Vy = 0.00 m/s         Right wheel = 5.263 rpm
         ω = 0 deg/s

----------------------------------------------------------------------
```

---
## ROS Graph

The node communication follows this flow:

```
[keyop_node] → /velocity_topic (Twist) → [model_node] → /left_wheel_ctrl/command  (Float64)
                                                        → /right_wheel_ctrl/command (Float64)
```

---
> ## Contributors
>
> [Camilo Andrés Borda Gil](https://github.com/Canborda) (caabordagi@unal.edu.co)  
> Daniel Fernando Diaz Coy (dafdiazco@unal.edu.co)  
> Andrés Felipe Rivera Torres (afriverat@unal.edu.co)

---
