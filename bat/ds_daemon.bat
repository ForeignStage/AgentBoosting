@echo off
:: Start FSWatcher daemon in background (minimized window)
start "AgentHub-Watcher" /min "PYTHON313/pythonw.exe" "E:\AgentHub\ModelBoosting\core\watchdog\fs_watcher.py"
echo [DAEMON] fs_watcher started.
