@echo off
:: run build with standard parameters
:: PJ 20180210 changed port to 8082 so doesn't clash with Jenkins default port 8080
:: PJ changed so that it doesn't push to docker hub, just runs locally, with new batch file
:: PJ changed so that tag does not clash with ones used to upload to ECS or Docker Hub
:: PJ changed to use single-step batch files for build docs, build container and run container

SETLOCAL

SET source%=docs
SET todo%=0
SET container%=local/imprcm-docs
SET tag%=docs-99
SET localport%=8082

@echo source: %source% todo: %todo% container: %container% tag: %tag% port: %localport%
@echo .

call build_docs.bat %source% %todo%
call build_container.bat %container% %tag%
call run_container_local.bat %container% %tag% %localport%

timeout /T -1

