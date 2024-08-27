import shutil
import PyInstaller.__main__

PyInstaller.__main__.run([
  '--name=TheStaircase',
  '--icon=assets/logo.ico',
  '--windowed',
  '--onefile',
  '--add-data=sc2reader:sc2reader',
  'main.py'
])

shutil.rmtree('dist/assets', ignore_errors=True)
shutil.copytree('./assets', 'dist/assets')
