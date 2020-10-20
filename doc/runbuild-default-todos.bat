:: run build with standard parameters
:: PJ 20180210 changed port to 8082 so doesn't clash with Jenkins default port 8080
:: PJ changed so that it doesn't push to docker hub, just runs locally, with new batch file
build_run_docs_withtodo.bat docs vivacityrail/imprcm-docs docs-01 8082
