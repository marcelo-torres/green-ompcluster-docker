# Metrics

The following steps get the tasks' runtime estimates. Therefore, it was executed in each one of the following machines: intel_i5h, amd_epyc_7453 and intel_i3.

```shell
docker compose up -d 
docker attach $head_container
cd /volume
bash get_iterations_task_bench.sh
bash get_graph_size.sh
python3 get_tasks_durations_files
```