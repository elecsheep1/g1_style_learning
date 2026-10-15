"""Unitree G1 29dof rev_1_0 asset configuration."""

from pathlib import Path

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import ArticulationCfg

ASSETS_DIR =  Path(__file__).resolve().parent

G1_29DOF_REV_1_0_USD_PATH = (
    ASSETS_DIR
    / "robots"
    / "g1_29dof_rev_1_0"
    / "g1_29dof_rev_1_0.usd"
)

if not G1_29DOF_REV_1_0_USD_PATH.is_file():
    raise FileNotFoundError(
        f"G1 USD not found: {G1_29DOF_REV_1_0_USD_PATH}\n"
        "Place the complete model directory under "
        "assets/robots/g1_29dof_rev_1_0/."
    )

G1_29DOF_REV_1_0 = ArticulationCfg(
    spawn=sim_utils.UsdFileCfg(
        usd_path=str(G1_29DOF_REV_1_0_USD_PATH),
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=True,
            solver_position_iteration_count=8,
            solver_velocity_iteration_count=4,
        ),
    ),

    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.8),
        rot=(0.0, 0.0, 0.0, 1.0),
        joint_pos={
            ".*_hip_pitch_joint": -0.1,
            ".*_knee_joint": 0.3,
            ".*_ankle_pitch_joint": -0.2,
            ".*_shoulder_pitch_joint": 0.3,
            "left_shoulder_roll_joint": 0.25,
            "right_shoulder_roll_joint": -0.25,
            ".*_elbow_joint": 0.97,
            "left_wrist_roll_joint": 0.15,
            "right_wrist_roll_joint": -0.15,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,

    actuators={
        # 双侧 hip_pitch、hip_yaw，以及 waist_yaw：5 个。
        "hip_pitch_yaw_and_waist_yaw": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*_hip_pitch_joint",
                ".*_hip_yaw_joint",
                "waist_yaw_joint",
            ],
            effort_limit_sim=88.0,
            velocity_limit_sim=32.0,
            stiffness={
                ".*_hip_.*": 100.0,
                "waist_yaw_joint": 200.0,
            },
            damping={
                ".*_hip_.*": 2.0,
                "waist_yaw_joint": 5.0,
            },
            armature=0.01,
        ),

        # 双侧 hip_roll、knee：4 个。
        "hip_roll_and_knee": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*_hip_roll_joint",
                ".*_knee_joint",
            ],
            effort_limit_sim=139.0,
            velocity_limit_sim=20.0,
            stiffness={
                ".*_hip_roll_joint": 100.0,
                ".*_knee_joint": 150.0,
            },
            damping={
                ".*_hip_roll_joint": 2.0,
                ".*_knee_joint":4.0,
            },
            armature=0.01,
        ),

        # 肩 6 + 肘 2 + 腕 roll 2 + 踝 4 + 腰 roll/pitch 2：16 个。
        "arms_ankles_and_waist": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*_shoulder_.*_joint",
                ".*_elbow_joint",
                ".*_wrist_roll_joint",
                ".*_ankle_.*_joint",
                "waist_roll_joint",
                "waist_pitch_joint",
            ],
            effort_limit_sim=25.0,
            velocity_limit_sim=37.0,
            stiffness=40.0,
            damping={
                ".*_shoulder_.*": 1.0,
                ".*_elbow_joint": 1.0,
                ".*_wrist_roll_joint": 1.0,
                ".*_ankle_.*": 2.0,
                "waist_.*": 5.0,
            },
            armature=0.01,
        ),

        # 双侧 wrist_pitch、wrist_yaw：4 个。
        "wrist_pitch_and_yaw": ImplicitActuatorCfg(
            joint_names_expr=[
                ".*_wrist_pitch_joint",
                ".*_wrist_yaw_joint",
            ],
            effort_limit_sim=5.0,
            velocity_limit_sim=22.0,
            stiffness=40.0,
            damping=1.0,
            armature=0.01,
        ),
    },

)