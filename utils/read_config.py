def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Skip lines that are comments or empty
            if line.startswith('#') or not line.strip():
                continue

            key, value = line.strip().split('=')
            config[key] = value
    
    config['tunnel_pointcloud_sim_path'] = config.get('tunnel_pointcloud_sim_path')
    config['blender_app_path'] = config.get('blender_app_path')
    config['number_of_simulations'] = int(config.get('number_of_simulations', 1))
    config['scanner_step_degree'] = float(config.get('scanner_step_degree', 0.3))
    return config