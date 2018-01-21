@echo off
setlocal
set CORE_VERSION="V8.30-1"
set KTRANS_BIN="C:\Program Files (x86)\Fanuc\WinOLPC\bin\ktrans.exe"
REM set KTRANS_BIN="ktrans.exe"

%KTRANS_BIN% /ver %CORE_VERSION% libind_log.kl
%KTRANS_BIN% /ver %CORE_VERSION% libssock.kl
%KTRANS_BIN% /ver %CORE_VERSION% fdpm_mdemo.kl
