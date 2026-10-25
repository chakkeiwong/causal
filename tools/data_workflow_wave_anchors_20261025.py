"""Author-inspected primary spans; every source remains pinned and retained."""
ANCHORS = {
 'datatable': [
  ('src01',1,16,'1.18.99','Development metadata declares1.18.99 and MPL2 alternative license notice; not installed release qualification.'),
  ('src02',1,20,'Mozilla Public License','Selected root MPL2 license; complete artifact rights remain separate.'),
  ('src05',524,525,'mult="all"','Default join signature retains unmatched rows and all matches; rolling is disabled.'),
  ('src05',913,937,'nrow(x)+nrow(i)','Many-to-many guard depends on options and duplicate matches; default row limit is not key uniqueness.'),
  ('src10',19,35,'reslen>limit','C delegate rejects strictly above row limit, not equality; separate integer-size guard.'),
  ('src11',88,99,'datatable.join.many=TRUE','Pinned defaults allow many-to-many with cartesian expansion guard false.'),
  ('src03',78,88,'factor','Selected factor mapping preserves distinct NA handling; conversion needs an explicit schema.'),
 ],
 'targets': [
  ('src01',1,20,'1.12.0.9001','Pinned development package metadata and MIT declaration.'),
  ('src02',1,18,'MIT License','Root MIT terms; dependencies and delivery artifacts remain separate.'),
  ('src07',1,20,'thorough','Default cues include command,dependencies,format,repository,iteration,file and seed.'),
  ('src07',47,82,'row_has_error','Error metadata is outdated; command/dependency comparisons are conditional on cues.'),
  ('src13',106,142,'cue_never','Run decision checks absent/error metadata before never cue; never bypasses later change checks.'),
  ('src13',391,420,'builder_error_null','Distinct continue,abridge,trim,stop,null/workspace branches; null mode records error.'),
  ('src12',120,141,'target name','Target-name/configured seeds can be overridden inside commands or disabled with NA.'),
  ('src10',7,25,'warnings','Record has command,seed,dependency,bytes,seconds,warnings and error fields; not complete costs.'),
 ],
 'dask': [
  ('src01',1,27,'BSD 3-Clause','Selected BSD3 root terms; no full dependency clearance.'),
  ('src03',83,89,'TokenizationError','Deterministic token failure is enforced only when selected flag/configuration requests it.'),
  ('src03',194,230,'uuid.uuid4','Object/custom/pickle normalization includes nondeterministic fallbacks; task tokens are not complete provenance.'),
  ('src03',233,263,'pickle.loads','Token normalization tries pickle/cloudpickle round trips and may use UUID fallback; arbitrary untrusted objects are not safe payloads.'),
  ('src06',53,77,'mutate','Documentation advises against mutating delayed-task inputs.'),
  ('src08',69,83,'split_every','Array sum forwards chunk sum,dtype and reduction-tree control; numeric tolerance needs explicit qualification.'),
  ('src04',246,263,'failed','Local execute_task distinguishes exception payloads and failed flag; distributed fault guarantees are separate.'),
 ],
 'snakemake': [
  ('src01',1,20,'Permission is hereby granted','Selected MIT-style license terms.'),
  ('src02',1,20,'9.27.0','Pinned9.27.0 metadata requires Python>=3.11.'),
  ('src03',390,421,'keep_metadata','Finishing can remove incomplete markers without metadata; checksum collection has file-size policy.'),
  ('src03',418,452,'input_checksums','Completion record excludes unavailable checksums and records code,inputs,params,software and stack identity.'),
  ('src09',550,572,'job.attempt += 1','Error handler frees resources and requeues within restart budget; exhausted jobs marked failed.'),
 ],
 'beam': [
  ('src01',1,12,'Apache License','Selected Apache2 license; runners/connectors have separate artifact obligations.'),
  ('src03',36,57,'best effort','Deduplication is bounded by time/window,uses encoded-byte identity and does not preserve order.'),
  ('src03',70,75,'standardMinutes(10)','Selected default is processing time with ten-minute duration.'),
  ('src03',308,327,'seenState.clear','Emits first unseen element,sets relative expiry and clears seen state at timer.'),
  ('src04',43,61,'silently dropped','Timestamp change preserves windows; late data may be dropped under downstream lateness; null timestamp refused.'),
 ],
 'arrow': [
  ('src01',1,12,'Apache License','Selected Apache2 root terms,not complete transitive artifact clearance.'),
  ('src02',96,124,'positive','Positive tolerance admits future time; nonpositive admits past/exact time with bounded horizon.'),
  ('src02',264,279,'future_entries','Positive tolerance retains future queues,distinct from past-only memoization.'),
  ('src02',626,649,'out-of-order','Asof advance refuses decreasing on-key times in selected branch.'),
  ('src07',74,102,'batch_readahead','Scanner batch/readahead controls and memory pool affect resource use; not whole-run memory proof.'),
 ],
 'taskflow': [
  ('src01',1,20,'MIT LICENSE','Selected Taskflow MIT terms; complete toolchain/artifact custody separate.'),
  ('src06',45,79,'get()','Exception routing distinguishes blocking contexts and asynchronous future.get; completion observation needs error consumption.'),
  ('src02',1946,1986,'first thrown exception','Executor records anchored exception state and first caught exception; not an inventory of every concurrent failure.'),
 ],
 'dataframes': [
  ('src01',1,22,'MIT License','Selected DataFrames.jl MIT terms.'),
  ('src02',1,8,'1.8.2','Pinned package version1.8.2; Julia compatibility separate.'),
  ('src04',63,105,'matchmissing','Missing matching modes have distinct drop/error semantics; numeric NaN and negative zero join keys refused in selected branch.'),
  ('src04',489,545,'nonunique','Explicit left/right validation calls check key duplicates; defaults need explicit selection.'),
 ],
 'dagger': [
  ('src01',1,22,'Expat','Selected Dagger MIT Expat terms.'),
  ('src02',1,8,'0.22.6','Pinned package version0.22.6.'),
  ('src03',1,18,'last-ditch','Fault-handler documentation retains robustness caveat and requires surviving workers.'),
  ('src03',20,72,'reschedule_syncdeps','Worker failure evicts lost cache,clears cache references and requeues with count ordering.'),
  ('src12',230,270,'pending_deps','Reschedule delegate guards dependency wiring and skips already registered/running/finished tasks.'),
  ('src12',305,324,'set_failed!','Errored upstream propagates failure; ready replacements counted before scheduling.'),
 ],
}
REUSE = {
 'R':['exec19_duckdb_source','exec19_duckdb_reference'],
 'Python':['exec19_duckdb_source','exec19_duckdb_reference','exec19_feast_source','exec19_feast_reference','exec23_polars_sources','exec23_polars_reference','exec24_pandera_source','exec24_pandera_reference','exec24_splink_sources','exec24_splink_contract','exec24_openlineage_source','exec24_openlineage_reference','exec24_ray_sources','exec24_ray_contract'],
 'Java':['exec25_otm_spark','exec24_openlineage_source','exec24_openlineage_reference'],
 'Cxx':['exec19_duckdb_source','exec19_duckdb_reference'],
 'other_relevant':['exec25_otm_spark','exec25_otm_polars','exec23_polars_sources','exec23_polars_reference'],
}
NEW_GROUPS = {'R':['datatable','targets'],'Python':['dask','snakemake'],'Java':['beam'],'Cxx':['arrow','taskflow'],'other_relevant':['dataframes','dagger']}
FAMILIES = ['observations_data','computation_workflow']
