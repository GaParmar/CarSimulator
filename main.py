from datacollection import DataCollector

## Initializes the simulator and the controller
dc = DataCollector(controller="xbox", angle_scale=0.5, throttle_scale=1.0)

# collect data for {duration} seconds 
dc.collect_data(duration=100, output_folder="output/expert_5", override=True)

# reset the simulator to the default state
dc.reset()
