@echo off
:: run build with standard parameters, to pdf

SETLOCAL

SET source%=docs
SET master%=IMPRCM_documentation
SET todo%=0

@echo source: %source% master doc: %master% todo: %todo% 
@echo .

call build_docs_to_pdf.bat %source% %master% %todo%

timeout /T -1

