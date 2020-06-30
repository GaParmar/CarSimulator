from datacollection import DataCollector

dc = DataCollector()
dc.reset()
# collect data for {duration} seconds and then reset the env 
dc.collect_data(duration=500, output_folder="output/expert", override=True)
dc.reset()