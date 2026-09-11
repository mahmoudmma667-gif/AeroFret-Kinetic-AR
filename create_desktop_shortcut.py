"""Create a clean Windows Desktop Shortcut for AeroFret: Kinetic."""
import os
import sys

def create_shortcut():
    try:
        import win32com.client
    except ImportError:
        # Fallback using powershell script file with utf-8 encoding
        pass

    desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    shortcut_path = os.path.join(desktop, 'AeroFret Kinetic.lnk')
    target_path = os.path.abspath('run.bat')
    work_dir = os.path.abspath('.')

    ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{target_path}'
$Shortcut.WorkingDirectory = '{work_dir}'
$Shortcut.Description = 'AeroFret: Kinetic - Touchless Air Guitar'
$Shortcut.IconLocation = 'shell32.dll,41'
$Shortcut.Save()
"""
    tmp_ps = 'create_shortcut.ps1'
    with open(tmp_ps, 'w', encoding='utf-8') as f:
        f.write(ps_script)

    os.system(f'powershell -ExecutionPolicy Bypass -File "{tmp_ps}"')
    if os.path.exists(tmp_ps):
        os.remove(tmp_ps)

    if os.path.exists(shortcut_path):
        print(f"[SUCCESS] Shortcut created at: {shortcut_path}")
    else:
        print("[INFO] Fallback: Please use run.bat directly.")

if __name__ == '__main__':
    create_shortcut()
