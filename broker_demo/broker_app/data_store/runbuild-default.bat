@echo off
:: run build with standard parameters
:: PJ changed so that it doesn't push to docker hub, just runs locally, with new batch file
:: PJ changed so that tag does not clash with ones used to upload to ECS or Docker Hub
:: PJ changed to use single-step batch files for build docs, build container and run container

SETLOCAL

SET init%=0
SET datavolume=imprcm_data_store
SET container%=local/imprcm-demo-datastore
SET tag%=ds-99
SET localport%=5432

@echo init: %init%  container: %container%  tag: %tag%  volume: %datavolume%  port: %localport%
@echo .

call build_container.bat %container% %tag%
call run_container_local.bat %container% %tag% %init% %localport% %datavolume%

timeout /T -1

