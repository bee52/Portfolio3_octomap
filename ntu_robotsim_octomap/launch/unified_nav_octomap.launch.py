from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    nav2_params = LaunchConfiguration('nav2_params')

    declare_use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='true'
    )

    declare_nav2_params = DeclareLaunchArgument(
        'nav2_params',
        default_value=os.path.join(
            get_package_share_directory('ntu_robotsim_octomap'),
            'config',
            'nav2_params.yaml'
        )
    )

    ntu_share = get_package_share_directory('ntu_robotsim_octomap')
    odom_tf_share = get_package_share_directory('odom_to_tf_ros2')
    nav2_share = get_package_share_directory('nav2_bringup')

    maze_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ntu_share, 'launch', 'maze.launch.py'))
    )

    robot_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ntu_share, 'launch', 'single_robot_sim.launch.py'))
    )

    odom_to_tf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(odom_tf_share, 'launch', 'odom_to_tf.launch.py'))
    )

    octomap_filtered_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ntu_share, 'launch', 'octomap_filtered.launch.py'))
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'autostart': 'true',
            'params_file': nav2_params
        }.items()
    )

    return LaunchDescription([
        declare_use_sim_time,
        declare_nav2_params,
        maze_launch,
        robot_launch,
        odom_to_tf_launch,
        octomap_filtered_launch,
        nav2_launch
    ])
