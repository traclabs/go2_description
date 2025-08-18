from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import DeclareLaunchArgument
from launch.actions import RegisterEventHandler
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch.event_handlers import OnProcessExit
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


import os


##################################################################
def generate_launch_description():

    launch_args = [
        DeclareLaunchArgument(
            "x",
            default_value="5.0",
            description="X at which to spawn Spot. 0.84 for ground plane, 0 for marsyard is good",
        ),
        DeclareLaunchArgument(
           "y", default_value="0.0", description="y at which to spawn quadruped."),
        DeclareLaunchArgument(
            "z", default_value="0.40", description="Height at which to spawn quadruped."
        ),
        DeclareLaunchArgument(
            "roll", default_value="0.0", description="Roll at which to spawn quadruped."
        ),
        DeclareLaunchArgument(
            "yaw", default_value="-0.5", description="Yaw at which to spawn quadruped."
        ),
        DeclareLaunchArgument(
            "use_sim_time", default_value="True", description="If true, use simulated clock"
        )
    ]



    # Robot gonna fall at the beginning. Here we pick it up
    stand_up = ExecuteProcess(
        cmd=[
            "gz",
            "service",
            "-s",
            "/world/urban_circuit_02/set_pose", # IMPORTANT!!! If world you are using has a different name than urban..., change this
            "--reqtype",
            "gz.msgs.Pose",
            "--reptype",
            "gz.msgs.Boolean",
            "--timeout",
            "1000",
            "--req",
            [
                'name: "go2", position: {x: ',
                LaunchConfiguration("x"),
                ", y: ",
                LaunchConfiguration("y"),
                ", z: ",
                LaunchConfiguration("z"),
                "}",
            ],
        ],
        name="stand_up",
        output="both",
    )

    return LaunchDescription(
        launch_args
        + [
            SetParameter(name="use_sim_time", value=True),
            stand_up
        ]
    )
