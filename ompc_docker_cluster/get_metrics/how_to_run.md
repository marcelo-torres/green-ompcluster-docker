# Metrics

The following steps get the tasks' runtime estimates. Therefore, it was executed in each one of the following real machines: intel_i5h, amd_epyc_7453 and intel_i3.

```shell
docker compose up -d 
docker attach $head_container
cd /volume
bash get_iterations_task_bench.sh
```

After collecting all estimates in each machine, we moved the selected traces to "selected_traces." The following commands generate the task duration files for each topology:

```shell
bash get_graph_size.sh
python3 get_tasks_durations_files
```