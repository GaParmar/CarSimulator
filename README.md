# CarSimulator
Collect data from car simulator for dagger

# Usage
 - `conda activate pytorch_sac_ae` (specific to my morpheus server)
 - ```
    dc = DataCollector()
    dc.reset()
    # collect data for {duration} seconds and then reset the env 
    dc.collect_data(duration=500, output_folder="output/expert", override=True)
    dc.reset()
    ```

## References
 - https://github.com/autorope/donkeycar/blob/dev/donkeycar/parts/controller.py
 -